# Chapter 4：用 MCP Server 幫 Claude Code 裝外掛

Claude Code 預設只能讀寫你本機的檔案、執行終端機指令。但如果你想讓它直接開瀏覽器測試 UI、操作 GitHub PR、或是查最新的函式庫文件，光靠預設能力是不夠的。這就是 MCP（Model Context Protocol）存在的原因——讓 Claude Code 能連接到外部服務，大幅擴充它能做到的事。

---

## MCP 是什麼？一句話講清楚

MCP，全名 Model Context Protocol，是 Anthropic 制定的一套標準協定，讓 AI 可以連接外部服務。

最直白的比喻：**MCP server 就像是給 Claude Code 安裝外掛（plugin）**。Claude Code 本身沒辦法開瀏覽器，但裝了 Playwright MCP server 之後，它就可以了。Claude Code 預設不認識你的 GitHub，但裝了 GitHub MCP server，它就能幫你開 PR、讀 issue、做 code review。

說白了，MCP 解決的問題就是：**Claude 很聰明，但它需要「手」才能觸碰外部世界**。

---

## MCP 的架構：三個角色

理解 MCP 架構不需要看論文，只要記住三個角色：

- **MCP Client**：就是 Claude Code 本身。它負責呼叫 MCP server，把工具用起來。
- **MCP Server**：一個獨立的程式，可以跑在你本機，也可以是遠端服務。它負責實際跟外部系統溝通（瀏覽器、資料庫、Slack、GitHub 等）。
- **傳輸層**：Client 跟 Server 之間用 JSON-RPC 格式溝通，支援三種傳輸方式：

| 傳輸方式 | 適合場景 | 說明 |
|----------|----------|------|
| `stdio` | 本機 server | 最常見，Claude Code 直接用子程序啟動 server |
| `HTTP + SSE` | 遠端 server | Server 跑在別台機器，用 HTTP 連線 |
| `WebSocket` | 雙向即時溝通 | 需要持續互動的場景 |

大多數情況你用的都是 `stdio`——裝好 MCP server 後，Claude Code 會自動幫你啟動那個程式，你不用管傳輸細節。

---

## 怎麼安裝 MCP Server

### 方法一：用 CLI 直接加

最簡單的方式是用 `claude mcp add` 指令：

```bash
# 基本格式
claude mcp add <name> <command>

# 例：安裝 Context7（查函式庫最新文件用）
claude mcp add context7 npx @upstash/context7-mcp

# 例：安裝 Playwright MCP（瀏覽器自動化）
claude mcp add playwright npx @playwright/mcp@latest
```

### Scope 選項：這個 server 要裝給誰用？

安裝時可以用 `-s` 指定範圍，這個選擇很重要：

```bash
# user scope：裝給你個人所有專案用（預設）
claude mcp add -s user context7 npx @upstash/context7-mcp

# project scope：只給當前專案用，設定存到 .mcp.json，可以 commit 讓團隊共享
claude mcp add -s project playwright npx @playwright/mcp@latest

# local scope：只在本機跑，不會進 .mcp.json，適合測試用
claude mcp add -s local my-test-server npx my-server
```

如果你想讓整個團隊都用同一組 MCP server，就用 `-s project`，然後把 `.mcp.json` commit 進 git。這樣新人 clone 專案後，環境就自動一致了。

### 方法二：用 `/mcp` 指令管理

在 Claude Code 的對話框裡輸入 `/mcp`，會顯示目前安裝的所有 MCP server 狀態，也可以從這裡管理。這個方式比較適合快速確認現在裝了哪些東西。

---

## 三個你該認識的 MCP Server

### 1. Playwright MCP：讓 Claude 幫你測試 UI

裝了 Playwright MCP 之後，Claude Code 可以直接開瀏覽器操作網頁。最實用的場景：

- 叫 Claude 幫你寫 E2E 測試，它可以自己打開瀏覽器確認行為
- 讓 Claude 抓網頁內容、截圖
- 測試你的前端改動有沒有跑壞介面

```bash
claude mcp add -s project playwright npx @playwright/mcp@latest
```

裝好後，你可以直接告訴 Claude：「幫我打開 http://localhost:3000，確認登入流程是否正常」，它就會自己操作瀏覽器做測試。

### 2. GitHub MCP：讓 Claude 直接操作 GitHub

這個 server 讓 Claude Code 可以操作你的 GitHub repo，包括：

- 讀取和建立 issue
- 開 PR、review 程式碼
- 查 commit 歷史

```bash
# 需要先設 GitHub token
export GITHUB_TOKEN=your_github_token

claude mcp add -s user github npx @modelcontextprotocol/server-github
```

### 3. Context7：解決 Claude 用過時 API 的問題

這是最多人第一個裝的 MCP server，因為它解決了一個非常常見的痛點：**Claude 的訓練資料有截止日期，它背的函式庫 API 可能已經過時了**。

裝了 Context7 之後，你問問題時加上 `use context7`，Claude 就會先去查那個函式庫的最新官方文件，再回答你。不再用三個月前就 deprecated 的 API 了。

```bash
claude mcp add -s user context7 npx @upstash/context7-mcp
```

