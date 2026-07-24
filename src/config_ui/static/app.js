const copy = {
  en: {
    language: "Language",
    eyebrow: "Local configuration",
    title: "A safer place to configure Horizon.",
    intro:
      "This editor runs only on your computer. Configuration controls will appear here in the next implementation stage.",
    checking: "Securing your local session…",
    checkingDetail: "Checking the one-time startup link and browser session.",
    ready: "Local session ready",
    readyDetail:
      "The secure shell is connected. No configuration data has been loaded yet.",
    failed: "Could not start a local session",
    failedDetail:
      "Close this tab and start horizon-config again to generate a fresh one-time link.",
    privacy:
      "Loopback only · No cloud account · No configuration data on this page",
  },
  "zh-CN": {
    language: "语言",
    eyebrow: "本地配置",
    title: "更安全地配置 Horizon。",
    intro: "此编辑器只在你的电脑上运行。配置控件将在下一实施阶段提供。",
    checking: "正在保护本地会话…",
    checkingDetail: "正在验证一次性启动链接和浏览器会话。",
    ready: "本地会话已就绪",
    readyDetail: "安全外壳已连接，尚未加载任何配置数据。",
    failed: "无法启动本地会话",
    failedDetail: "请关闭此标签页并重新运行 horizon-config，以生成新的一次性链接。",
    privacy: "仅限本机回环 · 无需云端账户 · 此页面不包含配置数据",
  },
};

const elements = {
  languageLabel: document.querySelector("#language-label"),
  languageSelect: document.querySelector("#language-select"),
  eyebrow: document.querySelector("#eyebrow"),
  title: document.querySelector("#page-title"),
  intro: document.querySelector("#intro"),
  statusIcon: document.querySelector("#status-icon"),
  statusTitle: document.querySelector("#status-title"),
  statusDetail: document.querySelector("#status-detail"),
  privacy: document.querySelector("#privacy-note"),
};

let status = "checking";

function preferredLanguage() {
  try {
    const saved = window.localStorage.getItem("horizon-config-language");
    if (saved && copy[saved]) {
      return saved;
    }
  } catch {
    // Local storage is optional; session bootstrap does not depend on it.
  }
  return navigator.language.toLowerCase().startsWith("zh") ? "zh-CN" : "en";
}

function render(language) {
  const text = copy[language] || copy.en;
  document.documentElement.lang = language;
  elements.languageSelect.value = language;
  elements.languageLabel.textContent = text.language;
  elements.eyebrow.textContent = text.eyebrow;
  elements.title.textContent = text.title;
  elements.intro.textContent = text.intro;
  elements.privacy.textContent = text.privacy;

  if (status === "ready") {
    elements.statusTitle.textContent = text.ready;
    elements.statusDetail.textContent = text.readyDetail;
  } else if (status === "failed") {
    elements.statusTitle.textContent = text.failed;
    elements.statusDetail.textContent = text.failedDetail;
  } else {
    elements.statusTitle.textContent = text.checking;
    elements.statusDetail.textContent = text.checkingDetail;
  }
}

function setStatus(nextStatus) {
  status = nextStatus;
  elements.statusIcon.className = `status-icon ${nextStatus}`;
  elements.statusIcon.replaceChildren();
  const marker = document.createElement("span");
  marker.className = nextStatus === "checking" ? "spinner" : "status-marker";
  marker.textContent = nextStatus === "ready" ? "✓" : nextStatus === "failed" ? "!" : "";
  elements.statusIcon.append(marker);
  render(elements.languageSelect.value);
}

async function exchangeBootstrapToken(token) {
  const response = await fetch("/api/v1/session/bootstrap", {
    method: "POST",
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token }),
  });
  if (!response.ok) {
    throw new Error("bootstrap rejected");
  }
}

async function checkExistingSession() {
  const response = await fetch("/api/v1/session", {
    credentials: "same-origin",
  });
  if (!response.ok) {
    throw new Error("session unavailable");
  }
}

async function initializeSession() {
  const fragment = new URLSearchParams(window.location.hash.slice(1));
  const bootstrapToken = fragment.get("bootstrap");

  if (window.location.hash) {
    window.history.replaceState(null, "", `${window.location.pathname}${window.location.search}`);
  }

  if (bootstrapToken) {
    await exchangeBootstrapToken(bootstrapToken);
  } else {
    await checkExistingSession();
  }
}

const language = preferredLanguage();
render(language);
elements.languageSelect.addEventListener("change", (event) => {
  const selected = event.target.value;
  try {
    window.localStorage.setItem("horizon-config-language", selected);
  } catch {
    // Language selection still works for the current page.
  }
  render(selected);
});

initializeSession()
  .then(() => setStatus("ready"))
  .catch(() => setStatus("failed"));
