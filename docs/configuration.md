---
layout: default
title: Configuration Guide
---

# Configuration Guide

Horizon is configured through two files: a `.env` file for API keys and a `data/config.json` file for sources, AI provider, and filtering options.

## AI Providers

Configure the default model used by Horizon's AI-powered stages. Individual
stages can optionally override this default.

`api_key_env` is always an environment variable name, not the API key value.
Store secrets in `.env` or your shell environment, then point `api_key_env` at
that variable:

```bash
OPENAI_API_KEY=sk-your-key
GOOGLE_API_KEY=your-gemini-key
```

When Horizon starts, environment variables have priority because
`data/config.json` does not store the secret. For local VS Code runs, create
`.env` in the repository root and launch Horizon from that same root directory.

Common API key variable names:

| Provider | `api_key_env` value |
| --- | --- |
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Azure OpenAI | `AZURE_OPENAI_API_KEY` |
| Gemini | `GOOGLE_API_KEY` |
| MiniMax | `MINIMAX_API_KEY` |
| Aliyun DashScope | `DASHSCOPE_API_KEY` |
| Doubao | `DOUBAO_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |

**Anthropic Claude**:

```json
{
  "ai": {
    "provider": "anthropic",
    "model": "claude-sonnet-4.5-20250929",
    "api_key_env": "ANTHROPIC_API_KEY",
    "throttle_sec": 0
  }
}
```

**OpenAI**:

```json
{
  "ai": {
    "provider": "openai",
    "model": "gpt-4",
    "api_key_env": "OPENAI_API_KEY",
    "throttle_sec": 0
  }
}
```

**Gemini**:

```json
{
  "ai": {
    "provider": "gemini",
    "model": "gemini-2.0-flash",
    "api_key_env": "GOOGLE_API_KEY",
    "throttle_sec": 0
  }
}
```

**Azure OpenAI**:

```json
{
  "ai": {
    "provider": "azure",
    "model": "gpt-4o-production",
    "api_key_env": "AZURE_OPENAI_API_KEY",
    "azure_endpoint_env": "AZURE_OPENAI_ENDPOINT",
    "api_version": "2024-10-21",
    "throttle_sec": 0
  }
}
```

Set `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` in your `.env`. The `model` field should be your Azure deployment name, not just the base model family name.

**MiniMax**:

The built-in provider defaults to `MiniMax-M3` and the global
OpenAI-compatible endpoint:

```json
{
  "ai": {
    "provider": "minimax",
    "model": "MiniMax-M3",
    "api_key_env": "MINIMAX_API_KEY",
    "base_url": "https://api.minimax.io/v1",
    "throttle_sec": 0
  }
}
```

Available models: `MiniMax-M3`, `MiniMax-M2.7`, `MiniMax-M2.7-highspeed`.

Use the endpoint for your account region and preferred compatible API:

| Region | OpenAI-compatible base URL | Anthropic-compatible base URL |
| --- | --- | --- |
| Global | `https://api.minimax.io/v1` | `https://api.minimax.io/anthropic` |
| China | `https://api.minimaxi.com/v1` | `https://api.minimaxi.com/anthropic` |

For the Anthropic-compatible API, keep `provider` set to `minimax` and pass
the base URL directly without adding `/v1`. Horizon selects its Anthropic
client for this endpoint, and the SDK appends `/v1/messages` when sending a
request:

```json
{
  "ai": {
    "provider": "minimax",
    "model": "MiniMax-M3",
    "api_key_env": "MINIMAX_API_KEY",
    "base_url": "https://api.minimax.io/anthropic",
    "throttle_sec": 0
  }
}
```

**Aliyun DashScope** (OpenAI-compatible):

```json
{
  "ai": {
    "provider": "ali",
    "model": "qwen-plus",
    "api_key_env": "DASHSCOPE_API_KEY",
    "throttle_sec": 0
  }
}
```

