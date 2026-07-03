---
layout: default
title: "Horizon Summary: 2026-07-03 (EN)"
date: 2026-07-03
lang: en
---

> From 48 items, 10 important content pieces were selected

---

1. [Wordgard: New Rich-Text Editor by ProseMirror Creator](#item-1) ⭐️ 8.0/10
2. [Startup Critique: Wealth-Motivated Founders Produce Half-Baked Products](#item-2) ⭐️ 8.0/10
3. [Apple's Safari MCP Server Enables LLM-Powered Browser Automation](#item-3) ⭐️ 8.0/10
4. [Limiting negative dentries in Linux kernel discussed at LSFMM+BPF 2026](#item-4) ⭐️ 8.0/10
5. [CDD Recovers Verbatim Finetuning Data from Logits Alone](#item-5) ⭐️ 8.0/10
6. [Google Gemini Omni Flash Tops Video Arena](#item-6) ⭐️ 8.0/10
7. [Anthropic Accuses Alibaba of Massive Distillation Attack on Claude](#item-7) ⭐️ 8.0/10
8. [Huawei Mate 80 Pro Gaming Efficiency Beats Snapdragon 8 Gen3](#item-8) ⭐️ 8.0/10
9. [NASA Launches Rescue Satellite to Save Falling Swift Telescope](#item-9) ⭐️ 8.0/10
10. [Tencent Xuanwu Lab's Atyun AI Surpasses Mythos in CyberGym Test](#item-10) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Wordgard: New Rich-Text Editor by ProseMirror Creator](https://wordgard.net/) ⭐️ 8.0/10

Marijn Haverbeke, the creator of ProseMirror, has released Wordgard 0.1, a new in-browser rich-text editor library focused on extensibility and programmatic access. Wordgard represents a fresh take on WYSIWYG editing from one of the most influential figures in the field, potentially shaping the next generation of web editors and impacting frameworks like TipTap. Wordgard is a complete rewrite, not an upgrade path from ProseMirror, sharing many concepts but requiring significant migration work. It is designed for editing content that fits a specific schema, rather than generic HTML.

hackernews · indy · Jul 3, 08:50 · [Discussion](https://news.ycombinator.com/item?id=48772573)

**Background**: ProseMirror is a widely-used open-source rich-text editor framework by Marijn Haverbeke, powering editors like TipTap. Wordgard is the next iteration integrating lessons learned over nine years, offering a reimagined architecture for customizability and programmatic control.

<details><summary>References</summary>
<ul>
<li><a href="https://wordgard.net/">Wordgard</a></li>
<li><a href="https://marijnhaverbeke.nl/blog/wordgard-0.1.html">Wordgard Release 0.1</a></li>
<li><a href="https://wordgard.net/docs/guide/">Wordgard System Guide</a></li>

</ul>
</details>

**Discussion**: The community is generally excited but curious about the rationale behind a new editor. Some note the lack of an upgrade path from ProseMirror, while others praise the design and find the approach validating. Users also discuss difficulties in statically typing ProseMirror schemas.

**Tags**: `#rich-text editor`, `#ProseMirror`, `#web development`, `#WYSIWYG`

---

<a id="item-2"></a>
## [Startup Critique: Wealth-Motivated Founders Produce Half-Baked Products](https://weli.dev/blog/half-baked-product/) ⭐️ 8.0/10

A blog post criticizes startup founders whose primary motivation is wealth, arguing that lack of domain expertise leads to half-baked products. The post illustrates the disconnect between founders, engineers, and salespeople in product development. This critique highlights a common but overlooked pitfall in startups, where misaligned incentives and lack of domain knowledge result in products that fail to meet customer needs. It resonates deeply with the tech community, as evidenced by high engagement and many comments. The article received 1141 points and 348 comments on Hacker News, indicating significant community interest. Commenters noted the recurring nature of such problems and called for more perspectives from salespeople.

hackernews · weli · Jul 3, 08:23 · [Discussion](https://news.ycombinator.com/item?id=48772388)

**Background**: Startup founders often come from business or finance backgrounds and may lack deep domain expertise. This can lead to products that are technically weak or disconnected from user needs. The 'half-baked product' phenomenon is when a product is launched before it is fully tested or validated.

**Discussion**: Commenters generally agreed with the article's premise, with 'TrackerFF' noting the mismatch between founder and domain expert expectations. 'brap' identified the core problem as a disconnect between roles. Some expressed a desire to hear the salesperson's perspective.

**Tags**: `#startups`, `#founder motivation`, `#product development`, `#domain expertise`

---

<a id="item-3"></a>
## [Apple's Safari MCP Server Enables LLM-Powered Browser Automation](https://webkit.org/blog/18136/introducing-the-safari-mcp-server-for-web-developers/) ⭐️ 8.0/10

Apple has introduced the Safari MCP server, a tool that allows large language models (LLMs) to interact with and automate the Safari browser for web development tasks such as debugging, testing, and layout inspection. This integration marks a significant step in bringing AI-powered browser automation to Apple's ecosystem, potentially streamlining workflows for web developers and enabling more efficient cross-browser testing. It also positions Safari alongside Chrome and Firefox in supporting MCP, fostering competition and innovation in developer tools. The Safari MCP server is part of WebKit's developer tools and works by exposing browser state and actions through the Model Context Protocol (MCP), allowing LLMs to perform operations like opening pages, inspecting computed styles, and checking layouts. It is available for download and can be used with various LLM-powered agents.

hackernews · coloneltcb · Jul 3, 01:37 · [Discussion](https://news.ycombinator.com/item?id=48769639)

**Background**: MCP (Model Context Protocol) is an open standard that enables AI models to interact with external tools and data sources. It allows language models to access real-time information and perform actions, going beyond static text generation. Apple's adoption of MCP for Safari aligns with a broader industry trend where browser vendors are integrating AI to enhance developer productivity.

<details><summary>References</summary>
<ul>
<li><a href="https://webkit.org/blog/18136/introducing-the-safari-mcp-server-for-web-developers/">Introducing the Safari MCP server for web developers | WebKit</a></li>

</ul>
</details>

**Discussion**: Community reactions have been largely positive, with developers expressing excitement about adding Safari to their cross-browser testing setups using MCP. Some commenters noted existing alternatives like Playwright-CLI and Apple's safaridriver, while others shared personal use cases for browser automation. The discussion also highlighted that Chrome and Firefox already have official MCP servers, making Safari's addition a welcome completion of the major browser set.

**Tags**: `#safari`, `#webkit`, `#mcp`, `#web development`, `#AI integration`

---

<a id="item-4"></a>
## [Limiting negative dentries in Linux kernel discussed at LSFMM+BPF 2026](https://lwn.net/Articles/1079407/) ⭐️ 8.0/10

At the 2026 Linux Storage, Filesystem, Memory Management, and BPF Summit, a session led by Miklos Szeredi discussed problems caused by excessive negative dentries in directories, including soft lockups, reference count overflow, and long hash chains. Negative dentries are a key optimization for filesystem lookups, but when a directory accumulates millions of them, they can cause severe performance issues and even security side-channel problems. The proposals discussed could lead to kernel patches that improve filesystem reliability and memory management. Proposed solutions include moving negative dentries to the end of the d_children list so iterators can stop early, adding cond_resched() calls to avoid soft lockups, or switching to a more suitable data structure. Concerns were raised about ordering issues with getdents() and potential complications when a negative dentry becomes positive.

rss · LWN.net · Jul 3, 14:10

**Background**: Negative dentries are directory entries that cache the non-existence of a file, speeding up lookups by avoiding repeated filesystem access. The dentry cache stores three types: in-use, unused, and negative. Problems arise when directories have hundreds of millions of negative dentries, causing soft lockups or lockref overflow.

<details><summary>References</summary>
<ul>
<li><a href="https://www.halolinux.us/kernel-reference/the-dentry-cache.html">The dentry Cache - Linux Kernel Reference - Halo Linux Services</a></li>
<li><a href="https://kernel-internals.org/vfs/dcache-icache/">Dentry and Inode Caches - Linux Kernel Internals</a></li>
<li><a href="https://lwn.net/Articles/890025/">Negative dentries , 20 years later [LWN.net]</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#filesystem`, `#dentries`, `#memory management`, `#performance optimization`

---

<a id="item-5"></a>
## [CDD Recovers Verbatim Finetuning Data from Logits Alone](https://www.reddit.com/r/MachineLearning/comments/1umn2dk/contrastive_decoding_diffing_cdd_recovering/) ⭐️ 8.0/10

Researchers introduce Contrastive Decoding Diffing (CDD), a method that recovers verbatim fine-tuning data from large language models using only logit differences between base and finetuned models, without requiring weight or activation access. This technique significantly improves over prior white-box methods, achieving high verbatim recovery scores on the SDF benchmark, and has important implications for ML safety and interpretability by enabling data leakage detection without full model access. CDD uses a single default configuration across model families ranging from 1B to 32B parameters, and on 19 out of 20 model pairs it achieves a verbatim recovery score of 4 or higher out of 5, whereas the prior Activation Difference Lens (ADL) method never exceeds 3 out of 5 despite requiring full weight access.

reddit · r/MachineLearning · /u/CebulkaZapiekana · Jul 3, 19:01

**Background**: Contrastive decoding is a technique that improves text generation by contrasting logits from a weak and a strong model. Model diffing refers to comparing models to isolate changes introduced by fine-tuning. CDD applies these ideas in a grey-box setting, where only logit outputs are available, to extract verbatim training data.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2210.15097">Contrastive Decoding : Open-ended Text Generation as Optimization</a></li>
<li><a href="https://transformer-circuits.pub/2024/model-diffing/index.html">Stage-Wise Model Diffing</a></li>

</ul>
</details>

**Tags**: `#machine learning`, `#LLM safety`, `#model interpretability`, `#fine-tuning`, `#logit analysis`

---

<a id="item-6"></a>
## [Google Gemini Omni Flash Tops Video Arena](https://x.com/Designarena/status/2072759122366509130) ⭐️ 8.0/10

Google DeepMind's Gemini Omni Flash model achieved a score of 1404 points on the Video Arena blind test leaderboard, surpassing ByteDance's Seedance 2.0 Mini by 101 points. This milestone marks a significant shift in AI video generation ranking, demonstrating Google's competitive edge over ByteDance in the rapidly evolving field of generative AI video. Video Arena rankings are based on anonymous user votes, and Google's video model ranking has improved by 7 positions compared to the Veo series era.

telegram · zaihuapd · Jul 3, 05:51

**Background**: Video Arena is a crowdsourced blind test platform where users compare AI-generated videos without knowing the provider. ByteDance's Seedance series had previously dominated the leaderboard, with Seedance 2.0 Mini holding first place at 1303 points. Gemini Omni Flash, announced by Google DeepMind, supports text-to-video, image-to-video, and reference-to-video generation, and is rolling out to developers via the Gemini API.

<details><summary>References</summary>
<ul>
<li><a href="https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/">Introducing Gemini Omni</a></li>
<li><a href="https://deepmind.google/models/gemini-omni/">Gemini Omni — Google DeepMind</a></li>
<li><a href="https://arena.ai/video">Video Arena : Compare the Best AI Video Generators</a></li>

</ul>
</details>

**Tags**: `#AI`, `#video generation`, `#Google DeepMind`, `#Gemini`, `#ByteDance`

---

<a id="item-7"></a>
## [Anthropic Accuses Alibaba of Massive Distillation Attack on Claude](https://t.me/zaihuapd/42327) ⭐️ 8.0/10

Anthropic has accused Alibaba of conducting a massive distillation attack on its Claude AI model, using approximately 25,000 fraudulent accounts to carry out over 28.8 million interactions between April 22 and June 5, 2026. In response, Alibaba ordered all employees to uninstall Claude-related products, including Sonnet, Opus, Fable, and Claude Code, effective July 10. This incident represents the largest known distillation attack against an AI company, highlighting the growing threat of model extraction via API abuse. It could escalate tensions between US and Chinese tech firms and spur stricter security measures across the industry. The attack involved 25,000 accounts and 28.8 million interactions over a 45-day period, targeting Claude's reasoning capabilities. Anthropic has since tightened its risk-control policies, and Alibaba's internal ban on Claude products retroactively prohibits use of Anthropic's models including Sonnet, Opus, Fable, and Claude Code.

telegram · zaihuapd · Jul 3, 06:21

**Background**: Model distillation attacks involve repeatedly querying a proprietary large language model and using the input-output pairs to train a competing model, effectively stealing its capabilities. Anthropic has developed classifiers and behavioral fingerprinting systems to detect such attacks, including chain-of-thought elicitation and coordinated account activity. The accusation against Alibaba and its Qwen AI lab underscores the risks of API-based AI services.

<details><summary>References</summary>
<ul>
<li><a href="https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks">Detecting and preventing distillation attacks \ Anthropic</a></li>
<li><a href="https://en.wikipedia.org/wiki/Claude_(AI)">Claude (AI) - Wikipedia</a></li>
<li><a href="https://cloud.google.com/blog/topics/threat-intelligence/distillation-experimentation-integration-ai-adversarial-use">GTIG AI Threat Tracker: Distillation, Experimentation, and (Continued) Integration of AI for Adversarial Use | Google Cloud Blog</a></li>

</ul>
</details>

**Tags**: `#AI Security`, `#Model Distillation`, `#Anthropic`, `#Alibaba`, `#Intellectual Property`

---

<a id="item-8"></a>
## [Huawei Mate 80 Pro Gaming Efficiency Beats Snapdragon 8 Gen3](https://www.bilibili.com/video/BV1F7T46wEyT) ⭐️ 8.0/10

Geekerwan's review reveals that the Huawei Mate 80 Pro series, equipped with the Kirin 9030 chip, achieves superior gaming energy efficiency compared to the Snapdragon 8 Gen3, thanks to HarmonyOS native optimization and software-hardware synergy. This demonstrates Huawei's significant progress in chip design and software optimization, potentially reshaping mobile performance standards. It highlights how software-hardware integration can overcome theoretical hardware limitations, benefiting both consumers and the broader ecosystem. The Kirin 9030 Pro features a 9-core CPU and a 6-core Maleoon 935 GPU; in Genshin Impact at 60fps max settings, the Mate 80 Pro Max consumes only 4.9W, outperforming Snapdragon 8 Gen3 efficiency. The chip's transistor count is approximately 15 billion, with CPU multi-core efficiency between Snapdragon 8 Gen2 and Gen3.

telegram · zaihuapd · Jul 3, 13:27

**Background**: The Kirin 9030 is a system-on-chip designed by HiSilicon, a wholly owned subsidiary of Huawei. It uses ARM-based CPU cores and Mali-based GPU cores (Maleoon 935). The Mate 80 Pro series is Huawei's flagship smartphone line, and the review focuses on real-world gaming performance and energy efficiency under HarmonyOS optimization.

<details><summary>References</summary>
<ul>
<li><a href="https://grokipedia.com/page/Kirin_9030">Kirin 9030</a></li>
<li><a href="https://nanoreview.net/en/soc/hisilicon-kirin-9030">HiSilicon Kirin 9030 Pro: specs and benchmarks</a></li>
<li><a href="https://www.notebookcheck.net/HiSilicon-Maleoon-935-Benchmarks-and-Specs.1249609.0.html">HiSilicon Maleoon 935 - Benchmarks and Specs - Notebookcheck Tech</a></li>

</ul>
</details>

**Tags**: `#Huawei`, `#Mate 80 Pro`, `#Kirin 9030`, `#HarmonyOS`, `#Mobile Gaming`

---

<a id="item-9"></a>
## [NASA Launches Rescue Satellite to Save Falling Swift Telescope](https://apnews.com/article/swift-nasa-satellite-rescue-katalyst-a7ddd740ca099587c58865f583c7245a) ⭐️ 8.0/10

On July 3, NASA launched the LINK spacecraft to grab the aging Swift space telescope and boost its orbit by about 240 km, preventing an imminent reentry. This mission marks the first time a private spacecraft will grab a U.S. government satellite, setting a milestone for commercial satellite servicing and extending a key astronomy mission. The LINK spacecraft uses a robotic arm to secure the telescope, then thrusters to slowly raise its orbit; if successful, Swift could resume observations as early as September.

telegram · zaihuapd · Jul 3, 15:43

**Background**: The Swift Observatory, launched in 2004, studies gamma-ray bursts and has been in a decaying orbit due to increased solar activity. Without intervention, it would have burned up in the atmosphere as early as October. This rescue is part of NASA's push to commercialize in-orbit servicing.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Swift_rescue_mission">Swift rescue mission - Wikipedia</a></li>
<li><a href="https://science.nasa.gov/missions/swift/swift-boost-mission/partners-nasa-ready-for-june-launch-of-swift-boost-mission/">Partners, NASA Ready for June Launch of Swift Boost Mission - NASA Science</a></li>
<li><a href="https://easternherald.com/2026/07/03/swift-telescope-rescue-launch-delay-pegasus-xl/">NASA Swift Telescope Rescue Delayed by Rocket Anomaly</a></li>

</ul>
</details>

**Tags**: `#space`, `#NASA`, `#satellite servicing`, `#astronomy`, `#Swift telescope`

---

<a id="item-10"></a>
## [Tencent Xuanwu Lab's Atyun AI Surpasses Mythos in CyberGym Test](https://mp.weixin.qq.com/s/BzU7g-2iG7d6h4ViwMhxyg) ⭐️ 8.0/10

Tencent Xuanwu Lab's Atyun AI achieved 84.0% on the CyberGym cybersecurity benchmark, surpassing Anthropic's Claude Mythos Preview, while consuming less than 0.1% of Mythos's budget. This demonstrates that a cost-effective, open-source-based AI can outperform a major proprietary model in vulnerability discovery, potentially lowering barriers for organizations to adopt AI-driven security auditing. Atyun AI is built on the locally deployable open-source model GLM-5.1 and discovered multiple high-severity logical vulnerabilities in projects like curl, gnark, OpenSSL, Python cryptography, and Java bc-java, with scores up to 9.3. It ranked 1st in critical vulnerability severity on the Berkeley BVI real-world vulnerability leaderboard.

telegram · zaihuapd · Jul 3, 16:12

**Background**: CyberGym is a large-scale benchmark introduced by UC Berkeley that includes 1,507 real-world vulnerabilities across 188 open-source software projects to evaluate AI agents' cybersecurity capabilities. GLM-5.1 is a flagship open-source LLM by Z.AI, designed for long-horizon autonomous tasks. Claude Mythos Preview is Anthropic's specialized cybersecurity model under the "Glass Wing Project."

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2506.02548">[2506.02548] CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale</a></li>
<li><a href="https://www.cybergym.io/cybergym/">CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale</a></li>
<li><a href="https://docs.z.ai/guides/llm/glm-5.1">GLM - 5 . 1 - Overview - Z.AI DEVELOPER DOCUMENT</a></li>

</ul>
</details>

**Tags**: `#AI`, `#网络安全`, `#漏洞检测`, `#腾讯玄武`, `#基准测试`

---