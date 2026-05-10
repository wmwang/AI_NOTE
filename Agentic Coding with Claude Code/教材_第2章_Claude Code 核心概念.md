# Claude Code 的核心工作方式：從零建立專案到 Spec-Driven Design

第二章不急著教你高級技巧，它的目標是讓你真正理解 Claude Code 是怎麼運作的——它怎麼觀察專案、怎麼建立 context、怎麼在你和程式碼之間扮演主動角色。本章以一個叫做 **HookHub** 的 Next.js 專案作為貫穿全書的範例，從安裝到第一次實作，一步步走過去。

---

## 安裝 Claude Code

在開始之前，確認你的機器已經安裝 Claude Code。

Claude Code 現在提供原生安裝程式，會自動偵測作業系統並安裝對應版本。照官方安裝指南操作。

安裝完成後，執行以下指令確認：

```bash
claude --version
```

> Windows 使用者請在 **WSL（Windows Subsystem for Linux）** 或等效的 Unix-like shell 環境中執行。這樣才能讓 `npx`、`npm`、`claude` 等指令行為一致。

---

## 建立 Next.js 專案

### 用指令建立專案

```bash
npx create-next-app@latest
```

執行後，選擇預設選項繼續。如果遇到權限錯誤，改用 `sudo` 執行：

```bash
sudo npx create-next-app@latest
```

安裝完成後，進入專案目錄：

```bash
cd hookhub
```

啟動開發伺服器：

```bash
npm run dev
```

開啟瀏覽器，前往 `http://localhost:3000`，你應該會看到 Next.js 預設的起始頁面。

---

## 初始化 Claude Code

### 執行 `/init`

Next.js 專案跑起來之後，回到 Claude Code，執行 `/init` 指令。

這個指令的作用是：**讓 Claude 掃描專案，理解它的結構、技術棧、主要檔案，然後自動生成 `CLAUDE.md`**。

Claude 執行 `/init` 時會：
1. 分析 repository 的目錄結構
2. 讀取主要檔案內容
3. 識別技術棧與框架
4. 將這些資訊整理成 `CLAUDE.md` 的草稿

### 生成的 CLAUDE.md 長什麼樣

`/init` 完成後，Claude 會請求你的許可來寫入檔案。**這個許可流程很重要**——保持對每次寫入的控制，是安全 agentic coding 的基本原則。

選擇 **Yes**，讓 Claude 完成 `CLAUDE.md` 的建立。

生成的 `CLAUDE.md` 包含：

| 項目 | 內容 |
|------|------|
| 專案目標 | 這個專案要解決什麼問題 |
| 商業問題 | 專案的使用情境 |
| 執行方式 | 怎麼啟動、怎麼 build |
| 技術框架 | Next.js、TypeScript、Tailwind 等 |
| 目錄結構 | 主要資料夾和檔案的說明 |

```markdown
## Essential Commands
```bash
# Development
npm run dev       # Start development server on http://localhost:3000

# Production
npm run build     # Create production build
npm run start     # Start production server

# Code Quality
npm run lint      # Run ESLint
```
```

> 從這個時間點開始，每次你送 prompt 給 Claude Code，它都會先載入相關的 `CLAUDE.md` 檔案。這些檔案會隨著專案演進而動態更新。當有重大改變時，可以再次執行 `/init`，或手動新增額外的 `CLAUDE.md`。

---

## 連接 Playwright MCP

### 什麼是 MCP

**Model Context Protocol（MCP）** 是讓 Claude Code 連接外部工具的機制。你可以把它想成：**替 Claude 安裝外掛**，讓它獲得原本沒有的能力。

Playwright MCP 給了 Claude Code **瀏覽器自動化**的能力——可以打開網頁、操作 UI、截圖，這在測試使用者介面時非常有用。

### 安裝 Playwright MCP

```bash
# 只在這個專案
claude mcp add playwright npx @playwright/mcp@latest

# 在你所有的專案都生效（user scope）
claude mcp add playwright npx @playwright/mcp@latest -s user
```

### 驗證 MCP 是否連線

在 Claude Code 中輸入 `/mcp`，按 Enter，你應該會看到類似：

```
Manage MCP servers

1. playwright  ✓ connected · Enter to view details
```

### 測試 Playwright MCP

在 Claude Code 輸入：

```
open browser and add cnn.com
```

Claude 會請求許可，使用 Playwright 工具導航到 URL。選 Yes，瀏覽器就會自動打開。這是**外部工具**，不是 Claude Code 的內建工具——內建工具是指編輯檔案、建立檔案、刪除檔案這類操作。

---

## 用 Cursor Rules 擴充 Context

### cursor.directory 是什麼

除了 `CLAUDE.md`，你還可以用 **Cursor rules** 給 Claude 更豐富的 context。

`cursor.directory` 收集了大量針對不同技術棧的 Markdown 規則檔，讓 AI coding assistant 扮演更精準的角色——例如：「你是一位精通 Next.js、TypeScript、React 的資深前端工程師」。

