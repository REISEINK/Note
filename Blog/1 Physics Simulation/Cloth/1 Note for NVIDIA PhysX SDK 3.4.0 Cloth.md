
### Simulation Algorithm

* 每一帧 Cloth Solver 都会运行多次。所以总的迭代次数由 Solver Frequency 和 Simulation Frame Time 共同决定。
* 每一次迭代执行
	* Particle positions
	* Solves Constraints
	* Performs character
	* Self-collision
* 每一次帧会执行
	* Inter-collision （after all cloth instances in the scene have been stepped forward
* 每一次迭代插值
	* Local frame
	* Motion constraints
	* Collision shapes

##### Solver Frequency
Solver Frequency的含义是每秒迭代次数。一秒60帧的情况下，Solver Frequency = 240 代表每帧迭代 4 次。
##### Particle Intergration
布料模拟迭代的第一步是根据粒子的当前位置、速度和外部加速度来预测新的粒子位置。PhysX采用了Verlet积分，跟PBD一样，其对应PBD算法中的第(5)步。
##### Local Space Simulation and Inertia Scale
* PxCloth::SetGlobalPose() 只移动布料的位置
* PxCloth::setTargetPose() 还会由于位置变化而产生加速度(惯性)

* 局部帧加速度影响布料的程度可以通过惯性缩放控制来控制: cloth.setInertiaScale(0.5f)
* 限制局部帧加速度影响粒子的程度对于快速移动的情况有效
##### Distance Constraints
布料Solver最重要的作用之一就是保持粒子之间的距离，使布料不发生拉伸。这主要是通过应用粒子对之间的距离约束来实现的。
* Stiffness: 表示约束的强度，Stiffness 越大，布料就越硬，顶点之间就更倾向于维持原来的长度。
* Stiffness Multiplier: 约束强度的缩放值。在 Limit 范围内时，会对约束强度进行缩放
* Stretch Limit: 拉伸长度的限制。超过该限制，约束强度不会进行缩放。
* Compression Limit: 压缩长度的限制。超过该限制，约束强度不会进行缩放。

#### Tether Constraints
其实就是FTL(Follow the leader) Constraints，每次迭代只会求解一次。Distance Constraints 会根据Solver Frequency 求解 Frequency / FrameRate 次。
Tether Constraints 是自动生成的，PxClothMeshDesc::invMasses 设为 0 的那些粒子作为Leader。

#### Motion Constraints
限制粒子移动到动画位置一定范围（范围用球体表示）之外。对应UE布料中的 Max Distance。
如果Motion Constraints的球体半径设置为0或负数，粒子将被锁定在球体中心。
* 球体的中心是如何确定的？动画位置？

#### Separation Constraints
与Motion Constraints相反，限制粒子移动到球体之内。对应UE布料中的Backstop。

##### Collision Detection
衣料的碰撞是独立于PhysX的，但也可以使用PxClothFlag::eSCENE_COLLISION去开启与PxScene actors的碰撞。
布料支持与球体，胶囊体，平面，凸包和三角面的碰撞。其中球体和胶囊体的碰撞支持连续碰撞检测，还使用空间加速结构剔除距离远的粒子。因此，碰撞的物理资产推荐以球体和胶囊体为主。

##### Friction and Mass Scaling
摩擦力应用于与Virtual Particle 碰撞。

##### Self Collision of Single Cloth Actor
Self-collision distance 定义了每个粒子周围球体的直径，Solver 确保这些球体在模拟过程中不会重叠。Self-collision stiffness 定义了分离碰撞的粒子的冲量的强度。
如果两个粒子的静止位置比碰撞距离更近，则忽略它们之间的碰撞。但是，较大的碰撞距离和使用休息位置会显著降低自碰撞的性能，因此应谨慎使用。

### Best Practices / Troubleshooting

#### Performance Tips
As a rough guideline, a dozen cloth instances with 2000 particles each and a solver frequency of 300Hz can be simulated in real-time as part of a game.

#### Fast-Moving Characters
* 局部空间下模拟
* _PxClothFlag::eSWEPT_CONTACT_

#### Avoiding Stretching
*  Tether constraints

####  Avoiding Jitter

* 避免不同约束之前的冲突
* 减少Solver Frequency 和 降低对应的约束的Stiffness

#### PVD Support
* 调试用