---
layout: default
title: "Horizon Summary: 2026-07-07 (EN)"
date: 2026-07-07
lang: en
---

> From 47 items, 21 important content pieces were selected

---

1. [MIRA: 5B Parameter Interactive World Model for Rocket League](#item-1) ⭐️ 9.0/10
2. [16-Year-Old KVM Flaw Allows VM Escape on Intel and AMD](#item-2) ⭐️ 9.0/10
3. [China weighs export ban on top domestic AI models](#item-3) ⭐️ 9.0/10
4. [Kokoro: Local, CPU-Friendly High-Quality TTS Model](#item-4) ⭐️ 8.0/10
5. [StreetComplete: Fixing OpenStreetMap one quest at a time](#item-5) ⭐️ 8.0/10
6. [EU Chat Control Proposals: Privacy vs Child Safety](#item-6) ⭐️ 8.0/10
7. [EU Mandates Driver Monitoring Cameras in All New Cars](#item-7) ⭐️ 8.0/10
8. [Microsoft lays off idTech engine team at id Software](#item-8) ⭐️ 8.0/10
9. [Chat Control passed first round in EU Parliament](#item-9) ⭐️ 8.0/10
10. [Why 98% Success Often Isn't Enough](#item-10) ⭐️ 8.0/10
11. [Astro 7.0 Released with Rust-Powered Tooling and Faster Builds](#item-11) ⭐️ 8.0/10
12. [sqlite-utils 4.0 adds database migrations and nested transactions](#item-12) ⭐️ 8.0/10
13. [Woodruff: Trusted publishing is not a trust signal](#item-13) ⭐️ 8.0/10
14. [Faster RCU and Lockless Memory Allocation in Linux](#item-14) ⭐️ 8.0/10
15. [Mozilla CTO to host AMA on Open Source AI report](#item-15) ⭐️ 8.0/10
16. [Google's new 'Save media' setting lets Lens, voice data train AI](#item-16) ⭐️ 8.0/10
17. [Chinese Firms Shift from Nvidia to Domestic AI Chips](#item-17) ⭐️ 8.0/10
18. [New-api fixes billing integer overflow vulnerability](#item-18) ⭐️ 8.0/10
19. [NVIDIA Blackwell wafers made in US, but packaged in Taiwan](#item-19) ⭐️ 8.0/10
20. [DeepSeek develops own AI chip to reduce reliance on NVIDIA and Huawei](#item-20) ⭐️ 8.0/10
21. [CA, NY Push 3D Printer Gun-Blueprint Blocking Software, Sparking Debate](#item-21) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [MIRA: 5B Parameter Interactive World Model for Rocket League](https://www.reddit.com/r/MachineLearning/comments/1upofuw/mira_multiplayer_interactive_world_models_trained/) ⭐️ 9.0/10

Researchers from General Intuition, Kyutai, and Epic Games released MIRA, a 5B parameter interactive world model trained on 10k hours of synthetic Rocket League data, enabling real-time 4-player gameplay at 20 FPS on a single B200 GPU. MIRA demonstrates the feasibility of large-scale world models for multiplayer, physically complex environments, potentially accelerating research in game AI, simulation, and reinforcement learning by providing a playable demo and open-source tools. The model uses a latent diffusion architecture to generate video frames conditioned on all four players' actions, and the team released a 1,000-hour dataset of 4-player gameplay, a technical report, and a playable online demo.

reddit · r/MachineLearning · /u/MasterScrat · Jul 7, 07:59

**Background**: World models are neural networks that learn to simulate the dynamics of an environment, enabling agents to plan and reason. Previous single-player world models treat other agents as part of the environment, but MIRA conditions on multiple agent actions, making it suitable for multiplayer games. Rocket League is a high-speed physics-based game where players control rocket-powered cars to hit a ball into goals.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/mira-wm/mira">MIRA: Multiplayer Interactive World Models with ... - GitHub</a></li>
<li><a href="https://arxiv.org/abs/2607.05352">[2607.05352] Multiplayer Interactive World Models with ...</a></li>
<li><a href="https://www.linkedin.com/posts/generalintuition_introducing-mira-a-playable-multiplayer-activity-7479870314252922880-y9CV">Introducing MIRA. A playable, multiplayer world model. A ...</a></li>

</ul>
</details>

**Tags**: `#world models`, `#reinforcement learning`, `#simulation`, `#interactive AI`, `#game AI`

---

<a id="item-2"></a>
## [16-Year-Old KVM Flaw Allows VM Escape on Intel and AMD](https://github.com/V4bel/Januscape) ⭐️ 9.0/10

Researchers disclosed Januscape (CVE-2026-53359), a use-after-free vulnerability in KVM's shadow MMU that allows a guest VM to escape to the host on both Intel and AMD platforms. The bug has existed in the Linux kernel for approximately 16 years, from 2010 to June 2026. This is the first publicly known guest-to-host escape exploit that works on both Intel VMX and AMD SVM, making it a critical threat to multi-tenant cloud environments using KVM. The vulnerability was used as a 0-day in Google's kvmCTF and could compromise isolation boundaries of cloud providers. The flaw resides in the function kvm_mmu_get_child_sp() within the shadow MMU code shared by both Intel and AMD x86 KVM implementations. PoC code has been released that triggers host kernel panic from a guest, and on RHEL-like distributions, a local unprivileged user can also escalate to root.

telegram · zaihuapd · Jul 7, 10:14

**Background**: KVM (Kernel-based Virtual Machine) is a Linux kernel module that allows the host to run multiple virtual machines. The shadow MMU is a component of KVM that manages guest page tables by shadowing them with host physical addresses, a technique used when hardware-assisted nested paging is unavailable or disabled. A use-after-free bug occurs when memory is freed but still referenced, leading to potential corruption or exploitation.

<details><summary>References</summary>
<ul>
<li><a href="https://thehackernews.com/2026/07/16-year-old-linux-kvm-flaw-lets-guest.html">16-Year-Old Linux KVM Flaw Lets Guest VMs Escape to Host on ...</a></li>
<li><a href="https://cyberpress.org/16-year-old-linux-kvm-vulnerability/">16-Year-Old Linux KVM Vulnerability Allows Malicious Guests ...</a></li>
<li><a href="https://docs.kernel.org/virt/kvm/x86/mmu.html">The x86 kvm shadow mmu — The Linux Kernel documentation</a></li>

</ul>
</details>

**Tags**: `#vulnerability`, `#KVM`, `#virtualization`, `#security`, `#Linux kernel`

---

<a id="item-3"></a>
## [China weighs export ban on top domestic AI models](https://www.reuters.com/world/beijing-is-looking-curbing-overseas-access-chinas-top-ai-models-sources-say-2026-07-07/) ⭐️ 9.0/10

China's Ministry of Commerce is considering restricting overseas access to its most advanced AI models, including unreleased ones, and has held meetings with Alibaba, ByteDance, and Zhipu. This policy could reshape global AI competition by limiting technology transfer and potentially triggering reciprocal measures from other nations. The scope of restrictions is still under discussion and may only apply to future models; it remains uncertain whether the rules will be finalized.

telegram · zaihuapd · Jul 7, 11:42

**Background**: AI models are software systems trained on large datasets. Export controls are a tool governments use to prevent strategic technologies from falling into rivals' hands. China has been rapidly advancing its AI capabilities, prompting national security concerns.

**Tags**: `#AI regulation`, `#China`, `#export control`, `#AI models`, `#geopolitics`

---

<a id="item-4"></a>
## [Kokoro: Local, CPU-Friendly High-Quality TTS Model](https://ariya.io/2026/03/local-cpu-friendly-high-quality-tts-text-to-speech-with-kokoro/) ⭐️ 8.0/10

Kokoro is an open-source TTS model (82M parameters) that runs efficiently on CPU, including Apple Silicon, without requiring a dedicated GPU. This fills a gap for users without powerful GPUs, enabling high-quality TTS on everyday computers for accessibility, reading, and automation workflows. Kokoro supports manual IPA pronunciation guides and has a CLI tool; it produces natural-sounding speech but may struggle with single words or homographs.

hackernews · speckx · Jul 7, 18:24 · [Discussion](https://news.ycombinator.com/item?id=48821576)

**Background**: Text-to-speech (TTS) converts written text into spoken audio. High-quality TTS often requires neural networks that benefit from GPU acceleration, making local CPU-only solutions rare. Kokoro is designed to be efficient on CPUs, leveraging the mlx-audio library on Apple Silicon.

<details><summary>References</summary>
<ul>
<li><a href="https://grokipedia.com/page/Kokoro_TTS">Kokoro TTS</a></li>
<li><a href="https://github.com/nazdridoy/kokoro-tts">GitHub - nazdridoy/kokoro-tts: A CLI text-to-speech tool using the ...</a></li>

</ul>
</details>

**Discussion**: Community comments show enthusiastic adoption. Users appreciate Kokoro for accessibility products, reading articles via RSS, and even as the backbone of voice-controlled interfaces. Some note limitations with homographs and single-word utterances, but overall sentiment is positive.

**Tags**: `#TTS`, `#local`, `#CPU`, `#accessibility`, `#open-source`

---

<a id="item-5"></a>
## [StreetComplete: Fixing OpenStreetMap one quest at a time](https://streetcomplete.app/) ⭐️ 8.0/10

StreetComplete is a free, open-source Android app that turns contributing to OpenStreetMap into simple, gamified quests, such as answering questions about opening hours or pedestrian crossings. By lowering the barrier to entry, StreetComplete enables casual users to contribute high-quality data to OpenStreetMap, helping keep the map accurate and complete without requiring technical expertise. StreetComplete is designed for on-the-go use, prompting users with nearby quests that can be answered with minimal taps, and it requires no prior knowledge of OpenStreetMap's tagging system.

hackernews · kls0e · Jul 7, 12:38 · [Discussion](https://news.ycombinator.com/item?id=48816883)

**Background**: OpenStreetMap (OSM) is a collaborative project to create a free, editable map of the world, powered by volunteer contributions. However, the learning curve for editing OSM can be steep for newcomers. StreetComplete addresses this by providing a simple interface that guides users through specific, bite-sized tasks.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/StreetComplete">StreetComplete - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/OpenStreetMap">OpenStreetMap</a></li>

</ul>
</details>

**Discussion**: Community comments show strong positive reception, with users praising its beginner-friendly UI and fun approach. However, some users express concerns about data duplication and limited editing capabilities for adding new roads or footpaths. There is also discussion about Google potentially using OSM data without reciprocating, and challenges in getting local shop owners to update their own data.

**Tags**: `#OpenStreetMap`, `#crowdsourcing`, `#mapping`, `#open data`, `#mobile app`

---

<a id="item-6"></a>
## [EU Chat Control Proposals: Privacy vs Child Safety](https://fightchatcontrol.eu/chat-control-overview) ⭐️ 8.0/10

The European Union is advancing Chat Control proposals 1.0 and 2.0, which would require messaging platforms to scan all private messages and uploaded content for child sexual abuse material, potentially undermining end-to-end encryption. These proposals represent a significant shift towards mass surveillance, threatening the privacy and security of all EU citizens' digital communications. If enacted, they could set a global precedent for weakening encryption and enable broader government surveillance capabilities. Chat Control relies on client-side scanning, which checks content on users' devices before encryption, bypassing end-to-end protection. The proposals have been criticized for technical risks like false positives and potential abuse by authorities for purposes beyond child protection.

hackernews · gasull · Jul 7, 14:23 · [Discussion](https://news.ycombinator.com/item?id=48818311)

**Background**: Chat Control is a set of EU legislative proposals aimed at combating child sexual abuse material online. The key technical mechanism is client-side scanning (CSS), which analyzes content on a device before it is encrypted, effectively circumventing end-to-end encryption. This approach has raised serious privacy concerns as it could enable mass surveillance of all communications.

<details><summary>References</summary>
<ul>
<li><a href="https://www.internetsociety.org/wp-content/uploads/2020/03/2022-Client-Side-Scanning-Factsheet-EN.pdf">CC BY-NC-SA 4.0 Client-Side Scanning</a></li>
<li><a href="https://academic.oup.com/cybersecurity/article/10/1/tyad020/7590463">Bugs in our pockets: the risks of client-side scanning | Journal of Cybersecurity | Oxford Academic</a></li>

</ul>
</details>

**Discussion**: Commenters are broadly critical: one notes the proposals grant 'dictatorial powers' under the guise of protecting children, while another highlights the irony of banning a political party that opposes chat control. Technical users question how encrypted messages can be scanned without breaking encryption, pointing to either on-device scanning or privileged decryption as flawed options.

**Tags**: `#privacy`, `#surveillance`, `#encryption`, `#EU law`, `#policy`

---

<a id="item-7"></a>
## [EU Mandates Driver Monitoring Cameras in All New Cars](https://allaboutcookies.org/eu-mandatory-distracted-driver-system) ⭐️ 8.0/10

As of July 2024, the EU General Safety Regulation 2019/2144 requires all new car models sold in the European Union to be equipped with a driver monitoring system (DMS) that uses a camera to detect distraction and drowsiness. This regulation aims to reduce accidents caused by driver inattention, but it also raises significant privacy and usability concerns among drivers and consumer advocates. The DMS must be integrated into the vehicle's type-approval process and cannot be permanently disabled. The system typically uses infrared cameras to track eye and head movements, issuing alerts when distraction is detected.

hackernews · nickslaughter02 · Jul 7, 20:50 · [Discussion](https://news.ycombinator.com/item?id=48823557)

**Background**: Driver monitoring systems use in-car cameras and computer vision to assess driver alertness. They were first introduced by Toyota in 2006. The EU's General Safety Regulation 2019/2144, effective from 2022 for new types and 2024 for all new vehicles, mandates progressive safety features including DMS as part of a broader push toward automated driving and road safety.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Driver_monitoring_system">Driver monitoring system - Wikipedia</a></li>
<li><a href="https://eur-lex.europa.eu/eli/reg/2019/2144/oj/eng">Regulation - 2019/2144 - EN - EUR-Lex</a></li>
<li><a href="https://www.tuv.com/regulations-and-standards/en/eu-regulation-2019-2144-automotive-type-approval-general-safety-requirements.html">EU - Regulation 2019/2144 - Automotive Type Approval General</a></li>

</ul>
</details>

**Discussion**: Community comments are mixed: some users report positive experiences with similar systems (e.g., Ford's BlueCruise), noting accuracy and life-saving potential, while others express frustration with intrusive alerts, poor user experience, and privacy concerns. There is also skepticism about potential abuse and mandatory integration.

**Tags**: `#EU regulation`, `#driver monitoring`, `#privacy`, `#automotive safety`, `#UX`

---

<a id="item-8"></a>
## [Microsoft lays off idTech engine team at id Software](https://gamefromscratch.com/microsoft-fire-idtech-team-at-id-software/) ⭐️ 8.0/10

Microsoft has laid off the entire idTech engine team at id Software, which may indicate a strategic shift away from the in-house idTech engine toward using Unreal Engine 5. This move could accelerate industry consolidation around Unreal Engine, reducing engine diversity and potentially impacting the unique technical identity of id Software games. The layoffs affect the team responsible for idTech, a proprietary engine powering titles like Doom: The Dark Ages, and come amid broader Microsoft gaming layoffs; no official confirmation of the switch to Unreal Engine 5 has been provided.

hackernews · bauc · Jul 7, 15:33 · [Discussion](https://news.ycombinator.com/item?id=48819244)

**Background**: id Software has historically developed its own game engines, from id Tech 1 through id Tech 7, which powered iconic series like Doom and Quake. These engines were known for their performance and innovation. Unreal Engine 5, created by Epic Games, is a widely adopted third-party engine with advanced features like Nanite and Lumen.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Id_Tech">id Tech - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Id_Tech_7">id Tech 7 - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Unreal_Engine_5">Unreal Engine 5</a></li>

</ul>
</details>

**Discussion**: Commenters express concern that Microsoft is sacrificing unique technical culture for cost-saving homogenization, with some noting that using Unreal Engine could enable hiring cheaper contractors. Others question the lack of evidence for the specific layoffs and suggest open-sourcing idTech instead.

**Tags**: `#id Software`, `#Microsoft`, `#game engines`, `#Unreal Engine`, `#corporate strategy`

---

<a id="item-9"></a>
## [Chat Control passed first round in EU Parliament](https://www.heise.de/en/news/Showdown-in-Strasbourg-The-unexpected-return-of-Chat-Control-1-0-11356680.html) ⭐️ 8.0/10

The European Parliament unexpectedly revived the controversial Chat Control law during its second reading, and it passed the first procedural round, giving proponents a tactical advantage. This law would mandate mass surveillance of private messages, threatening end-to-end encryption and digital privacy. Its advancement could set a dangerous precedent for widespread surveillance in the EU. In the second reading, amendments or rejection require an absolute majority of 361 MEPs, while the law itself can pass with a simple majority of those present. Many MEPs have already left for summer break, making rejection harder.

hackernews · miroljub · Jul 7, 15:16 · [Discussion](https://news.ycombinator.com/item?id=48819008)

**Background**: Chat Control, formally the EU CSA Regulation, was first proposed in 2022 to combat child sexual abuse material by requiring platforms to scan private messages. It has been highly controversial due to its impact on privacy and encryption. The temporary version expired in April 2026, but the permanent regulation is now being pushed again through aggressive procedural tactics.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Chat_Control">Chat Control - Wikipedia</a></li>
<li><a href="https://edri.org/our-work/chat-control-what-is-actually-going-on/">Chat Control: What is actually going on? - European Digital ...</a></li>

</ul>
</details>

**Discussion**: Commenters expressed frustration over the procedural tactics, noting that unpopular laws are repeatedly re-introduced with minor tweaks. One user quoted Jean-Claude Juncker's remark about pushing laws step by step until there is no turning back. Others doubted that enough 'no' votes could be found to stop the law by Thursday.

**Tags**: `#EU`, `#privacy`, `#surveillance`, `#regulation`, `#democracy`

---

<a id="item-10"></a>
## [Why 98% Success Often Isn't Enough](https://whynothugo.nl/journal/2026/07/03/98-isnt-very-much/) ⭐️ 8.0/10

A blog post by Hugo Landau argues that a 98% success rate is often insufficient in practice, using the analogy of cleaning up pine needles to illustrate how even a tiny remaining mess can render the effort unacceptable. The post challenges the common assumption that high percentages are sufficient, highlighting that context matters greatly in determining acceptable thresholds, which is crucial for software reliability, quality assurance, and risk assessment. The author uses the example of removing 99% of pine needles—while numerically impressive, the remaining 1% is still visually distinct and unacceptable. The post also points out that percentages can be misleading near their extremes, where a change from 98% to 99% cuts the failure rate in half.

hackernews · speckx · Jul 7, 12:45 · [Discussion](https://news.ycombinator.com/item?id=48816959)

**Background**: Percentages are commonly used to measure success rates, but they can obscure the practical significance of failures. For example, a 99.9% uptime still means significant downtime over a year for critical systems. The blog post explores this idea with everyday analogies.

**Discussion**: Comments generally agree with the premise but add nuance: some argue that 98% is sufficient in business contexts, while others reinforce that percentages can be deceptive and that small failure rates compound in large systems. A notable comment from nemo1618 uses the pine needle analogy to support the post's view.

**Tags**: `#statistics`, `#quality`, `#software engineering`, `#reliability`, `#decision-making`

---

<a id="item-11"></a>
## [Astro 7.0 Released with Rust-Powered Tooling and Faster Builds](https://astro.build/blog/astro-7/) ⭐️ 8.0/10

Astro 7.0 has been released, featuring a new Rust-powered compiler and Markdown pipeline, reduced dependencies from 247 to 190, and build performance improvements of 15-61% when combined with Vite 8 and Rolldown bundler. This release marks a significant step in reducing JavaScript ecosystem bloat and improving build performance for static sites. Developers using Astro for content-driven websites will benefit from faster compilation and lower maintenance overhead. Astro 7.0 also stabilizes route caching and adds experimental CDN cache providers for Netlify, Vercel, and Cloudflare. The Rust compiler was contributed by a community member (Princesseuh).

hackernews · saikatsg · Jul 7, 18:30 · [Discussion](https://news.ycombinator.com/item?id=48821653)

**Background**: Astro is a modern static site generator that allows developers to use components from various UI frameworks (React, Vue, Svelte, etc.) while shipping zero JavaScript by default. It has evolved from a JavaScript-based build tool to incorporate Rust for performance-critical tasks, following a trend seen in the developer tools ecosystem (e.g., Astral's Python tools). The reduction in dependencies aligns with a broader industry push toward leaner Node.js projects.

<details><summary>References</summary>
<ul>
<li><a href="https://astro.build/blog/astro-7/">Astro 7.0 | Astro - astro.build</a></li>
<li><a href="https://astro.build/blog/astro-6/">Astro 6.0 | Astro</a></li>

</ul>
</details>

**Discussion**: Community reactions are mixed but largely positive. Princesseuh, the Rust compiler contributor, offered to answer questions. Some users praised the dependency reduction (from 247 to 190) and the familiar static-site workflow. However, concerns were raised about version instability (seven major versions implying frequent breaking changes) and confusion over Astro's role as a framework that also supports other frameworks.

**Tags**: `#web development`, `#Astro`, `#JavaScript`, `#static site generator`, `#build tools`

---

<a id="item-12"></a>
## [sqlite-utils 4.0 adds database migrations and nested transactions](https://simonwillison.net/2026/Jul/7/sqlite-utils-4/#atom-everything) ⭐️ 8.0/10

sqlite-utils 4.0, released on July 7, 2026, introduces three major features: database schema migrations, nested transactions via a new db.atomic() method, and support for compound foreign keys. This release significantly enhances sqlite-utils as a tool for managing SQLite databases, addressing common needs for schema versioning and transactional safety. Developers using Python for data management will benefit from easier migration workflows and more robust transaction handling. Migrations are defined in Python files using the Migrations class and the table.transform() method, which implements SQLite's recommended pattern of creating a temporary table. Nested transactions use SQLite savepoints under the hood, and compound foreign keys allow referencing multiple columns.

rss · Simon Willison · Jul 7, 19:32

**Background**: SQLite is an embedded SQL database engine that does not natively support schema migrations or nested transactions. The sqlite-utils library, created by Simon Willison, provides a Python API and CLI for manipulating SQLite databases. Prior to version 4.0, users had to manually handle schema changes using SQLite's limited ALTER TABLE capabilities. This release automates migration tracking and execution, and introduces nested transactions via savepoints.

<details><summary>References</summary>
<ul>
<li><a href="https://sqlite.org/lang_transaction.html">Transaction - SQLite java - SQLiteDatabase nested transaction and workaround ... Code sample How to Handle Nested Transactions in SQLite - Sling Academy Understanding Nested Transactions in SQLite and Effective ... How to use transactions — sqlite7 documentation sqlite-utils 4.0rc1 adds migrations and nested transactions</a></li>
<li><a href="https://sqlite.org/foreignkeys.html">SQLite Foreign Key Support</a></li>

</ul>
</details>

**Tags**: `#sqlite-utils`, `#SQLite`, `#database migrations`, `#Python`, `#schema`

---

<a id="item-13"></a>
## [Woodruff: Trusted publishing is not a trust signal](https://lwn.net/Articles/1081690/) ⭐️ 8.0/10

William Woodruff published a blog post arguing that PyPI's trusted publishing should not be interpreted as a signal of package trust or quality, but rather as a form of authentication. This clarifies a common misconception among developers, which could otherwise lead to over-reliance on trusted publishing for software supply chain security decisions. Woodruff emphasizes that trusted publishing uses OpenID Connect (OIDC) to establish identity between a CI/CD workflow and PyPI, and that PyPI deliberately avoids rendering it as a green checkmark.

rss · LWN.net · Jul 7, 14:27

**Background**: Trusted publishing is a mechanism introduced by PyPI that allows packages to be published without storing long-lived API tokens. Instead, it uses OIDC to exchange short-lived identity tokens between a trusted third-party service (like GitHub Actions) and PyPI. It is designed to simplify the publishing workflow, but Woodruff warns that it should not be conflated with package trust or security assurance.

<details><summary>References</summary>
<ul>
<li><a href="https://docs.pypi.org/trusted-publishers/">Publishing to PyPI with a Trusted Publisher</a></li>
<li><a href="https://docs.pypi.org/trusted-publishers/using-a-publisher/">Publishing with a Trusted Publisher - PyPI Docs</a></li>

</ul>
</details>

**Tags**: `#PyPI`, `#security`, `#software supply chain`, `#trusted publishing`, `#authentication`

---

<a id="item-14"></a>
## [Faster RCU and Lockless Memory Allocation in Linux](https://lwn.net/Articles/1081009/) ⭐️ 8.0/10

Puranjay Mohan presented work on improving RCU performance by allowing normal RCU callbacks to be executed after expedited grace periods, and a new kmalloc_nolock() function for lockless memory allocation from any kernel context was discussed at LSFMM+BPF 2026. These developments significantly enhance kernel scalability by reducing memory allocation latency and speeding up RCU grace period completion, benefiting high-performance workloads under memory pressure. The RCU improvement involves tracking both non-expedited and expedited grace-period numbers to allow callbacks to run when either completes, while kmalloc_nolock() enables lockless allocation without needing to hold locks.

rss · LWN.net · Jul 7, 13:39

**Background**: Read-copy-update (RCU) is a synchronization mechanism in the Linux kernel that allows readers to access data without locks while writers create new versions. RCU grace periods ensure all readers have finished before old data is freed. kmalloc() is the standard kernel memory allocator, but traditionally requires proper lock context; kmalloc_nolock() extends it to work in any context.

<details><summary>References</summary>
<ul>
<li><a href="https://www.oreilly.com/library/view/linux-device-drivers/0596005903/ch08.html">8. Allocating Memory - Linux Device Drivers, 3rd Edition [Book]</a></li>
<li><a href="http://www.jikos.cz/jikos/Kmalloc_Internals.html">Kmalloc Internals: Exploring Linux Kernel Memory Allocation</a></li>
<li><a href="https://people.netfilter.org/rusty/unreliable-guides/kernel-hacking/routines-kmalloc.html">kmalloc()/kfree() include/linux/slab.h</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#RCU`, `#memory allocation`, `#performance`, `#LSFMM+BPF`

---

<a id="item-15"></a>
## [Mozilla CTO to host AMA on Open Source AI report](https://www.reddit.com/r/MachineLearning/comments/1upxdvc/raffi_krikorian_cto_mozilla_ama_on_the_state_of/) ⭐️ 8.0/10

Mozilla CTO Raffi Krikorian announced an AMA on July 14, 2026, to discuss the inaugural State of Open Source AI report, covering hidden costs of 'free' models, enterprise adoption, the China effect, developer trust, and the agentic harness. This AMA addresses critical, often misunderstood aspects of open source AI in production, providing insights that can guide developers and enterprises in navigating real-world costs, trust, and strategic leverage in the AI ecosystem. The report and AMA focus on five themes: the hidden tax of 'free' models, real versus marketing claims in enterprise adoption, how Chinese models reshape leverage, developer trust based on a survey of 950+ developers, and why the 'agentic harness' layer is the new battleground for open source.

reddit · r/MachineLearning · /u/raffikrikorian · Jul 7, 14:51

**Background**: Open source AI models like Llama and Mistral are widely used, but deploying them in production often incurs unexpected costs from infrastructure and proprietary tooling. The 'agentic harness' refers to the operational layer around a model that manages context, tool access, and safety, which is now the focus of competition. This report aims to clarify these real-world dynamics beyond popular narratives.

<details><summary>References</summary>
<ul>
<li><a href="https://harness-engineering.ai/blog/agent-harness-complete-guide/">The Complete Guide to Agent Harness: What It Is and Why It ...</a></li>
<li><a href="https://opendatascience.com/what-is-an-agent-harness-the-architecture-behind-reliable-agentic-ai/">What is an Agent Harness? The Architecture Behind Agentic AI</a></li>

</ul>
</details>

**Tags**: `#open source AI`, `#Mozilla`, `#AI industry`, `#enterprise AI`, `#developer trust`

---

<a id="item-16"></a>
## [Google's new 'Save media' setting lets Lens, voice data train AI](https://techcrunch.com/2026/07/06/if-you-use-google-youre-training-its-ai-heres-how-to-opt-out/) ⭐️ 8.0/10

Google introduced a new 'Save media' setting within Search service history that saves media from features like Google Lens, Search Live, voice search, and Translate speaking exercises, and uses it to improve Google services and AI models. This policy change affects millions of users who use these features, raising privacy concerns about how media is used for AI training. It also highlights the importance of opt-out mechanisms in an era of growing AI data collection. The setting is part of the 'Search service history' in Google Account settings, and users can opt out by turning off 'Save media'. Media includes images, files, audio, and video from Google Lens, Search Live, voice search, and Translate speaking exercises.

telegram · zaihuapd · Jul 7, 04:00

**Background**: Google Lens is an AI-powered visual search tool that identifies objects and provides relevant information. Search Live is a feature allowing interactive voice and camera conversations with Google Search. These features generate media that Google may now save for model training.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Google_Lens">Google Lens</a></li>
<li><a href="https://support.google.com/websearch/answer/16329036?hl=en&co=GENIE.Platform=Android">Have a real-time conversation with Live in Search - Android - Google Search Help</a></li>

</ul>
</details>

**Tags**: `#Google`, `#privacy`, `#AI training`, `#search settings`

---

<a id="item-17"></a>
## [Chinese Firms Shift from Nvidia to Domestic AI Chips](https://www.bloomberg.com/news/articles/2026-07-07/chinese-firms-leave-nvidia-for-local-ai-suppliers-survey-shows) ⭐️ 8.0/10

A survey of 60 Chinese executives shows firms are reducing Nvidia AI accelerator purchases and plan to allocate 46% of their AI chip budget to domestic alternatives within the next 12 months, up from 30% currently. This shift signals a major realignment in the global AI hardware supply chain, driven by China's data center investment plan and geopolitical tensions, which could significantly impact Nvidia's revenue and accelerate domestic chipmakers like Hygon and Cambricon. China plans to invest roughly 2 trillion yuan ($275 billion) in data centers over the next five years, with at least 80% of core technology sourced domestically, benefiting companies such as Tencent, Alibaba, Huawei, Hygon, and Cambricon.

telegram · zaihuapd · Jul 7, 04:45

**Background**: The survey reflects the ongoing impact of U.S. export controls on advanced Nvidia chips to China, prompting a push for self-sufficiency in AI accelerators. Hygon and Cambricon are two prominent domestic chip designers: Hygon produces CPUs and AI accelerators using x86-compatible designs, while Cambricon focuses on AI chips for cloud and edge computing. Both have seen significant market growth amid the shift.

<details><summary>References</summary>
<ul>
<li><a href="https://zh.wikipedia.org/zh-tw/海光信息">海光信息 - 維基百科，自由的百科全書</a></li>
<li><a href="https://baike.baidu.com/item/中科寒武纪科技股份有限公司/24545271">中科寒武纪科技股份有限公司_百度百科 一天吃透一家上市科技公司：寒武纪 - 知乎 中科寒武纪科技股份有限公司 - 爱企查 三年涨超40倍，寒武纪市值超万亿_上市_公司_股价 投资者关系 - 寒武纪 - Cambricon 算力需求井喷，寒武纪业绩快报：2025年实现上市后首次全年盈利 ，但第...</a></li>

</ul>
</details>

**Tags**: `#AI chips`, `#China`, `#Nvidia`, `#semiconductors`, `#supply chain`

---

<a id="item-18"></a>
## [New-api fixes billing integer overflow vulnerability](https://github.com/QuantumNous/new-api/commit/d0bd8aa) ⭐️ 8.0/10

The new-api project has released two commits that add boundary checks and saturation arithmetic to prevent integer overflow in quota calculations, which could cause negative charges. This fix addresses a severe billing vulnerability that could allow users to artificially gain credits by triggering negative deductions, impacting any deployment using new-api for metering or billing. It underscores the importance of robust input validation in financial logic. The vulnerability stemmed from missing validation on user-controllable parameters in quota calculation; when oversized values caused integer overflow, deductions became negative. The fix introduces upper-bound validation and saturation arithmetic that clamps results to the maximum representable value instead of wrapping around.

telegram · zaihuapd · Jul 7, 07:26

**Background**: Integer overflow occurs when an arithmetic operation exceeds the maximum value a fixed-width integer can hold, causing it to 'wrap around' to a negative or very small value. In security contexts, this can bypass checks and lead to unintended behavior. Saturation arithmetic is a technique that clamps the result to the range's extremes instead of wrapping, preventing such exploits.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Saturation_arithmetic">Saturation arithmetic</a></li>
<li><a href="https://cwe.mitre.org/data/definitions/190.html">CWE-190: Integer Overflow or Wraparound (4.20)</a></li>
<li><a href="https://github.com/QuantumNous/new-api/issues/5876">32-bit (armv7/玩客云) compatibility issue: quota int overflow causes ...</a></li>

</ul>
</details>

**Tags**: `#security`, `#bug fix`, `#integer overflow`, `#billing`, `#open source`

---

<a id="item-19"></a>
## [NVIDIA Blackwell wafers made in US, but packaged in Taiwan](https://www.tomshardware.com/tech-industry/nvidia-and-intel-tout-chips-built-in-america-but-every-arizona-made-blackwell-die-is-still-packaged-in-taiwan) ⭐️ 8.0/10

TSMC's Arizona Fab 21 has begun mass production of NVIDIA Blackwell wafers using the custom 4NP process, but these wafers must be shipped to Taiwan for CoWoS-L advanced packaging. This highlights a critical gap in the US semiconductor supply chain: while advanced logic fabrication is now possible domestically, the US still lacks high-volume advanced packaging and HBM memory capabilities, creating ongoing reliance on Taiwanese facilities and delaying full supply chain independence until at least 2028-2029. The 4NP process is a customized 4nm-class node for NVIDIA, and CoWoS-L combines chip-on-wafer-on-substrate with an RDL interposer and local silicon interconnect. Amkor, TSMC, and SK Hynix are building packaging and HBM capacity in the US, but these facilities are not yet operational.

telegram · zaihuapd · Jul 7, 09:47

**Background**: Advanced packaging, such as TSMC's CoWoS-L, is essential for high-performance AI chips like NVIDIA Blackwell, as it integrates multiple dies and memory stacks into a single package. US semiconductor policy has focused on expanding domestic fabrication, but packaging and memory supply chains remain concentrated in Asia, particularly Taiwan and South Korea.

<details><summary>References</summary>
<ul>
<li><a href="https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm">CoWoS® - Taiwan Semiconductor Manufacturing Company Limited</a></li>
<li><a href="https://www.tomshardware.com/tech-industry/tsmc-readies-lower-cost-4nm-manufacturing-tech-up-to-85-cheaper">TSMC readies lower-cost 4nm manufacturing tech: Up to 8.5% ...</a></li>
<li><a href="https://www.intel.com/content/www/us/en/foundry/process/18a.html">Intel 18A | See Our Biggest Process Innovation</a></li>

</ul>
</details>

**Tags**: `#semiconductor`, `#NVIDIA`, `#Blackwell`, `#supply chain`, `#advanced packaging`

---

<a id="item-20"></a>
## [DeepSeek develops own AI chip to reduce reliance on NVIDIA and Huawei](https://www.reuters.com/world/china/chinas-deepseek-developing-its-own-ai-chip-sources-say-2026-07-07/) ⭐️ 8.0/10

Chinese AI company DeepSeek has begun developing its own AI chip focused on inference, aiming to reduce dependence on NVIDIA and Huawei chips. The project started about a year ago and is still in early stages, with DeepSeek actively recruiting chip design engineers and contacting foundries and storage companies. This move could reshape the AI hardware landscape in China and reduce DeepSeek's vulnerability to US export controls, which currently restrict access to advanced NVIDIA chips. If successful, it may also intensify competition with Huawei's Ascend series and other domestic chipmakers. The chip is designed specifically for inference, the phase where trained models generate responses, rather than training. DeepSeek previously relied on NVIDIA H800 and Huawei Ascend chips, and founder Liang Wenfeng acknowledged in a rare 2024 interview that chip restrictions are a challenge for the company.

telegram · zaihuapd · Jul 7, 11:08

**Background**: AI inference is the process of using a trained model to generate outputs from new inputs, as opposed to training which teaches the model. NVIDIA H800 GPUs are high-performance datacenter GPUs, while Huawei Ascend series is a Chinese AI chip alternative, but both are subject to US export restrictions. Developing proprietary inference chips can reduce dependence on external suppliers and optimize cost and performance for specific workloads.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/NVIDIA_H800_GPU">NVIDIA H800 GPU</a></li>
<li><a href="https://www.digitalocean.com/resources/articles/ai-inference-vs-training">AI Inference vs Training: Key Differences Explained</a></li>
<li><a href="https://tech-insider.org/huawei-ascend-950pr-ai-chip-nvidia-china-2026/">Huawei Ascend 950PR: The 1.56 PFLOP AI Chip vs Nvidia [2026]</a></li>

</ul>
</details>

**Tags**: `#AI Chips`, `#DeepSeek`, `#Semiconductors`, `#China Tech`, `#US-China Trade`

---

<a id="item-21"></a>
## [CA, NY Push 3D Printer Gun-Blueprint Blocking Software, Sparking Debate](https://www.theverge.com/tech/960802/3d-printed-gun-laws-ghost-guns) ⭐️ 8.0/10

California and New York are advancing legislation that would require 3D printers sold in their states to include software capable of detecting and blocking gun blueprints, with New York's law already signed and California's AB 2047 passing the Assembly. This legislation represents a significant intervention in the open-source 3D printing ecosystem and DIY culture, raising concerns about digital rights, censorship, and the potential for misuse beyond gun control, such as intellectual property enforcement. New York's law also applies to CNC machines, while California's AB 2047 would ban sale of uncertified printers after March 2029 with fines up to $25,000; critics warn the technology may inadvertently block everyday objects and require cloud scanning of user files.

telegram · zaihuapd · Jul 7, 14:02

**Background**: 3D printers build objects layer by layer from digital models using slicing software that converts CAD files into G-code instructions. CNC machines are computer-controlled subtractive tools that carve material from a block. Gun blueprints for these machines can be shared online, enabling unregulated firearm production. Supporters compare the blocking software to anti-counterfeiting measures in printers, but opponents fear it could limit technological freedom.

<details><summary>References</summary>
<ul>
<li><a href="https://gnet-research.org/2024/11/06/blocking-the-blueprint-technological-barriers-against-3d-printed-firearms/">Blocking the Blueprint: Technological Barriers Against 3D ...</a></li>
<li><a href="https://www.technology.org/2026/06/13/new-york-law-3d-printers-block-guns/">New York Law Makes 3D Printers Block Guns - Technology Org</a></li>
<li><a href="https://en.wikipedia.org/wiki/Computer_numerical_control">Computer numerical control - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#3D printing`, `#gun control`, `#legislation`, `#digital rights`, `#open source`

---