Use the [DashScope compatible-mode](https://help.aliyun.com/zh/dashscope/developer-reference/use-dashscope-by-calling-openai-api) endpoint. Set `DASHSCOPE_API_KEY` in your `.env`. Optional: set `base_url` to override the default `https://dashscope.aliyuncs.com/compatible-mode/v1`.

**Ollama**:

```json
{
  "ai": {
    "provider": "ollama",
    "model": "llama3.1",
    "api_key_env": "",
    "base_url": "http://192.168.1.10:11434",
    "throttle_sec": 0
  }
}
```

Omit `base_url` to use the default `http://localhost:11434/v1`.
For remote Ollama servers, set `ai.base_url` in `data/config.json` or set
`HORIZON_OLLAMA_BASE_URL` in `.env`. `OLLAMA_BASE_URL` and `OLLAMA_HOST` are
also recognized. If the value omits `/v1`, Horizon appends it automatically
for Ollama's OpenAI-compatible endpoint.

### Stage-specific AI models

The top-level `ai` fields remain the default for every AI call. Add entries
under `ai.stages` only where a pipeline stage should use a different model or
provider:

| Stage | AI work performed |
| --- | --- |
| `analysis` | Score items, generate the initial summary and tags, and re-analyze expanded Twitter discussions |
| `deduplication` | Detect semantically duplicated stories after score filtering |
| `enrichment` | Extract concepts and generate grounded background and discussion context |
| `translation` | Produce the lightweight Chinese translation used when full enrichment fails |
| `source_recommendation` | Recommend additional sources in the setup wizard |

For example, use a fast model by default and a stronger model only for
background enrichment:

```json
{
  "ai": {
    "provider": "deepseek",
    "model": "deepseek-v4-flash",
    "api_key_env": "DEEPSEEK_API_KEY",
    "temperature": 0.3,
    "max_tokens": 4096,
    "stages": {
      "analysis": {
        "model": "deepseek-v4-flash"
      },
      "deduplication": {
        "model": "deepseek-v4-flash"
      },
      "enrichment": {
        "model": "deepseek-v4-pro"
      },
      "translation": {
        "model": "deepseek-v4-flash"
      },
      "source_recommendation": {
        "model": "deepseek-v4-flash"
      }
    }
  }
}
```

Each stage entry is an override. Fields that are omitted inherit the top-level
AI configuration. A stage can override `provider`, `provider_chain`, `model`,
`base_url`, `api_key_env`, `temperature`, `max_tokens`, `throttle_sec`, and the
analysis or enrichment concurrency settings.

When a stage changes `provider`, Horizon first loads that provider's built-in
model, API-key environment variable, endpoint, and Azure-specific defaults,
then applies the explicit stage values. This prevents credentials or endpoints
from the default provider leaking into another provider. For example:

```json
{
  "ai": {
    "provider": "deepseek",
    "model": "deepseek-v4-flash",
    "api_key_env": "DEEPSEEK_API_KEY",
    "stages": {
      "enrichment": {
        "provider": "ollama",
        "model": "llama3.1"
      }
    }
  }
}
```

`provider_chain` is still automatic failure fallback within a stage; it does
not route different tasks by itself. A stage inherits a top-level chain unless
the stage explicitly sets `"provider_chain": null`. Final Markdown rendering
is programmatic and does not call an AI model.

### AI throttling

If your model has a strict per-minute request cap, you can slow the scorer down in `data/config.json`:

```json
{
  "ai": {
    "throttle_sec": 4.5
  }
}
```

- `throttle_sec`: Pause between scored items in seconds. Default is `0`.
- `4.5` is a reasonable starting point for free-tier models capped around 15 requests per minute.
- Set it back to `0` if you have enough throughput headroom and want maximum speed.

### AI Concurrency

By default, AI scoring and enrichment run one item at a time. If your API endpoint supports concurrent requests, you can increase throughput:

```json
{
  "ai": {
    "analysis_concurrency": 4,
    "enrichment_concurrency": 2
  }
}
```

- `analysis_concurrency`: Number of items scored in parallel. Default is `1`.
- `enrichment_concurrency`: Number of high-scoring items enriched in parallel. Default is `1`.
- Both values are clamped to a minimum of `1`.
- Preserve the existing retry behavior per item.
- Result ordering is preserved regardless of concurrency.
- If you also use `throttle_sec`, each concurrent task sleeps independently after finishing an item.

**Custom Base URL** (for proxies):

```json
{
  "ai": {
    "provider": "anthropic",
    "base_url": "https://your-proxy.com/v1",
    ...
  }
}
```

For OpenAI-compatible gateways, Horizon sends `temperature` by default. If a newer reasoning-style model rejects that parameter with an error such as `temperature is deprecated for this model`, Horizon retries once without it and remembers that capability for later requests.

## Information Sources

All sources are configured under the top-level `sources` key in `config.json`.

### GitHub

```json
{
  "sources": {
    "github": [
      {
        "type": "user_events",
        "username": "gvanrossum",
        "enabled": true,
        "category": "oss"
      },
      {
        "type": "repo_releases",
        "owner": "python",
        "repo": "cpython",
        "enabled": true,
        "category": "oss"
      }
    ]
  }
}
```

### Hacker News

```json
{
  "sources": {
    "hackernews": {
      "enabled": true,
      "fetch_top_stories": 30,
      "min_score": 100,
      "category": "tech"
    }
  }
}
```

### RSS Feeds

```json
{
  "sources": {
    "rss": [
      {
        "name": "Blog Name",
        "url": "https://example.com/feed.xml",
        "enabled": true,
        "category": "ai-ml"
      }
    ]
  }
}
```

### Reddit

Reddit scraping is free and does not require API keys. Subreddit posts and comments prefer `old.reddit.com`; JSON and RSS endpoints are used as fallbacks when needed.

```json
{
  "sources": {
    "reddit": {
      "enabled": true,
      "fetch_comments": 5,
      "subreddits": [
        {
          "subreddit": "MachineLearning",
          "sort": "hot",
          "fetch_limit": 25,
          "min_score": 10,
          "category": "ai-ml"
        }
      ],
      "users": [
        {
          "username": "spez",
          "sort": "new",
          "fetch_limit": 10,
          "category": "social"
        }
      ]
    }
  }
}
```

### Telegram

Telegram scraping uses the public web preview at `https://t.me/s/<channel>`, so no API key is required. Only public channels are supported.

```json
{
  "sources": {
    "telegram": {
      "enabled": true,
      "channels": [
        {
          "channel": "zaihuapd",
          "enabled": true,
          "fetch_limit": 20,
          "category": "ai-news"
        }
      ]
    }
  }
}
```

- `enabled` — enable or disable Telegram fetching globally
- `channels` — list of public Telegram channels to monitor
- `channel` — Telegram channel username only, without `@` or the full `https://t.me/` URL
- `fetch_limit` — maximum number of recent messages to inspect per channel per run (default: `20`)
- `category` — optional tag for balanced digest grouping (e.g., `"ai-news"`, `"finance"`)

### Twitter

Requires an [Apify](https://apify.com) account. Set `APIFY_TOKEN` in your `.env` file. The free tier includes $5/month of credit, enough for roughly 20,000 tweets.

```json
{
  "sources": {
    "twitter": {
      "enabled": true,
      "users": ["karpathy", "ylecun"],
      "fetch_limit": 10,
      "category": "social",
      "fetch_reply_text": false,
      "max_replies_per_tweet": 3,
      "max_tweets_to_expand": 10,
      "reply_min_likes": 5
    }
  }
}
```

- `users` — Twitter screen names to monitor, without the `@` prefix
- `fetch_limit` — maximum tweets to fetch per run (across all users combined; minimum 100 due to actor constraint)
- `category` — optional tag for balanced digest grouping (applies to all tweets from this source)
- `fetch_reply_text` — when `true`, fetch actual reply bodies for important tweets and append them under `--- Top Comments ---` so the AI can factor in community discussion. Disabled by default.
- `max_replies_per_tweet` — maximum reply lines to append per tweet (default: 3)
- `max_tweets_to_expand` — cap on how many tweets get reply expansion per run, to control Apify credit usage (default: 10)
- `reply_min_likes` — only include replies with at least this many likes (default: 0)

The scraper uses the `altimis/scweet` actor by default. You can override it with `actor_id` if needed.

### OpenBB Financial News

OpenBB is useful when you want equity or macro news from providers such as yfinance, Benzinga, FMP, Intrinio, Tiingo, SEC, or Federal Reserve through one SDK.

Install the optional dependency before enabling the source:

```bash
uv sync --extra openbb
```

If your platform struggles to build transitive dependencies, prefer:

```bash
uv pip install --only-binary=:all: openbb openbb-benzinga
```

```json
{
  "sources": {
    "openbb": {
      "enabled": true,
      "watchlists": [
        {
          "name": "megacaps",
          "enabled": true,
          "provider": "yfinance",
          "fetch_limit": 20,
          "category": "equities",
          "symbols": ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]
        }
      ]
    }
  }
}
```

- `enabled` — enable or disable the OpenBB source globally
- `watchlists` — list of named ticker groups; each watchlist becomes one `news.company()` call per run
- `name` — label shown in Horizon metadata and selection breakdowns
- `provider` — OpenBB provider name such as `yfinance` or `benzinga`
- `fetch_limit` — maximum news rows requested for that watchlist
- `category` — optional tag stored on fetched items
- `symbols` — ticker symbols to fetch together; group symbols by provider to keep requests efficient

OpenBB provider credentials are handled by the OpenBB SDK itself, using its own environment variables or user settings. Horizon does not pass those secrets through `data/config.json`.

### Google News

Uses the public Google News RSS search endpoint to fetch recent articles for a query. This is the built-in query-based news source; use normal RSS entries for known publications and the GitHub Trending RSS preset for popular repositories.

```json
{
  "sources": {
    "google_news": {
      "enabled": true,
      "query": "artificial intelligence",
      "language": "en",
      "country": "US",
      "ceid": null,
      "max_results": 100,
      "category": "ai-news"
    }
  }
}
```

- `query` — Google News search expression. Horizon appends the configured time window.
- `language` / `country` — locale used for the RSS request.
- `ceid` — optional Google News edition identifier; defaults to `"{country}:{language}"`.
- `max_results` — maximum number of feed entries accepted per run.
- `category` — optional tag for balanced digest grouping.

No API key is required.

If an existing configuration used `sources.gdelt`, move its query to
`sources.google_news`. For GitHub popularity tracking, use the
`GitHub Trending - Daily` RSS preset instead of a dedicated source block.

## Filtering

Content is scored 0-10:

- **9-10**: Groundbreaking - Major breakthroughs, paradigm shifts
- **7-8**: High Value - Important developments, deep technical content
- **5-6**: Interesting - Worth knowing but not urgent
- **3-4**: Low Priority - Generic or routine content
- **0-2**: Noise - Spam, off-topic, or trivial

```json
{
  "filtering": {
    "ai_score_threshold": 7.0,
    "time_window_hours": 24,
    "max_items": 20,
    "category_groups": {
      "ai": {
        "name": "AI / Machine Learning",
        "limit": 5,
        "categories": ["ai-news", "ai-tools", "machine-learning", "llm"]
      },
      "finance": {
        "name": "Finance",
        "limit": 5,
        "categories": ["finance", "equities", "crypto"]
      }
    },
    "default_group": "other",
    "default_group_limit": 3
  }
}
```

- `ai_score_threshold`: Only include content scoring >= this value
- `time_window_hours`: Fetch content from last N hours
- `max_items`: Optional final cap after all group limits are applied
- `category_groups`: Optional map of quota groups. Each group requires a positive
  `limit` and a non-empty `categories` list. Items within each group are kept by
  AI score, highest first.
- `category_groups.*.name`: Optional display name used in run logs
- `default_group`: Group key for items whose category does not match any
  configured group. Default is `other`.
- `default_group_limit`: Optional positive limit for unmatched items. If omitted,
  unmatched items are unlimited except for `max_items`.

Balanced digest filtering runs after AI score threshold filtering and topic
deduplication, but before enrichment. This reduces enrichment calls to only the
items that can appear in the final digest.

Group matching uses the source category stored in `ContentItem.metadata.category`.
All source types support a `category` field: `sources.rss[].category`,
`sources.github[].category`, `sources.hackernews.category`,
`sources.reddit.subreddits[].category`, `sources.reddit.users[].category`,
`sources.telegram.channels[].category`, `sources.twitter.category`,
`sources.openbb.watchlists[].category`, and `sources.google_news.category`.
Sources without a category set enter the default group.

If the same category appears in multiple groups, Horizon logs a warning and uses
the first group in configuration order. Omitting both `category_groups` and
`max_items` preserves the previous filtering behavior.

## Parallel Domain Pipelines

Horizon can split the shared fetched and URL-deduplicated item set into
independent news domains. Each enabled domain runs analysis, score filtering,
topic deduplication, balancing, enrichment, and summary generation as an
isolated pipeline. A failure in one domain does not discard successful sibling
digests.

```json
{
  "ai": {
    "analysis_concurrency": 2,
    "enrichment_concurrency": 2,
    "total_concurrency": 4,
    "search_concurrency": 3
  },
  "domain_concurrency": 3,
  "domains": {
    "ai": {
      "name": "AI News",
      "categories": ["ai-news", "ai-tools", "machine-learning", "llm"],
      "score_threshold": 7.0,
      "max_items": 10,
      "languages": ["en", "zh"],
      "analysis_guidance": "Prioritize material model, research, and infrastructure changes.",
      "enrichment_guidance": "Explain technical tradeoffs and ecosystem impact."
    },
    "economy": {
      "name": "Economy",
      "categories": ["economy", "finance", "equities", "crypto"]
    },
    "entertainment": {
      "name": "Entertainment",
      "categories": ["entertainment", "movies", "music", "gaming"]
    },
    "general": {
      "name": "General News",
      "categories": [],
      "default": true
    }
  }
}
```

- `domains`: Optional map keyed by a filesystem-safe domain identifier. If this
  map is omitted or empty, Horizon keeps the original single serial pipeline.
- `domains.*.categories`: Source categories routed to the domain. A category may
  appear in multiple domains; Horizon deep-copies the item so the pipelines can
  enrich it independently.
- `domains.*.default`: Exactly one enabled domain must be the default. Items with
  a missing or unmatched category are sent there, so routing never silently
  drops content.
- `domains.*.score_threshold` and `domains.*.max_items`: Optional per-domain
  overrides. Omitted values inherit `filtering.ai_score_threshold` and
  `filtering.max_items`.
- `domains.*.languages`: Optional per-domain output languages. Omitted values
  inherit `ai.languages`.
- `domains.*.analysis_guidance` and `domains.*.enrichment_guidance`: Optional
  instructions appended to that domain's AI prompts.
- `domain_concurrency`: Maximum number of domain pipelines running at once.
- `ai.total_concurrency`: Shared upper bound for in-flight AI requests across
  all domains. If omitted, Horizon uses the larger of `analysis_concurrency` and
  `enrichment_concurrency`.
- `ai.search_concurrency`: Shared upper bound for enrichment web searches across
  all domains.

Source fetching and exact URL deduplication still happen once before routing.
Domain routing uses `ContentItem.metadata.category`, populated from each
source's `category` setting. Topic deduplication remains domain-local, which
allows the same story to be selected independently for different audiences.

Domain summaries use isolated filenames such as
`data/summaries/horizon-2026-07-22-ai-en.md`. When GitHub Pages is enabled, the
corresponding post is `docs/_posts/2026-07-22-summary-ai-en.md`. Email subjects
and webhook titles also include the domain display name.

## Environment Variable Substitution

Any string value in `data/config.json` supports `${VAR_NAME}` syntax. Variables are expanded at runtime from the environment (including values loaded from `.env`). This lets you keep secrets, tenant-specific endpoints, and private URLs out of the checked-in JSON file.

Example:

```json
{
  "ai": {
    "base_url": "${HORIZON_AI_BASE_URL}"
  },
  "sources": {
    "rss": [
      {
        "name": "LWN.net",
        "url": "https://lwn.net/headlines/full_text?key=${LWN_KEY}",
        "enabled": true
      }
    ]
  },
  "webhook": {
    "url_env": "HORIZON_WEBHOOK_URL",
    "headers": "Authorization: Bearer ${HORIZON_WEBHOOK_TOKEN}"
  }
}
```

- `${NAME}` is replaced only when `NAME` is a valid identifier like `LWN_KEY` or `HORIZON_AI_BASE_URL`.
- Unset variables are left as `${NAME}` instead of becoming an empty string, so configuration mistakes fail loudly downstream.
- Expansion is recursive through dicts, lists, and tuples; non-string values are left unchanged.

## Email Delivery

Email delivery is optional and disabled unless `email.enabled` is `true`. Horizon sends summaries over SMTP to the fixed recipient list in the configuration.

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.qq.com",
    "smtp_port": 465,
    "smtp_username": null,
    "email_address": "xxx@qq.com",
    "recipients": ["reader@example.com"],
    "password_env": "EMAIL_PASSWORD",
    "sender_name": "Horizon Daily"
  }
}
```

- `enabled`: Turns daily email delivery on or off.
- `smtp_server` / `smtp_port`: SMTP server used to send emails.
- `smtp_username`: Optional SMTP login username. If omitted, Horizon uses `email_address`.
- `email_address`: Sender email address and default SMTP login username.
- `recipients`: Fixed list of recipient email addresses.
- `password_env`: Environment variable containing the email password or app password. Defaults to `EMAIL_PASSWORD`.
- `sender_name`: Display name shown in sent emails.

Resend SMTP example:

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.resend.com",
    "smtp_port": 465,
    "smtp_username": "resend",
    "password_env": "RESEND_API_KEY",
    "email_address": "noreply@example.com",
    "recipients": ["reader@example.com"],
    "sender_name": "Horizon Daily"
  }
}
```

