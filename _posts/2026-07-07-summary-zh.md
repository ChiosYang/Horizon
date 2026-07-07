---
layout: default
title: "Horizon Summary: 2026-07-07 (ZH)"
date: 2026-07-07
lang: zh
---

> 从 47 条内容中筛选出 21 条重要资讯。

---

1. [MIRA：面向火箭联盟的 50 亿参数交互式世界模型](#item-1) ⭐️ 9.0/10
2. [KVM 十六年老漏洞导致虚拟机逃逸，影响 Intel 和 AMD](#item-2) ⭐️ 9.0/10
3. [中国拟限制顶尖国产 AI 模型出口](#item-3) ⭐️ 9.0/10
4. [Kokoro：本地、CPU 友好、高质量的文本转语音模型](#item-4) ⭐️ 8.0/10
5. [StreetComplete：一次一个任务完善 OpenStreetMap](#item-5) ⭐️ 8.0/10
6. [欧盟聊天控制提案：隐私与儿童安全之争](#item-6) ⭐️ 8.0/10
7. [欧盟强制要求所有新车安装驾驶员监控摄像头](#item-7) ⭐️ 8.0/10
8. [微软解雇 id Software 的 idTech 引擎团队](#item-8) ⭐️ 8.0/10
9. [欧盟议会通过聊天控制第一轮投票](#item-9) ⭐️ 8.0/10
10. [为什么 98%的成功率常常不够](#item-10) ⭐️ 8.0/10
11. [Astro 7.0 发布：Rust 工具链与构建性能提升](#item-11) ⭐️ 8.0/10
12. [sqlite-utils 4.0 新增数据库迁移与嵌套事务](#item-12) ⭐️ 8.0/10
13. [Woodruff：可信发布并非可信信号](#item-13) ⭐️ 8.0/10
14. [Linux 内核中更快的 RCU 和无锁内存分配](#item-14) ⭐️ 8.0/10
15. [Mozilla CTO 就开源 AI 报告举办 AMA](#item-15) ⭐️ 8.0/10
16. [谷歌新增‘保存媒体’设置，Lens 和语音数据用于 AI 训练](#item-16) ⭐️ 8.0/10
17. [中国企业从英伟达转向国产 AI 芯片](#item-17) ⭐️ 8.0/10
18. [new-api 修复计费整数溢出漏洞](#item-18) ⭐️ 8.0/10
19. [英伟达 Blackwell 晶圆美国制造，但封装仍需台湾](#item-19) ⭐️ 8.0/10
20. [DeepSeek 自主研发 AI 芯片以减少对英伟达和华为的依赖](#item-20) ⭐️ 8.0/10
21. [加州纽约力推 3D 打印机装枪支拦截软件引争议](#item-21) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [MIRA：面向火箭联盟的 50 亿参数交互式世界模型](https://www.reddit.com/r/MachineLearning/comments/1upofuw/mira_multiplayer_interactive_world_models_trained/) ⭐️ 9.0/10

来自 General Intuition、Kyutai 和 Epic Games 的研究人员发布了 MIRA，这是一个具有 50 亿参数的交互式世界模型，在 1 万小时的合成《火箭联盟》数据上训练，能够在单个 B200 GPU 上以 20 FPS 支持 4 人实时游戏。 MIRA 展示了大规模世界模型在多玩家、物理复杂环境中的可行性，通过提供可玩演示和开源工具，可能加速游戏 AI、模拟和强化学习的研究。 该模型使用潜在扩散架构，根据所有四名玩家的动作生成视频帧，团队还发布了 1000 小时的四人游戏数据集、技术报告和可玩的在线演示。

reddit · r/MachineLearning · /u/MasterScrat · 7月7日 07:59

**背景**: 世界模型是学习模拟环境动态的神经网络，使智能体能够进行规划和推理。之前的单玩家世界模型将其他智能体视为环境的一部分，但 MIRA 以多个智能体的动作为条件，使其适用于多玩家游戏。《火箭联盟》是一款基于物理的高速游戏，玩家控制火箭动力汽车将球打入球门。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/mira-wm/mira">MIRA: Multiplayer Interactive World Models with ... - GitHub</a></li>
<li><a href="https://arxiv.org/abs/2607.05352">[2607.05352] Multiplayer Interactive World Models with ...</a></li>
<li><a href="https://www.linkedin.com/posts/generalintuition_introducing-mira-a-playable-multiplayer-activity-7479870314252922880-y9CV">Introducing MIRA. A playable, multiplayer world model. A ...</a></li>

</ul>
</details>

**标签**: `#world models`, `#reinforcement learning`, `#simulation`, `#interactive AI`, `#game AI`

---

<a id="item-2"></a>
## [KVM 十六年老漏洞导致虚拟机逃逸，影响 Intel 和 AMD](https://github.com/V4bel/Januscape) ⭐️ 9.0/10

研究人员公开了 Januscape（CVE-2026-53359），这是 KVM shadow MMU 中的一个 use-after-free 漏洞，允许客户虚拟机在 Intel 和 AMD 平台上逃逸到宿主机。该漏洞在 Linux 内核中存在约 16 年，从 2010 年持续到 2026 年 6 月。 这是首个已知的同时适用于 Intel VMX 和 AMD SVM 的客户机到宿主机逃逸漏洞，对使用 KVM 的多租户云环境构成严重威胁。该漏洞曾被用作 Google kvmCTF 的 0-day 攻击，可能破坏云服务商的隔离边界。 漏洞位于 Intel 和 AMD x86 KVM 实现共享的 shadow MMU 代码中的 kvm_mmu_get_child_sp() 函数。已发布 PoC 代码可在客户机内触发宿主机内核 panic，在 RHEL 等发行版中，本地普通用户还可利用该缺陷提权至 root。

telegram · zaihuapd · 7月7日 10:14

**背景**: KVM（基于内核的虚拟机）是 Linux 内核模块，允许宿主机运行多个虚拟机。Shadow MMU 是 KVM 的一个组件，通过使用主机物理地址来影子化客户机页表，用于当硬件辅助嵌套分页不可用或禁用时。Use-after-free 漏洞发生在内存被释放后仍被引用，可能导致数据损坏或被利用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://thehackernews.com/2026/07/16-year-old-linux-kvm-flaw-lets-guest.html">16-Year-Old Linux KVM Flaw Lets Guest VMs Escape to Host on ...</a></li>
<li><a href="https://cyberpress.org/16-year-old-linux-kvm-vulnerability/">16-Year-Old Linux KVM Vulnerability Allows Malicious Guests ...</a></li>
<li><a href="https://docs.kernel.org/virt/kvm/x86/mmu.html">The x86 kvm shadow mmu — The Linux Kernel documentation</a></li>

</ul>
</details>

**标签**: `#vulnerability`, `#KVM`, `#virtualization`, `#security`, `#Linux kernel`

---

<a id="item-3"></a>
## [中国拟限制顶尖国产 AI 模型出口](https://www.reuters.com/world/beijing-is-looking-curbing-overseas-access-chinas-top-ai-models-sources-say-2026-07-07/) ⭐️ 9.0/10

中国商务部正在考虑限制最先进国产 AI 模型的海外访问，包括尚未发布的模型，并已与阿里巴巴、字节跳动和智谱等公司开会讨论。 这项政策可能通过限制技术转移来重塑全球 AI 竞争格局，并可能引发其他国家的对等措施。 限制范围仍在商讨中，可能仅适用于未来发布的新模型；尚不确定这些规则是否会最终落地。

telegram · zaihuapd · 7月7日 11:42

**背景**: AI 模型是在大型数据集上训练的软件系统。出口管制是政府用来防止战略技术落入对手手中的工具。中国正在快速提升 AI 能力，引发国家安全方面的考虑。

**标签**: `#AI regulation`, `#China`, `#export control`, `#AI models`, `#geopolitics`

---

<a id="item-4"></a>
## [Kokoro：本地、CPU 友好、高质量的文本转语音模型](https://ariya.io/2026/03/local-cpu-friendly-high-quality-tts-text-to-speech-with-kokoro/) ⭐️ 8.0/10

Kokoro 是一个开源文本转语音模型（8200 万参数），可在 CPU 上高效运行，包括 Apple Silicon，无需专用 GPU。 这填补了没有强大 GPU 的用户的空白，使得在日常计算机上实现高质量文本转语音成为可能，适用于无障碍、阅读和自动化工作流。 Kokoro 支持手动 IPA 发音指南，并带有命令行工具；它生成的语音自然，但在单个词或同形异义词上可能表现不佳。

hackernews · speckx · 7月7日 18:24 · [社区讨论](https://news.ycombinator.com/item?id=48821576)

**背景**: 文本转语音（TTS）将书面文本转换为口语音频。高质量的 TTS 通常需要神经网络，这些网络受益于 GPU 加速，因此本地纯 CPU 解决方案较为罕见。Kokoro 设计为在 CPU 上高效运行，在 Apple Silicon 上利用 mlx-audio 库。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://grokipedia.com/page/Kokoro_TTS">Kokoro TTS</a></li>
<li><a href="https://github.com/nazdridoy/kokoro-tts">GitHub - nazdridoy/kokoro-tts: A CLI text-to-speech tool using the ...</a></li>

</ul>
</details>

**社区讨论**: 社区评论显示热情的采用。用户赞赏 Kokoro 用于无障碍产品、通过 RSS 阅读文章，甚至作为语音控制界面的基础。一些人指出同形异义词和单个词语发声的限制，但整体情绪积极。

**标签**: `#TTS`, `#local`, `#CPU`, `#accessibility`, `#open-source`

---

<a id="item-5"></a>
## [StreetComplete：一次一个任务完善 OpenStreetMap](https://streetcomplete.app/) ⭐️ 8.0/10

StreetComplete 是一款免费开源的安卓应用，它将贡献 OpenStreetMap 变成简单的游戏化任务，例如回答营业时间或人行横道等问题。 通过降低入门门槛，StreetComplete 使普通用户也能为 OpenStreetMap 贡献高质量数据，无需技术专业知识即可帮助保持地图的准确和完整。 StreetComplete 专为移动使用设计，提示用户附近可快速完成的任务，无需事先了解 OpenStreetMap 的标签系统。

hackernews · kls0e · 7月7日 12:38 · [社区讨论](https://news.ycombinator.com/item?id=48816883)

**背景**: OpenStreetMap (OSM) 是一个协作项目，旨在创建免费可编辑的世界地图，由志愿者贡献驱动。然而，对于新手来说，编辑 OSM 的学习曲线可能很陡峭。StreetComplete 通过提供一个简单的界面来引导用户完成具体的小任务，解决了这一问题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/StreetComplete">StreetComplete - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/OpenStreetMap">OpenStreetMap</a></li>

</ul>
</details>

**社区讨论**: 社区评论显示强烈的好评，用户称赞其对初学者友好的界面和有趣的方式。然而，一些用户对数据重复以及无法添加新道路或小径等有限编辑功能表示担忧。还有讨论关于 Google 可能使用 OSM 数据而不回馈，以及让当地店主更新自己数据的困难。

**标签**: `#OpenStreetMap`, `#crowdsourcing`, `#mapping`, `#open data`, `#mobile app`

---

<a id="item-6"></a>
## [欧盟聊天控制提案：隐私与儿童安全之争](https://fightchatcontrol.eu/chat-control-overview) ⭐️ 8.0/10

欧盟正在推进聊天控制 1.0 和 2.0 提案，要求消息平台扫描所有私人消息和上传内容以查找儿童性虐待材料，这可能削弱端到端加密。 这些提案代表了向大规模监控的重大转变，威胁到所有欧盟公民数字通信的隐私和安全。如果通过，可能开创削弱加密的全球先例，并赋予政府更广泛的监控能力。 聊天控制依赖于客户端扫描，即在加密前检查用户设备上的内容，绕过端到端保护。这些提案因误报等技术风险以及当局可能超出儿童保护目的滥用而受到批评。

hackernews · gasull · 7月7日 14:23 · [社区讨论](https://news.ycombinator.com/item?id=48818311)

**背景**: 聊天控制是一套欧盟立法提案，旨在打击网上的儿童性虐待材料。其关键技术机制是客户端扫描（CSS），即在内容加密前在设备上进行分析，从而有效绕过端到端加密。这种方法引发了严重的隐私担忧，因为它可能实现对所有通信的大规模监控。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.internetsociety.org/wp-content/uploads/2020/03/2022-Client-Side-Scanning-Factsheet-EN.pdf">CC BY-NC-SA 4.0 Client-Side Scanning</a></li>
<li><a href="https://academic.oup.com/cybersecurity/article/10/1/tyad020/7590463">Bugs in our pockets: the risks of client-side scanning | Journal of Cybersecurity | Oxford Academic</a></li>

</ul>
</details>

**社区讨论**: 评论者普遍持批评态度：有人指出这些提案以保护儿童为名赋予‘独裁权力’，另有人强调禁止反对聊天控制的政党具有讽刺意味。技术用户质疑如何在不断开加密的情况下扫描加密消息，指出设备端扫描或特权解密都是有缺陷的方案。

**标签**: `#privacy`, `#surveillance`, `#encryption`, `#EU law`, `#policy`

---

<a id="item-7"></a>
## [欧盟强制要求所有新车安装驾驶员监控摄像头](https://allaboutcookies.org/eu-mandatory-distracted-driver-system) ⭐️ 8.0/10

自 2024 年 7 月起，欧盟《一般安全法规 2019/2144》要求所有在欧盟销售的新车型必须配备驾驶员监控系统（DMS），该系统通过摄像头检测分心和疲劳驾驶。 该法规旨在减少因驾驶员注意力不集中引发的事故，但也引发了驾驶员和消费者权益倡导者对隐私和可用性的重大担忧。 DMS 必须纳入车辆型式认证流程，且不能被永久禁用。该系统通常使用红外摄像头追踪眼球和头部运动，在检测到分心时发出警报。

hackernews · nickslaughter02 · 7月7日 20:50 · [社区讨论](https://news.ycombinator.com/item?id=48823557)

**背景**: 驾驶员监控系统利用车内摄像头和计算机视觉评估驾驶员警觉性，最早由丰田在 2006 年推出。欧盟《一般安全法规 2019/2144》自 2022 年起对新车型、2024 年起对所有新车生效，强制要求逐步引入包括 DMS 在内的安全功能，作为推动自动驾驶和道路安全更广泛举措的一部分。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Driver_monitoring_system">Driver monitoring system - Wikipedia</a></li>
<li><a href="https://eur-lex.europa.eu/eli/reg/2019/2144/oj/eng">Regulation - 2019/2144 - EN - EUR-Lex</a></li>
<li><a href="https://www.tuv.com/regulations-and-standards/en/eu-regulation-2019-2144-automotive-type-approval-general-safety-requirements.html">EU - Regulation 2019/2144 - Automotive Type Approval General</a></li>

</ul>
</details>

**社区讨论**: 社区评论褒贬不一：一些用户对类似系统（如福特的 BlueCruise）持正面评价，认为其准确且具有挽救生命的潜力，而另一些人则对侵入性警报、糟糕的用户体验和隐私问题表示不满。还有人怀疑该系统可能被滥用以及强制集成的必要性。

**标签**: `#EU regulation`, `#driver monitoring`, `#privacy`, `#automotive safety`, `#UX`

---

<a id="item-8"></a>
## [微软解雇 id Software 的 idTech 引擎团队](https://gamefromscratch.com/microsoft-fire-idtech-team-at-id-software/) ⭐️ 8.0/10

微软解雇了 id Software 旗下整个 idTech 引擎团队，这可能意味着公司将战略性地放弃自研的 idTech 引擎，转而使用 Unreal Engine 5。 此举可能加速游戏引擎领域的垄断，减少引擎多样性，并可能损害 id Software 游戏的独特技术特色。 此次裁员影响负责 idTech（驱动《毁灭战士：黑暗纪元》等游戏的专有引擎）的团队，并且是微软更广泛游戏裁员的一部分；官方尚未确认是否转向 Unreal Engine 5。

hackernews · bauc · 7月7日 15:33 · [社区讨论](https://news.ycombinator.com/item?id=48819244)

**背景**: id Software 历史上一直开发自有游戏引擎，从 id Tech 1 到 id Tech 7，驱动了《毁灭战士》和《雷神之锤》等经典系列。这些引擎以性能和创新著称。Unreal Engine 5 由 Epic Games 开发，是一个广泛使用的第三方引擎，具有 Nanite 和 Lumen 等高级特性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Id_Tech">id Tech - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Id_Tech_7">id Tech 7 - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Unreal_Engine_5">Unreal Engine 5</a></li>

</ul>
</details>

**社区讨论**: 评论者担心微软为了节省成本而牺牲独特的技术文化，一些评论指出使用 Unreal Engine 可以雇佣更廉价的承包商。另一些人质疑裁员的具体证据，并建议将 idTech 开源。

**标签**: `#id Software`, `#Microsoft`, `#game engines`, `#Unreal Engine`, `#corporate strategy`

---

<a id="item-9"></a>
## [欧盟议会通过聊天控制第一轮投票](https://www.heise.de/en/news/Showdown-in-Strasbourg-The-unexpected-return-of-Chat-Control-1-0-11356680.html) ⭐️ 8.0/10

欧洲议会出人意料地在二读阶段重新提出备受争议的《聊天控制法》，并在第一轮程序投票中通过，为支持者提供了战术优势。 该法律将强制对私人信息进行大规模监控，威胁端到端加密和数字隐私。其推进可能为欧盟广泛监控树立危险先例。 在二读中，修正或否决需要绝对多数（361 票），而法律本身只需出席议员的简单多数即可通过。许多议员已因暑假离场，使得否决变得更加困难。

hackernews · miroljub · 7月7日 15:16 · [社区讨论](https://news.ycombinator.com/item?id=48819008)

**背景**: 《聊天控制法》正式名称为欧盟《儿童性虐待条例》，最初于 2022 年提出，要求平台扫描私人信息以打击儿童性虐待内容。因其对隐私和加密的影响而极具争议。临时版本已于 2026 年 4 月到期，但永久法规现在正通过激进程序策略再次推动。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Chat_Control">Chat Control - Wikipedia</a></li>
<li><a href="https://edri.org/our-work/chat-control-what-is-actually-going-on/">Chat Control: What is actually going on? - European Digital ...</a></li>

</ul>
</details>

**社区讨论**: 评论者对程序策略表示沮丧，指出不受欢迎的法律通过细微调整被反复提出。一位用户引用了让-克洛德·容克的言论，即逐步推动法律直到无法回头。其他人怀疑到周四能否找到足够的反对票来阻止该法律。

**标签**: `#EU`, `#privacy`, `#surveillance`, `#regulation`, `#democracy`

---

<a id="item-10"></a>
## [为什么 98%的成功率常常不够](https://whynothugo.nl/journal/2026/07/03/98-isnt-very-much/) ⭐️ 8.0/10

Hugo Landau 的一篇博客文章认为，在实际中，98%的成功率往往不够，他通过清理松针的比喻说明，即使留下很小的残余也会使努力无法接受。 这篇文章挑战了普遍认为高百分比就够了的假设，强调上下文在很大程度上决定可接受的门槛，这对软件可靠性、质量保证和风险评估至关重要。 作者以清理 99%的松针为例，虽然在数字上令人印象深刻，但剩余的 1%在视觉上仍然明显且无法接受。文章还指出，百分比在极端值附近可能具有误导性，从 98%到 99%的变化将使失败率减半。

hackernews · speckx · 7月7日 12:45 · [社区讨论](https://news.ycombinator.com/item?id=48816959)

**背景**: 百分比常用于衡量成功率，但可能掩盖失败的实际影响。例如，99.9%的正常运行时间对于关键系统而言仍然意味着相当多的停机时间。该博客文章通过日常类比探讨了这一想法。

**社区讨论**: 评论普遍同意前提但增加了细微差别：一些人认为在商业环境中 98%就足够了，而其他人则强调百分比可能具有欺骗性，小的失败率在大型系统中会累积。nemo1618 的评论用松针类比支持了文章的观点。

**标签**: `#statistics`, `#quality`, `#software engineering`, `#reliability`, `#decision-making`

---

<a id="item-11"></a>
## [Astro 7.0 发布：Rust 工具链与构建性能提升](https://astro.build/blog/astro-7/) ⭐️ 8.0/10

Astro 7.0 已发布，引入了基于 Rust 的新编译器和 Markdown 处理管线，依赖项从 247 个减少到 190 个，并结合 Vite 8 和 Rolldown 打包工具使构建性能提升 15-61%。 此次发布标志着在减少 JavaScript 生态臃肿和提升静态网站构建性能方面迈出了重要一步。使用 Astro 构建内容驱动型网站的开发者将受益于更快的编译速度和更低的维护成本。 Astro 7.0 还稳定了路由缓存功能，并为 Netlify、Vercel 和 Cloudflare 添加了实验性 CDN 缓存提供程序。Rust 编译器由社区成员 Princesseuh 贡献。

hackernews · saikatsg · 7月7日 18:30 · [社区讨论](https://news.ycombinator.com/item?id=48821653)

**背景**: Astro 是一个现代静态网站生成器，允许开发者使用多种 UI 框架（React、Vue、Svelte 等）的组件，默认不发送任何 JavaScript。它已从基于 JavaScript 的构建工具演进，引入 Rust 来承担性能关键任务，顺应了开发工具生态中（如 Astral 的 Python 工具）使用 Rust 的趋势。依赖项的减少也符合业界推动精简 Node.js 项目的大方向。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://astro.build/blog/astro-7/">Astro 7.0 | Astro - astro.build</a></li>
<li><a href="https://astro.build/blog/astro-6/">Astro 6.0 | Astro</a></li>

</ul>
</details>

**社区讨论**: 社区反响总体积极。Rust 编译器贡献者 Princesseuh 表示愿意回答相关问题。一些用户赞赏依赖项从 247 减少到 190 以及熟悉的静态站点工作流。但也有人对版本稳定性（七个大版本意味着频繁的重大变更）以及 Astro 作为框架同时支持其他框架的角色感到困惑。

**标签**: `#web development`, `#Astro`, `#JavaScript`, `#static site generator`, `#build tools`

---

<a id="item-12"></a>
## [sqlite-utils 4.0 新增数据库迁移与嵌套事务](https://simonwillison.net/2026/Jul/7/sqlite-utils-4/#atom-everything) ⭐️ 8.0/10

sqlite-utils 4.0 于 2026 年 7 月 7 日发布，新增三大特性：数据库模式迁移、通过新的 db.atomic() 方法实现的嵌套事务，以及对复合外键的支持。 此版本显著增强了 sqlite-utils 作为 SQLite 数据库管理工具的能力，满足了模式版本控制和事务安全性的常见需求。使用 Python 进行数据管理的开发者将受益于更简便的迁移工作流和更健壮的事务处理。 迁移通过 Python 文件中的 Migrations 类和 table.transform() 方法定义，该方法实现了 SQLite 推荐的临时表模式。嵌套事务底层使用 SQLite 保存点，复合外键则支持引用多个列。

rss · Simon Willison · 7月7日 19:32

**背景**: SQLite 是一个嵌入式 SQL 数据库引擎，本身不支持模式迁移或嵌套事务。sqlite-utils 库由 Simon Willison 创建，提供 Python API 和命令行工具来操作 SQLite 数据库。在 4.0 版本之前，用户需要手动使用 SQLite 有限的 ALTER TABLE 功能来处理模式更改。此版本自动化了迁移跟踪和执行，并通过保存点引入了嵌套事务。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://sqlite.org/lang_transaction.html">Transaction - SQLite java - SQLiteDatabase nested transaction and workaround ... Code sample How to Handle Nested Transactions in SQLite - Sling Academy Understanding Nested Transactions in SQLite and Effective ... How to use transactions — sqlite7 documentation sqlite-utils 4.0rc1 adds migrations and nested transactions</a></li>
<li><a href="https://sqlite.org/foreignkeys.html">SQLite Foreign Key Support</a></li>

</ul>
</details>

**标签**: `#sqlite-utils`, `#SQLite`, `#database migrations`, `#Python`, `#schema`

---

<a id="item-13"></a>
## [Woodruff：可信发布并非可信信号](https://lwn.net/Articles/1081690/) ⭐️ 8.0/10

William Woodruff 发表博客文章指出，PyPI 的可信发布不应被理解为软件包可信或质量的信号，而仅仅是一种身份验证方式。 这澄清了开发者中一个常见误解，否则可能导致对可信发布的过度依赖，影响软件供应链安全决策。 Woodruff 强调，可信发布使用 OpenID Connect（OIDC）在 CI/CD 工作流与 PyPI 之间建立身份，且 PyPI 故意避免将其显示为绿色勾选标记。

rss · LWN.net · 7月7日 14:27

**背景**: 可信发布是 PyPI 引入的一种机制，允许在不存储长期 API 令牌的情况下发布软件包。它使用 OIDC 在可信第三方服务（如 GitHub Actions）与 PyPI 之间交换短时身份令牌。该机制旨在简化发布工作流，但 Woodruff 警告不应将其与软件包可信或安全保证混为一谈。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.pypi.org/trusted-publishers/">Publishing to PyPI with a Trusted Publisher</a></li>
<li><a href="https://docs.pypi.org/trusted-publishers/using-a-publisher/">Publishing with a Trusted Publisher - PyPI Docs</a></li>

</ul>
</details>

**标签**: `#PyPI`, `#security`, `#software supply chain`, `#trusted publishing`, `#authentication`

---

<a id="item-14"></a>
## [Linux 内核中更快的 RCU 和无锁内存分配](https://lwn.net/Articles/1081009/) ⭐️ 8.0/10

Puranjay Mohan 在 LSFMM+BPF 2026 上介绍了改进 RCU 性能的工作，允许普通 RCU 回调在快速宽限期结束后执行，同时讨论了新的 kmalloc_nolock() 函数，该函数支持从任何内核上下文进行无锁内存分配。 这些开发通过减少内存分配延迟和加速 RCU 宽限期完成，显著提高了内核的可扩展性，使内存压力下的高性能工作负载受益。 RCU 改进涉及跟踪非快速和快速宽限期编号，以便在任一完成后允许回调运行；而 kmalloc_nolock() 则实现了无需持有锁的无锁分配。

rss · LWN.net · 7月7日 13:39

**背景**: 读-复制-更新（RCU）是 Linux 内核中的一种同步机制，允许读者无需锁即可访问数据，而写者创建新版本。RCU 宽限期确保所有读者完成后才释放旧数据。kmalloc() 是标准内核内存分配器，但传统上需要正确的锁上下文；kmalloc_nolock() 将其扩展到任何上下文中工作。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.oreilly.com/library/view/linux-device-drivers/0596005903/ch08.html">8. Allocating Memory - Linux Device Drivers, 3rd Edition [Book]</a></li>
<li><a href="http://www.jikos.cz/jikos/Kmalloc_Internals.html">Kmalloc Internals: Exploring Linux Kernel Memory Allocation</a></li>
<li><a href="https://people.netfilter.org/rusty/unreliable-guides/kernel-hacking/routines-kmalloc.html">kmalloc()/kfree() include/linux/slab.h</a></li>

</ul>
</details>

**标签**: `#Linux kernel`, `#RCU`, `#memory allocation`, `#performance`, `#LSFMM+BPF`

---

<a id="item-15"></a>
## [Mozilla CTO 就开源 AI 报告举办 AMA](https://www.reddit.com/r/MachineLearning/comments/1upxdvc/raffi_krikorian_cto_mozilla_ama_on_the_state_of/) ⭐️ 8.0/10

Mozilla CTO Raffi Krikorian 宣布将于 2026 年 7 月 14 日举办 AMA，讨论首份《开源 AI 现状报告》，内容涵盖“免费”模型的隐藏成本、企业采用情况、中国效应、开发者信任以及代理套件（agentic harness）。 此次 AMA 讨论生产环境中开源 AI 的关键且常被误解的方面，可为开发者和企业在 AI 生态中应对真实成本、信任和战略杠杆提供指导。 该报告及 AMA 聚焦五大主题：“免费”模型的隐藏成本、企业采用中的现实与营销差异、中国模型如何重塑杠杆、基于 950 多名开发者调查的信任度，以及为何“代理套件”（agentic harness）层成为开源的新战场。

reddit · r/MachineLearning · /u/raffikrikorian · 7月7日 14:51

**背景**: 像 Llama 和 Mistral 这样的开源 AI 模型被广泛使用，但在生产环境中部署时，常因基础设施和专有工具而产生意外成本。“代理套件”（agentic harness）是指围绕模型的管理上下文、工具访问和安全的操作层，现在成为竞争焦点。该报告旨在澄清这些现实动态，超越流行叙事。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://harness-engineering.ai/blog/agent-harness-complete-guide/">The Complete Guide to Agent Harness: What It Is and Why It ...</a></li>
<li><a href="https://opendatascience.com/what-is-an-agent-harness-the-architecture-behind-reliable-agentic-ai/">What is an Agent Harness? The Architecture Behind Agentic AI</a></li>

</ul>
</details>

**标签**: `#open source AI`, `#Mozilla`, `#AI industry`, `#enterprise AI`, `#developer trust`

---

<a id="item-16"></a>
## [谷歌新增‘保存媒体’设置，Lens 和语音数据用于 AI 训练](https://techcrunch.com/2026/07/06/if-you-use-google-youre-training-its-ai-heres-how-to-opt-out/) ⭐️ 8.0/10

谷歌在搜索服务历史记录中新增了“保存媒体”设置，该设置会保存来自 Google Lens、Search Live、语音搜索和翻译口语练习等功能的媒体，并将其用于改进谷歌服务和 AI 模型。 这项政策变化影响了使用这些功能的数百万用户，引发了关于媒体数据如何用于 AI 训练的隐私担忧。它也凸显了在 AI 数据收集日益增多的时代，选择退出机制的重要性。 该设置是谷歌账号“搜索服务历史记录”的一部分，用户可以通过关闭“保存媒体”来选择退出。媒体包括来自 Google Lens、Search Live、语音搜索和翻译口语练习的图片、文件、音频和视频。

telegram · zaihuapd · 7月7日 04:00

**背景**: Google Lens 是一款基于 AI 的视觉搜索工具，可以识别物体并提供相关信息。Search Live 是一项允许用户与谷歌搜索进行语音和摄像头交互对话的功能。这些功能产生的媒体现在可能会被谷歌保存用于模型训练。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Google_Lens">Google Lens</a></li>
<li><a href="https://support.google.com/websearch/answer/16329036?hl=en&co=GENIE.Platform=Android">Have a real-time conversation with Live in Search - Android - Google Search Help</a></li>

</ul>
</details>

**标签**: `#Google`, `#privacy`, `#AI training`, `#search settings`

---

<a id="item-17"></a>
## [中国企业从英伟达转向国产 AI 芯片](https://www.bloomberg.com/news/articles/2026-07-07/chinese-firms-leave-nvidia-for-local-ai-suppliers-survey-shows) ⭐️ 8.0/10

一项对 60 家中国企业高管的调查显示，企业正在减少对英伟达 AI 加速器的采购，计划在未来 12 个月内将国产 AI 芯片的预算占比从目前的 30%提升至 46%。 这一转变标志着全球 AI 硬件供应链的重大调整，受中国数据中心投资计划和地缘政治紧张局势的推动，可能显著影响英伟达的收入，并加速海光信息、寒武纪等国产芯片厂商的发展。 中国计划未来五年在数据中心领域投资约 2 万亿元人民币（合 2750 亿美元），其中至少 80%的核心技术将由国内企业提供，腾讯、阿里巴巴、华为、海光信息和寒武纪等公司有望受益。

telegram · zaihuapd · 7月7日 04:45

**背景**: 该调查反映了美国对华出口限制先进英伟达芯片的持续影响，促使中国推动 AI 加速器的自给自足。海光信息和寒武纪是两家知名的国产芯片设计公司：海光信息设计兼容 x86 的 CPU 和 AI 加速器，寒武纪则专注于云端和边缘计算的 AI 芯片。两者在这一转变中都获得了显著的市场增长。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://zh.wikipedia.org/zh-tw/海光信息">海光信息 - 維基百科，自由的百科全書</a></li>
<li><a href="https://baike.baidu.com/item/中科寒武纪科技股份有限公司/24545271">中科寒武纪科技股份有限公司_百度百科 一天吃透一家上市科技公司：寒武纪 - 知乎 中科寒武纪科技股份有限公司 - 爱企查 三年涨超40倍，寒武纪市值超万亿_上市_公司_股价 投资者关系 - 寒武纪 - Cambricon 算力需求井喷，寒武纪业绩快报：2025年实现上市后首次全年盈利 ，但第...</a></li>

</ul>
</details>

**标签**: `#AI chips`, `#China`, `#Nvidia`, `#semiconductors`, `#supply chain`

---

<a id="item-18"></a>
## [new-api 修复计费整数溢出漏洞](https://github.com/QuantumNous/new-api/commit/d0bd8aa) ⭐️ 8.0/10

new-api 项目发布两个提交，增加边界检查和饱和运算，防止配额计算中的整数溢出，该溢出可能导致负数扣费。 此修复解决了一个严重的计费漏洞，用户可能通过触发负数扣费来非法获取积分，影响所有使用 new-api 进行计量或计费的部署。这凸显了在财务逻辑中进行严格输入验证的重要性。 该漏洞源于配额计算中对用户可控参数缺少验证；超大数值导致整数溢出后，扣费变为负数。修复引入了上限验证和饱和运算，将结果钳制在最大可表示值，而不是回绕。

telegram · zaihuapd · 7月7日 07:26

**背景**: 整数溢出发生在算术运算超过固定宽度整数可存储的最大值，导致其“回绕”为负数或极小值。在安全场景中，这可能绕过检查并导致意外行为。饱和运算是一种技术，它将结果钳制在范围的极值而不是回绕，从而防止此类漏洞。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Saturation_arithmetic">Saturation arithmetic</a></li>
<li><a href="https://cwe.mitre.org/data/definitions/190.html">CWE-190: Integer Overflow or Wraparound (4.20)</a></li>
<li><a href="https://github.com/QuantumNous/new-api/issues/5876">32-bit (armv7/玩客云) compatibility issue: quota int overflow causes ...</a></li>

</ul>
</details>

**标签**: `#security`, `#bug fix`, `#integer overflow`, `#billing`, `#open source`

---

<a id="item-19"></a>
## [英伟达 Blackwell 晶圆美国制造，但封装仍需台湾](https://www.tomshardware.com/tech-industry/nvidia-and-intel-tout-chips-built-in-america-but-every-arizona-made-blackwell-die-is-still-packaged-in-taiwan) ⭐️ 8.0/10

台积电亚利桑那州 Fab 21 已开始采用定制 4NP 制程量产英伟达 Blackwell 晶圆，但这些晶圆仍需运往台湾进行 CoWoS-L 先进封装。 这凸显了美国半导体供应链的关键缺口：尽管已能本土制造先进逻辑芯片，但美国仍缺乏大规模先进封装和高带宽存储器（HBM）生产能力，导致持续依赖台湾设施，完整的供应链自主最早要到 2028-2029 年才能实现。 4NP 是为英伟达定制的 4nm 级工艺节点，而 CoWoS-L 结合了基板上晶圆上芯片（CoWoS）技术与 RDL 中介层和局部硅互连（LSI）。Amkor、台积电和 SK 海力士正在美国建设封装和 HBM 产能，但这些设施尚未投产。

telegram · zaihuapd · 7月7日 09:47

**背景**: 先进封装（如台积电的 CoWoS-L）对于英伟达 Blackwell 等高性能 AI 芯片至关重要，因为它能将多个芯片和存储器堆叠集成到一个封装中。美国半导体政策一直侧重于扩大本土制造能力，但封装和存储器供应链仍集中在亚洲，尤其是台湾和韩国。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm">CoWoS® - Taiwan Semiconductor Manufacturing Company Limited</a></li>
<li><a href="https://www.tomshardware.com/tech-industry/tsmc-readies-lower-cost-4nm-manufacturing-tech-up-to-85-cheaper">TSMC readies lower-cost 4nm manufacturing tech: Up to 8.5% ...</a></li>
<li><a href="https://www.intel.com/content/www/us/en/foundry/process/18a.html">Intel 18A | See Our Biggest Process Innovation</a></li>

</ul>
</details>

**标签**: `#semiconductor`, `#NVIDIA`, `#Blackwell`, `#supply chain`, `#advanced packaging`

---

<a id="item-20"></a>
## [DeepSeek 自主研发 AI 芯片以减少对英伟达和华为的依赖](https://www.reuters.com/world/china/chinas-deepseek-developing-its-own-ai-chip-sources-say-2026-07-07/) ⭐️ 8.0/10

中国 AI 公司 DeepSeek 已开始自主研发专注于推理的 AI 芯片，旨在减少对英伟达和华为芯片的依赖。该项目启动约一年，目前仍处于早期阶段，DeepSeek 正在积极招募芯片设计工程师，并与代工厂和存储公司接洽。 此举可能重塑中国的 AI 硬件格局，并降低 DeepSeek 对美国出口管制的脆弱性——目前的管制限制了先进英伟达芯片的获取。如果成功，还可能加剧与华为昇腾系列及其他国产芯片制造商的竞争。 该芯片专门面向推理阶段（即训练好的模型生成回答的环节），而非训练。DeepSeek 此前依赖英伟达 H800 和华为昇腾芯片，创始人梁文锋在 2024 年一次罕见采访中承认，芯片管制是公司面临的挑战。

telegram · zaihuapd · 7月7日 11:08

**背景**: AI 推理是利用训练好的模型从新输入生成输出的过程，而训练则是教会模型。英伟达 H800 GPU 是高性能数据中心 GPU，华为昇腾系列是中国的 AI 芯片替代品，但两者均受美国出口限制。自主研发推理芯片可以减少对外部供应商的依赖，并针对特定工作负载优化成本和性能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/NVIDIA_H800_GPU">NVIDIA H800 GPU</a></li>
<li><a href="https://www.digitalocean.com/resources/articles/ai-inference-vs-training">AI Inference vs Training: Key Differences Explained</a></li>
<li><a href="https://tech-insider.org/huawei-ascend-950pr-ai-chip-nvidia-china-2026/">Huawei Ascend 950PR: The 1.56 PFLOP AI Chip vs Nvidia [2026]</a></li>

</ul>
</details>

**标签**: `#AI Chips`, `#DeepSeek`, `#Semiconductors`, `#China Tech`, `#US-China Trade`

---

<a id="item-21"></a>
## [加州纽约力推 3D 打印机装枪支拦截软件引争议](https://www.theverge.com/tech/960802/3d-printed-gun-laws-ghost-guns) ⭐️ 8.0/10

加利福尼亚州和纽约州正在推进立法，要求州内销售的 3D 打印机必须内置能检测并拦截枪支蓝图的软件；纽约州已于 5 月底签署相关法律，加州的 AB 2047 法案已在众议院通过。 这项立法是对开源 3D 打印生态和 DIY 文化的重大干预，引发了对数字权利、审查制度以及可能被滥用于知识产权执法等超出枪支管控范围的担忧。 纽约州的法律还适用于 CNC 机床；加州 AB 2047 法案拟从 2029 年 3 月起禁止销售未获认证的打印机，违规罚款最高 2.5 万美元；批评者警告该技术可能误拦日常物品，并要求云端扫描用户文件。

telegram · zaihuapd · 7月7日 14:02

**背景**: 3D 打印机通过切片软件将 CAD 模型转换为 G-code 指令，逐层构建物体。CNC 机床是计算机控制的减材工具，从材料块中雕刻出零件。这些机器的枪支蓝图可在网上分享，从而制造不受监管的枪支。支持者将拦截软件比作打印机防伪措施，但反对者担心这会限制技术自由。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://gnet-research.org/2024/11/06/blocking-the-blueprint-technological-barriers-against-3d-printed-firearms/">Blocking the Blueprint: Technological Barriers Against 3D ...</a></li>
<li><a href="https://www.technology.org/2026/06/13/new-york-law-3d-printers-block-guns/">New York Law Makes 3D Printers Block Guns - Technology Org</a></li>
<li><a href="https://en.wikipedia.org/wiki/Computer_numerical_control">Computer numerical control - Wikipedia</a></li>

</ul>
</details>

**标签**: `#3D printing`, `#gun control`, `#legislation`, `#digital rights`, `#open source`

---