
### PxPart
#### PxBase

* 反射: 提供了运行时类型识别的功能。
* 序列化: `PxBase`没有直接提供序列化相关的接口，不过`PxBase`是`PxCollection`的成员，而PxCollection提供了序列化功能，~~猜测PxBase的派生类中实现了序列化方法~~PhysX 的序列化系统是基于 `PxSerialization` 类来实现的，这个系统能够对 `PxBase` 及其派生类对象进行序列化(From ChatGPT)。
* 继承关系
![](https://docs.nvidia.com/gameworks/content/gameworkslibrary/physx/apireference/files/classPxBase__inherit__graph.png)
```c++
struct PxBaseFlag  
{    
enum Enum  
   {  
      eOWNS_MEMORY   = (1<<0),  
      eIS_RELEASABLE = (1<<1)  
   };  
};

// 提供反射的接口类
class PxBase
{
public:
	// 作用: 释放PxBase的instance
	virtual void release()

	// 返回动态类型的字符串名称（派生类的类名）
    virtual const char* getConcreteTypeName()

	// 如果类型匹配，返回对应类型的指针，否则返回NULL
    template<class T> T* is() 
	    { return typeMatch<T>() ? static_cast<T*>(this) : NULL; }
	template<class T> const T* is() const 
		{ return typeMatch<T>() ? static_cast<const T*>(this) : NULL; }

	// 设置/清除flag
	PX_FORCE_INLINE void setBaseFlag(PxBaseFlag::Enum flag, bool value)
		{ mBaseFlag = value ? mBaseFlags|flag : mBaseFlag&~flag}
	PX_FORCE_INLINE void setBaseFlag(PxBaseFlag inFlags) 
		{ mBaseFlag = inFlags; }

	// 获取flag
	PX_FORCE_INLINE PxBaseFlags getBaseFlags() const { return mBaseFlags; }

	// 
	virtual bool is Releasable() const { mBaseFlags & PxBaseFlags & 
		PxBaseFlags::eIS_RELEASABLE; }

protected:
	// 构造函数
	PX_INLINE PxBase(PxType concreteType, PxBaseFlags baseFlags)  
	            : mConcreteType(concreteType), mBaseFlags(baseFlags) {}   
	
	// 反序列化的构造函数
	PX_INLINE PxBase(PxBaseFlags baseFlags) : mBaseFlags(baseFlags) {}  

	// 析构函数
	virtual ~PxBase()

	virtual bool isKindOf(const char* superClass) const 
		{ return !::strcmp(superClass, "PxBase"); }

	template<class T>  bool typeMatch() const { // implementation }



protected:
	PxType  mConcreteType; 
	PxBaseFlags mBaseFlags;
 
}
```


#### PxActor
* 继承自`PxBase`，相较于`PxBase`，主要多了`PxActorFlag`、`PxActorType`、`getScene()`方法、`getWorldBounds()`方法、`DominanceGroup`和`OwnerClient`相关的接口。
* `PxActor`是物理SDK中主要模拟对象的基类。`PxActor`被`PxScene`持有并包含在内。

```c++
typedef PxU8 PxDominanceGroup;

struct PxActorFlag
{
	enum Enum 
	{
		eVISUALIZATION = (1 << 0),
		eDISABLE_GRAVITY = (1 << 1),
		eSEND_SLEEP_NOTIFIES = (1 << 2),
		eDISABLE_SIMULATION = (1 << 3)
	};
};

struct PxActorType
{
	enum Enum
	{
		eRIGID_STATIC,
		eRIGID_DYNAMIC,
		eARTICULATION_LINK,
		eACTOR_COUNT,
		eACTOR_FORCE_DWORD = 0x7fffffff
	};
};

class PxActor : public PxBase  
{    
public:
	// 删除该Actor，不会保持对已删除实例的引用
	virtual void release() = 0;

	// 获取该Actor的类型
	virtual PxActorType::Enum getType() const = 0;

	// 获取该Actor所属的PxScene
	virtual PxScene* getScene() const = 0;

	// Debug用，不会在SDK中使用
	virtual void setName(const char* name) = 0;
	virtual const char* getName() const = 0;

	// 获取该Actor的包围盒
	virtual PxBounds3 getWorldBounds(float inflation=1.01f) const = 0;

	// Actor Flag相关
	virtual void setActorFlags(PxActorFlag::Enum flag, bool value) = 0;
	virtual void setActorFlags(PxActorFlags inFlags) = 0;
	virutal void getActorFlags() const = 0;

	// Dominance Group相关
	virtual void setDominanceGroup(PxDominanceGroup dominanceGroup) = 0;
	virtual PxDominanceGroup getDominanceGroup() const = 0;

	// OwnerClient相关
	virtual void setOwnClient(PxClientID inClient) = 0;
	virtual PxClientID getOwnerClient() const = 0;

	// 如果Actor是aggregate的一部分，返回aggregate
	virtual PxAggregate* getAggregate() const = 0;

	void* userData;

protected:
	// 构造/析构函数
	PX_INLINE PxActor(PxType concreteType, PxBaseFlags baseFlags) :
				  : PxBase(concreteType, baseFlags), userData(NULL) {}
	PX_INLINE PxActor(PxBaseFlags baseFlags) : PxBase(baseFlags) {}
	virtual ~PxActor() {}
	
	virtual bool isKindOf(const char* name) const 
		{ return !::strcmp("PxActor", name) || PxBase::isKindOf(name) }
}
```

##### Question
* release() ”不会保持对已删除实例的引用“ 具体指的是啥？


#### PxRigidActor
* `PxRigidBody`是表示刚体的基类，派生类包括`PxRigidDynamic`、`PxRigidStatic`表示动态刚体和静态刚体。
* `PxRigidBody`通过定义一组attached shapes来指定对象的几何形状
* 继承自`PxActor`，相较于父类，主要多了`GlobalPose`相关的接口，Shape、Constraint相关的接口。

```c++
class PxRigidActor : public PxActor  
{    
public:
	virtual void release() = 0;

	// 获取Actor的世界空间变换
	virtual PxTransfrom getGlobalPose() const = 0;
	// 设置Actor的世界空间变换
	virtual void setGlobalPose(const PxTransform& pose, bool autowake = true) = 0;

	// Shape相关
	virtual void attachShape(PxShape& shape) = 0;
	virtual void detachShape(PxShape& shape, bool wakeOnLostTouch = true) = 0;
	virtual uint32_t getNbShapes() const = 0;
	virtual uint32_t getShapes(PxShape** userBuffer, uint32_t bufferSize, 
		uint32_t startIndex) const = 0;

	// Constraint相关
	virtual uint32_t getNbConstraints() const = 0;
	virtual uint32_t getConstraints(PxConstraint** userBuffer, 
		uint32_t bufferSize, uint32_t startIndex = 0) const = 0

protected:
	// 构造/析构函数
	PX_INLINE PxRigidActor(PxType concreteType, PxBaseFlags baseFlags) 
				  : PxActor(concreteType, baseFlags) {}  
	PX_INLINE PxRigidActor(PxBaseFlags baseFlags) : PxActor(baseFlags) {}  
	virtual ~PxRigidActor()    {}
	
	virtual bool isKindOf(const char* name) const  
		{ return !::strcmp("PxRigidActor", name) || PxActor::isKindOf(name); }
}
```

#### PxRigidStatic

#### PxRigidBody
* 继承自`PxRigActor`, 主要多了一系列刚体运动的接口，包括质心、质量、惯性、速度、力、力矩、碰撞，此外还有RigidBodyFlag控制PxRigidBody的行为。


```c++
struct PxRigidBodyFlag  
{  
   enum Enum  
   {  
     eUSE_KINEMATIC_TARGET_FOR_SCENE_QUERIES = (1<<1),  
     eENABLE_CCD                             = (1<<2),
     eENABLE_CCD_FRICTION                    = (1<<3),  
     eENABLE_POSE_INTEGRATION_PREVIEW        = (1 << 4),  
     eENABLE_SPECULATIVE_CCD                 = (1 << 5),  
     eENABLE_CCD_MAX_CONTACT_IMPULSE         = (1 << 6)  
   };  
};

class PxRigidBody : public PxRigidActor
{
public:

	// 质心/质量
	virtual void setCMassLocalPose(const PxTransform& pose) = 0；
	virtual PxTransform getCMassLocalPose() const = 0;
	virtual void setMass(flaot Mass) = 0;
	virtual float getMass() const = 0;
	virtual float getInvMass() const = 0;

	// 惯性
	virtual void setMassSpaceInertiaTensor(const PxVec3& m) = 0;
	virtual PxVec3 getMassSpaceInertiaTensor() const = 0;
	virtual PxVec3 getMassSpaceInvInertiaTensor() const = 0;

	// 速度
	virtual PxVec3 getLinearVelocity() const = 0;
	virtual PxVec3 setLinearVelocity(const PxVec3& linVel, 
		bool autowake = true) = 0;
	virtual PxVec3 getAngularVelocity() const = 0;
	virtual PxVec3 setAngularVelocity(const PxVec3& angVel, 
		bool autowake = true) = 0;

	// 力/力矩
	virtual void addForce(const PxVec3& force, PxForceMode::Enum mode =
		PxForceMode::eFORCE, bool autowake = true) = 0;
	virtual void addTorque(const PxVec3& torque, PxForceMode::Enum mode = 
		PxForceMode::eFORCE, bool autowake = true) = 0;
	virtual void clearForce(PxForceMode::Enum mode = PxForceMode::eFORCE) = 0;
	virtual void clearTorque(PxForceMode::Enum mode = PxForceMode::eFORCE) = 0;

	// RigidBodyFlag
	virtual void setRigidBodyFlag(PxRigidBodyFlag::Enum flag, bool value) = 0;  
	virtual void setRigidBodyFlags(PxRigidBodyFlags inFlags) = 0;
	virtual PxRigidBodyFlags getRigidBodyFlags() const = 0;

	// 碰撞相关
	virtual void setMinCCDAdvanceCoefficient(PxReal advanceCoefficient) = 0;
	virtual float getMinCCDAdvanceCoefficient() const = 0;
	virtual void setMaxDepenetrationVelocity(PxReal biasClamp) = 0;
	virtual float getMaxDepenetrationVelocity() const = 0;
	virtual void setMaxContactImpulse(PxReal maxImpulse) = 0;
	virtual float getMaxContactImpulse() const = 0;

protected:
	PX_INLINE PxRigidBody(PxType concreteType, PxBaseFlags baseFlags) 
				  :PxRigidActor(concreteType, baseFlags) {}  
	PX_INLINE PxRigidBody(PxBaseFlags baseFlags) : PxRigidActor(baseFlags) {}  
	virtual ~PxRigidBody() {}  
	virtual bool isKindOf(const char* name) const { return 
		!::strcmp("PxRigidBody", name) || PxRigidActor::isKindOf(name); }

}
```




#### PxRigidDynamic

#### PxArticulationLink

#### 
#### Question
* PX_INLINE和PX_FORCEINLINE的区别？
* 为啥NpRigidDynamic没有像NpRigidStatic一样直接持有相关数据
#### 

### NpPart

##### 继承关系
以NpActorTemplate为例，NpActor继承PxActor不是直接像常规写法一样
```c++
class NpActor : public PxActor {}
```
而是通过模板继承的，通过具体如下所示
```c++
template<class APIClass>
class NpActorTemplate : public APIClass, public NpActor, public Ps::UserAllocated 
{
}
```
在这里实现了NpActorTemplate继承自APIClass，如果想让NpActorTemplate继承PxActor，只需要这样使用即可
```c++
NpActorTemplate<PxActor> NpActor;
```
不过实际上PhysX使用的方法还是稍有不同，先NpRigidBodyTemplate->NpRigidActorTemplate->NpActorTemplate一路继承下来，然后NpRigidDynamic直接继承NpRigidDynamicT, 即NpRigidBodyTemplate\<PxRigidDynamic\>

```c++
class NpRigidActorTemplate : public NpActorTemplate<APIClass> {}
class NpRigidBodyTemplate : public NpRigidActorTemplate<APIClass> {}

typedef NpRigidBodyTemplate<PxRigidDynamic> NpRigidDynamicT;
class NpRigidDynamic : public NpRigidDynamicT {}
```
##### 
NpRigidDynamic又如何被Scene使用的？

```c++
class NpRigidDynamic;  
typedef NpRigidBodyTemplate<PxRigidDynamic> NpRigidDynamicT;

class NpRigidDynamic : public NpRigidDynamicT
{

}
```