# OpenSpec 使用手冊

> AI 原生的規格驅動開發工具

## 目錄

- [安裝](#安裝)
- [快速開始](#快速開始)
- [專案結構](#專案結構)
- [核心指令](#核心指令)
- [工作流程](#工作流程)
- [進階功能](#進階功能)
- [故障排除](#故障排除)

## 安裝

### 系統需求

- Node.js 20.19.0 或更高版本

### 安裝步驟

```bash
# 全域安裝 OpenSpec
npm install -g @fission-ai/openspec@latest

# 或使用 pnpm
pnpm add -g @fission-ai/openspec@latest

# 或使用 yarn
yarn global add @fission-ai/openspec@latest

# 或使用 bun
bun add -g @fission-ai/openspec@latest
```

### 初始化專案

```bash
# 進入你的專案目錄
cd your-project

# 初始化 OpenSpec
openspec init
```

初始化會建立：
- `openspec/` 目錄結構
- AI 技能檔案（供 AI 編輯器偵測使用）
- 專案配置（可選）

## 快速開始

### 第一個變更

```text
你: /opsx:propose 加入深色模式

AI:  已建立 openspec/changes/加入深色模式/
     ✓ proposal.md — 為什麼要做、要做什麼
     ✓ specs/       — 需求和情境
     ✓ design.md    — 技術方案
     ✓ tasks.md     — 實作檢查清單
     準備好開始實作了！

你: /opsx:apply

AI:  執行任務中...
     ✓ 1.1 新增主題 context provider
     ✓ 1.2 建立切換元件
     ✓ 2.1 新增 CSS 變數
     ✓ 2.2 連接 localStorage
     所有任務完成！

你: /opsx:archive

AI:  已封存至 openspec/changes/archive/2025-01-23-加入深色模式/
     規格已更新。準備好下一個功能了。
```

## 專案結構

初始化後，專案會有以下結構：

```
openspec/
├── specs/              # 來源真實值（你的系統目前行為）
│   └── <領域>/
│       └── spec.md
├── changes/            # 提議的變更（每個變更一個資料夾）
│   └── <變更名稱>/
│       ├── proposal.md   # 提案：為什麼、做什麼
│       ├── design.md     # 設計：技術方案
│       ├── tasks.md      # 任務：實作清單
│       └── specs/       # 增量規格（變更內容）
│           └── <領域>/
│               └── spec.md
└── config.yaml         # 專案配置（可選）
```

### 兩個核心目錄

- **`specs/`** — 來源真實值，描述系統目前如何運作
- **`changes/`** — 提議的修改，每個變更獨立資料夾，完成後合併到 specs/

## 核心指令

### 預設快速路徑（core 設定檔）

#### `/opsx:propose` — 提出新變更

```text
/opsx:propose [變更名稱或描述]
```

**功能：**
- 建立新的變更資料夾
- 一次性建立所有規劃文件（proposal、specs、design、tasks）
- 準備好執行 `/opsx:apply`

**範例：**
```text
/opsx:propose add-user-profile
/opsx:propose fix-login-bug
/opsx:propose 加入兩步驗證功能
```

#### `/opsx:explore` — 探索想法

```text
/opsx:explore [主題]
```

**功能：**
- 自由探索想法和問題
- 調查代碼庫
- 比較不同方案
- 沒有固定結構

**範例：**
```text
你: /opsx:explore

AI:  你想探索什麼？

你: 我們該如何改善頁面載入效能？

AI:  讓我來調查你的設定...
     [分析套件大小、找出慢查詢、審查組件渲染模式]

     我發現了三個主要瓶頸：
     1. 未優化的大圖片
     2. ProductList 中的同步資料獲取
     3. Context 變更導致的重新渲染

     你想先解決哪一個？
```

#### `/opsx:apply` — 執行實作

```text
/opsx:apply [變更名稱]
```

**功能：**
- 讀取 tasks.md
- 逐一執行任務
- 寫入代碼、建立檔案、執行測試
- 用勾選框標記完成的任務

**範例：**
```text
你: /opsx:apply

AI:  執行加入深色模式...

     讀取 tasks.md：
     - [ ] 1.1 建立 ThemeContext
     - [ ] 1.2 新增 CSS 自訂屬性
     - [ ] 1.3 實作 localStorage 持久化

     執行 1.1：建立 ThemeContext...
     [建立 src/context/ThemeContext.tsx]

     ✓ 1.1 完成

     執行 1.2：新增 CSS 自訂屬性...
     [更新 src/styles/globals.css]

     ✓ 1.2 完成
     ...
```

#### `/opsx:archive` — 封存變更

```text
/opsx:archive [變更名稱]
```

**功能：**
- 檢查文件完成狀態
- 檢查任務完成度（未完成會警告）
- 如果尚未同步，提示同步增量規格
- 將變更資料夾移至 `openspec/changes/archive/YYYY-MM-DD-<名稱>/`

**範例：**
```text
你: /opsx:archive

AI:  封存加入深色模式...

     文件狀態：
     ✓ proposal.md 存在
     ✓ specs/ 存在
     ✓ design.md 存在
     ✓ tasks.md 存在 (8/8 任務完成)

     增量規格：尚未同步
     → 要現在同步嗎？

你: 是

AI:  ✓ 已同步規格至 openspec/specs/ui/spec.md
     ✓ 已移至 openspec/changes/archive/2025-01-24-加入深色模式/

     變更已成功封存。
```

### 擴展工作流程指令

啟用擴展指令：
```bash
openspec config profile
openspec update
```

#### `/opsx:new` — 建立新變更骨架

```text
/opsx:new [變更名稱] [--schema <schema-name>]
```

建立變更資料夾，等待你用 `/opsx:continue` 或 `/opsx:ff` 生成文件。

#### `/opsx:continue` — 建立下一個文件

```text
/opsx:continue [變更名稱]
```

一次建立一個文件，適合逐步建立並審查。

#### `/opsx:ff` — 快速生成規劃文件

```text
/opsx:ff [變更名稱]
```

一次性建立所有規劃文件，適合明確的需求。

#### `/opsx:verify` — 驗證實作

```text
/opsx:verify [變更名稱]
```

驗證實作是否與文件一致，檢查：
- **完整性**：所有任務完成、所有需求實作
- **正確性**：實作符合規格意圖、邊緣情況處理
- **一致性**：設計決策反映在代碼中

#### `/opsx:sync` — 同步增量規格

```text
/opsx:sync [變更名稱]
```

將變更的增量規格合併到主要規格（通常由 archive 自動處理）。

#### `/opsx:bulk-archive` — 批量封存

```text
/opsx:bulk-archive [變更名稱...]
```

一次封存多個完成的變更，自動處理規格衝突。

#### `/opsx:onboard` — 引導式教學

```text
/opsx:onboard
```

互動式教學，引導你完成完整的 OpenSpec 工作流程。

## 工作流程

### 快速功能

適合明確需求、直接執行的功能：

```text
/opsx:new ──► /opsx:ff ──► /opsx:apply ──► /opsx:verify ──► /opsx:archive
```

### 探索式

當需求不明確或需要先調查時：

```text
/opsx:explore ──► /opsx:new ──► /opsx:continue ──► ... ──► /opsx:apply
```

### 平行變更

同時處理多個變更：

```text
變更 A: /opsx:new ──► /opsx:ff ──► /opsx:apply (進行中)
                                          │
                                     上下文切換
                                          │
變更 B: /opsx:new ──► /opsx:ff ──────► /opsx:apply
```

### 完成變更

建議的完成流程：

```text
/opsx:apply ──► /opsx:verify ──► /opsx:archive
                   │                 │
             驗證實作          如需要提示同步
```

## 進階功能

### 專案配置

建立 `openspec/config.yaml` 來設定專案預設值：

```yaml
# openspec/config.yaml
schema: spec-driven

context: |
  技術堆疊：TypeScript、React、Node.js
  API 慣例：RESTful、JSON 回應
  測試：Vitest 單元測試、Playwright E2E
  程式碼風格：ESLint 搭配 Prettier、嚴格 TypeScript

rules:
  proposal:
    - 包含回滾計畫
    - 識別受影響的團隊
  specs:
    - 使用 Given/When/Then 格式描述情境
  design:
    - 複雜流程包含序列圖
```

### 自訂 Schema

```bash
# 建立新的 schema
openspec schema init my-workflow

# 或複製現有的 schema 作為起點
openspec schema fork spec-driven my-workflow

# 驗證 schema 結構
openspec schema validate my-workflow
```

### CLI 指令參考

```bash
# 列出所有變更
openspec list

# 查看變更詳情
openspec show add-dark-mode

# 檢查變更狀態
openspec status --change add-dark-mode

# 驗證規格格式
openspec validate add-dark-mode

# 互動式儀表板
openspec view

# 列出可用的 schema
openspec schemas

# 檢查 schema 解析位置
openspec schema which my-workflow

# 查看全域設定
openspec config

# 更新 OpenSpec
openspec update
```

## 故障排除

### 「找不到變更」

指令無法識別要操作的變更。

**解決方案：**
- 明確指定變更名稱：`/opsx:apply add-dark-mode`
- 檢查變更資料夾是否存在：`openspec list`
- 確認你在正確的專案目錄

### 「沒有可建立的文件」

所有文件都已完成或被依賴阻塞。

**解決方案：**
- 執行 `openspec status --change <name>` 查看什麼被阻塞
- 檢查所需文件是否存在
- 先建立缺少的依賴文件

### 「找不到 Schema」

指定的 schema 不存在。

**解決方案：**
- 列出可用 schema：`openspec schemas`
- 檢查 schema 名稱拼寫
- 如果是自訂的，建立 schema：`openspec schema init <name>`

### 指令無法識別

AI 工具無法識別 OpenSpec 指令。

**解決方案：**
- 確認 OpenSpec 已初始化：`openspec init`
- 重新生成技能：`openspec update`
- 檢查 `.claude/skills/` 目錄是否存在
- 重新啟動 AI 工具以載入新技能

### 文件生成不正常

AI 建立的文件不完整或不正確。

**解決方案：**
- 在 `openspec/config.yaml` 中加入專案上下文
- 為特定文件加入規則指引
- 在變更描述中提供更多細節
- 使用 `/opsx:continue` 而非 `/opsx:ff` 以獲得更多控制

## 更新 OpenSpec

```bash
# 升級套件
npm install -g @fission-ai/openspec@latest

# 重新生成 AI 指引
openspec update
```

## 支援的 AI 工具

OpenSpec 支援 20+ 種 AI 編輯器，包括：

- **Claude Code** — `/opsx:propose`, `/opsx:apply`
- **Cursor** — `/opsx-propose`, `/opsx-apply`
- **Windsurf** — `/opsx-propose`, `/opsx-apply`
- **GitHub Copilot** — `/opsx-propose`, `/opsx-apply`
- **Trae** — `/openspec-propose`, `/openspec-apply-change`

## 相關資源

- [概念入門](./OpenSpec_觀念入門.md) — 深入理解核心概念
- [原始文件](https://github.com/Fission-AI/OpenSpec) — GitHub 原始碼
- [Discord 社群](https://discord.gg/YctCnvvshC) — 獲得幫助和問題解答
