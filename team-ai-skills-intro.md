---
title: 團隊 AI Skills 共享平台介紹
date: 2026-04-11
tags:
  - ai-skills
  - team-tooling
  - onboarding
aliases:
  - AI 技能安裝指南
  - Skills 平台介紹
---

# 🧰 團隊 AI Skills 共享平台

> 一個 Git Repo，讓全團隊的 AI 開發助手都擁有相同的超能力。

---

## 🎯 這是什麼？為什麼需要它？

我們團隊同時使用 **Claude Code** 和 **Cline** 兩種 AI coding agent。但 AI agent 出廠只有通用能力——它不知道怎麼查我們的 ADO 工單、不懂怎麼 review 我們的 PR、也無法分析我們的 VB6 舊系統。

**AI Skills** 就是讓 AI agent 學會這些「團隊專屬能力」的方式。

| 沒有 Skills | 有 Skills |
|:---:|:---:|
| ❌ AI 不知道怎麼查 ADO 工單 | ✅ 「幫我查 #12345 工單」直接回答 |
| ❌ 每個人自己教 AI 一遍 | ✅ 裝好就有，全團隊一致 |
| ❌ 好用的 prompt 只在個人電腦 | ✅ 統一版控，`git pull` 就能更新 |
| ❌ 新人不知道 AI 能幹嘛 | ✅ 安裝器自動列出可用技能 |

> 💡 **一句話總結**：`git clone` → 說「幫我安裝技能」→ AI 自動引導你裝好所有團隊技能。

---

## 📦 專案結構總覽

```
clinewithADO/
├── 📁 Skills/                  ← 團隊技能倉庫（所有技能的原始碼）
│   ├── ado-devops/             ← ADO 工單/PR/Repo 操作
│   ├── ado-pr-review/          ← AI Code Review
│   ├── legacy-code-analyzer/   ← 舊系統分析
│   ├── superpowers-plugin/     ← Superpowers 離線安裝包
│   └── ...（共 13+ 個技能）
│
├── 📁 .claude/skills/
│   └── team-skill-installer/   ← 🔧 一鍵安裝引導技能
│       ├── SKILL.md            ← 安裝流程定義
│       └── scripts/            ← 安裝腳本（Python 跨平台）
│
└── 📁 Docker/                  ← Cline + ADO MCP Docker 方案
```

安裝後，技能會被複製到家目錄：

```
~/.claude/skills/<技能名稱>/    ← Claude Code 讀取
~/.cline/skills/<技能名稱>/     ← Cline 讀取
```

> 📌 放在家目錄下，**不管開哪個專案都有效**，不會汙染個別專案。

---

## 🛠️ 可安裝的技能一覽

### 🏢 ADO 整合系列（使用 Azure DevOps 的團隊必裝）

| 技能 | 說明 | 推薦 |
|:---|:---|:---:|
| **ado-devops** | 查工單、看 PR、管 Repo、搜 Wiki — ADO 全方位操作 | ⭐ 必裝 |
| **ado-pr-review** | AI 自動 Code Review，在 ADO PR 上留 inline 意見 | ⭐ 推薦 |
| **ado-pr-knowledge** | 從歷史 PR review 提煉團隊 Code Review 規則 | ⭐ 推薦 |

### 🔧 開發流程系列

| 技能 | 說明 | 推薦 |
|:---|:---|:---:|
| **superpowers-workflow** | 完整開發流程整合：brainstorming → 計畫 → 實作 → review | ⭐ 推薦 |
| **kiro-skill** | 互動式需求釐清 → 設計文件 → 任務清單 | ⭐ 推薦 |
| **bmad-method** | 多代理人開發框架（PM / Architect / Dev 角色分工） | 🔬 進階 |
| **spec-kit-skill** | GitHub Spec-Kit 憲章驅動開發（9 個子指令） | 🔬 進階 |

### 🏗️ 舊系統與特定領域

| 技能 | 說明 | 推薦 |
|:---|:---|:---:|
| **legacy-code-analyzer** | VB6 / C# / VB.NET 舊系統深度分析與報告 | ⭐ 推薦 |
| **npe-guardian** | Java NullPointerException 偵測與修復 | 🎯 Java 專案 |
| **prometheus** | 自然語言查 Prometheus 指標 | 🎯 K8s 環境 |

### ✍️ 文件與工具

| 技能 | 說明 | 推薦 |
|:---|:---|:---:|
| **tech-article-writer** | 繁體中文科技文章 / AI 教學文撰寫 | ⭐ 推薦 |
| **skill-creator** | 開發並測試新的 AI 技能 | 🔬 進階 |
| **skill-manual-writer** | 為技能自動產生操作手冊 | 🔬 進階 |

