
## AnimNode
* AnimNode的概念/作用
* AnimNode的使用场景/如何使用
### AnimNode_Base

```C++
USTRUCT()
struct AnimNode_Base
{
	GENERATED_BODY()

	// 在动画节点第一次运行时调用。如果动画结点处于状态机或者缓存姿势分支内，可以被多次调用
	// Q: 动画结点处于状态机或者缓存姿势分支内，具体是啥场景
	ENGINE_API virtual void Initialize_AnyThread(const FAnimationInitializeContext&
		Context);

	// 缓存此节点需要跟踪(Track)的骨骼
	ENGINE_API virtual void CacheBones_AnyThread(const FAnimationCacheBonesContext&
		Context);

	// 更新相对于此节点的图(Graph)状态
	// Q: Graph指的是啥?AnimGraph?
	ENGINE_API virtual void Update_AnyThread(const FAnimationUpdateContext& 
		Context);

	// 根据Update方法中设置的权重来评估局部空间的骨骼变换。
	ENGINE_API virtual void Evaluate_AnyThread(FPoseContext& Output);

	
	// 根据Update方法中设置的权重来评估组件空间的骨骼变换。
	ENGINE_API virtual void EvaluateComponentSpace_AnyThread(
		FComponentSpacePoseContext& Output);

	
	
}
```


### AnimNode核心方法调用流程

* USkeletalMeshComponent::TickComponent
	* USkeletalMeshComponent::TickPose
		* void USkeletalMeshComponent::TickAnimation
			* USkeletalMeshComponent::TickAnimInstances
				* UAnimInstance::UpdateAnimation
					* UAnimInstance::ParallelUpdateAnimation
						* FAnimInstanceProxy::UpdateAnimation
							* FAnimInstanceProxy::UpdateAnimation_WithRoot
								* InitializeRootNode_WithRoot
									* **FAnimNode_Base::Initialize_AnyThread**
								* CacheBones
									* **FAnimNode_Base::CacheBones_AnyThread**
								* UpdateAnimationNode
									* **FAnimNode_Base::Update_AnyThread**

Q: 数据如何传输、计算

### FAnimNode_SkeletalControlBase

^718985

继承了FAnimNode_Base，骨架控制相关的AnimNode会继承该基类。核心的方法，Initialize、CacheBones、Update、Evaluate相较于FAnimNode_Base，加了一个递归调用连接的节点对应函数的功能。
##### Initialize_AnyThread
```c++
void FAnimNode_SkeletalControlBase::Initialize_AnyThread(const
	FAnimationInitializeContext& Context)  
{  
	DECLARE_SCOPE_HIERARCHICAL_COUNTER_ANIMNODE(Initialize_AnyThread) 

	// 啥也没干，基类实现是空的
	FAnimNode_Base::Initialize_AnyThread(Context);  

	// 见FPoseLinkBase::Initialize
	ComponentPose.Initialize(Context);  

	// 初始化，赋值为false
	AlphaBoolBlend.Reinitialize();  
	AlphaScaleBiasClamp.Reinitialize();  
}

void FPoseLinkBase::Initialize(const FAnimationInitializeContext& InContext)  
{  
	// relink
	AttemptRelink(InContext);
	
	if (LinkedNode != nullptr)  
	{      
		FAnimationInitializeContext LinkContext(InContext);  
		LinkContext.SetNodeId(LinkID);  

		// 递归调用连接的AnimNode的Initialize_AnyThread
		LinkedNode->Initialize_AnyThread(LinkContext);  
	}
}
```

##### CacheBones_AnyThread
```c++
void FAnimNode_SkeletalControlBase::CacheBones_AnyThread(const
FAnimationCacheBonesContext& Context)  
{  
	FAnimNode_Base::CacheBones_AnyThread(Context);

	// 在SkeletalControlBase是纯虚函数，实现在派生类
	InitializeBoneReferences(Context.AnimInstanceProxy->GetRequiredBones());

	// 执行LinkNode的CacheBones_AnyThread
	ComponentPose.CacheBones(Context);  
}

void FPoseLinkBase::CacheBones(const FAnimationCacheBonesContext& InContext) 
{  
	if (LinkedNode != nullptr)  
	{      
		LinkedNode->CacheBones_AnyThread(InContext);  
	}
}

```

##### Update_AnyThread
```c++
void FAnimNode_SkeletalControlBase::Update_AnyThread(const
	FAnimationUpdateContext& Context)  
{  
	UpdateComponentPose_AnyThread(Context);  
	
	ActualAlpha = 0.f;  
	if (IsLODEnabled(Context.AnimInstanceProxy))  
	{      
		GetEvaluateGraphExposedInputs().Execute(Context);  
	
		// 根据EAnimAlphaInputType的类型计算ActualAlpha
		// 太长，略去
	
		// Make sure Alpha is clamped between 0 and 1.  
		ActualAlpha = FMath::Clamp<float>(ActualAlpha, 0.f, 1.f);  

		if (FAnimWeight::IsRelevant(ActualAlpha) && IsValidToEvaluate(
			Context.AnimInstanceProxy->GetSkeleton(), 
			Context.AnimInstanceProxy->GetRequiredBones()))  
		  {         
			  UpdateInternal(Context);  
		  }   
	}  
}

// 在SkeletalControlBase这里又是虚函数，只是声明了COUNTER
void FAnimNode_SkeletalControlBase::UpdateInternal(const FAnimationUpdateContext&
	Context)  
{  
	DECLARE_SCOPE_HIERARCHICAL_COUNTER_ANIMNODE(UpdateInternal)  
}
```

##### Evaluate_AnyThread
```c++
```
## Reference
[虚幻引擎 动画节点（AnimNode）详解 - 知乎](https://zhuanlan.zhihu.com/p/611398524)
[从源码深入理解Unreal动画系统_ue 动画蓝图源码解析-CSDN博客](https://blog.csdn.net/hacning/article/details/134463920)
[虚幻4渲染编程（动画篇）【第六卷：自定义动画节点】 - 知乎](https://zhuanlan.zhihu.com/p/52266316)
