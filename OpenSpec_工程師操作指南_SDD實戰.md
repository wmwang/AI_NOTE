---
title: OpenSpec 技術導入指南：以 Spec-Driven Development 建立 AI 協作的工程規範
tags:
  - openspec
  - sdd
  - ai-coding
  - workflow
  - guide
aliases:
  - OpenSpec Guide
  - SDD 技術導入指南
date: 2026-04-12
---

# OpenSpec 技術導入指南：以 Spec-Driven Development 建立 AI 協作的工程規範

> AI coding assistant 的輸出品質，取決於輸入端的規格精度。OpenSpec 提供了一層輕量的 specification layer，在 prompt 與 implementation 之間建立可驗證的合約。

---

## 問題背景：AI 輔助開發中的 Alignment Gap

當前 AI coding assistant（Claude Code、Cursor、Copilot 等）的核心瓶頸並非模型能力不足，而是 **需求規格的結構化程度不夠**。

在典型的 AI 輔助開發場景中，需求以自然語言散落在 chat history 裡，隨著 context window 膨脹，模型對需求的理解逐漸發散。結果是：

- 每輪迭代的輸出偏移方向不可預測
- 修正 A 問題時引入 B regression
- 隱含需求未被顯式約束，模型以 hallucination 填補

這本質上是一個 **human-AI alignment 問題**——缺少一份雙方都能參照的、持久化的 specification artifact。

> [!important] SDD 的工程定位
> Spec-Driven Development 並非瀑布式的前置文件階段，而是在開發迴圈中引入一層 **可迭代、可驗證的行為規格**，作為 AI 實作的 ground truth。

---

## OpenSpec 概覽