Set `RESEND_API_KEY` in `.env`. Add every destination address to `email.recipients`.

When migrating from an older configuration, copy the addresses from
`data/subscribers.json` into `email.recipients`, then remove the legacy IMAP
and subscribe/unsubscribe fields. Horizon no longer reads the mailbox or the
subscriber file.

## Webhook Notification

Webhook notification is optional and disabled unless `webhook.enabled` is `true`. Horizon can call Feishu/Lark, DingTalk, Slack, Discord, or any custom webhook endpoint when the pipeline succeeds or fails.

```json
{
  "webhook": {
    "enabled": true,
    "url_env": "HORIZON_WEBHOOK_URL",
    "delivery": "summary",
    "overview_position": "first",
    "platform": "generic",
    "layout": "markdown",
    "languages": null,
    "request_body": {
      "text": "#{message_title}\n#{summary}"
    },
    "headers": ""
  }
}
```

- `enabled`: Turns webhook delivery on or off. The default is `false`.
- `url_env`: Environment variable that contains the webhook URL. For example, set `HORIZON_WEBHOOK_URL=https://...` in `.env`.
- `delivery`: Controls how messages are sent. Use `summary` for one full message, or `summary_and_items` for one overview message followed by one message per selected item.
- `overview_position`: Controls where the overview is sent in `summary_and_items` mode. Use `first` for the traditional order, or `last` to send item details in reverse and keep the overview as the newest chat message.
- `platform`: Optional webhook platform hint. Use `generic` by default, or `feishu` / `lark` to enable platform-specific card rendering.
- `layout`: Controls the message layout. Use `markdown` for templated Markdown delivery, or `collapsible` with `platform: "feishu"` / `"lark"` for a single Feishu Card JSON 2.0 message with each item in a collapsed panel.
- `languages`: Optional webhook-only language filter. Use `["zh"]` or `["en"]` to send only selected languages; use `null` or omit it to send all configured `ai.languages`.
- `request_body`: Optional request body. If empty, Horizon sends a `GET` request. If provided, Horizon sends a `POST` request.
- `headers`: Optional custom headers, one `Key: Value` pair per line.

