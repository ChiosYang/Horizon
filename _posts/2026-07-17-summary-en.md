---
layout: default
title: "Horizon Summary: 2026-07-17 (EN)"
date: 2026-07-17
lang: en
---

> From 46 items, 13 important content pieces were selected

---

1. [Firefox Runs Inside Another Browser via WebAssembly](#item-1) ⭐️ 9.0/10
2. [Moonshot AI Unveils Kimi K3, a 2.8 Trillion Parameter Open-Weight Model](#item-2) ⭐️ 9.0/10
3. [Japan to Buy 27,500 NVIDIA Rubin Chips for Robot AI](#item-3) ⭐️ 9.0/10
4. [TSMC adds $100B US investment, Q2 profit surges 77%](#item-4) ⭐️ 9.0/10
5. [New ArXiv Book on Mathematics of Data Science](#item-5) ⭐️ 8.0/10
6. [LLM-Assisted Programming: The Cognitive Toll of Code Review](#item-6) ⭐️ 8.0/10
7. [GPT-5.6 Codex Bug Can Delete Home Directory](#item-7) ⭐️ 8.0/10
8. [Inkling: Thinking Machines Lab&\#x27;s Open-Weight MoE Model](#item-8) ⭐️ 8.0/10
9. [Sched-ext gets sub-scheduler enqueue and proxy execution support](#item-9) ⭐️ 8.0/10
10. [ExTernD Boosts Ternary LLM Quantization with Expanded-Rank Decomposition](#item-10) ⭐️ 8.0/10
11. [QLoRA&\#x27;s default 2e-4 learning rate criticized for small datasets](#item-11) ⭐️ 8.0/10
12. [EU orders Google to open Android features and search data to rivals](#item-12) ⭐️ 8.0/10
13. [Truth Social to Sell Fast Access to Trump Posts to Wall Street](#item-13) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Firefox Runs Inside Another Browser via WebAssembly](https://simonwillison.net/2026/Jul/16/firefox-in-webassembly/#atom-everything) ⭐️ 9.0/10

Puter has compiled the Firefox browser to WebAssembly, allowing it to run completely inside another browser like Chrome. The project uses the Gecko engine and cost an estimated $25,000 in AI tokens to develop. This demonstration proves that full desktop browsers can run inside web environments, opening new possibilities for virtualization, cross-platform software delivery, and in-browser development tools. It also showcases how AI-assisted programming can tackle massive engineering challenges. The project relies on the Wisp protocol to proxy all network traffic through Puter&\#x27;s server because WebAssembly code cannot open arbitrary network connections. The team had to scale up servers due to high traffic from Hacker News, and the demo supports end-to-end encryption.

rss · Simon Willison · Jul 16, 23:34

**Background**: WebAssembly \(WASM\) is a binary instruction format that allows code written in languages like C++ to run at near-native speed in web browsers. Traditionally, browsers cannot be nested inside other browsers because of security and performance constraints. Compiling a full browser like Firefox into WASM is a monumental task requiring enormous computation and optimization, which this project achieved through extensive use of AI assistance.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Wire_protocol">Wire protocol</a></li>
<li><a href="https://github.com/MercuryWorkshop/wisp-protocol">GitHub - MercuryWorkshop/wisp-protocol: Wisp is a low-overhead, easy to ...</a></li>

</ul>
</details>

**Discussion**: The Hacker News community showed strong interest, causing the team to scale up servers to handle traffic. The project was praised as a groundbreaking engineering feat, though some questioned the practical use cases and cost efficiency of AI-assisted development.

**Tags**: `#WebAssembly`, `#Firefox`, `#browser`, `#virtualization`, `#AI-assisted development`

---

<a id="item-2"></a>
## [Moonshot AI Unveils Kimi K3, a 2.8 Trillion Parameter Open-Weight Model](https://simonwillison.net/2026/Jul/16/kimi-k3/#atom-everything) ⭐️ 9.0/10

Chinese AI lab Moonshot AI announced Kimi K3, a 2.8 trillion parameter open-weight model, claiming it outperforms DeepSeek-V4-Pro and is competitive with top models like Claude Opus 4.8 and GPT-5.5. An open-weight release is promised by July 27, 2026. Kimi K3 represents a significant milestone as the largest open-weight model to date, potentially accelerating AI commoditization and intensifying competition between Chinese and US AI labs. Its high performance at a relatively lower cost per task could pressure pricing across the industry. The model uses 2.8 trillion parameters, with pricing at $3 per million input tokens and $15 per million output tokens, making it the most expensive Chinese open model to date. It achieved top ranking on Arena.ai&\#x27;s Frontend Code arena and a 1547 Elo on Artificial Analysis&\#x27;s long-horizon knowledge work evaluation.

rss · Simon Willison · Jul 16, 20:19

**Background**: The &\#x27;pelican benchmark&\#x27; is a humorous, informal test where an AI model is asked to generate an SVG image of a pelican riding a bicycle, often used to compare model capabilities. Open-weight models like Kimi K3 release their trained parameters publicly, enabling further research and fine-tuning. The rapid growth in parameter counts reflects the AI industry&\#x27;s push for more powerful models, with Chinese labs like Moonshot AI and DeepSeek challenging US leaders.

<details><summary>References</summary>
<ul>
<li><a href="https://playcode.io/blog/macbook-svg-benchmark">The Pelican Benchmark Is Saturated. We Made 9 AI... | Playcode Blog</a></li>
<li><a href="https://ndurner.github.io/pelican-benchmark">Pelican vs. Llama 3.1 405B and others | Nils Durner’s Blog</a></li>
<li><a href="https://huggingface.co/spaces/victor/pelican-benchmark">Pelican Benchmark - a Hugging Face Space by victor</a></li>

</ul>
</details>

**Discussion**: The community comments include Simon Willison&\#x27;s test of the model&\#x27;s pelican SVG generation, costing 25 cents, which he notes is the most expensive pelican from a Chinese model. Other commenters discuss the implications of commoditization, with softwaredoug suggesting Chinese labs aim to commoditize AI software to sell hardware, while m3h highlights the enormous model size and high operational costs.

**Tags**: `#AI`, `#open-source`, `#large language models`, `#Moonshot AI`, `#Kim K3`

---

<a id="item-3"></a>
## [Japan to Buy 27,500 NVIDIA Rubin Chips for Robot AI](https://www.bloomberg.com/news/articles/2026-07-16/japan-to-buy-nvidia-rubin-chips-to-build-sovereign-ai-for-robots) ⭐️ 9.0/10

Japan, through a newly formed company Noetra, announced plans to purchase 27,500 NVIDIA Rubin chips to build a large-scale data center for developing a sovereign foundation AI model for robotics. The project aims to release its first AI model by March 2027 and a robot-specific version within a few years. This $24 billion government-backed initiative marks Japan&\#x27;s strategic push to reduce dependence on US and Chinese AI technologies, aiming to capture over 30% of the global robotics market by 2040. It positions Japan as a potential &\#x27;third option&\#x27; in the global AI race alongside the US and China. Noetra, led by president Hiroyuki Tabata, will lead the project with partners including SoftBank, Preferred Networks \(backed by Toyota\), and NEC. The 27,500 Rubin chips are part of NVIDIA&\#x27;s next-generation architecture featuring the ARM-based &\#x27;Vera&\#x27; CPU, designed to work as a superchip with the Rubin GPU.

telegram · zaihuapd · Jul 16, 10:59

**Background**: NVIDIA&\#x27;s Rubin architecture, announced at CES 2026, is the successor to the Blackwell platform, promising significant leaps in computational power and efficiency for AI workloads. Sovereign AI refers to a nation&\#x27;s capability to develop and control its own AI infrastructure and models, reducing reliance on foreign technology. Robot foundation models are AI systems designed to generalize across various robot types and tasks, enabling autonomous operation in unstructured environments.

<details><summary>References</summary>
<ul>
<li><a href="https://explore.n1n.ai/blog/nvidia-rubin-chip-architecture-ai-future-2026-01-06">Nvidia Announces Rubin Chip Architecture as Blackwell Successor</a></li>
<li><a href="https://www.linkedin.com/pulse/navigating-future-sovereign-ai-blueprint-global-arif-sheikh-hluxc">the Future of Sovereign AI : A Blueprint for Global Empowerme</a></li>
<li><a href="https://www.linkedin.com/pulse/robotic-foundation-models-physical-ai-innovations-anand-ramachandran-fzfge">Robotic Foundation Models and Physical AI Models : Innovations...</a></li>

</ul>
</details>

**Tags**: `#AI`, `#Robotics`, `#NVIDIA`, `#Japan`, `#Sovereign AI`

---

<a id="item-4"></a>
## [TSMC adds $100B US investment, Q2 profit surges 77%](https://www.reuters.com/world/asia-pacific/tsmcs-second-quarter-profit-seen-hitting-record-ai-boom-2026-07-15/) ⭐️ 9.0/10

TSMC announced an additional $100 billion investment in Arizona plants, bringing total US investment to $265 billion, and reported a record Q2 net profit of NT$706.6 billion \($22 billion\), up 77% year-over-year. This massive investment underscores TSMC&\#x27;s confidence in sustained AI chip demand and solidifies its strategic expansion into the US, reshaping the global semiconductor supply chain and reducing reliance on Taiwan. TSMC raised its 2026 capital expenditure forecast to $60-64 billion and expects full-year dollar revenue to grow slightly over 40%. Arizona currently has eight fabs under construction or planned, with up to four more possible.

telegram · zaihuapd · Jul 16, 12:29

**Background**: TSMC is the world&\#x27;s largest dedicated semiconductor foundry, producing chips for major clients like Apple, Nvidia, and AMD. The US has been pushing to bring advanced chip manufacturing back home to secure supply chains, leading to the CHIPS Act subsidies. TSMC&\#x27;s initial investment in Arizona began in 2020.

**Tags**: `#TSMC`, `#semiconductor`, `#AI`, `#investment`, `#manufacturing`

---

<a id="item-5"></a>
## [New ArXiv Book on Mathematics of Data Science](https://arxiv.org/abs/2607.11938) ⭐️ 8.0/10

A new book titled &\#x27;Mathematics of Data Science&\#x27; has been posted on arXiv, emphasizing high-dimensional intuition and its importance for modern data science. This book fills a gap by providing a rigorous mathematical foundation for data science, helping practitioners understand why high-dimensional intuition breaks and how it affects model training and optimization. The book starts with explaining how intuition fails in high dimensions \(spikiness, volumes\) and connects to topics like stochastic gradient descent and high-dimensional models. It is available as open-access LaTeX source on arXiv.

hackernews · Anon84 · Jul 16, 20:38 · [Discussion](https://news.ycombinator.com/item?id=48939896)

**Background**: High-dimensional data is common in modern data science, but our low-dimensional intuition \(e.g., distances, volumes\) often misleads us. This &\#x27;curse of dimensionality&\#x27; makes many machine learning algorithms struggle. Understanding high-dimensional geometry is crucial for building robust models.

<details><summary>References</summary>
<ul>
<li><a href="https://www.math.uci.edu/~rvershyn/papers/HDP-book/HDP-2.pdf">High - Dimensional Probability</a></li>
<li><a href="https://en.wikipedia.org/wiki/High-dimensional_statistics">High-dimensional statistics - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Commenters praised the book&\#x27;s focus on high-dimensional intuition, with one noting it&\#x27;s essential for modern data science. Another mentioned a related upcoming book by Steve Brunton. Discussions also touched on the evolving definition of data science and the importance of statistics.

**Tags**: `#mathematics`, `#data-science`, `#high-dimensional`, `#education`, `#arxiv`

---

<a id="item-6"></a>
## [LLM-Assisted Programming: The Cognitive Toll of Code Review](https://pydantic.dev/articles/the-human-in-the-loop-is-tired) ⭐️ 8.0/10

An article argues that LLM-assisted programming replaces the rewarding experience of writing code with draining cognitive load from reviewing AI-generated code, flipping the traditional developer experience. This is significant because it highlights a hidden psychological cost of AI tools that could affect developer satisfaction, productivity, and long-term well-being, challenging the narrative that AI always improves developer experience. The article introduces the concept of the &\#x27;human reward function&\#x27; problem, where manual coding provided small dopamine hits that AI has automated away, leaving only the burden of review. Community members coined the term &\#x27;human on the hook&\#x27; to emphasize that humans are only held accountable when things go wrong.

hackernews · haritha1313 · Jul 17, 00:21 · [Discussion](https://news.ycombinator.com/item?id=48942000)

**Background**: Human-in-the-loop \(HITL\) is a paradigm where humans actively monitor or guide AI systems. In LLM-assisted programming, developers review AI-generated code, which can be cognitively demanding because they must verify correctness without having written the code themselves. The shift from writing to reviewing code changes the nature of developer work and its psychological rewards.

<details><summary>References</summary>
<ul>
<li><a href="https://www.geeksforgeeks.org/artificial-intelligence/human-in-the-loop-hitl-decision-making/">Human-in-the-Loop (HITL) - GeeksforGeeks</a></li>
<li><a href="https://hai.stanford.edu/ai-definitions/what-is-human-in-the-loop">What is Human-in-the-Loop? - Stanford HAI</a></li>
<li><a href="https://sanjewa.com/blogs/ai-code-review-cognitive-burden-harder-than-writing/">AI Code Review: Why It&#x27;s Harder Than Writing Code</a></li>

</ul>
</details>

**Discussion**: Commenters widely resonated with the &\#x27;human on the hook&\#x27; term, noting it captures the asymmetric risk where developers get no credit for success but bear blame for failures. Some reported enjoying AI assistance by treating it as a code generator rather than an agent, maintaining a planned approach to avoid cognitive overload.

**Tags**: `#LLM`, `#software engineering`, `#developer experience`, `#code review`, `#AI-assisted programming`

---

<a id="item-7"></a>
## [GPT-5.6 Codex Bug Can Delete Home Directory](https://simonwillison.net/2026/Jul/16/bad-codex-bug/#atom-everything) ⭐️ 8.0/10

Thibault Sottiaux reported a bug in GPT-5.6 Codex where the model can accidentally delete the user&\#x27;s home directory when full access mode is enabled and sandboxing protections are disabled. This bug underscores critical safety risks in AI coding agents, as accidental file deletion can lead to data loss and system compromise. It highlights the necessity of sandboxing and auto-review features for safe deployment of generative AI tools. The bug triggers when the model attempts to override the $HOME environment variable to set a temporary directory, but mistakenly deletes $HOME instead. It requires full access mode, no sandboxing, and auto-review disabled.

rss · Simon Willison · Jul 16, 17:45

**Background**: Codex is OpenAI&\#x27;s AI-powered coding assistant that can execute commands and modify files. Sandboxing isolates execution to prevent damage, and auto-review pauses risky actions for user approval. Without these protections, an AI agent can perform destructive operations like file deletion.

<details><summary>References</summary>
<ul>
<li><a href="https://northflank.com/blog/how-to-sandbox-ai-agents">How to sandbox AI agents in 2026: MicroVMs, gVisor &amp; isolation ...</a></li>
<li><a href="https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/">Practical Security Guidance for Sandboxing Agentic Workflows and ...</a></li>
<li><a href="https://openai.com/index/running-codex-safely/">Running Codex safely at OpenAI | OpenAI</a></li>

</ul>
</details>

**Tags**: `#codex`, `#coding-agents`, `#generative-ai`, `#ai-safety`

---

<a id="item-8"></a>
## [Inkling: Thinking Machines Lab&\#x27;s Open-Weight MoE Model](https://simonwillison.net/2026/Jul/16/inkling/#atom-everything) ⭐️ 8.0/10

Thinking Machines Lab, led by Mira Murati, released Inkling, an Apache-2.0 licensed Mixture-of-Experts multimodal model with 975B total parameters and 41B active parameters, trained on 45 trillion tokens of text, images, audio, and video. They also announced Inkling-Small \(276B total, 12B active\) whose weights will be released after testing. This release strengthens the US open-weights ecosystem with a competitive alternative to Chinese open models like DeepSeek and Qwen, joining NVIDIA Nemotron and Gemma 4. It provides a strong base model optimized for fine-tuning via Thinking Machines&\#x27; Tinker platform, lowering the barrier for customization. The model card is notably sparse, lacking detailed technical specifications and training data documentation beyond vague statements about public and third-party sources. Thinking Machines explicitly states Inkling is not a frontier model but a versatile base for fine-tuning, with multimodal capabilities and efficient inference.

rss · Simon Willison · Jul 16, 15:35

**Background**: Mixture-of-Experts \(MoE\) is a neural network architecture that divides computation into multiple specialized &\#x27;expert&\#x27; subnetworks, with a gating mechanism activating only a subset of experts per input. This allows models to have a large total parameter count while keeping the active \(computational cost\) parameters low, enabling efficient scaling. Open-weights models, like those released under Apache-2.0, provide publicly available weight files that anyone can download, modify, and deploy, fostering reproducibility and customization in the AI community.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Mixture_of_experts">Mixture of experts - Wikipedia</a></li>
<li><a href="https://developer.nvidia.com/blog/applying-mixture-of-experts-in-llm-architectures/">Applying Mixture of Experts in LLM Architectures | NVIDIA Technical Blog</a></li>
<li><a href="https://arxiv.org/abs/2507.11181">[2507.11181] Mixture of Experts in Large Language Models</a></li>

</ul>
</details>

**Tags**: `#open-weights`, `#Mixture-of-Experts`, `#multimodal`, `#LLM`, `#AI`

---

<a id="item-9"></a>
## [Sched-ext gets sub-scheduler enqueue and proxy execution support](https://lwn.net/Articles/1082717/) ⭐️ 8.0/10

The sched-ext extensible scheduler class in Linux is nearing completion of sub-scheduler hierarchies and proxy-execution support, specifically adding the enqueue\(\) callback path with a capability mechanism for hierarchical CPU access control. This enables multi-tenant systems to use different BPF-based schedulers for different control groups, improving isolation and flexibility. Proxy execution will resolve priority inversion issues by tracking blocked-on relationships. The enqueue path uses a three-level capability system \(idle CPU, dispatch queue, preemption\) passed down from parent to child schedulers. Parent schedulers grant capabilities via scx\_bpf\_sub\_grant\(\), and children cannot exceed their parent&\#x27;s capabilities.

rss · LWN.net · Jul 16, 14:00

**Background**: sched-ext allows custom CPU schedulers as BPF programs via struct\_ops. Originally single-scheduler, it now supports hierarchical sub-schedulers associated with cgroups. Proxy execution tracks task-blocking relationships to allow proxy tasks to execute on behalf of blocked ones, addressing priority inversion. The enqueue path was missing hierarchical control, which this patch series adds.

<details><summary>References</summary>
<ul>
<li><a href="https://www.kernel.org/doc/html/next/scheduler/sched-ext.html">Extensible Scheduler Class — The Linux Kernel documentation</a></li>
<li><a href="https://sched-ext.com/docs/OVERVIEW">Overview - sched_ext</a></li>
<li><a href="https://lwn.net/Articles/1030842/">A proxy-execution baby step [LWN.net]</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#scheduling`, `#sched\_ext`, `#BPF`, `#systems programming`

---

<a id="item-10"></a>
## [ExTernD Boosts Ternary LLM Quantization with Expanded-Rank Decomposition](https://www.reddit.com/r/MachineLearning/comments/1uy2zb3/externd_expandedrank_ternary_decomposition/) ⭐️ 8.0/10

ExTernD proposes a post-training quantization method that decomposes each weight matrix into two smaller ternary matrices and a diagonal scaling matrix, allowing the inner rank to be arbitrarily expanded to improve accuracy. This approach overcomes the inherent accuracy limit of fixed-size ternary quantization, enabling ternary LLMs to approach the accuracy of higher-precision methods with only a modest increase in VRAM, which is critical for efficient deployment. The expanded rank can be arbitrarily large, and experiments show that even moderate expansion yields significant accuracy improvements with only slightly more memory than current ternary methods.

reddit · r/MachineLearning · /u/LMTLS5 · Jul 16, 13:31

**Background**: Ternary quantization represents weights as -1, 0, or +1, saving memory and computation compared to full-precision models. However, previous fixed-size ternary post-training quantization \(PTQ\) for LLMs suffered from severe accuracy loss. ExTernD addresses this by using an expanded-rank decomposition that increases representational capacity without requiring retraining.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2303.01505">[2303.01505] Ternary Quantization: A Survey</a></li>
<li><a href="https://developer.nvidia.com/blog/optimizing-llms-for-performance-and-accuracy-with-post-training-quantization/">Optimizing LLMs for Performance and Accuracy with Post-Training Quantization | NVIDIA Technical Blog</a></li>

</ul>
</details>

**Tags**: `#quantization`, `#LLM`, `#efficiency`, `#deep learning`, `#post-training quantization`

---

<a id="item-11"></a>
## [QLoRA&\#x27;s default 2e-4 learning rate criticized for small datasets](https://www.reddit.com/r/MachineLearning/comments/1uy1z8b/the_qlora_2e4_default_is_wrong_under_10k_samples/) ⭐️ 8.0/10

A Reddit user argues that the widely recommended 2e-4 learning rate for QLoRA fine-tuning causes overfitting on datasets with fewer than 10,000 samples, and suggests using 1e-4 instead. This challenges a common assumption in the fine-tuning community and could save practitioners significant time and resources when working with small datasets, which are common in real-world applications. The user reports that switching from 2e-4 to 1e-4 and increasing epochs from 3 to 5 led to a major improvement in evaluation metrics, after weeks of debugging data and prompts. The 2e-4 default originates from fine-tuning on the 52k-sample Alpaca dataset, not smaller datasets.

reddit · r/MachineLearning · /u/Pretty-Ad774 · Jul 16, 12:50

**Background**: QLoRA is an efficient fine-tuning method that combines quantization and Low-Rank Adaptation \(LoRA\) to reduce memory usage, enabling fine-tuning of large language models on consumer GPUs. The learning rate is a critical hyperparameter; too high a rate on small datasets can cause overfitting, where the model memorizes training data but fails to generalize. The default 2e-4 learning rate was established in the QLoRA paper using the 52k-sample Alpaca dataset, but many real-world fine-tuning tasks use much smaller datasets.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2305.14314">[2305.14314] QLoRA: Efficient Finetuning of Quantized LLMs</a></li>
<li><a href="https://github.com/artidoro/qlora">GitHub - artidoro/qlora: QLoRA: Efficient Finetuning of Quantized LLMs · GitHub</a></li>

</ul>
</details>

**Tags**: `#QLoRA`, `#fine-tuning`, `#learning rate`, `#overfitting`, `#small datasets`

---

<a id="item-12"></a>
## [EU orders Google to open Android features and search data to rivals](https://www.theverge.com/policy/966438/eu-google-android-ai-interoperability-search-data-dma) ⭐️ 8.0/10

The European Commission ruled that Google must open 11 Android system features and certain search data to competitors, allowing rival AI assistants such as ChatGPT to gain system-level access equivalent to Google&\#x27;s own Gemini assistant. This decision could fundamentally reshape the Android ecosystem and search market by increasing competition for AI assistants and search engines, potentially giving users more choice. It also sets a precedent for regulating gatekeeper platforms under the EU&\#x27;s Digital Markets Act. The 11 features include core Android capabilities that rival assistants need for deep integration, and search data sharing is limited to specific uses to protect privacy. Google can still deny access based on legitimate security and privacy concerns, but any restrictions must comply with EU rules.

telegram · zaihuapd · Jul 16, 13:19

**Background**: The Digital Markets Act \(DMA\) is an EU regulation that designates large platforms like Google as &\#x27;gatekeepers&\#x27; and imposes obligations to ensure fair competition. Google&\#x27;s Android operating system and Google Search are core platform services under the DMA, and this ruling is a binding measure to enforce compliance.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Digital_Markets_Act">Digital Markets Act</a></li>
<li><a href="https://nairametrics.com/2026/07/16/eu-orders-google-to-share-android-features-search-data-with-rivals/">EU orders Google to share Android features, search data with ...</a></li>
<li><a href="https://www.upi.com/Top_News/World-News/2026/07/16/eu-google-specification-requirements-ai-android/7631784213542/">EU orders Google to share data, Android with competitors - UPI</a></li>

</ul>
</details>

**Tags**: `#EU regulation`, `#antitrust`, `#Android`, `#Google`, `#AI assistants`

---

<a id="item-13"></a>
## [Truth Social to Sell Fast Access to Trump Posts to Wall Street](https://www.cnn.com/2026/07/16/business/truth-social-data-wall-street) ⭐️ 8.0/10

Trump Media &amp; Technology Group \(TMTG\) announced the launch of Truth API, a paid data service providing millisecond-speed access to real-time posts from the top 10 accounts on Truth Social, available to institutional clients starting August 1. This enables algorithmic traders to act on Trump&\#x27;s market-moving statements faster than the public, raising serious concerns about market fairness, insider trading, and the blurring line between presidential business and public duty. The Truth API focuses on posts from the top 10 accounts, and TMTG has not disclosed pricing. CNN previously reported Trump used Truth Social to promote stocks he personally bought.

telegram · zaihuapd · Jul 17, 01:02

**Background**: Truth Social is a social media platform founded by Trump after being banned from major platforms. High-frequency trading \(HFT\) uses algorithms to execute trades in milliseconds, often relying on data speed advantages. By selling privileged data access, Truth Social monetizes its exclusive content, but critics argue it gives financial insiders an unfair edge.

<details><summary>References</summary>
<ul>
<li><a href="https://www.timesnownews.com/world/us/us-news/truth-api-explained-trump-media-new-service-gives-investors-faster-access-to-trump-posts-article-155113825">Truth API Explained: Trump Media New Service Gives Investors ...</a></li>
<li><a href="https://marketchameleon.com/articles/b/2026/7/16/trump-media-launches-truth-api-institutional-market-impact">Trump Media Unveils Truth API: Real-Time Access to ...</a></li>
<li><a href="https://zhuanlan.zhihu.com/p/20982511912">高频交易（HFT）：算法交易的闪电世界 - 知乎</a></li>

</ul>
</details>

**Tags**: `#social media`, `#algorithmic trading`, `#data monetization`, `#politics`, `#financial regulation`

---