[OpenSpec](https://github.com/Fission-AI/OpenSpec) 是 Fission AI 開源的 SDD 框架，設計目標是為 AI 輔助開發提供結構化的規格管理。核心設計原則：

| 原則 | 工程意義 |
|------|----------|
| **Fluid, not rigid** | 無 phase gate，規格可在任意階段修改，不阻塞開發流程 |
| **Brownfield-first** | 原生支援既有系統的漸進式導入，非 greenfield 限定 |
| **Minimal ceremony** | 三個 slash command 完成一輪完整的 propose → implement → archive |
| **Tool-agnostic** | 規格為純 Markdown，相容 25+ 種 AI 開發工具，無 vendor lock-in |

架構上，OpenSpec 扮演的角色類似 API spec 之於前後端分離——它是 **人機協作的 interface contract**，定義系統行為的期望邊界，由 AI 負責在邊界內實作。

---

## 安裝與初始化

### 環境需求

- Node.js ≥ 20.19.0

### 安裝

```bash
npm install -g @fission-ai/openspec@latest
```

### 初始化專案

```bash
cd your-project
openspec init
```

初始化後的目錄結構：

```
openspec/
├── specs/           # 系統現行行為規格（source of truth）
├── changes/         # 進行中的變更提案（每個 change 獨立目錄）
└── config.yaml      # 專案層級設定（選填）
```

> [!note] specs 與 changes 的分離設計
> `specs/` 描述系統的 **current state**，按 domain 組織（如 `specs/auth/`、`specs/payments/`）。
> `changes/` 描述 **pending mutations**，每個變更提案擁有獨立的 proposal、delta specs、design 與 task list。
> 這個分離確保變更邊界明確、多人並行無衝突、歷史紀錄完整保留。

---

## 核心工作流

OpenSpec 的標準開發流程由三個 slash command 組成：

```
/opsx:propose → /opsx:apply → /opsx:archive
```

### Phase 1：Propose — 建立變更提案

```
/opsx:propose add-dark-mode
```

執行後，AI agent 會進入需求釐清階段，確認實作細節後在 `openspec/changes/add-dark-mode/` 下生成四份 artifact：

| Artifact | 用途 |
|----------|------|
| `proposal.md` | 變更意圖、範圍界定、影響分析 |
| `specs/` | Delta Specs（差異規格） |
| `design.md` | 技術方案設計 |
| `tasks.md` | 實作任務的 ordered checklist |

#### Delta Specs 格式

Delta specs 採用三種變更類型標記，語義明確：

```markdown
## ADDED Requirements

### REQ-DARK-001: Theme Toggle

The system SHALL provide a toggle to switch between light and dark mode.

#### Scenario: User enables dark mode
- **Given** the user is on any page
- **When** the user clicks the theme toggle
- **Then** all UI elements switch to dark theme colors

## MODIFIED Requirements

### REQ-UI-003: Default Theme (Modified)
...

## REMOVED Requirements

### REQ-UI-007: Fixed Light Theme
...
```

> [!info] 規格撰寫規範
> - 需求陳述使用 `SHALL` / `MUST` 等 RFC 2119 規範性措辭
> - 每個需求至少包含一個 Scenario
> - Scenario 採用 Given-When-Then（BDD）格式，可直接對應驗收條件

### Phase 2：Apply — 依規格實作

```
/opsx:apply
```

AI agent 依據 `tasks.md` 逐項執行實作。規格在實作過程中仍可修改——OpenSpec 不設 phase gate，支援 spec 與 code 的 co-evolution。

### Phase 3：Archive — 合併歸檔

```
/opsx:archive
```

歸檔操作執行以下步驟：
1. Delta specs 合併至主規格目錄（`specs/`）
2. Change 目錄移至 `changes/archive/`（附時間戳）
3. 完整的 proposal → design → spec → task 鏈保留為歷史紀錄

---

## 進階工作流

需要更精細控制時，可使用 expanded workflow：

```
/opsx:new → /opsx:ff | /opsx:continue → /opsx:apply → /opsx:verify → /opsx:archive
```

| 指令 | 功能 |
|------|------|
| `/opsx:new` | 建立空的 change scaffold |
| `/opsx:ff` | Fast-forward：一次性生成全部 artifact |
| `/opsx:continue` | 恢復中斷的 change context |
| `/opsx:verify` | 驗證實作與規格的一致性 |
| `/opsx:sync` | 同步規格與程式碼狀態 |
| `/opsx:onboard` | 以現有 codebase 生成初始 specs |
| `/opsx:bulk-archive` | 批次歸檔已完成的 changes |

---

## CLI 指令參考

```bash
openspec list                        # 列出進行中的 changes
openspec show <name>                 # 顯示 change 詳情
openspec validate <name>             # 驗證規格格式
openspec validate <name> --strict    # 嚴格模式驗證
openspec view                        # 互動式 dashboard
openspec config profile              # 切換 workflow profile
openspec update                      # 更新 agent instructions
```

---

## 適用範圍界定：何時需要 Propose？

以下變更 **不改變系統行為規格**，無需建立提案，直接實作即可：

- Bug fix（修復與既有規格的偏差）
- Typo / 文案修正
- 依賴套件升級
- 測試補齊
- 內部重構（不改變外部行為契約）

> [!abstract] 判斷準則
> 變更是否修改了系統的 **外部可觀測行為**？若否，則不在 spec 管理範圍內。

---

## 工程效益分析

### 1. 降低 AI Hallucination 導致的迭代成本

規格作為 persistent ground truth，約束 AI 的實作邊界。每輪對話的 alignment 不再依賴 chat history 的隱含語義，而是以 `specs/` 中的顯式約束為準。

### 2. 變更影響範圍可控

每個 change 擁有獨立的 artifact 目錄。Code review 可先審閱 `proposal.md` 與 delta specs 確認意圖與邊界，再進入程式碼層級的 review——這顯著降低 reviewer 的認知負載。

### 3. 團隊並行開發的隔離性

不同 change 在各自的 `changes/<name>/` 目錄中獨立推進，spec-level conflict 在歸檔時才需處理。對於多人同時使用 AI agent 的團隊，這提供了天然的 workspace isolation。

### 4. 決策脈絡的持久化

歸檔後的 `changes/archive/` 保留完整的 proposal → design → spec → task 鏈。三個月後回溯某個功能的設計決策，不需要翻 Slack 或靠記憶——artifact 本身即是文件。

### 5. 工具遷移零成本

OpenSpec 的規格是純 Markdown + YAML，不依賴任何特定 AI 工具的私有格式。從 Claude Code 遷移到 Cursor 或 Copilot，規格資產完整保留。

---

## 方案比較

| 面向 | OpenSpec | Spec Kit (GitHub) | Kiro (AWS) | 無結構 AI Coding |
|------|----------|-------------------|------------|-----------------|
| **適用階段** | 1→N 持續演進 | 0→1 新建專案 | AWS 生態內 | 快速 prototyping |
| **導入成本** | 低（3 commands） | 中 | 中高 | 零 |
| **Vendor lock-in** | 無 | GitHub 生態 | AWS + 特定模型 | 無 |
| **Spec 迭代彈性** | 高（無 phase gate） | 有階段閘門 | 有階段閘門 | N/A |
| **規格持久化** | 自動歸檔 | 需手動管理 | 平台內建 | 無 |
| **Brownfield 支援** | 原生設計 | 有限 | 有限 | N/A |

---

## 實戰範例：既有專案導入 User Search 功能

```bash
# 初始化（首次導入）
openspec init
```

在 AI 工具中執行提案：

```
/opsx:propose add-user-search
```

AI agent 進入需求探索階段，典型的釐清項目包括：
- 搜尋支援的欄位範圍與索引策略
- 模糊搜尋的 matching algorithm 選擇
- 分頁機制（cursor-based vs offset）
- RBAC 權限控管範圍

確認後生成 artifact，以 CLI 驗證格式：

```bash
openspec validate add-user-search --strict
```

執行實作：

```
/opsx:apply
```

AI agent 依據 `tasks.md` 逐項完成。驗證後歸檔：

```
/opsx:archive
```

> [!success] 工程產出
> 完整的 proposal → delta specs → design → tasks artifact 鏈，可直接作為 PR description 的補充材料或 design doc 的附件。

---

## 導入建議

> [!warning] 模型相容性
> OpenSpec 的 spec generation 品質與模型推理能力高度相關。建議使用 Claude Opus 4.5+、GPT-5.2+ 或同等級 reasoning model。

1. **Context window 管理**——長對話容易造成 spec drift，建議在新 session 中以 `/opsx:continue` 恢復 change context
2. **規格描述行為而非實作**——spec 定義 "what the system does"，不規定 "how it's implemented"，保留技術選型的彈性
3. **單一職責原則**——每個 change 對應一個功能變更，避免在同一 change 中混入不相關的需求
4. **CI 整合 validate**——將 `openspec validate --strict` 加入 pre-commit hook 或 CI pipeline，確保 spec 格式一致性
5. **及時歸檔**——完成即 archive，避免 `changes/` 中堆積過多 open changes 造成管理負擔

---

## 小結

OpenSpec 的價值不在於引入更多流程，而在於 **將原本隱含在對話中的需求共識顯式化為可追蹤的 artifact**。

對於已經在使用 AI coding assistant 的團隊，這是一個低導入成本、高投資報酬的工程實踐——幾份 Markdown 文件、三個指令、零額外基礎設施，換來的是可預測的 AI 輸出品質與可追溯的變更歷史。

```bash
npm install -g @fission-ai/openspec@latest && cd your-project && openspec init
```