When `request_body` is a JSON object or array, Horizon renders placeholders and serializes it as JSON. When it is a string, Horizon renders it directly and detects JSON if the rendered string is valid JSON.

### Delivery Modes And Layouts

`delivery` controls how many webhook messages Horizon sends:

- `summary`: Sends one message containing the full daily summary. This is simple, but some chat platforms may reject long messages.
- `summary_and_items`: Sends one overview message plus one message per selected item. In each item message, `#{summary}` contains only that item's Markdown body. This is useful for platforms that reject or truncate long messages.

`layout` controls how each message is rendered:

- `markdown`: Uses your `request_body` template for each message. This is the default and works with generic webhooks, DingTalk, Slack, Discord, Feishu, and Lark.
- `collapsible`: Currently supported for `platform: "feishu"` or `"lark"`. Horizon ignores `request_body` and builds one Feishu/Lark Card JSON 2.0 message with each item in a collapsed panel.

For platforms without a platform-specific layout, keep `layout: "markdown"` and choose the message count with `delivery`.

Example `summary_and_items` Markdown delivery config:

```json
{
  "webhook": {
    "enabled": true,
    "url_env": "HORIZON_WEBHOOK_URL",
    "delivery": "summary_and_items",
    "overview_position": "last",
    "platform": "generic",
    "layout": "markdown",
    "request_body": {
      "text": "#{message_title}\n\n#{summary?limit=3000&split=---}"
    }
  }
}
```

