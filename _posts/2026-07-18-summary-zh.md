---
layout: default
title: "Horizon Summary: 2026-07-18 (ZH)"
date: 2026-07-18
lang: zh
---

> 从 39 条内容中筛选出 17 条重要资讯。

---

1. [GPT-5.6 通过提示解决凸优化 30 年难题](#item-1) ⭐️ 9.0/10
2. [台积电 A14 制程良率与性能接近 90%](#item-2) ⭐️ 9.0/10
3. [社区建设需要主动努力](#item-3) ⭐️ 8.0/10
4. [LG 显示器通过 Windows Update 未经同意静默安装软件](#item-4) ⭐️ 8.0/10
5. [Kimi K3 蒸馏实现前沿 AI 水平](#item-5) ⭐️ 8.0/10
6. [开源中的自行车棚效应反思](#item-6) ⭐️ 8.0/10
7. [Anthropic 因竞争压力使 Claude Fable 5 永久保留](#item-7) ⭐️ 8.0/10
8. [《半秒》一书详述 2024 年 XZ 后门事件](#item-8) ⭐️ 8.0/10
9. [Reddit 指控有缺陷的参赛作品赢得 DeepMind/Kaggle AGI 大奖](#item-9) ⭐️ 8.0/10
10. [GPT-2 词元嵌入空间的交互式地图](#item-10) ⭐️ 8.0/10
11. [深度学习综述分类 25 种 scRNA-seq 分析方法](#item-11) ⭐️ 8.0/10
12. [豆包手机放弃 GUI 自动化，转向 MCP 协议](#item-12) ⭐️ 8.0/10
13. [Meta 拟向 Anthropic 出租 AI 算力](#item-13) ⭐️ 8.0/10
14. [SpaceX 与五角大楼谈判提供 AI 算力，交易或达数十亿美元](#item-14) ⭐️ 8.0/10
15. [美国拟设类似 FINRA 的 AI 监管机构](#item-15) ⭐️ 8.0/10
16. [B 站 WAIC 展示开源主动式 AI 伙伴&\#x27;猫娘计划&\#x27;](#item-16) ⭐️ 8.0/10
17. [香港宏福苑大火报告：承包商违规与监管瓦解](#item-17) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [GPT-5.6 通过提示解决凸优化 30 年难题](https://old.reddit.com/r/math/comments/1uxj3cy/after_openais_cdc_proof_announcement_gpt56_used_a/) ⭐️ 9.0/10

GPT-5.6（Sol Pro）仅通过一个提示就解决了一个凸优化领域长达 30 年的公开问题——一个 30 年悬而未决的猜想——给出了在球形域上最小化凸 Lipschitz 函数复杂度的上界的新证明。 这标志着一个重要的里程碑：AI 模型做出了真正的数学贡献，可能加速优化理论的研究，并表明大型语言模型可以解决人类数学家几十年来未能攻克的难题。 该成就是由 GPT-5.6 的 Sol Pro 变体完成的，而非 Ultra 版本；解决的问题是凸优化中一个虽小但真实的贡献，专注于凸 Lipschitz 函数一阶方法的时间复杂度。

hackernews · mbustamanter · 7月18日 13:00 · [社区讨论](https://news.ycombinator.com/item?id=48957779)

**背景**: 凸优化是数学优化的一个子领域，研究在凸集上最小化凸函数。许多此类问题可以高效求解，但一些理论问题——例如精确的最坏情况复杂度——仍然开放。这个被解决的问题涉及限制在球面上使用次梯度法找到凸 Lipschitz 函数近似最小值所需的步数。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Convex_optimization">Convex optimization</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区普遍认可了这一贡献，一位专家指出这是真实但小众的结果。其他人讨论了其对数学研究的影响，认为低垂的果实现在可能由 AI 处理，而人类研究者将专注于更深层次的新方法。还有澄清说使用的模型是 Sol Pro 而非 Ultra。

**标签**: `#AI`, `#convex optimization`, `#mathematical proof`, `#LLM`, `#research`

---

<a id="item-2"></a>
## [台积电 A14 制程良率与性能接近 90%](https://www.tomshardware.com/tech-industry/semiconductors/tsmc-confirms-significant-yield-and-performance-improvements-in-a14-update-strong-interest-from-ai-hpc-and-smartphone-customers) ⭐️ 9.0/10

台积电在财报电话会上宣布，其 A14（1.4 纳米级）制程的器件性能已接近目标水平的 90%，256Mb SRAM 良率也接近 90%，分别高于 4 月的 85%和 80%+，来自 AI、高性能计算和智能手机客户的兴趣浓厚。 这一进展表明台积电有望按计划于 2028 年量产，甚至可能提前，这将为 AI 和 HPC 芯片带来显著的能效提升，并巩固台积电在先进制程领域的领先地位。 与 N2（2 纳米级）相比，A14 在同功耗下性能提升 10-15%，同频下功耗降低 25-30%，逻辑晶体管密度提高 23%；它采用第二代 GAA 纳米片晶体管，得益于 N2 积累的经验。

telegram · zaihuapd · 7月18日 05:00

**背景**: 全环绕栅极（GAA）纳米片晶体管是一种新一代晶体管设计，栅极环绕沟道的四周，能够实现更好的静电控制，允许超越 FinFET 的进一步微缩。台积电的 A14 是 1.4 纳米级节点，继 N2（2 纳米）之后，预计在 2028 年左右进入量产。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://wccftech.com/tsmc-1-4nm-process-faces-no-obstacles-as-risk-production-to-start-in-2027/">TSMC ’s Facing No Development Obstacles With Its Next-Generation...</a></li>
<li><a href="https://www.phonearena.com/news/tsmc-says-what-follows-2nm-node_id153534">For the first time, TSMC reveals what will follow the 2 nm node</a></li>
<li><a href="https://www.synopsys.com/blogs/chip-design/what-are-gate-all-around-gaa-transistors.html">What are Gate-All-Around (GAA) Transistors? | Synopsys Blog</a></li>

</ul>
</details>

**标签**: `#semiconductor`, `#TSMC`, `#A14`, `#AI`, `#HPC`

---

<a id="item-3"></a>
## [社区建设需要主动努力](https://www.benlandautaylor.com/p/if-you-build-it-they-will-come) ⭐️ 8.0/10

文章认为，社区需要主动努力来建立和维护，将被动消费与草根主动性和脆弱性的必要性进行了对比。 这一观点意义重大，因为它挑战了常见的对社交场景的被动态度，指出社会疏离可能源于个人在社区结构中的投入不足。 文章借鉴了个人经验和世代观察，指出像俱乐部和舞会这样的草根社会机构已经衰落，并质疑为什么这些没有被传承下来。

hackernews · barry-cotter · 7月18日 15:37 · [社区讨论](https://news.ycombinator.com/item?id=48959090)

**背景**: 社区建设常常被误解为自然发生的事，但实际上它需要刻意的努力和脆弱性。文章将此与更广泛的社会趋势联系起来，即人们将自己视为被动消费者而非主动参与者。

**社区讨论**: 评论者分享了作为‘社会结构’所需的脆弱性的个人经历，指出当努力得不到回报时，可能会导致有毒的内心对话。其他人观察到代际鸿沟，即老一辈的社会机构没有传承给年轻一代。

**标签**: `#community building`, `#social dynamics`, `#grassroots organizations`, `#open source culture`, `#generational shifts`

---

<a id="item-4"></a>
## [LG 显示器通过 Windows Update 未经同意静默安装软件](https://videocardz.com/newz/lg-monitors-silently-install-software-through-windows-update-without-user-consent) ⭐️ 8.0/10

LG 显示器会在用户连接 HDMI 时，通过 Windows Update 静默安装专有软件到 Windows 电脑上，无需用户同意。 这种做法绕过了用户控制，带来了安全和隐私风险，因为该软件随系统启动运行且拥有完全系统权限，可能被恶意利用。 该软件在插入新 LG 显示器或之前连接过的显示器时会自动安装，并且每次系统启动时运行，没有任何沙箱保护。

hackernews · baranul · 7月18日 10:21 · [社区讨论](https://news.ycombinator.com/item?id=48956688)

**背景**: Windows Update 可以在连接设备时自动下载并安装来自硬件供应商的驱动相关软件，旨在简化设置，但如果供应商分发非必要或潜在不受欢迎的软件，则可能被滥用。用户可以通过组策略或设备安装设置禁用此行为。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://learn.microsoft.com/en-us/windows-hardware/drivers/dashboard/understanding-windows-update-automatic-and-optional-rules-for-driver-distribution">Understanding Windows Update rules for driver distribution - Windows drivers | Microsoft Learn</a></li>
<li><a href="https://blog.zealtyro.com/lg-monitors-silently-installing-windows-software/">LG Monitors Silently Installing Software via Windows Update : What...</a></li>
<li><a href="https://mundobytes.com/en/How-to-prevent-Windows-Update-from-automatically-installing-drivers-in-Windows-10-and-11/">Prevent automatic driver installation in Windows Update</a></li>

</ul>
</details>

**社区讨论**: 用户对静默安装感到震惊，有人称其为“恶意软件”，并指出即使是旧款显示器也会触发安装。评论者提供了通过组策略或设备安装设置禁用制造商应用自动下载的解决方法，并就微软和 LG 谁应负主要责任展开辩论。

**标签**: `#security`, `#privacy`, `#Windows`, `#drivers`, `#LG`

---

<a id="item-5"></a>
## [Kimi K3 蒸馏实现前沿 AI 水平](https://stephen.bochinski.dev/blog/2026/07/18/the-kimi-k3-moment/) ⭐️ 8.0/10

一家中国实验室通过从更大模型中蒸馏知识，实现了与 GPT-5.6 和 Opus 4.8 等前沿 AI 模型的性能持平，并发布了 Kimi K3 模型。 这一里程碑表明，模型蒸馏可以迅速缩小与领先 AI 实验室的差距，可能颠覆竞争格局，并引发关于开放权重模型的国家安全担忧。 Kimi K3 拥有 2.8 万亿参数，定价为每百万 token 输入/输出 3/15 美元，与 GPT-5.6 Sol（5/30 美元）和 Opus 4.8（5/25 美元）相当。一些用户报告称，在复杂任务上它比领先模型花费的时间显著更长。

hackernews · sbochins · 7月18日 17:32 · [社区讨论](https://news.ycombinator.com/item?id=48960218)

**背景**: 模型蒸馏将知识从大型“教师”模型转移到较小的“学生”模型，从而以较低成本实现高效性能。开放权重模型公开提供模型参数，与闭源前沿模型不同。该技术被视为实现 AI 能力民主化的一种方式，在 AI 社区中被广泛讨论。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Knowledge_distillation">Knowledge distillation - Wikipedia</a></li>
<li><a href="https://www.ibm.com/think/topics/knowledge-distillation">What is Knowledge distillation? | IBM</a></li>
<li><a href="https://www.analyticsvidhya.com/blog/2025/04/open-weight-models/">What are Open Source and Open Weight Models ? | Analytics Vidhya</a></li>

</ul>
</details>

**社区讨论**: 评论者意见不一：一些人认为蒸馏是不可避免且合法的方法，而另一些人则担心国家安全的打压。用户 SwellJoe 报告说，Kimi K3 在处理一个 OpenAI 模型快速完成的任务时表现吃力，表明可能存在质量权衡。用户 credit\_guy 指出参数和定价的相似性，暗示直接竞争。

**标签**: `#AI`, `#distillation`, `#open-weight models`, `#geopolitics`, `#frontier labs`

---

<a id="item-6"></a>
## [开源中的自行车棚效应反思](https://queue.acm.org/detail.cfm?id=3818307) ⭐️ 8.0/10

Poul-Henning Kamp 的文章《再见，感谢所有的自行车棚》回顾了开源中的自行车棚效应，并提供了如何有效管理琐碎决策的见解。 这篇文章之所以重要，是因为自行车棚效应浪费了社区的时间和精力；理解它有助于开源项目聚焦重要问题并保持生产力。 作者 PHK 是 FreeBSD 的著名开发者，创造了 MD5crypt；文章结合了历史背景和避免琐碎争议的实用建议。

hackernews · Ygg2 · 7月18日 17:27 · [社区讨论](https://news.ycombinator.com/item?id=48960155)

**背景**: 自行车棚效应，也称为帕金森琐碎定律，描述了人们在琐碎事务上花费过多时间而忽视重要事务的倾向。这是组织和开源社区中的常见现象，简单但不重要的问题往往引发过度讨论。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.thebehavioralscientist.com/glossary/bikeshedding">Bikeshedding - The Behavioral Scientist</a></li>
<li><a href="https://thedecisionlab.com/biases/bikeshedding?ref=cynicalsignals.com">Bikeshedding - The Decision Lab</a></li>

</ul>
</details>

**社区讨论**: 评论者强调了可逆决策的概念作为自行车棚效应的解决方案，并提到了 PHK 对 MD5crypt 等的贡献。部分评论还涉及了技术领域的年龄限制和性别问题。

**标签**: `#open source`, `#bikeshedding`, `#software engineering`, `#community management`

---

<a id="item-7"></a>
## [Anthropic 因竞争压力使 Claude Fable 5 永久保留](https://simonwillison.net/2026/Jul/18/claude-make-fable-5-permanent/#atom-everything) ⭐️ 8.0/10

Anthropic 推翻了之前的决定，宣布从 7 月 20 日起，Claude Fable 5 将包含在所有 Max 和 Team Premium 计划中，使用限制为 50%，并为 Pro 和 Team Standard 用户提供 100 美元积分。这一变化源于来自 GPT-5.6 Sol 和 Kimi 3 的竞争压力。 这一逆转表明 AI 模型市场存在激烈的竞争动态，订阅计划必须包含顶级模型才能保持竞争力。Anthropic 高级计划的用户现在可以信赖持续访问公司最强大的模型，缓解了对‘Fable 末日’的担忧。 最初将 Fable 5 从订阅中移除的计划是出于算力限制，它仍然被排除在每月 20 美元的 Pro 计划之外。Max 计划的定价为每月 100 美元和 200 美元，50%的限制意味着订阅者可以将总使用配额的一半用于 Fable 5。

rss · Simon Willison · 7月18日 06:00

**背景**: Claude Fable 5 是 Anthropic 公开发布的最强大的大型语言模型，专为高要求编码任务和长期自主工作而设计。它最初与私有版本 Claude Mythos 5 一同发布。竞争格局包括 OpenAI 的 GPT-5.6 Sol（一款具有最先进编码和推理能力的旗舰模型）和 Moonshot AI 的 Kimi 3（Kimi K3），后者拥有 2.8 万亿参数，在基准测试中排名第三。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Fable_5">Claude Fable 5</a></li>
<li><a href="https://www.anthropic.com/claude/fable">Claude Fable \ Anthropic</a></li>
<li><a href="https://openai.com/index/gpt-5-6/">GPT‑5.6: Frontier intelligence that scales with your ambition</a></li>
<li><a href="https://en.wikipedia.org/wiki/Kimi_%28chatbot%29">Kimi (chatbot) - Wikipedia</a></li>

</ul>
</details>

**标签**: `#AI`, `#Claude`, `#Anthropic`, `#model availability`, `#competition`

---

<a id="item-8"></a>
## [《半秒》一书详述 2024 年 XZ 后门事件](https://lwn.net/Articles/1083466/) ⭐️ 8.0/10

作者 Adrian Mastronardi 发布了免费书籍《半秒》，详细叙述了 2024 年 XZ 后门事件的经过，包括社会工程学和技术细节。 这本书全面记录了一次几乎危及数百万 Linux 系统的关键供应链攻击，成为网络安全教育和意识的重要资源。 该书以非商业性、禁止演绎的 Creative Commons 许可证发布，可在 half-second.com 免费获取。书中重点描述了被操纵的孤独维护者、在半秒内发现后门的工程师，以及身份不明的攻击者。

rss · LWN.net · 7月18日 16:52

**背景**: 2024 年 3 月，在广泛用于 Linux 系统的压缩库 XZ Utils 中发现了一个后门。该后门编号为 CVE-2024-3094，允许攻击者通过 OpenSSH 远程执行代码，并且是通过针对项目维护者的复杂社会工程学活动植入的。这一事件凸显了开源供应链安全中的脆弱性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/XZ_Utils_backdoor">XZ Utils backdoor - Wikipedia</a></li>
<li><a href="https://gist.github.com/thesamesam/223949d5a074ebc3dce9ee78baad9e27">xz-utils backdoor situation (CVE-2024-3094) · GitHub</a></li>
<li><a href="https://systemweakness.com/the-xz-backdoor-cve-2024-3094-how-a-supply-chain-attack-nearly-compromised-every-linux-server-fae44fe73a21">The XZ Backdoor (CVE-2024–3094): How a Supply Chain Attack ...</a></li>

</ul>
</details>

**标签**: `#XZ backdoor`, `#supply chain security`, `#open source security`, `#cybersecurity`, `#book`

---

<a id="item-9"></a>
## [Reddit 指控有缺陷的参赛作品赢得 DeepMind/Kaggle AGI 大奖](https://www.reddit.com/r/MachineLearning/comments/1uzyf66/did_blatant_ai_slop_just_win_a_25k_usd_deepmind/) ⭐️ 8.0/10

一篇 Reddit 帖子提供了证据，表明 DeepMind/Kaggle“衡量 AGI 进展”竞赛的大奖得主提交了有缺陷且毫无意义的方法，质疑了评审过程的公正性。 这一事件引发了对高知名度 AI 竞赛中研究诚信和评估标准的严重担忧，可能削弱对基准驱动进展声明的信任。 该帖子分析了获奖作品的写作、方法、代码和数据，声称其生成了随机数字和毫无根据的声明。组织者表示评审过程得当，这只是主观解读的问题。

reddit · r/MachineLearning · /u/TheWerkmeister · 7月18日 15:10

**背景**: 这项由 Google DeepMind 赞助、在 Kaggle 上举办的竞赛要求参与者设计新的基于认知科学的 AI 基准来衡量 AGI 进展，大奖奖金为 25000 美元。这一争议凸显了如何评估 AI 系统以及竞赛中同行评审严谨性的持续辩论。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blog.google/innovation-and-ai/models-and-research/google-deepmind/measuring-agi-cognitive-framework/">Measuring Progress Towards AGI: A Cognitive Framework</a></li>
<li><a href="https://arxiv.org/html/2603.13372v1">The ARC of Progress towards AGI: A Living Survey of Abstraction and Reasoning</a></li>

</ul>
</details>

**标签**: `#AI ethics`, `#Kaggle`, `#DeepMind`, `#research integrity`, `#LLM evaluation`

---

<a id="item-10"></a>
## [GPT-2 词元嵌入空间的交互式地图](https://www.reddit.com/r/MachineLearning/comments/1v09muj/interactive_map_of_gpt2s_token_embedding_space/) ⭐️ 8.0/10

一位 Reddit 用户创建了 GPT-2-small 词元嵌入空间的交互式地图，利用 t-SNE 降维和最小生成树来可视化 32,070 个字母词元之间的关系。 该工具使 GPT-2 的词元嵌入更易于解释和访问，帮助研究人员和从业者无需运行前向传播即可理解词元之间的关系。它促进了对语言模型如何在词元层面表示含义的更好直觉。 该地图在嵌入表的压缩表示上使用 t-SNE，边由最小生成树绘制，仅显示最近的亲缘关系。它支持移动设备，支持双指缩放，并包含一个搜索框，可跳转到任何词元。

reddit · r/MachineLearning · /u/Limp-Contest-7309 · 7月18日 22:42

**背景**: 词元嵌入是语言模型（如 GPT-2）中子词单元的密集向量表示。t-SNE 是一种非线性降维技术，将高维数据投影到 2D 或 3D 以便可视化，同时保留局部结构。最小生成树以最小总边权重连接所有点，揭示最接近的成对关系。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.datacamp.com/tutorial/introduction-t-sne">Introduction to t - SNE : Nonlinear Dimensionality Reduction and Data...</a></li>
<li><a href="https://www.geeksforgeeks.org/dsa/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/">Kruskal’s Minimum Spanning Tree (MST) Algorithm - GeeksforGeeks</a></li>
<li><a href="https://www.alignmentforum.org/posts/BMghmAxYxeSdAteDc/an-exploration-of-gpt-2-s-embedding-weights">An exploration of GPT-2&#x27;s embedding weights</a></li>

</ul>
</details>

**标签**: `#machine learning`, `#embeddings`, `#interpretability`, `#visualization`, `#NLP`

---

<a id="item-11"></a>
## [深度学习综述分类 25 种 scRNA-seq 分析方法](https://www.reddit.com/r/MachineLearning/comments/1v06nc1/deep_learning_tackles_singlecell_analysis_a/) ⭐️ 8.0/10

一篇 Reddit 帖子总结了一篇全面的综述论文，该论文将 25 种用于单细胞 RNA-seq 分析的深度学习方法分为六个子类别，并提供了包含每种方法的目的、架构和新颖性的详细表格。 该综述为计算生物学研究人员提供了有价值的结构化概览，帮助他们了解深度学习在单细胞基因组学中快速发展的领域。它突出了 AI 技术如何以前所未有的分辨率推进我们分析细胞异质性的能力。 所涵盖的方法分为六类：数据插补、降维、聚类、基因调控网络推断、轨迹推断和细胞类型注释。表格中包含了每种方法的指标和独特性描述。

reddit · r/MachineLearning · /u/teraRockstar · 7月18日 20:35

**背景**: 单细胞 RNA 测序（scRNA-seq）在单个细胞水平上测量基因表达，揭示组织中的细胞异质性。深度学习模型，如自编码器和变分自编码器，越来越多地应用于数据去噪、批次校正和细胞聚类等任务。这篇综述论文系统性地回顾了这些应用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.linkedin.com/pulse/single-cell-rna-sequencing-placental-biology-danish-muhammad-1bgxe">Single - Cell RNA Sequencing in Placental Biology and Pregnancy...</a></li>
<li><a href="https://www.technologynetworks.com/informatics/news/deep-learning-tech-will-open-up-the-epigenome-287581">Deep Learning Tech Will Open Up the... | Technology Networks</a></li>
<li><a href="https://reactjsnotes.online/a-microscope-to-see-the-diversity-of-cells/">a microscope to see the diversity of cells - React JS Software</a></li>

</ul>
</details>

**标签**: `#deep learning`, `#single-cell RNA-seq`, `#computational biology`, `#survey`, `#bioinformatics`

---

<a id="item-12"></a>
## [豆包手机放弃 GUI 自动化，转向 MCP 协议](https://www.latepost.com/news/dj_detail?id=3648) ⭐️ 8.0/10

豆包手机放弃了原本通过模拟点击操作微信、淘宝等超级应用的 GUI 自动化方式，转而要求这些应用提供 MCP 服务以开放数据和操控权限。该公司已将备货量从 3 万台提升至数十万台。 这一转变反映了 AI 手机助手使用 GUI 自动化面临的现实挑战——此前超级应用曾封禁此类访问。豆包采用 MCP 框架，与苹果、Google 等公司的行业趋势一致，可能重塑 AI 代理与平台服务的集成方式。 豆包手机助手软件于 2025 年 7 月 15 日获得生成式人工智能服务备案。其技术预览版于 2024 年 12 月发布，但因微信和淘宝的封禁而被迫下线相关功能。

telegram · zaihuapd · 7月18日 00:29

**背景**: GUI 自动化是指 AI 助手读取屏幕并模拟人类点击来操作应用，但这种方式很脆弱，经常被超级应用封禁。MCP（模型上下文协议）是一种新兴标准，允许 AI 模型通过协议直接请求应用的数据和操作，类似于 AI 领域的 USB-C 接口。这减少了摩擦，并打开了受控访问的通道。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://modelcontextprotocol.io/">What is the Model Context Protocol ( MCP )? - Model Context Protocol</a></li>
<li><a href="https://developer.volcengine.com/articles/7485579294153342995">比Playwright更高效！ BrowserTools MCP 让Cursor...</a></li>
<li><a href="https://developer.aliyun.com/article/1137931">基于Python uiautomation实现Windows GUI ...</a></li>

</ul>
</details>

**标签**: `#AI assistant`, `#MCP`, `#Doubao phone`, `#super apps`, `#industry dynamics`

---

<a id="item-13"></a>
## [Meta 拟向 Anthropic 出租 AI 算力](https://www.nytimes.com/2026/07/17/technology/meta-anthropic-ai-computing-power.html) ⭐️ 8.0/10

Meta 正与 AI 初创公司 Anthropic 进行早期谈判，拟将其数据中心 AI 算力出租给后者，潜在交易规模高达两年 100 亿美元。 这笔交易凸显出 AI 算力基础设施的严重稀缺，可能为 Meta 开辟新的收入来源以抵消其巨额资本支出，同时为 Anthropic 提供关键的算力资源。 Anthropic 于 2026 年 6 月提出该方案，Meta 正在评估；若达成协议，Anthropic 将按月付款，双方均可提前退出。谈判尚处早期阶段，未必能最终成交。

telegram · zaihuapd · 7月18日 01:14

**背景**: Meta 今年计划投入高达 1450 亿美元，其中大量用于 AI 与数据中心建设。这笔潜在交易凸显出在全球 GPU 短缺背景下，AI 初创公司争抢算力，而大型科技公司则寻求将其基础设施投资变现。

**标签**: `#AI`, `#cloud computing`, `#Meta`, `#Anthropic`, `#data center`

---

<a id="item-14"></a>
## [SpaceX 与五角大楼谈判提供 AI 算力，交易或达数十亿美元](https://www.wsj.com/tech/ai/spacex-in-talks-to-provide-computing-power-for-pentagons-ai-push-15e752e4) ⭐️ 8.0/10

SpaceX 正与美国国防部谈判，拟提供用于运行 AI 模型的数据中心算力，交易金额可能高达数十亿美元。 该交易将显著深化 SpaceX 与五角大楼的关系，并加速美国军方对 AI 的应用，对国家安全和云计算市场产生深远影响。 谈判仍在进行中，存在破裂可能。SpaceX 近期还与 Anthropic 和谷歌签署了类似算力供应协议，并计划大幅扩展其云计算业务。

telegram · zaihuapd · 7月18日 01:44

**背景**: 五角大楼正加速获取云计算能力，以支持国家安全及日常作战中的 AI 应用。包括 SpaceX、亚马逊、谷歌、微软和甲骨文在内的多家科技公司已获准在机密环境中使用其 AI 模型。SpaceX 以其星链卫星网络和星舰运载火箭闻名，同时也在建设其云计算服务。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Anthropic">Anthropic - Wikipedia</a></li>

</ul>
</details>

**标签**: `#AI`, `#SpaceX`, `#五角大楼`, `#云计算`, `#国防`

---

<a id="item-15"></a>
## [美国拟设类似 FINRA 的 AI 监管机构](https://www.bloomberg.com/news/articles/2026-07-17/us-considers-creating-finra-like-watchdog-to-vet-top-ai-models) ⭐️ 8.0/10

特朗普政府正考虑设立一个类似美国金融业监管局（FINRA）的独立机构，负责审查顶尖 AI 模型的安全性，该方案由财政部长斯科特·贝森特牵头，目前正由白宫幕僚长苏茜·威尔斯审阅。 此举旨在回应华尔街对网络安全的担忧以及硅谷对临时性政府管控的不满，让两大行业在安全标准制定中拥有更大话语权。若实施，或将确立美国 AI 监管的新范式。 该计划与 Google DeepMind 首席执行官德米斯·哈萨比斯提出的由行业资助的独立监管机构的建议方向一致。Anthropic 和 OpenAI 此前曾对美国政府要求修改或推迟模型发布提出异议。相关框架仍在讨论中，尚未经总统特朗普审阅。

telegram · zaihuapd · 7月18日 05:45

**背景**: 美国金融业监管局（FINRA）是一个自律监管组织，在 SEC 监管下监督经纪公司并执行规则以保护投资者，于 2007 年由 NASD 和纽交所监管部门合并而成。拟议的 AI 监管机构将类似地成为一个独立的、由行业资助的机构，负责制定和执行安全标准，并向政府机构汇报。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://baike.baidu.com/item/%E7%BE%8E%E5%9B%BD%E9%87%91%E8%9E%8D%E4%B8%9A%E7%9B%91%E7%AE%A1%E5%B1%80/9213493">美国金融业监管局_百度百科 Rules &amp; Guidance - FINRA.org 美国金融业监管局：Financial Industry Regulatory Authority (FINRA) 据市场相关消息，美国正筹划设立一个职能类似美国金融业监管局（FINRA... 美国金融投行FINRA监管牌照 - cnjrp.com 美国金融业监管局 (FINRA) | 美股导航</a></li>

</ul>
</details>

**标签**: `#AI regulation`, `#US policy`, `#AI safety`, `#governance`, `#technology policy`

---

<a id="item-16"></a>
## [B 站 WAIC 展示开源主动式 AI 伙伴&\#x27;猫娘计划&\#x27;](https://finance.sina.com.cn/roll/2026-07-18/doc-iniifanf8394663.shtml) ⭐️ 8.0/10

B 站在 2026 世界人工智能大会上展示了开源 AI 伙伴&\#x27;猫娘计划&\#x27;（Project N.E.K.O.），这是一个能够理解桌面内容并主动发起对话的原生全模态系统。 这标志着从被动 AI 助手向主动感知用户数字环境并交互的 AI 伙伴的重大转变，可能改变用户与虚拟角色的互动方式。 该系统采用 UI、AI 大脑与记忆系统分离的架构，核心数据可保留在本地。支持 Live2D 和 VRM 角色模型、物理反馈、带声线克隆的 TTS 语音模块以及多语言切换。

telegram · zaihuapd · 7月18日 06:45

**背景**: AI 伙伴是为提供情感支持和交互而设计的虚拟角色。传统 AI 助手是被动的，仅在用户召唤时响应。&\#x27;猫娘计划&\#x27;是主动式的，即持续感知用户屏幕和环境，基于上下文主动发起对话。VRM 是用于 VR 和 VTubing 的开放 3D 角色格式标准，而 VoiceClone 使用 AI 从音频样本中复制声音。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://vrm.dev/en/">3D humanoid avatar file format for VR | VRM</a></li>
<li><a href="https://voicecloneai.app/blog/how-ai-voice-cloning-works">How AI Voice Cloning Works: A Complete Guide... | VoiceClone AI</a></li>
<li><a href="https://multimodal-react.github.io/">MM-ReAct: Prompting ChatGPT for Multimodal Reasoning and Action</a></li>

</ul>
</details>

**标签**: `#AI companion`, `#multimodal AI`, `#open-source`, `#computer vision`, `#virtual being`

---

<a id="item-17"></a>
## [香港宏福苑大火报告：承包商违规与监管瓦解](https://china.caixin.com/2026-07-17/102465415.html) ⭐️ 8.0/10

一份关于 2025 年香港火灾（造成 168 人死亡）的 627 页调查报告显示，承包商蓄意使用非阻燃材料并提交伪造防火证书，而多个政府部门未能执行安全监管。 这场灾难暴露了香港建筑物维修监管的系统性失灵，突显了自我监管和执法不力的致命后果。调查结果可能推动该地区建筑安全及监管问责制的改革。 承建商宏业建筑在外墙翻新中使用了非阻燃安全网和发泡胶板，并篡改消防系统，包括排空水箱和关闭主电掣。房屋局独立审查组仅进行文件检查，并提前通知巡查。

telegram · zaihuapd · 7月18日 10:01

**背景**: 在高层建筑翻新过程中，常使用施工安全网和发泡保温材料。阻燃材料对于防止火势沿楼梯间等垂直井道迅速蔓延至关重要。施工期间必须保持消防主电掣和喷淋系统正常运行以确保消防安全。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.strongarmstore.com/products/debris-safety-netting-non-fr-black">Construction Safety Netting | Scaffold Netting - Black Non FR</a></li>
<li><a href="https://en.wikipedia.org/wiki/Backdraft">Backdraft - Wikipedia</a></li>

</ul>
</details>

**标签**: `#safety`, `#regulation`, `#construction`, `#Hong Kong`, `#disaster`

---