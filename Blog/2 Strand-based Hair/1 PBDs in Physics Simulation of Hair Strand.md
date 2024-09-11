
### 前言

随着计算机硬件设备性能的提升和算法的进步，Strand-based(基于发丝)的头发渲染在近年来的各家游戏引擎都得到了实现。
最早是Frostbite在Siggraph2019分享的发丝渲染技术，物理模拟的部分在之后在寒霜官网有相关的视频叙述，然后是UE的Groom和AMD的TressFX，Unity在Siggraph2022也分享了他们的发丝物理模拟和渲染技术。以下是相关的资料。
##### Frostbite
[Strand-based hair rendering in Frostbite (realtimerendering.com)](https://www.advances.realtimerendering.com/s2019/hair_presentation_final.pdf)
[How Frostbite is Advancing the Future of Hair Rendering Technology (ea.com)](https://www.ea.com/frostbite/news/the-future-of-hair-rendering-technology-in-frostbite)
##### Groom
[UE4 Hair Strands浅析 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/128669105)
[虚幻引擎Groom资产编辑器用户指南 | 虚幻引擎5.2文档 (unrealengine.com)](https://docs.unrealengine.com/5.2/zh-CN/groom-asset-editor-user-guide-in-unreal-engine/)
##### TressFX
[【GPUOpen】TressFX 4.1新一代真实感毛发 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/343741493)
[保姆级毛发算法调研分析，十万长文带你深入TressFX（一） - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/517553643)
##### Unity
[Probe-based lighting, strand-based hair system, and physical hair shading in Unity’s ‘Enemies’](https://www.advances.realtimerendering.com/s2022/SIGGRAPH2022-Advances-Enemies-Ciardi%20et%20al.pptx)

这些头发系统中发丝的物理模拟的核心算法都是[PBD](https://matthias-research.github.io/pages/publications/posBasedDyn.pdf))或者[XPBD](https://matthias-research.github.io/pages/publications/XPBD.pdf))，其中TressFX和Unity使用的都是PBD，UE的Groom用的是XPBD，Unity和Groom还引入了[Position and Orientation Based Dynamics](https://animation.rwth-aachen.de/media/papers/2016-SCA-Cosserat-Rods.pdf)，下文会分别对这三个算法做简要介绍。

### Position Based Dynamics

#### 目的
和任何一个实时物理模拟算法一样，
* Stability
* Robustness 
* Speed  
* Visually plausible
用一个简单粗暴（但不太正确）的方式理解为啥PBD在效率上强于传统方法。下面列出了不同方法的计算路径，可以看到PBD明显地缩短了计算所需的步骤。
* 基于力的方法: 力->加速度->速度->位置
* 基于冲量的方法: 冲量->速度->位置
* PBD: 约束->位置

### 算法流程

#### 