這些 Cursor rules 同樣適用於 Claude Code。

### 建立 memory 目錄結構

在專案中建立一個 `memory` 目錄，並在裡面建立 `frontend` 子目錄：

```
memory/
├── frontend/
│   └── CLAUDE.md    ← 貼入你從 cursor.directory 複製的 Next.js rule
└── spec/
    └── CLAUDE.md    ← 之後放 spec 文件
```

在 `memory/frontend/CLAUDE.md` 裡貼入類似這樣的 persona：

```markdown
You are a Senior Front-End Developer and an expert in React, Next.js, JavaScript, TypeScript, HTML, CSS...
```

### 重要：memory 檔案不會自動載入

這個設計是刻意的。Claude Code 預設只會自動載入特定位置的 `CLAUDE.md`，**memory 目錄裡的檔案不會自動讀取**。

你可以根據需要**明確告訴 Claude 什麼時候要載入這些 context**——例如在做前端 UI 工作時才載入 frontend context，而不是讓它一直佔用 context window。

---

## Spec-Driven Design：不要 Vibe Coding

### 什麼是 Spec-Driven Design

本章最核心的概念之一：**在寫任何程式碼之前，先讓 Claude 幫你寫一份 spec（規格文件）**。

Vibe coding 的問題是：你沒有明確的需求，Claude 靠感覺生成程式碼，每次結果都可能不一樣，品質不穩定。

**Spec-driven design 的邏輯：**
1. 先產生 spec 文件，描述應用程式、使用情境、非功能需求
2. 在 prompt 裡告訴 Claude 去參考這份 spec 文件
3. Claude 用 spec 最佳化 context window，生成更一致、更高品質的程式碼

### 用 Plan Mode 生成 Spec

按 `Shift + Tab` 切換到 **Plan Mode**。Plan Mode 讓 Claude 只使用唯讀工具——不寫入、不修改任何檔案——先研究再規劃。

送出需求描述，例如：

```
I want you to help me write a spec file for a project I am building.
It's a hub for browsing open-source Claude hooks.
This is an MVP with display-only functionality.
The main page should display hooks in a grid view.
```

Claude 開始研究，然後提出一份計畫，包含：
- 專案概覽與 MVP scope
- Hook 的資料模型（名稱、分類、描述、repo 連結）
- UI/UX 需求
- 技術架構
- User stories

### 把 Spec 存成 CLAUDE.md

批准計畫後，告訴 Claude 把 spec 寫進 spec 目錄：

```
write it into memory/spec/CLAUDE.md
```

這份 spec 文件的存在，讓 Claude 在後續實作時有明確的參考依據。

---

## 實作主頁：讓 Spec 驅動程式碼

### 管理 Context Window

在實作之前，先處理 context 污染的問題。每次對話的來回都在累積 context，當 context 塞滿，Claude 的輸出品質就會下降。

最直接的做法：用 `/clear` 清除對話歷史，讓 context 乾淨。

### 用 `@` 引用 Spec 文件

開新 session 後，送出 prompt 時用 `@` 符號引用 spec 文件：

```
Can you please help me implement the main page grid as specified in @memory/spec/CLAUDE.md?
```

這樣 Claude 就能把 spec 文件的內容納入 context，照著規格實作。

### 執行實作

Claude 開始工作：
1. 建立 to-do list
2. 依序執行每個任務
3. 生成元件檔案
4. 跑 linting 確認沒有 error
5. 輸出實作摘要

---

## 最終專案結構

完成本章所有步驟後，你的專案結構應該如下：

```
hookhub/
├── app/
├── components/
├── memory/
│   ├── frontend/
│   │   └── CLAUDE.md
│   └── spec/
│       └── CLAUDE.md
├── CLAUDE.md
├── package.json
└── ...
```

---

## 本章重點整理

| 概念 | 核心要點 |
|------|---------|
| **`/init`** | 讓 Claude 掃描專案、自動生成 `CLAUDE.md`，建立 context 基礎 |
| **許可系統** | 每次檔案寫入都要你批准，是安全 agentic coding 的基本保障 |
| **MCP** | 外部工具的連接機制，例如 Playwright 給了 Claude 瀏覽器自動化能力 |
| **memory 目錄** | 存放長期 context 的地方，不自動載入，需要明確引用 |
| **Spec-Driven Design** | 先讓 Claude 生成規格文件，再用規格文件驅動實作，提升一致性與品質 |
| **Plan Mode** | 唯讀模式，先研究和規劃，不寫入任何檔案 |

**三個立即可以做的事：**

1. 在你下一個專案的第一步執行 `/init`，讓 Claude 自動建立 `CLAUDE.md`，而不是手動從頭填寫
2. 試試 Playwright MCP——安裝後，讓 Claude 打開你自己的網站做基本的 UI 驗證
3. 在開始任何新功能前，先用 Plan Mode 讓 Claude 幫你寫 spec，不要直接跳進 vibe coding
