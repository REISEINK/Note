#### local frame accelerations

* 局部帧加速度影响布料的程度可以通过惯性缩放控制来控制: cloth.setInertiaScale(0.5f)
* 限制局部帧加速度影响粒子的程度对于快速移动的情况有效


#### 胶囊体
* 还提到胶囊体（球体使用不同的半径）共享球体以模拟关节，并highly encouraged，我们没用
![[Pasted image 20240124170244.png]]


#### Continuous Collision Detection
* 可以尝试开启
#### Virtual Particle Collision
* UE没用

#### Inter-Collision
* 尝试开启
