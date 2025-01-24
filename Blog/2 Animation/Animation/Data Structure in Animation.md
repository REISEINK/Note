#### USkeleton
`USkeleton` 是 **Unreal Engine** 中动画系统的核心类之一，表示一个**骨架资源（Skeleton Asset）**。它定义了角色动画使用的骨骼层次结构，负责管理与角色骨骼相关的各种数据，包括骨骼的继承关系、骨骼绑定、动画序列等。

##### USkeleton的作用
- **定义骨骼层次结构**  
`USkeleton` 包含角色的骨骼层级树，每个骨骼都有父子关系，形成一个层次结构。这是角色动画与姿态（Pose）操作的基础。
- **绑定动画序列**  
所有与角色相关的动画序列（`UAnimSequence`）都会绑定到 `USkeleton`，确保动画可以正确应用到对应的骨骼。 
- **共享动画资源**  
不同的 **SkeletalMesh**（骨骼网格体）可以共用同一个 `USkeleton`，从而实现动画资源的重用。例如，多个角色使用同一套动画时，只需要一个 `USkeleton`。
- **管理骨骼相关的额外数据**  
`USkeleton` 还可以存储额外的骨骼数据，如挂点、蒙皮信息（Skinning Data）、曲线（Curves）、骨骼重定向（Retargeting）规则等。


##### USkeleton 关键成员
```C++ 
class USkeleton : public UObject, public IInterface_AssetUserData, public 
	IInterface_PreviewMeshProvider
{
	friend class UAnimationBlueprintLibrary;
	friend class FSkeletonDetails;

	GENERATED_UCLASS_BODY()

protectd:
	// Skeleton的骨骼树，存储骨骼的层次结构。骨骼用FBoneNode表示，包括名字、父骨骼的index和
	// 骨骼的重定向模式（如何处理骨骼的动画数据）
	// Q: 重定向怎么处理骨骼的动画数据的？
	UPROPERTY(VisibleAnywhere, Category=Skeleton)
	TArray<struct FBoneNode> BoneTree;

	// 参考骨骼，
	// RawRefBonePose：T-Pose. ReferenceSkeleton包含每个骨骼的初始变换，这些变换定义了骨
	// 骼在绑定时的初始位置
	FReferenceSkelton ReferenceSkelton;

	// 挂点
	UPROPERTY()
	TArray<TObjectPtr<class USkeletalMeshSocket>> Sockets;

	// 重定向
	// Q: 重定向相关重要的是这一项吗
	TMap<const USkeleton*, FSkeletonRemapping*> SkeletonRemappings;

	// 动画曲线相关
	
}
```

