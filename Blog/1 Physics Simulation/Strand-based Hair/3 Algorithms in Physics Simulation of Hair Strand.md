发丝的物理模拟中，除了最核心的PBD/XPBD算法来约束头发的长度、形状以外，为了头发整体效果更加真实，还需要实现比如发丝之间的交互、发丝在风场中会受风力影响、发丝跟随角色运动等效果，下文会简要介绍一下实现这些效果的这些算法。

### Collective Propeties of Hair

#### Frosibite (Strand-Strand Interactions)

#### Friction

**Volumetric Methods for Simulation and Rendering of Hair**
A drag term for each hair is then computed based on the velocity difference between the hair particle and the grid velocity. ... For example, if a particle is moving faster than its neighbors, with velocity smoothing it will slow down.
![[Pasted image 20230531102943.png]]

![[Pasted image 20230531103027.png]]

#### Volume Preservation
![[Pasted image 20230531103111.png]]
#### Velocity Field

This velocity is rasterized to![[Pasted image 20230531103111.png]] a grid and made divergence free using the Chorin projection method. The divergence free velocity field is compared to the original grid velocity field, and this difference is interpolated to the particles and applied as an impulse.

由于水流不会凭空产生或消失，即不可压缩流体的总散度必为零。在流体力学中，散度指流体运动时单位体积的改变率。

![[Pasted image 20230601103400.png]]
#### Pressure Grid

#### Fluid Drag


#### Self collision




### Wind(风场)




### VelocityShockPropagation(VSP)速度震动传播



### SDF(有向距离场)

![[TressFX_SDF.png]]

![[TressFX_SDF2.png]]


