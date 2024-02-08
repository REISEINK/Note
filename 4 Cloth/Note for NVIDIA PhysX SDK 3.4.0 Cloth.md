
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



#### Constraints

##### Distance Constraints

##### Collision Detection
衣料的碰撞是独立于PhysX的，但也可以使用PxClothFlag::eSCENE_COLLISION去开启与PxScene actors的碰撞。
布料支持与球体，胶囊体，平面，凸包和三角面的碰撞。其中球体和胶囊体的碰撞支持连续碰撞检测，还使用空间加速结构剔除距离远的粒子。因此，碰撞的物理资产推荐以球体和胶囊体为主。

* 还提到胶囊体共享球体以模拟关节，并highly encouraged，UE中可以吗？
* ![[Pasted image 20240124170244.png]]

连续碰撞检测开启？
##### Friction and Mass Scaling

##### Self Collision of Single Cloth Actor
Self-collision distance 定义了每个粒子周围球体的直径，Solver 确保这些球体在模拟过程中不会重叠。Self-collision stiffness 定义了分离碰撞的粒子的冲量的强度。
如果两个粒子的静止位置比碰撞距离更近，则忽略它们之间的碰撞。但是，较大的碰撞距离和使用休息位置会显著降低自碰撞的性能，因此应谨慎使用。
