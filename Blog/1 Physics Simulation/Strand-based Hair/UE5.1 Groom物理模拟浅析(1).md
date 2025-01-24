### 底层算法简述
UE中Groom的物理模拟用的是XPBD算法， 是基于PBD[]改进实现的。

PBD，即Position-Based Dynamics，其基本思路就是，相比传统的基于力的方法，力->加速度->速度->位移的计算路径，通过前置的一系列的对位置的约束，能够简化这个过程。PBD实际就将物理模拟的计算过程，转化为对约束的求解，计算的路径就变成了外力 + 约束 -> 位移。下图为Games104讲Cloth Solver时对PBD的简要概括。个人理解的话，约束就相当于对衣料或头发的物理性质的描述（有点像在深度学习模型中引入先验知识）。
![[Pasted image 20230325145257.png]]

至于如何求解这个约束，推荐直接看PBD的论文。原文我是觉得写的有点抽象的，如果跟我一样之前没有接触过物理以及数学上迭代求解这方面的内容，可以先看Games104的物理那部分内容，然后看Games103讲基于约束的方法，最后再去读论文。知乎上讲的比较好的有这篇文章[]。

XPBD的话，在PBD的基础上，提出了通过约束描述弹性势能，解决了PBD算法中单位时间内求解约束的迭代次数会对模拟效果产生影响的问题，让siftness能够准确地描述模拟物体的物理性质。个人理解，XPBD和PBD在模拟的性能上差异不大，主要是为了让TA/美术更容易去调节布料或者头发的参数。

### Groom物理模拟

Groom的物理模拟部分的实现的路径是UnrealEngine\Engine\Plugins\Runtime\HairStrands，主要的代码都在\Source\HairStrandsCore下，该目录的\Public下是Groom相关的头文件，\Private下是头文件对应的源文件和与Niagara相关的数据接口文件。

上文中所提到的求解约束的方法，在UE中就是Niagara Solver。下图展示了Groom的资产编辑器，红框标注的地方就是选择Niagara Solver的地方。Niagara Solver的资产路径在Content\Emitters下，官方默认的Groom Springs/Rods使用的是StableSprings/RodsSystem，另外还提供了GroomSprings/RodsSystem，新建NiagaraSystem的时候可以继承它们。关于Groom资产编辑器的物理参数，想详细了解的同学可以查阅官方文档，以及这篇文章[]。
![[Snipaste_2023-03-25_14-44-48.png]]

打开Niagara System，可以看到解算器的具体实现过程。图中显示的是GroomSpringsSystem中Emitter的实现过程。Rods和Springs的实现基本上是一致的，只是在求解的时候使用的material不同。发射器中调用的HLSL函数，具体实现在Shaders\Private下。
![[Pasted image 20230325150211.png]]

#### Advance Groom State
Emitter实现了Groom的物理模拟。UE中对Groom的物理模拟的实现就不止是XPBD而已了，还有速度场、导线、插值等等，不过XPBD依然是物理模拟最核心的内容。XPBD的具体实现在Advance Groom state中。
