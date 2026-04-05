---
title: OpenSpec vs Superpowers - AI 編碼工作流選型指南
date: 2026-04-05
tags:
  - AI編碼
  - 開發工具
  - 工作流
  - Claude Code
  - OpenSpec
  - Superpowers
source: https://cloud.tencent.com/developer/article/2649111
aliases:
  - AI 編碼工作流比較
---

# OpenSpec vs Superpowers：AI 編碼工作流選型指南

> [!info] 文章來源
> 原文：[OpenSpec vs Superpowers：2 套 AI 编码工作流，3 个场景怎么选？](https://cloud.tencent.com/developer/article/2649111)
> 作者：術哥無界 | ShugeX

## 核心問題

用 AI 編碼工具做專案，常見的坑：
- 讓 Claude Code 重構模組，它改著改著忘了之前定的方案
- 讓 Cursor 寫新功能，測試全掛

**問題根源：缺少一套規範的工作流來約束 AI。**

這兩套方案解決不同層面的問題：
- **Superpowers** → 管「行為紀律」（AI 怎麼做）
- **OpenSpec** → 管「規格管理」（AI 做什麼）

---

## 1. OpenSpec：給 AI 加上「規格說明書」

### 核心概念
AI 原生規格驅動開發框架（Fission AI 建立）。讓 AI 按照一份結構化的規格文件來寫程式，而不是隨心所欲。

### 增量規格系統（Delta-Based Specs）

> [!tip] 核心創新
> 變更以增量形式表達，不需要重寫整個規格文件。

| 類型 | 說明 |
|------|------|
| `ADDED` | 新行為追加到主規格 |
| `MODIFIED` | 替換現有需求塊 |
| `REMOVED` | 刪除需求塊 |
| `RENAMED` | 用 `FROM:/TO:` 格式改標題 |

對**棕地專案**（已有程式碼庫）特別友好。

```javascript
# 增量規格示例
change: user-auth-refactor
deltas:
  - type: ADDED
    title: "OAuth2 回調處理"
    requirement: |
      系統 SHALL 支援 Google OAuth2 回調，
      並在回調後自動建立或關聯本地使用者帳戶

  - type: MODIFIED
    title: "密碼重置流程"
    replaces: "密碼找回"
    requirement: |
      密碼重置 SHALL 透過郵件發送一次性連結，
      連結有效期 15 分鐘
```

### DAG 工件依賴圖

內部使用 Kahn 演算法的拓撲排序，自動排執行順序：

```
proposal（根節點）
    ├── specs（依賴：proposal）
    ├── design（依賴：proposal）
    │     └── tasks（依賴：specs, design）
    │           └── apply phase（依賴：tasks）
```

### 驗證引擎

自動檢查規格的完整性與一致性：
- **重複偵測**：發現內容重複的需求
- **跨節衝突偵測**：不同章節之間互相矛盾的地方
- **SHALL/MUST 關鍵字檢查**：確保需求符合 RFC 2119 標準
- **場景覆蓋檢查**：需求是否覆蓋所有使用場景

### 支援工具
22 個 AI 編碼工具：Claude Code、Cursor、Windsurf、GitHub Copilot、Gemini CLI、Codex、RooCode、Cline 等

### 短板

> [!warning] 注意事項
> - 需要 Node.js >= 20.19.0
> - 只有 1 個內建 Schema，擴展需自己寫
> - 沒有內建實作驗證（還是要靠測試）
> - 只支援 Markdown 格式
> - 沒有並行變更的衝突解決機制
> - 純命令列，沒有 Web UI

---

## 2. Superpowers：給 AI 加上「行為紀律」

### 核心概念
純 Markdown + YAML 文件，作為 prompt 上下文注入 AI Agent 的對話。**零運行時依賴，沒有任何可執行程式碼。**

### 14 個技能組成的工作流管道

| 技能 | 作用 |
|------|------|
| `using-superpowers` | 啟動技能，每次回應前檢查適用技能 |
| `brainstorming` | Socratic 設計，透過提問驅動方案形成 |
| `using-git-worktrees` | 建立隔離的 git worktree 做變更 |
| `writing-plans` | 把規格拆成 2-5 分鐘的小任務 |
| `subagent-driven-development` | 每個任務派遣獨立子 Agent + 兩階段審查 |
| `test-driven-development` | 嚴格 RED-GREEN-REFACTOR 循環 |
| `systematic-debugging` | 4 階段根因調查 |
| `verification-before-completion` | 聲明成功前必須提供證據 |
| `requesting/receiving-code-review` | 程式碼審查工作流 |
| `finishing-a-development-branch` | 合併/PR/清理 |
| `dispatching-parallel-agents` | 並行 Agent 派遣 |

### 子 Agent 驅動開發（亮點）

每個任務派遣一個擁有**新鮮上下文**的獨立子 Agent，完成後經過兩階段審查：
1. 規格合規性審查
2. 程式碼品質審查

子 Agent 結束時必須給出明確狀態：`DONE`、`DONE_WITH_CONCERNS`、`BLOCKED` 或 `NEEDS_CONTEXT`

### 反合理化設計（Anti-Rationalization）

> [!note] 研究數據
> 基於 Cialdini 說服原則設計，在 N=28,000 次 AI 對話中驗證，**合規率從 33% 提升到 72%**（Meincke et al., 2025）。

AI 常見藉口與反駁都已預先建立，防止 AI 找理由跳過規範（例如：「這功能很簡單，不需要測試」）。

### 支援平台
5 個：Claude Code、Cursor、Codex、OpenCode、Gemini CLI  
（在 Claude Code 上表現最好）

### 短板

> [!warning] 注意事項
> - 無實際程式碼執行，純 prompt 工程
> - Token 消耗較大（14 個技能文件全量注入）
> - 過於有主見，快速原型開發可能太重
> - 無程序化強制執行（靠說服，不是硬約束）
> - 子 Agent 功能依賴平台支援

---

## 3. 三種場景選型

### 場景 A：大型企業專案的需求變更管理

**背景**：50+ 模組，8 人團隊，每週 3-5 個需求變更

**推薦：OpenSpec**
- 增量規格系統應對頻繁變更
- DAG 依賴圖保證執行順序
- 驗證引擎防止需求衝突
- 22 個 AI 工具適配，混合工具環境友好

---

### 場景 B：個人開發者快速原型迭代

**背景**：一人 SaaS 專案，需求每天都在變

**推薦：Superpowers**
- 零配置開箱即用
- TDD 自動化，防止跳過測試
- 系統化調試（4 階段根因調查）
- 驗證前置，防止 AI 自說自話「搞定了」

---

### 場景 C：團隊協作的規範化開發流程

**背景**：5 人團隊，中型 Web 應用，從零開始

**推薦：OpenSpec + Superpowers 組合**

```
OpenSpec 管規格層（做什麼）
Superpowers 管行為層（怎麼做）
```

---

## 4. 組合實戰方案

### 第一層：OpenSpec 做專案骨架

```bash
npm install -g @fission-ai/openspec
openspec init
openspec propose "使用者認證模組重構"
openspec spec --change user-auth-refactor
```

### 第二層：Superpowers 做行為約束

推薦只選 5 個核心技能（非全量 14 個）：
- `test-driven-development`
- `writing-plans`
- `systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`

### 第三層：兩者協作流程

```
OpenSpec 規格文件
    ↓ 作為 writing-plans 技能的輸入
Superpowers 拆分任務
    ↓ 每個任務對照 OpenSpec 規格執行
Superpowers TDD 技能
    ↓ 按規格寫測試，再寫實作
OpenSpec 驗證引擎
    ↓ 檢查實作是否滿足規格
Superpowers 驗證技能
    ↓ 提供測試通過的證據
```

> [!warning] 組合方案的坑
> 1. **Token 消耗疊加**：兩套文件同時注入，上下文窗口壓力大
> 2. **維護成本**：兩套工具都要維護配置
> 3. **學習曲線**：團隊需同時理解兩套工具

---

## 5. 快速選型決策表

| 維度 | OpenSpec | Superpowers | 組合方案 |
|------|----------|-------------|----------|
| 核心能力 | 規格管理 + 變更追蹤 | 行為約束 + TDD 強制 | 兩者兼備 |
| 適合規模 | 中大型 | 個人/小型 | 中型團隊 |
| 適合類型 | 棕地專案 | 綠地專案 | 混合 |
| 上手成本 | 中 | 低 | 中高 |
| Token 消耗 | 低 | 中高 | 高 |
| AI 工具覆蓋 | 22 個 | 5 個 | 5 個 |
| 需求變更管理 | 強 | 弱 | 強 |
| 程式碼品質保障 | 弱 | 強 | 強 |

### 一句話選型建議

- **需求複雜、變更頻繁、多人協作** → OpenSpec
- **一人快速迭代、需要程式碼品質保障** → Superpowers
- **中型團隊、從零開始、有明確需求** → 組合方案

---

## 核心結論

> [!quote] 本質區別
> - **OpenSpec** 解決「AI 不知道該做什麼」的問題
> - **Superpowers** 解決「AI 不知道該怎麼做」的問題

**選型原則：先想清楚你的核心問題是什麼，再選對應的工具。**