With `summary_and_items`, Horizon sends one overview plus one message per selected item. `overview_position: "last"` sends item messages first and keeps the overview as the newest chat message; omit it or set `"first"` to send the overview first.

### Webhook Templates

Available variables:

| Variable | Description |
|----------|-------------|
| `#{date}` | Report date, for example `2026-04-24` |
| `#{language}` | Language code, such as `en` or `zh` |
| `#{important_items}` | Number of items that passed the score threshold |
| `#{all_items}` | Total number of fetched items |
| `#{result}` | `success` or `failed` |
| `#{timestamp}` | Unix timestamp |
| `#{message_title}` | Message title, such as the daily title, overview title, or item title |
| `#{message_kind}` | Message kind: `summary`, `overview`, `item`, `failure`, or `manual` |
| `#{summary}` | Message Markdown. In `summary_and_items` mode this is the overview or one item body, depending on the message |

When `delivery` is `summary_and_items`, item messages also include:

| Variable | Description |
|----------|-------------|
| `#{item_index}` | 1-based item number |
| `#{item_count}` | Total number of item messages |
| `#{item_title}` | Current item title |
| `#{item_url}` | Current item URL |
| `#{item_score}` | Current item AI score |

For webhook delivery, Horizon flattens HTML disclosure blocks such as `<details><summary>...</summary>` in `#{summary}` into plain Markdown link lists. This makes the generated summary easier to render in chat products. Saved Markdown files, GitHub Pages, and email content are unchanged.

