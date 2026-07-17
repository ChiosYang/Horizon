---
layout: default
title: "Horizon Summary: 2026-07-17 (ZH)"
date: 2026-07-17
lang: zh
---

> 从 46 条内容中筛选出 13 条重要资讯。

---

1. [Firefox 通过 WebAssembly 在另一个浏览器中运行](#item-1) ⭐️ 9.0/10
2. [Moonshot AI 发布 Kimi K3，一个 2.8 万亿参数的开源模型](#item-2) ⭐️ 9.0/10
3. [日本购买 2.75 万块英伟达 Rubin 芯片用于机器人 AI](#item-3) ⭐️ 9.0/10
4. [台积电再投千亿美元赴美，Q2 利润飙升 77%](#item-4) ⭐️ 9.0/10
5. [arXiv 新书：数据科学的数学基础](#item-5) ⭐️ 8.0/10
6. [LLM 辅助编程：代码审查的认知负担](#item-6) ⭐️ 8.0/10
7. [GPT-5.6 Codex 漏洞可删除用户主目录](#item-7) ⭐️ 8.0/10
8. [Inkling：思考机器实验室的开源权重 MoE 模型](#item-8) ⭐️ 8.0/10
9. [sched-ext 获得子调度器入队和代理执行支持](#item-9) ⭐️ 8.0/10
10. [ExTernD 通过扩展秩分解提升三元 LLM 量化精度](#item-10) ⭐️ 8.0/10
11. [QLoRA 的默认学习率 2e-4 在小数据集上受批评](#item-11) ⭐️ 8.0/10
12. [欧盟裁定谷歌须开放 Android 系统功能与搜索数据给竞争对手](#item-12) ⭐️ 8.0/10
13. [Truth Social 将向华尔街出售特朗普帖子的快速访问权限](#item-13) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Firefox 通过 WebAssembly 在另一个浏览器中运行](https://simonwillison.net/2026/Jul/16/firefox-in-webassembly/#atom-everything) ⭐️ 9.0/10

Puter 已将 Firefox 浏览器编译为 WebAssembly，使其能够在 Chrome 等另一个浏览器内完全运行。该项目使用 Gecko 引擎，开发成本估计为 25,000 美元的 AI 代币。 这一演示证明完整的桌面浏览器可以在网页环境中运行，为虚拟化、跨平台软件分发和浏览器内开发工具开辟了新可能性。它也展示了 AI 辅助编程如何应对巨大的工程挑战。 该项目依赖 Wisp 协议通过 Puter 的服务器代理所有网络流量，因为 WebAssembly 代码无法打开任意网络连接。团队因 Hacker News 的高流量不得不扩展服务器，并且演示支持端到端加密。

rss · Simon Willison · 7月16日 23:34

**背景**: WebAssembly \(WASM\) 是一种二进制指令格式，允许用 C++ 等语言编写的代码在浏览器中以接近原生的速度运行。传统上，由于安全和性能限制，浏览器无法嵌套在其他浏览器内。将 Firefox 这样的完整浏览器编译成 WASM 是一项需要巨大计算量和优化工作的艰巨任务，而该项目通过大量使用 AI 辅助实现了这一目标。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Wire_protocol">Wire protocol</a></li>
<li><a href="https://github.com/MercuryWorkshop/wisp-protocol">GitHub - MercuryWorkshop/wisp-protocol: Wisp is a low-overhead, easy to ...</a></li>

</ul>
</details>

**社区讨论**: Hacker News 社区表现出浓厚兴趣，导致团队不得不扩展服务器以应对流量。该项目被誉为突破性的工程壮举，尽管一些人质疑其实用场景和 AI 辅助开发的成本效益。

**标签**: `#WebAssembly`, `#Firefox`, `#browser`, `#virtualization`, `#AI-assisted development`

---

<a id="item-2"></a>
## [Moonshot AI 发布 Kimi K3，一个 2.8 万亿参数的开源模型](https://simonwillison.net/2026/Jul/16/kimi-k3/#atom-everything) ⭐️ 9.0/10

中国 AI 实验室 Moonshot AI 宣布了 Kimi K3，一个 2.8 万亿参数的开源模型，声称其性能超越 DeepSeek-V4-Pro，并与 Claude Opus 4.8 和 GPT-5.5 等顶级模型竞争。开放权重版本承诺于 2026 年 7 月 27 日发布。 Kimi K3 作为迄今为止最大的开放权重模型，代表了一个重要里程碑，可能加速 AI 的商品化，并加剧中美 AI 实验室之间的竞争。其每任务成本较低但性能高，可能对整个行业的价格造成压力。 该模型使用 2.8 万亿参数，定价为每百万输入 tokens 3 美元、每百万输出 tokens 15 美元，使其成为迄今为止最昂贵的中国开放模型。它在 Arena.ai 的前端代码竞技场中获得最高排名，并在 Artificial Analysis 的长期知识工作评估中达到 1547 Elo。

rss · Simon Willison · 7月16日 20:19

**背景**: “鹈鹕基准测试”是一种幽默的非正式测试，要求 AI 模型生成一个骑自行车的鹈鹕的 SVG 图像，常用于比较模型能力。像 Kimi K3 这样的开放权重模型公开其训练参数，便于进一步研究和微调。参数数量的快速增长反映了 AI 行业追求更强大模型的趋势，而 Moonshot AI 和 DeepSeek 等中国实验室正在挑战美国领先者。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://playcode.io/blog/macbook-svg-benchmark">The Pelican Benchmark Is Saturated. We Made 9 AI... | Playcode Blog</a></li>
<li><a href="https://ndurner.github.io/pelican-benchmark">Pelican vs. Llama 3.1 405B and others | Nils Durner’s Blog</a></li>
<li><a href="https://huggingface.co/spaces/victor/pelican-benchmark">Pelican Benchmark - a Hugging Face Space by victor</a></li>

</ul>
</details>

**社区讨论**: 社区评论包括 Simon Willison 对模型生成鹈鹕 SVG 的测试，花费 25 美分，他指出这是来自中国模型最贵的鹈鹕。其他评论者讨论了商品化的含义，softwaredoug 认为中国实验室旨在通过商品化 AI 软件来销售硬件，而 m3h 则强调了巨大的模型规模和高运营成本。

**标签**: `#AI`, `#open-source`, `#large language models`, `#Moonshot AI`, `#Kim K3`

---

<a id="item-3"></a>
## [日本购买 2.75 万块英伟达 Rubin 芯片用于机器人 AI](https://www.bloomberg.com/news/articles/2026-07-16/japan-to-buy-nvidia-rubin-chips-to-build-sovereign-ai-for-robots) ⭐️ 9.0/10

日本通过新成立的 Noetra 公司宣布计划购买 27,500 块英伟达 Rubin 芯片，建设大型数据中心，用于开发面向机器人的主权基础 AI 模型。该项目计划在 2027 年 3 月前发布首个 AI 模型，并在几年内推出机器人专用版本。 这项获得 240 亿美元政府支持的战略举措标志着日本减少对美中 AI 技术依赖的雄心，目标是在 2040 年前占据全球机器人市场 30%以上份额。它使日本成为中美之外全球 AI 竞赛中的“第三种选择”。 由田场广信领导的 Noetra 将牵头该项目，合作伙伴包括软银、丰田支持的 Preferred Networks 和 NEC。27,500 块 Rubin 芯片属于英伟达下一代架构，配备基于 ARM 的“Vera”CPU，设计为与 Rubin GPU 协同工作的超级芯片。

telegram · zaihuapd · 7月16日 10:59

**背景**: 英伟达 Rubin 架构在 2026 年 CES 上发布，是 Blackwell 平台的继任者，为 AI 工作负载提供显著的计算能力和效率提升。主权 AI 指国家自主开发和掌控 AI 基础设施及模型的能力，以减少对外国技术的依赖。机器人基础模型是设计用于跨多种机器人类型和任务泛化的 AI 系统，使机器人能够在非结构化环境中自主运行。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://explore.n1n.ai/blog/nvidia-rubin-chip-architecture-ai-future-2026-01-06">Nvidia Announces Rubin Chip Architecture as Blackwell Successor</a></li>
<li><a href="https://www.linkedin.com/pulse/navigating-future-sovereign-ai-blueprint-global-arif-sheikh-hluxc">the Future of Sovereign AI : A Blueprint for Global Empowerme</a></li>
<li><a href="https://www.linkedin.com/pulse/robotic-foundation-models-physical-ai-innovations-anand-ramachandran-fzfge">Robotic Foundation Models and Physical AI Models : Innovations...</a></li>

</ul>
</details>

**标签**: `#AI`, `#Robotics`, `#NVIDIA`, `#Japan`, `#Sovereign AI`

---

<a id="item-4"></a>
## [台积电再投千亿美元赴美，Q2 利润飙升 77%](https://www.reuters.com/world/asia-pacific/tsmcs-second-quarter-profit-seen-hitting-record-ai-boom-2026-07-15/) ⭐️ 9.0/10

台积电宣布再向美国亚利桑那州工厂投资 1000 亿美元，总投资额达 2650 亿美元；同时公布第二季度净利润达 7066 亿新台币（约 220 亿美元），同比飙升 77%，创历史新高。 这一巨额投资凸显了台积电对 AI 芯片需求持续增长的信心，并巩固了其向美国扩张的战略，重塑全球半导体供应链，降低对台湾的依赖。 台积电将 2026 年资本支出预测上调至 600 亿至 640 亿美元，并预计全年美元营收增长略超 40%。亚利桑那州目前已有 8 座工厂在建或规划中，未来可能再增 4 座。

telegram · zaihuapd · 7月16日 12:29

**背景**: 台积电是全球最大的专业半导体代工厂，为苹果、英伟达、AMD 等主要客户生产芯片。美国一直推动将先进芯片制造迁回本土以保障供应链安全，并出台了《芯片法案》提供补贴。台积电在亚利桑那州的首笔投资始于 2020 年。

**标签**: `#TSMC`, `#semiconductor`, `#AI`, `#investment`, `#manufacturing`

---

<a id="item-5"></a>
## [arXiv 新书：数据科学的数学基础](https://arxiv.org/abs/2607.11938) ⭐️ 8.0/10

一本名为《数据科学的数学》的新书已在 arXiv 上发布，强调高维直觉及其对现代数据科学的重要性。 这本书填补了空白，为数据科学提供了严谨的数学基础，帮助从业者理解高维直觉为何失效以及它如何影响模型训练和优化。 该书从解释高维下直觉如何失效（尖峰性、体积等）入手，并联系到随机梯度下降和高维模型等主题。它作为开放获取的 LaTeX 源码在 arXiv 上提供。

hackernews · Anon84 · 7月16日 20:38 · [社区讨论](https://news.ycombinator.com/item?id=48939896)

**背景**: 高维数据在现代数据科学中很常见，但我们低维的直觉（如距离、体积）常常误导我们。这种“维度诅咒”使得许多机器学习算法难以处理。理解高维几何对于构建稳健模型至关重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.math.uci.edu/~rvershyn/papers/HDP-book/HDP-2.pdf">High - Dimensional Probability</a></li>
<li><a href="https://en.wikipedia.org/wiki/High-dimensional_statistics">High-dimensional statistics - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 评论者称赞该书对高维直觉的关注，有人指出它对现代数据科学至关重要。另有人提到 Steve Brunton 即将出版的相关书籍。讨论还涉及数据科学定义的演变以及统计学的重要性。

**标签**: `#mathematics`, `#data-science`, `#high-dimensional`, `#education`, `#arxiv`

---

<a id="item-6"></a>
## [LLM 辅助编程：代码审查的认知负担](https://pydantic.dev/articles/the-human-in-the-loop-is-tired) ⭐️ 8.0/10

一篇文章指出，LLM 辅助编程将编写代码的有益体验转变为审查 AI 生成代码的沉重认知负荷，颠覆了传统开发体验。 这意义重大，因为它揭示了 AI 工具隐藏的心理成本，可能影响开发者的满意度、生产力和长期福祉，挑战了 AI 总能改善开发者体验的说法。 文章提出了‘人类奖励函数’问题，即手动编码带来多巴胺刺激，而 AI 将其自动化后只剩下审查的负担。社区成员创造了‘human on the hook’一词，强调人类只在出现问题时才被追究责任。

hackernews · haritha1313 · 7月17日 00:21 · [社区讨论](https://news.ycombinator.com/item?id=48942000)

**背景**: 人在回路中（HITL）是指人类主动监控或引导 AI 系统的范式。在 LLM 辅助编程中，开发人员审查 AI 生成的代码，由于他们自己并未编写代码，因此验证正确性可能非常耗费认知。从编写代码到审查代码的转变改变了开发工作的性质及其心理回报。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.geeksforgeeks.org/artificial-intelligence/human-in-the-loop-hitl-decision-making/">Human-in-the-Loop (HITL) - GeeksforGeeks</a></li>
<li><a href="https://hai.stanford.edu/ai-definitions/what-is-human-in-the-loop">What is Human-in-the-Loop? - Stanford HAI</a></li>
<li><a href="https://sanjewa.com/blogs/ai-code-review-cognitive-burden-harder-than-writing/">AI Code Review: Why It&#x27;s Harder Than Writing Code</a></li>

</ul>
</details>

**社区讨论**: 评论者普遍对‘human on the hook’一词产生共鸣，指出它捕捉到了不对称风险：开发者在成功时没有功劳，但在失败时却要承担责任。一些人表示，通过将 AI 视为代码生成器而非代理，并保持计划性方法以避免认知过载，他们享受到了 AI 辅助。

**标签**: `#LLM`, `#software engineering`, `#developer experience`, `#code review`, `#AI-assisted programming`

---

<a id="item-7"></a>
## [GPT-5.6 Codex 漏洞可删除用户主目录](https://simonwillison.net/2026/Jul/16/bad-codex-bug/#atom-everything) ⭐️ 8.0/10

Thibault Sottiaux 报告了一个 GPT-5.6 Codex 的漏洞：在启用完全访问模式且关闭沙箱保护时，模型可能意外删除用户的主目录。 该漏洞凸显了 AI 编码代理的关键安全风险，意外删除文件可能导致数据丢失和系统受损。它强调了安全部署生成式 AI 工具时沙箱保护和自动审核功能的必要性。 该漏洞在模型尝试覆盖 $HOME 环境变量以设置临时目录时触发，但错误地删除了 $HOME。触发条件包括完全访问模式、无沙箱保护以及关闭自动审核。

rss · Simon Willison · 7月16日 17:45

**背景**: Codex 是 OpenAI 的 AI 编码助手，可以执行命令和修改文件。沙箱技术隔离执行环境以防止损害，自动审核功能会暂停有风险的操作等待用户批准。没有这些保护，AI 代理可能执行破坏性操作，如删除文件。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://northflank.com/blog/how-to-sandbox-ai-agents">How to sandbox AI agents in 2026: MicroVMs, gVisor &amp; isolation ...</a></li>
<li><a href="https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/">Practical Security Guidance for Sandboxing Agentic Workflows and ...</a></li>
<li><a href="https://openai.com/index/running-codex-safely/">Running Codex safely at OpenAI | OpenAI</a></li>

</ul>
</details>

**标签**: `#codex`, `#coding-agents`, `#generative-ai`, `#ai-safety`

---

<a id="item-8"></a>
## [Inkling：思考机器实验室的开源权重 MoE 模型](https://simonwillison.net/2026/Jul/16/inkling/#atom-everything) ⭐️ 8.0/10

由 Mira Murati 领导的思考机器实验室发布了 Inkling，这是一个采用 Apache-2.0 许可的混合专家多模态模型，总参数量 975B，活跃参数量 41B，在包含文本、图像、音频和视频的 45 万亿 token 上训练。他们还宣布了 Inkling-Small（总参数量 276B，活跃参数量 12B），其权重将在测试完成后发布。 此次发布增强了美国开源权重生态系统，提供了与 DeepSeek、Qwen 等中国开源模型竞争的新选择，与 NVIDIA Nemotron 和 Gemma 4 并列。它提供了一个针对微调优化（通过思考机器的 Tinker 平台）的强基座模型，降低了定制门槛。 模型卡信息稀疏，缺乏详细技术规格和训练数据文档，仅含糊提及使用公共和第三方来源。思考机器明确表示 Inkling 不是前沿模型，而是一个适合微调的多功能基座模型，具有多模态能力和高效推理。

rss · Simon Willison · 7月16日 15:35

**背景**: 混合专家（MoE）是一种神经网络架构，它将计算划分为多个专门的“专家”子网络，通过门控机制每个输入仅激活部分专家。这使得模型可以拥有很大的总参数量，同时保持较低的活跃参数（计算成本），从而实现高效扩展。开源权重模型（如 Apache-2.0 许可下发布的模型）提供公开可下载、修改和部署的权重文件，促进了 AI 社区的可复现性和定制化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Mixture_of_experts">Mixture of experts - Wikipedia</a></li>
<li><a href="https://developer.nvidia.com/blog/applying-mixture-of-experts-in-llm-architectures/">Applying Mixture of Experts in LLM Architectures | NVIDIA Technical Blog</a></li>
<li><a href="https://arxiv.org/abs/2507.11181">[2507.11181] Mixture of Experts in Large Language Models</a></li>

</ul>
</details>

**标签**: `#open-weights`, `#Mixture-of-Experts`, `#multimodal`, `#LLM`, `#AI`

---

<a id="item-9"></a>
## [sched-ext 获得子调度器入队和代理执行支持](https://lwn.net/Articles/1082717/) ⭐️ 8.0/10

Linux 的可扩展调度类 sched-ext 即将完成子调度器层次结构和代理执行支持，具体新增了 enqueue\(\) 回调路径及用于层级 CPU 访问控制的能力机制。 这使得多租户系统可以为不同的控制组使用不同的基于 BPF 的调度器，提高了隔离性和灵活性。代理执行将通过跟踪阻塞-依赖关系来解决优先级反转问题。 入队路径使用三级能力系统（空闲 CPU、调度队列、抢占），从父调度器向下传递。父调度器通过 scx\_bpf\_sub\_grant\(\) 授予能力，子调度器不能超越父调度器的能力。

rss · LWN.net · 7月16日 14:00

**背景**: sched-ext 允许通过 struct\_ops 将自定义 CPU 调度器实现为 BPF 程序。最初只支持单个调度器，现在支持与控制组关联的层次化子调度器。代理执行跟踪任务阻塞关系，允许代理任务代表被阻塞的任务执行，解决优先级反转。入队路径此前缺少层级控制，此补丁系列补全了这一点。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.kernel.org/doc/html/next/scheduler/sched-ext.html">Extensible Scheduler Class — The Linux Kernel documentation</a></li>
<li><a href="https://sched-ext.com/docs/OVERVIEW">Overview - sched_ext</a></li>
<li><a href="https://lwn.net/Articles/1030842/">A proxy-execution baby step [LWN.net]</a></li>

</ul>
</details>

**标签**: `#Linux kernel`, `#scheduling`, `#sched\_ext`, `#BPF`, `#systems programming`

---

<a id="item-10"></a>
## [ExTernD 通过扩展秩分解提升三元 LLM 量化精度](https://www.reddit.com/r/MachineLearning/comments/1uy2zb3/externd_expandedrank_ternary_decomposition/) ⭐️ 8.0/10

ExTernD 提出了一种后训练量化方法，将每个权重矩阵分解为两个较小的三元矩阵和一个对角缩放矩阵，从而可以任意扩展内部秩以提高精度。 该方法克服了固定尺寸三元量化的固有精度限制，使三元 LLM 能够在仅适度增加 VRAM 的情况下接近高精度方法的精度，这对高效部署至关重要。 扩展秩可以任意大，实验表明，即使适度扩展也能在仅比当前三元方法略多内存的情况下显著提高精度。

reddit · r/MachineLearning · /u/LMTLS5 · 7月16日 13:31

**背景**: 三元量化将权重表示为-1、0 或+1，相比全精度模型节省内存和计算。然而，先前用于 LLM 的固定尺寸三元后训练量化（PTQ）存在严重的精度损失。ExTernD 通过使用扩展秩分解来解决这一问题，在不需重新训练的情况下增加表示能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2303.01505">[2303.01505] Ternary Quantization: A Survey</a></li>
<li><a href="https://developer.nvidia.com/blog/optimizing-llms-for-performance-and-accuracy-with-post-training-quantization/">Optimizing LLMs for Performance and Accuracy with Post-Training Quantization | NVIDIA Technical Blog</a></li>

</ul>
</details>

**标签**: `#quantization`, `#LLM`, `#efficiency`, `#deep learning`, `#post-training quantization`

---

<a id="item-11"></a>
## [QLoRA 的默认学习率 2e-4 在小数据集上受批评](https://www.reddit.com/r/MachineLearning/comments/1uy1z8b/the_qlora_2e4_default_is_wrong_under_10k_samples/) ⭐️ 8.0/10

一位 Reddit 用户指出，针对少于 1 万样本的小数据集，QLoRA 微调中广泛推荐的默认学习率 2e-4 会导致过拟合，建议改用 1e-4。 这挑战了微调社区中的一个常见假设，可能为处理小数据集的实践者节省大量时间和资源，而小数据集在实际应用中很常见。 该用户报告称，将学习率从 2e-4 改为 1e-4，并将轮次从 3 增加到 5，导致评估指标大幅提升，此前他们花了数周调试数据和提示模板。2e-4 的默认值源于对 52k 样本的 Alpaca 数据集的微调，而非更小的数据集。

reddit · r/MachineLearning · /u/Pretty-Ad774 · 7月16日 12:50

**背景**: QLoRA 是一种高效的微调方法，结合了量化和低秩适应（LoRA）以减少内存使用，使得在消费级 GPU 上微调大语言模型成为可能。学习率是一个关键超参数；在小数据集上学习率过高会导致过拟合，即模型记住训练数据但无法泛化。默认学习率 2e-4 是在使用 52k 样本的 Alpaca 数据集的 QLoRA 论文中确立的，但许多实际微调任务使用的数据集要小得多。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2305.14314">[2305.14314] QLoRA: Efficient Finetuning of Quantized LLMs</a></li>
<li><a href="https://github.com/artidoro/qlora">GitHub - artidoro/qlora: QLoRA: Efficient Finetuning of Quantized LLMs · GitHub</a></li>

</ul>
</details>

**标签**: `#QLoRA`, `#fine-tuning`, `#learning rate`, `#overfitting`, `#small datasets`

---

<a id="item-12"></a>
## [欧盟裁定谷歌须开放 Android 系统功能与搜索数据给竞争对手](https://www.theverge.com/policy/966438/eu-google-android-ai-interoperability-search-data-dma) ⭐️ 8.0/10

欧盟委员会裁定谷歌必须向竞争对手开放 Android 的 11 项系统功能及部分搜索数据，使得 ChatGPT 等第三方 AI 助手能够获得与谷歌 Gemini 同等的系统级权限和数据访问。 这一决定可能从根本上重塑 Android 生态系统和搜索市场，加剧 AI 助手和搜索引擎的竞争，为用户提供更多选择。同时，它也为欧盟《数字市场法案》下监管守门人平台设立了先例。 这 11 项功能包括第三方助手深度集成所需的核心 Android 能力，搜索数据共享则限于特定用途以保护隐私。谷歌仍可基于合理的安全和隐私考量拒绝访问，但任何限制必须符合欧盟规定。

telegram · zaihuapd · 7月16日 13:19

**背景**: 《数字市场法案》（DMA）是欧盟的一项法规，将谷歌等大型平台指定为“守门人”，并施加义务以确保公平竞争。谷歌的 Android 操作系统和 Google 搜索是 DMA 下的核心平台服务，此次裁决是强制合规的约束性措施。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Digital_Markets_Act">Digital Markets Act</a></li>
<li><a href="https://nairametrics.com/2026/07/16/eu-orders-google-to-share-android-features-search-data-with-rivals/">EU orders Google to share Android features, search data with ...</a></li>
<li><a href="https://www.upi.com/Top_News/World-News/2026/07/16/eu-google-specification-requirements-ai-android/7631784213542/">EU orders Google to share data, Android with competitors - UPI</a></li>

</ul>
</details>

**标签**: `#EU regulation`, `#antitrust`, `#Android`, `#Google`, `#AI assistants`

---

<a id="item-13"></a>
## [Truth Social 将向华尔街出售特朗普帖子的快速访问权限](https://www.cnn.com/2026/07/16/business/truth-social-data-wall-street) ⭐️ 8.0/10

特朗普媒体科技集团（TMTG）宣布推出 Truth API 付费数据服务，从 8 月 1 日起向机构客户提供 Truth Social 上排名前 10 账户的毫秒级实时帖子访问。 这使得算法交易者能够比公众更快地对特朗普影响市场的言论做出反应，引发了对市场公平性、内幕交易以及总统商业与公共职责界限模糊的严重担忧。 Truth API 针对前 10 个账户的帖子，TMTG 未公布定价。CNN 此前报道特朗普曾利用 Truth Social 宣传他个人买入的股票。

telegram · zaihuapd · 7月17日 01:02

**背景**: Truth Social 是特朗普在被主要平台封禁后创建的社交媒体平台。高频交易（HFT）利用算法在毫秒级执行交易，通常依赖数据速度优势。通过出售特权数据访问，Truth Social 将其独家内容货币化，但批评者认为这给了金融内部人士不公平的优势。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.timesnownews.com/world/us/us-news/truth-api-explained-trump-media-new-service-gives-investors-faster-access-to-trump-posts-article-155113825">Truth API Explained: Trump Media New Service Gives Investors ...</a></li>
<li><a href="https://marketchameleon.com/articles/b/2026/7/16/trump-media-launches-truth-api-institutional-market-impact">Trump Media Unveils Truth API: Real-Time Access to ...</a></li>
<li><a href="https://zhuanlan.zhihu.com/p/20982511912">高频交易（HFT）：算法交易的闪电世界 - 知乎</a></li>

</ul>
</details>

**标签**: `#social media`, `#algorithmic trading`, `#data monetization`, `#politics`, `#financial regulation`

---