實際使用範例：

```
# 不加 context7（可能拿到舊的 API）
你：幫我用 Next.js 寫一個 API route

# 加了 context7（查最新文件再回答）
你：幫我用 Next.js 寫一個 API route，use context7
```

就這樣，簡單加三個字，Claude 就會去查最新的 Next.js 文件，給你符合當下版本的答案。

---

## MCP vs Hooks vs Skills：搞清楚差別

Claude Code 有三種擴充機制，有時候很容易搞混用途：

| 維度 | MCP Server | Hooks | Skills |
|------|------------|-------|--------|
| **目的** | 連接外部服務 | 自動化工作流 | 標準化流程 |
| **觸發方式** | Claude 判斷何時使用 | 特定事件（存檔、完成等） | Claude 判斷或 `/指令` |
| **最適合** | 外部 API / 資料庫 / 服務 | 前後鉤子（pre/post hook） | 重複性流程（PR review、debugging） |
| **設定位置** | `.mcp.json` 或 user 設定 | `settings.json` 的 hooks 區段 | `.claude/skills/` |
| **類比** | 裝驅動程式 / 外掛 | 設定自動備份規則 | 存一套 SOP |

簡單判斷原則：
- 需要連接外部系統（GitHub、資料庫、瀏覽器）→ 用 **MCP Server**
- 想在某個事件發生時自動執行某件事 → 用 **Hooks**
- 有一套固定的工作流程想讓 Claude 照著跑 → 用 **Skills**

---

## 安全考量：裝之前先想清楚

MCP server 有存取外部系統的能力，所以安全性要認真對待。幾個原則：

**只裝你信任的 server。** MCP server 是獨立程式，它的權限就是你給的。裝一個來路不明的 server，等於讓不知名的程式碼在你機器上跑，並且能以你的身份操作外部服務。

**API key 不要存進 `.mcp.json`。** `.mcp.json` 可能會被 commit 進 git，千萬不要把 token 或密碼直接寫在裡面。正確做法是用環境變數：

```bash
# 錯誤做法（不要這樣）
# 把 token 寫死在設定裡

# 正確做法：用環境變數
export GITHUB_TOKEN=ghp_your_token_here
claude mcp add -s project github npx @modelcontextprotocol/server-github
```

**Project-level 的 `.mcp.json` 進 git 很方便，但要謹慎。** 把 `.mcp.json` commit 進去讓團隊共享設定是好做法，但記得只放 server 的設定，不放任何機密資訊。

---

## Context7 實際操作：從安裝到使用

讓我們走一遍完整流程，以 Context7 為例：

```bash
# 第一步：安裝 Context7 MCP server
claude mcp add -s user context7 npx @upstash/context7-mcp

# 第二步：確認安裝成功
# 在 Claude Code 裡輸入 /mcp，確認 context7 出現在列表裡
```

安裝完成後，在對話裡加上 `use context7` 就會觸發查詢：

```
# 場景一：查 React 最新的 hook 用法
你：用 React 寫一個帶 loading state 的 data fetching hook，use context7

# 場景二：查 Prisma 最新的 API
你：幫我用 Prisma 做一個多對多關聯查詢，use context7

# 場景三：確認函式庫有沒有 breaking change
你：我的 axios 版本是 1.x，跟舊的 0.x 有哪些 breaking change？use context7
```

Claude 收到這些 prompt 後，會先呼叫 Context7 MCP server 去查對應的官方文件，拿到最新資料後再組合成回答。你不需要自己去查 changelog，讓 Claude 幫你做這件事。

---

## 本篇重點整理

| 主題 | 重點 |
|------|------|
| **MCP 是什麼** | 讓 Claude Code 連接外部服務的協定，像是給 Claude 裝外掛 |
| **架構** | Claude Code 是 client，MCP server 是獨立程式，用 JSON-RPC 溝通 |
| **安裝指令** | `claude mcp add -s [user/project/local] <name> <command>` |
| **Scope 選擇** | project → 團隊共享；user → 個人所有專案；local → 本機測試 |
| **Playwright MCP** | 讓 Claude 開瀏覽器，適合 UI 測試和網頁操作 |
| **GitHub MCP** | 讓 Claude 操作 PR、issue、code review |
| **Context7** | 解決 Claude 用過時 API 的問題，加 `use context7` 查最新文件 |
| **安全原則** | 只裝信任的 server；API key 用環境變數，不要存進 `.mcp.json` |

**三個立即可以做的事：**

1. **裝 Context7，今天就用起來**：執行 `claude mcp add -s user context7 npx @upstash/context7-mcp`，然後在你下一個問 API 相關問題時，記得加上 `use context7`。效果馬上就感受得到。

2. **把常用的 MCP server 加進專案的 `.mcp.json`**：如果你的專案有自動化測試需求，裝 Playwright MCP 並加進 `-s project`，然後把 `.mcp.json` commit 進去，讓整個團隊一起受益。

3. **確認你的 MCP server 設定沒有洩漏機密**：執行 `cat .mcp.json`（如果有的話），確認裡面沒有任何 token、密碼、API key。有的話，改成從環境變數讀取，並把機密從 git history 裡清乾淨。