Use `#{key?limit=N&split=DELIM}` to truncate long values by splitting on `DELIM` and keeping segments until the total character count reaches `N`.

```text
#{summary?limit=3000&split=---}
```

### DingTalk

In DingTalk, create a custom group robot and use a custom keyword such as `Horizon`. The keyword must appear in the body content.

```json
{
  "msgtype": "markdown",
  "markdown": {
    "title": "Horizon #{date} Daily",
    "text": "Horizon result: #{result}\n\nHorizon important items: #{important_items}/#{all_items}\n\n#{summary}"
  }
}
```

### Feishu / Lark

In Feishu or Lark, create a custom group robot and use a custom keyword such as `Horizon`. The keyword must appear in the body content.

Use Card JSON 2.0 for Markdown rendering. The card must include `"schema": "2.0"` and put rich-text Markdown components under `card.body.elements`.

To keep the group chat compact while still allowing readers to browse the full briefing inside Feishu, use the collapsible layout:

```json
{
  "webhook": {
    "enabled": true,
    "url_env": "HORIZON_WEBHOOK_URL",
    "platform": "feishu",
    "layout": "collapsible",
    "languages": ["zh"]
  }
}
```

With this layout, Horizon sends one interactive card containing the overview and one collapsed panel per selected item. Each panel can be expanded in Feishu to read the full item detail. The regular `request_body` template is ignored for this rendered card.

