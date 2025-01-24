
## Constraint
### Distance Constraint

距离约束的目的就是让布料中的两个顶点，能够一定程度上维持两者的距离不变，从而保持布料的形态。具体到公式上，就是希望满足下述公式的值为0 。
$$
C(p_1, p_2) = |p_1 - p_2| - d
$$
布料模拟迭代过程中求解 Distance Constraint 所做的事情，可以由下图简单概括。对于两个顶点太近的情况，就让它们拉远。
![[Pasted image 20240123154901.png]]
反之，两个顶点太远的情况，则让他们靠近。
![[Pasted image 20240123154918.png]] 

Vertical Constraint、Horizontal Constraint、Bend Constraint、Shear Constraint其实都是距离约束，只是顶点的连接方式不同，下图显示了布料中四种距离约束连接方式的不同，从上到下分别是(1) Vertical Constraint和Horizontal Constraint (2) Shear Constraint (3) Bend Constraint 。
![[Pasted image 20240123160138.png]]
Vertical Constraint 和 Horizontal Constraint 中连接的是相邻的顶点，前者在垂直方向上，后者在水平方向上。这两个约束的目的是希望相邻顶点之间能够维持原距离，从而保持布料在垂直方向和水平方向上的形状。
Shear Constraint 中连接的则是对角线的顶点。对角的顶点维持原距离，说明布料没有发生扭转之类的情况。
Bend Constraint 中连接的是次相邻的垂直或水平方向上的顶点。这种情况下顶点的距离没有变化，说明布料没有发生折叠。这里NvCloth应该是做了一个简化，PBD原文里是用的是三角面之间的角度来表示弯曲程度，如下图所示。
![[Pasted image 20240123164038.png]]

![[Pasted image 20240123164028.png]]
* Stiffness: 表示约束的强度，Stiffness 越大，布料就越硬，顶点之间就更倾向于维持原来的长度。
* Stiffness Multiplier: 约束强度的缩放值。在 Limit 范围内时，会对约束强度进行缩放
* Stretch Limit: 拉伸长度的限制。超过该限制，约束强度不会进行缩放。
* Compression Limit: 压缩长度的限制。超过该限制，约束强度不会进行缩放。

举个例子，对于下述的 4 个距离约束，假设Stiffness = 0.8，Stiffness Multiplier = 0.5， Stretch Limit = 1.2，Compression Limit = 0.6，如果构成约束的边压缩超过 60% 或拉伸超过 120% ，Stiffness = 0.8，否则 Stiffness = 0.8 * 0.5 = 0.4 。

## Collision
#### Collision


#### Self-Collision
布料中的自碰撞用来处理
* Self-collision
## AeroDynamics

#### Wind

#### Drag




## Solver
跟论文PBD的实现的不同和NvCloth的一些trick


## Reference