### ⚡ 基礎套件（建議全裝）

| 套件 | 說明 |
|:---|:---|
| **Superpowers** | AI 進階工作流程插件 — brainstorming、TDD、debugging、計畫撰寫等結構化開發流程，讓 AI 先思考再動手 |
| **OpenSpec** | 規格驅動開發框架 — 提案 → 規格 → 設計 → 任務清單，中大型功能開發必備 |

---

## 🚀 安裝方式：三步完成

### Step 1：Clone 專案

```bash
git clone <repo-url>
cd clinewithADO
```

### Step 2：開啟 AI Agent

打開 **Claude Code** 或 **Cline**，確認工作目錄在 `clinewithADO/`。

### Step 3：跟 AI 說話

> 「幫我安裝技能」

AI 會自動觸發 **team-skill-installer**，引導你完成：

1. ✅ 環境檢查（Python、Node.js）
2. ✅ 安裝基礎套件（Superpowers、OpenSpec）
3. ✅ 展示可用技能清單，讓你選擇要裝哪些
4. ✅ 一鍵安裝到 `~/.claude/skills/` 和 `~/.cline/skills/`
5. ✅ 顯示安裝摘要

> 💡 之後要更新或刪除技能，只要說「管理技能」或「更新技能」即可。

---

## 🔄 更新技能

當 repo 有新版本的技能時：

```bash
git pull
```

然後跟 AI 說「更新技能」，安裝器會自動比對版本差異，只更新有變動的技能。

---

## 🏗️ 架構設計理念

```
┌──────────────────────────────────────────────┐
│              Git Repo (版控中心)               │
│                                              │
│  Skills/           ← 技能原始碼（團隊共用）     │
│  .claude/skills/   ← 安裝器（自動觸發）         │
└──────────────┬───────────────────────────────┘
               │  git clone / git pull
               ▼
┌──────────────────────────────────────────────┐
│            同事的電腦                          │
│                                              │
│  ~/.claude/skills/  ← Claude Code 讀取        │
│  ~/.cline/skills/   ← Cline 讀取              │
│  ~/.claude/plugins/ ← Superpowers plugin      │
└──────────────────────────────────────────────┘
```

### 為什麼這樣設計？

| 設計決策 | 原因 |
|:---|:---|
| **離線安裝** | 公司內網可能無法存取外部 plugin marketplace |
| **Python 腳本** | 跨平台（Windows + macOS），團隊已有 Python 環境 |
| **雙路徑安裝** | 部分 Cline 版本不讀 `~/.claude/skills/`，需分開放 |
| **扁平結構** | Cline 只讀第一層子目錄，不支援巢狀 |
| **安裝前備份** | 更新時先備份舊版，降低風險 |
| **Git 版控** | 技能可追蹤變更歷史，`git pull` 即可同步最新版 |

---

## ❓ 常見問題

### Q：我只用 Claude Code，不用 Cline，需要裝嗎？
裝。安裝器會同時安裝到兩個路徑，不影響你的使用，但如果哪天你想試 Cline 就不用重裝。

### Q：我的 Windows 電腦可以用嗎？
可以。所有安裝腳本用 Python 3 撰寫，Windows / macOS / Linux 都能跑。

### Q：安裝完要重啟 IDE 嗎？
- **Claude Code**：Superpowers plugin 需要重啟才生效，技能不需要
- **Cline**：不需要重啟

### Q：技能會不會影響到我其他專案？
不會。技能只是給 AI agent 的「說明書」，告訴 AI 遇到特定情境該怎麼做。不會修改你的程式碼或專案設定。

### Q：我可以自己開發新技能嗎？
可以！安裝 **skill-creator** 技能後，跟 AI 說「幫我建一個新技能」就能開始。開發完放到 `Skills/` 目錄、發 PR，review 通過後全團隊就能用。

---

## 📊 效益總結

| 面向 | 效果 |
|:---|:---|
| ⏱️ **效率** | 新人 10 分鐘內裝好所有 AI 技能，立刻上手 |
| 🔄 **一致性** | 全團隊的 AI 能力統一，不會有人少裝、裝錯版本 |
| 📈 **可擴展** | 新技能放進 `Skills/`、發 PR，merge 後全團隊自動可用 |
| 🔒 **安全** | 離線安裝、不依賴外部服務、技能內容全部可 review |
| 🤝 **協作** | 誰有好用的 AI 工作流，包成 skill 分享給全組 |

---

> 🎉 **開始使用**：Clone 這個 repo，打開 AI agent，說「幫我安裝技能」。就這麼簡單。