```json
{
  "msg_type": "interactive",
  "card": {
    "schema": "2.0",
    "config": {
      "wide_screen_mode": true
    },
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "#{message_title}"
      },
      "template": "blue"
    },
    "body": {
      "elements": [
        {
          "tag": "markdown",
          "content": "Horizon result: #{result}\nHorizon important items: #{important_items}/#{all_items}"
        },
        {
          "tag": "hr"
        },
        {
          "tag": "markdown",
          "content": "#{summary}"
        }
      ]
    }
  }
}
```

## Static Site

Horizon always writes generated summaries to `data/summaries/`. GitHub Pages output is opt-in and disabled by default. Enable it to also copy publishable Markdown into `docs/_posts/`:

```json
{
  "github_pages": {
    "enabled": true
  }
}
```

The repository workflow in `.github/workflows/daily-summary.yml` uses `data/config.github.json`, which enables this setting.

To publish the site, enable Pages for the repository and run the scheduled workflow or trigger it manually. The generated site is built from the `docs/` directory.

## Performance Metrics

Every native `horizon` run writes a structured JSON report to `data/metrics/`, including runs that return no content or fail after the orchestrator starts. Each report contains:

- total run status, UTC timestamps, monotonic-clock duration, and Token usage;
- pipeline-stage durations, statuses, input/output item counts, safe attributes, and per-provider Token deltas;
- individual source-fetch durations, statuses, and output item counts.
- when domains are configured, per-domain stage durations and domain outcomes,
  including isolated failures and selected item counts.

Because domain stages overlap, their individual token fields remain zero to
avoid double-counting shared process-wide usage. The enclosing
`process_domains` stage and run total contain the aggregate Token delta.

Metric filenames contain a UTC timestamp and random suffix, for example `horizon-performance-20260722T020000Z-a1b2c3d4.json`. Runtime reports are ignored by Git. The bundled GitHub Actions workflow uploads them after every run as a `horizon-performance-<run-id>` artifact with 14-day retention, including when the Horizon step fails.

## MCP Server

Horizon includes an MCP server for AI assistants and MCP-compatible clients.

```bash
uv run horizon-mcp
```

Available tools include `hz_validate_config`, `hz_fetch_items`, `hz_score_items`, `hz_filter_items`, `hz_enrich_items`, `hz_generate_summary`, and `hz_run_pipeline`.

See [`src/mcp/README.md`](../src/mcp/README.md) for the full tool reference and [`src/mcp/integration.md`](../src/mcp/integration.md) for client setup.
