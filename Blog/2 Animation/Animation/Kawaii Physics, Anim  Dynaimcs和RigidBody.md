FAnimNode_KawaiiPhysics、FAnimNode_AnimDynamics和FAnimNode_RigidBody都是继承FAnimNode_SkeletalControlBase，可以参见[[AnimNode#^718985]]
### Kawaii Physics(1.10.0)
相较于另外两者的主要不同点在于，Kawaii Physics模拟时只基于当前的骨骼，不会为骨骼创建代理对象（比如AnimDynamics中的Box）进行模拟。
核心的函数就是FAnimNode_KawaiiPhysics::SimulateModifyBones，会执行骨骼链的伪物理解算。以下会对该函数的流程进行逐步说明。
注：会省略部分与物理模拟逻辑关系较小的代码，为了排版也可能缩写部分变量和函数名。

##### Gravity and Exponent
```c++
// 通过Δt和期望帧率计算Exponent
// 后续步骤中根据Stiffness恢复最初形状的过程，假设不引入Exponent, 这个过程实际是与Δt无关的，不同帧率的模拟效果会截然不同，引入Exponent缓解帧率变化带来的效果改变问题
const float Exponent = TargetFramerate * DeltaTime;

// 转换重力到组件空间
FVector GravityCS = ComponentTransform.InverseTransformVector(Gravity);
```
##### Move using Velocity and Damping
```C++

// 遍历需要模拟的骨骼，后文都是在该for循环内
for (int32 i = 0; i < ModifyBones.Num(); ++i)
{
	auto& Bone = ModifyBones[i];
	auto& ParentBone = ModifyBones[Bone.ParentIndex];

	FVector BonePoseLocation = Bone.PoseLocation;  
	FVector ParentBonePoseLocation = ParentBone.PoseLocation;

	// 计算速度，并根据阻尼削减速度大小
	FVector Velocity = (Bone.Location - Bone.PrevLocation) / DeltaTimeOld;  
	Bone.PrevLocation = Bone.Location;  
	Velocity *= (1.0f - Bone.PhysicsSettings.Damping);

	// 计算风对速度的影响，此处是直接速度 += 风速 * 时间，感觉是个简化的模型
	WindDirection = CompTransform.Inverse().TransformVector(WindDirection);
	FVector WindVelocity = WindDirection * WindSpeed * WindScale;
	WindVelocity *= FMath::FRandRange(0.0f, 2.0f);
	Velocity += WindVelocity * TargetFrameRate;

	// 实际上用的是Verlet积分，可以参照Reference 3
	Bone.Location += Velocity * DeltaTime;

```

##### Follow Translation and Rotation
```c++
// 跟随组件在组件空间的位移和旋转 应该是为了模拟惯性
Bone.Location += SkelCompMoveVector * (1.0f - WorldDampingLocation);  
Bone.Location += (SkelCompMoveRotation.RotateVector(Bone.PrevLocation) - Bone.PrevLocation)  * (1.0f - WorldDampingRotation);

// 重力 Q:为啥独立出来不参与之前的速度计算?
Bone.Location += GravityCS * DeltaTime;

```
##### Pull to Pose Location
```c++
// PoseLocation即动画位置，Stiffness == 1的情况下，将骨骼链视为刚体
// Stiffness越大，认为骨骼链难发生形变
FVector BaseLocation = ParentBone.Location + (BonePoseLocation - ParentBonePoseLocation);  
Bone.Location += (BaseLocation - Bone.Location) *  (1.0f - FMath::Pow(1.0f - Bone.PhysicsSettings.Stiffness, Exponent));
```
这一步会根据Stiffness往将骨骼动画位置靠近，让Stiffness控制骨骼链的刚度，Stiffness越大，骨骼链越接近刚体。这里与Dynamic Bone图中(2)->(3)过程中（详见[[#^aa7b58]])，骨骼往理想位置靠近从而模拟弹性运动，是正好相同的。（不如说整体思路都很相似）
![[Pasted image 20250120170949.png]]

##### Collision

```c++
AdjustBySphereCollision(Bone, SphericalLimits); 
AdjustBySphereCollision(Bone, SphericalLimitsData);
AdjustByCapsuleCollision(Bone, CapsuleLimits);  
AdjustByCapsuleCollision(Bone, CapsuleLimitsData);  
AdjustByPlanerCollision(Bone, PlanarLimits);  
AdjustByPlanerCollision(Bone, PlanarLimitsData);

if (bAllowWorldCollision)
{
	AdjustByWorldCollision(Bone, SkelComp, BoneContainer);
}

```

对于球体的碰撞，不同碰撞类型（将粒子限制在球内还是球外）处理方式相反。以把骨骼限制在球外为例，会沿着最短距离把骨骼推出球外，具体而言，推出的距离=骨骼到球心的距离-球半径+骨骼的物理半径，推出方向=球心位置->骨骼位置。
```c++
if (Sphere.LimitType == ESphericalLimitType::Outer)  
{  
	if ((Bone.Location - Sphere.Location).SizeSquared() > LimitDistance * LimitDistance)  
	{      
		continue;  
	}  
	else  
	{  
		Bone.Location += (LimitDistance - (Bone.Location - Sphere.Location).Size()) * (Bone.Location - Sphere.Location).GetSafeNormal();  
	}
}
```
对于胶囊体的碰撞，计算骨骼到胶囊体线段（由胶囊体的起点和终点确定）的距离，和限制距离（胶囊体半径+骨骼的物理半径）进行比较，如果小于限制距离，沿着离开胶囊体线段的最近距离移除胶囊体。
```c++
FVector StartPoint = Capsule.Location + Capsule.Rotation.GetAxisZ() * Capsule.Length * 0.5f;  
FVector EndPoint = Capsule.Location + Capsule.Rotation.GetAxisZ() * Capsule.Length * -0.5f;

const float DistSquared = FMath::PointDistToSegmentSquared(Bone.Location, StartPoint, EndPoint);  
  
const float LimitDistance = Bone.PhysicsSettings.Radius + Capsule.Radius;  
if (DistSquared < LimitDistance * LimitDistance)  
{  
	FVector ClosestPoint = FMath::ClosestPointOnSegment(Bone.Location, StartPoint, EndPoint);
	Bone.Location = ClosestPoint + (Bone.Location - ClosestPoint).GetSafeNormal() * LimitDistance;  
}
```
对面平面的碰撞，先计算骨骼在平面上的投影，并计算骨骼到平面上的距离。如果骨骼距离平面的距离小于骨骼的物理半径，或者骨骼在该帧与平面相交，调整骨骼的位置至平面上的投影点+平面法线方向乘以骨骼的物理半径。
可能的问题：隐含了一个假设，骨骼在上一帧的位置是在平面法线方向一侧的，如果因为一些原因骨骼穿过了平面，且上一帧就在平面法线方向另一侧，就不会执行碰撞，可能会导致骨骼穿过平面但是无法恢复。
```c++
FVector PointOnPlane = FVector::PointPlaneProject(Bone.Location, Planar.Plane);  
const float DistSquared = (Bone.Location - PointOnPlane).SizeSquared();  
  
FVector IntersectionPoint;  
if (DistSquared < Bone.PhysicsSettings.Radius * Bone.PhysicsSettings.Radius || FMath::SegmentPlaneIntersection(Bone.Location, Bone.PrevLocation, Planar.Plane, IntersectionPoint))  
{  
	Bone.Location = PointOnPlane + Planar.Rotation.GetUpVector() * Bone.PhysicsSettings.Radius;  
	continue;  
}
```

## Reference
1. [【UE笔记】记一个AnimNode_RigidBody的坑 - 知乎](https://zhuanlan.zhihu.com/p/483945074)
2. [动态骨骼Dynamic Bone算法详解 - 知乎](https://zhuanlan.zhihu.com/p/49188230) ^aa7b58
3. [游戏开发技术杂谈10：绳索模拟 - 知乎](https://zhuanlan.zhihu.com/p/511401119)