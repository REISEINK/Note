#### 总览

#### Emitter Spawn

##### Setup Groom Datas
设置物理模拟演算需要的数据接口，同时还设置了压力场大小（用于计算Fluid Drag、Friction、Volume Preservation）。

传入参数有三个，HairStrands、PhysicsAsset和PressureGrid。
HairStrands是GroomAsset，包括了Groom本身的各种信息，比如物理模拟、插值的相关参数，详细可以参照UE的官方文档[虚幻引擎Groom资产编辑器用户指南 | 虚幻引擎5.2文档 (unrealengine.com)](https://docs.unrealengine.com/5.2/zh-CN/groom-asset-editor-user-guide-in-unreal-engine/)。
PhysicsAsset用于计算碰撞约束， 

#### Emitter Update

##### Setup Groom Physics
设置物理模拟需要的各种参数。
包括发丝自身的属性、XPBD Solver相关的属性、重力、空气阻力、约束相关的属性等。

##### Spawn Groom Nodes
计算需要的粒子数量，生成粒子用于物理模拟。

#####
#### Particle Spawn

##### Reset Groom Points
将RestPositionBuffer的数据赋值给DeformedPositionBuffer，猜测用作插值？

##### Set Groom Location


##### 
#### Particle Update

##### Store Groom State
将粒子当前的Position和Orientation保存至PreviousPosition和PreviousOrientation，PreviousPosition和PreviousOrientation会参与后续的计算。
同时计算当前例子是否能够移动或者旋转（一根发丝由多个粒子组成，如下图所示），Groom默认是设置为第一个和第二个粒子不能移动，第一个粒子不能旋转（靠近头的粒子认为它会跟随头保持相对静止）。
![[Pasted image 20230712104332.png]]

##### UpdateGroomVelocity
计算流体阻力，可以参考寒霜视频中的Friction部分。将Groom粒子网格化，然后每个粒子的速度跟所属网格的平均速度做加权计算以模拟流体阻力。
![[Pasted image 20230712104903.png]]

##### RewindGroomState
XPBD算法中的Velocity Damping。详见PBD和XPBD论文的Damping一节。
![[Snipaste_2023-07-12_10-53-24.png]]

##### Attach Groom Roots
插值相关，略。

##### Advance Groom State
