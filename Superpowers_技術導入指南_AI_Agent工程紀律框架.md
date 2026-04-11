---
title: Superpowers 技術導入指南：為 AI Coding Agent 建立工程紀律的 Skills 框架
tags:
  - superpowers
  - ai-coding
  - tdd
  - workflow
  - agent-skills
  - code-review
aliases:
  - Superpowers Guide
  - AI Agent Skills 框架
date: 2026-04-12
---

# Superpowers 技術導入指南：為 AI Coding Agent 建立工程紀律的 Skills 框架

> AI coding agent 的能力上限取決於模型，但品質下限取決於流程約束。Superpowers 以 composable skills 的形式，將 TDD、systematic debugging、code review 等工程紀律注入 agent 的決策迴圈。

---

## 問題背景：AI Agent 有能力，缺紀律

AI coding agent 的行為模式有一個結構性問題：**它傾向於跳過所有「看起來不直接產出程式碼」的步驟。**

具體表現為：

- 未釐清需求就開始實作，產出與意圖偏離
- 跳過測試直接寫 production code，coverage 形同虛設
- 遇到 bug 直接 patch symptom，不做 root cause analysis
- 宣稱「已完成」但未實際執行驗證指令

這不是模型能力問題——同一個模型在有明確流程約束時，輸出品質截然不同。問題在於：**自然語言 prompt 無法可靠地強制執行工程實踐。** 說「請先寫測試」和實際建立一個 hard gate 阻止 agent 在測試通過前進入下一步，效果差距是數量級的。

Superpowers 的作者 Jesse Vincent（Request Tracker、Perl 6、Keyboardio、K-9 Mail 開發者）的觀察是：

> *"AI agents respond to structure. You cannot demand best practices through exhortation, but you can enforce them through explicit workflows and hard gates."*

> [!important] Superpowers 的工程定位
> 不是新模型、不是新工具、不是 wrapper——而是一組 **platform-agnostic 的 skill files**，以 Markdown 形式定義 agent 在開發流程中的行為規範與決策閘門。

---

## 架構概覽

### Composable Skills 架構

Superpowers 由 **14 個 skill module** 組成，每個 skill 是一份 Markdown 文件，定義特定開發情境下的 agent 行為規範。Skills 之間可組合（compose），按需啟用。

```
skills/
├── brainstorming/                  # 需求探索與設計提案
├── writing-plans/                  # 任務拆解與執行計畫
├── executing-plans/                # 計畫執行與 checkpoint
├── test-driven-development/        # TDD 強制流程
├── systematic-debugging/           # 四階段 root cause analysis
├── verification-before-completion/ # 完成宣告前的驗證閘門
├── requesting-code-review/         # 發起 code review
├── receiving-code-review/          # 接收與回應 review feedback
├── dispatching-parallel-agents/    # 多 agent 並行調度
├── subagent-driven-development/    # subagent 任務分派
├── using-git-worktrees/            # Git worktree 隔離開發
├── finishing-a-development-branch/ # 分支收尾與合併
├── using-superpowers/              # 框架入口與 skill discovery
└── writing-skills/                 # 自定義 skill 撰寫規範
```

### 觸發機制

安裝後，`SessionStart` hook 在每次對話開始時注入 `using-superpowers` skill，使 agent 在對話全程具備 skill awareness。Agent 會根據開發 context 自動判斷應啟用哪些 skill——無需手動 invoke。

### 跨平台相容性

Skills 本質上是 Markdown 文件，不依賴任何平台私有 API：

| 平台 | 整合深度 |
|------|----------|
| **Claude Code** | 最完整——支援 sandbox、native subagent、plugin system |
| **Cursor** | 核心 workflow 完整支援 |
| **GitHub Copilot CLI** | 透過 marketplace 安裝 |
| **Codex CLI** | 透過 repo 內 `.codex/INSTALL.md` 導入 |
| **Gemini CLI** | 透過 extensions 安裝 |

---

## 安裝

### Claude Code（推薦）

```bash
# 官方 plugin registry
/plugin install superpowers@claude-plugins-official

# 或透過 marketplace
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### Cursor

```
/add-plugin superpowers
```

### GitHub Copilot CLI

```bash
copilot plugin marketplace add obra/superpowers-marketplace
copilot plugin install superpowers@superpowers-marketplace
```

### Gemini CLI

```bash
gemini extensions install https://github.com/obra/superpowers
```

### 驗證安裝

啟動新 session，要求 agent 規劃一個功能或進行 debugging。若 agent 自動進入 brainstorming 或 systematic debugging 流程，表示 skill 已正確載入。

---

## 核心 Skills 詳解

### 1. Brainstorming — 需求探索與設計提案

**定位**：阻止 agent 在需求未釐清前開始寫 code。

**Hard gate**：設計提案未經使用者核准前，禁止產生任何實作程式碼。

**執行流程**：

1. Agent 以 Socratic questioning 逐步釐清需求——單次只問一個問題，偏好選擇題而非開放式提問
2. 探索 2-3 個替代方案，附 trade-off 分析
3. 產出 200-300 字的設計提案，交由使用者確認
4. 確認通過後方進入下一階段

**設計原則**：嚴格執行 YAGNI（You Ain't Gonna Need It），主動抑制 agent 過度設計的傾向。

> [!note] 為什麼是 hard gate？
> 自然語言指令（「請先確認需求」）在 agent 的 token prediction 中權重不穩定，容易被後續 context 覆蓋。Hard gate 則是流程層級的阻斷——skill 明確定義：**未取得使用者核准前，不得進入 implementation phase。**

---

### 2. Writing Plans — 原子級任務拆解

**定位**：將設計提案轉換為可由 subagent 獨立執行的任務清單。

**拆解標準**：

- 每個 task 的預期執行時間為 **2-5 分鐘**
- 包含 **完整的程式碼 context**（hardcoded file paths、exact command）
- 附帶 **驗證步驟**（執行什麼指令、預期什麼輸出）

**設計前提**：假設執行者 **對 codebase 零熟悉度、判斷力存疑**（"zero codebase familiarity and questionable judgment"）。這不是貶低——而是確保 plan 的 self-containedness，使其不依賴隱含知識即可正確執行。

這使得 plan 可以交給：
- 全新的 AI session（無 prior context）
- 不同的 AI 工具
- 不熟悉該模組的團隊成員

---

### 3. Test-Driven Development — 強制 TDD 流程

**定位**：Superpowers 中約束力最強的 skill。

**核心規則**：

> *"No production code without a failing test first. Already written? Delete it. Start over."*

**強制流程（Red-Green-Refactor）**：

```
RED    → 撰寫測試，執行確認失敗（驗證測試本身有效）
GREEN  → 撰寫最小實作使測試通過
REFACTOR → 重構，確保測試仍全數通過
```

**Anti-pattern 防護**：

Skill 預先列舉 agent 常見的規避理由，並逐一封堵：

| Agent 常見藉口 | Skill 的回應 |
|----------------|-------------|
| 「這段 code 太簡單不需要測試」 | 簡單的 code 寫測試也快，沒有跳過的理由 |
| 「我先寫 code 再補測試」 | 先寫的 code 必須刪除，從測試重新開始 |
| 「我可以手動驗證」 | 手動驗證不可重現，不符合 verification 標準 |
| 「測試框架還沒設定好」 | 設定測試框架本身就是第一個 task |

> [!warning] 嚴格性的工程理由
> TDD skill 的嚴格性並非教條——而是因為 AI agent 在缺乏約束時，**幾乎必然會跳過測試**。這是 LLM token prediction 的統計傾向：「生成程式碼」的 reward signal 遠強於「生成測試」。Hard gate 是對這個統計傾向的工程對策。

---

### 4. Systematic Debugging — 四階段根因分析

**定位**：阻止 agent 對 symptom 做 surface-level patch。

**四階段流程**：

| 階段 | 執行內容 |
|------|----------|
| **Root Cause Investigation** | 讀取完整錯誤訊息、穩定重現路徑、檢查近期變更 |
| **Pattern Analysis** | 與功能正常的同類程式碼比對，辨識差異 |
| **Hypothesis & Testing** | 每次只變更一個變數，失敗假設立即捨棄 |
| **Implementation** | 先寫重現測試，再修復，驗證測試通過 |

**關鍵規則**：

> *同一處修復累積 3 次以上 → 判定為架構層級問題，停止 patch，上報重新設計。*

這條規則直接對應工程實務中的 "fix-and-pray" anti-pattern——agent 傾向於反覆微調同一段 code 而非退一步思考架構。

---

### 5. Verification Before Completion — 完成宣告閘門

**定位**：阻止 agent 在未實際驗證的情況下宣稱「已完成」。

**強制流程**（每次宣告「完成」前必須執行）：

1. 識別驗證指令（test command、build command、lint 等）
2. **全新執行**該指令（不可引用先前的執行結果）
3. 讀取 **完整輸出**（包括 exit code）
4. 確認輸出與宣稱一致
5. 通過後方可宣告完成

> [!abstract] 為什麼需要這個 skill？
> AI agent 的一個常見行為是：在 context window 中「看到」先前的測試通過紀錄，便直接宣稱完成——但期間可能已做了多次修改。Verification skill 強制 agent 在 **當下狀態** 重新執行驗證。

---

### 6. Code Review — 雙階段審查

**定位**：以獨立 subagent 執行 code review，避免實作者自我審查的偏見。

**雙階段設計**：

| 階段 | 審查重點 | 執行者 |
|------|----------|--------|
| **Stage 1: Spec Compliance** | 實作是否符合規格要求 | 獨立 subagent（clean context） |
| **Stage 2: Code Quality** | 程式碼品質、可維護性、效能 | 另一個獨立 subagent |

Stage 1 未通過時，Stage 2 不啟動。這確保先驗證「做對了什麼」，再討論「做得好不好」。

**Receiving Code Review** skill 則規範 agent 接收 feedback 時的行為：
- 禁止 performative response（「Great point!」之類的客套）
- 必須以 restatement 展示理解
- 不同意時必須提供技術論據
- 實作修改前先驗證 feedback 的前提是否成立

---

### 7. Subagent-Driven Development — 多 Agent 並行調度

**定位**：將 plan 中的獨立 task 分派給多個 subagent 並行執行。

**核心機制**：

- 每個 subagent 接收 **clean context**（不含其他 task 的實作歷史），防止 context pollution
- 主 agent 負責 task dispatch、progress tracking、conflict resolution
- 每個 subagent 完成後經過 code review skill 審查

這使得 Claude Code 能夠 **自主運作數小時不偏移**——因為每個 subagent 的 context window 乾淨且有限。

---

## 標準開發工作流

完整的 Superpowers 開發流程：

```
Brainstorming → Writing Plans → Git Worktree →
Subagent-Driven Development → Code Review →
Verification → Branch Finishing
```

對應到一次功能開發的實際操作：

```
1. Brainstorming     使用者描述需求，agent 釐清並提出設計方案
2. Writing Plans     核准後，拆解為 2-5 分鐘的原子 task list
3. Git Worktree      建立隔離分支，確認 test baseline 通過
4. Subagent Execution 各 task 由 subagent 以 TDD 方式實作
5. Code Review       獨立 subagent 進行雙階段審查
6. Verification      全套測試 + build 重新執行
7. Branch Finishing   提供 merge / PR 選項，清理 worktree
```

> [!tip] 簡化流程
> 對於小型修改，可跳過 subagent dispatch，直接在單一 session 中走完 brainstorming → TDD → verification 流程。框架是 composable 的，不要求每次都啟用全部 skill。

---

## Rigid vs. Flexible：Skill 的約束力分級

Superpowers 刻意區分兩類 skill：

| 類型 | 代表 Skill | 約束方式 |
|------|-----------|----------|
| **Rigid** | TDD、Systematic Debugging、Verification | Hard gate + 明確後果（如刪除未測試的 code） |
| **Flexible** | Brainstorming、Code Review | 提供結構但容許 context-dependent 調整 |

Rigid skill 使用 `MUST`、`SHALL` 等強制措辭，並預先列舉 agent 的常見規避策略逐一封堵。Flexible skill 提供框架與 checklist，但允許依情境省略或調整步驟。

---

## 自定義 Skill 開發

`writing-skills` skill 定義了建立新 skill 的標準流程，本身也遵循 TDD 方法論：

1. **建立 pressure test scenario**——讓一個 **未安裝該 skill 的 subagent** 執行目標任務
2. **觀察失敗模式**——記錄 agent 在哪些環節跳過步驟或產出不符預期
3. **撰寫 skill**——針對觀察到的失敗模式設計對應的約束規則
4. **驗證**——讓一個 **全新的 subagent**（安裝了 skill）重新執行相同任務
5. **迭代修補**——找出 agent 仍能繞過的漏洞，補強 skill 內容

常見的自定義 skill 方向：

- **Deploy**：release checklist 與 rollback 流程
- **ADR（Architecture Decision Records）**：設計決策的結構化紀錄
- **Security Review**：安全性審查的 checklist
- **Onboarding**：新成員 codebase 導覽流程

---

## 與 OpenSpec 的協作模式

Superpowers 管理的是 **session 內的開發紀律**，OpenSpec 管理的是 **跨 session 的規格持久化**。兩者互補：

```
Brainstorming → OpenSpec Propose（持久化規格）→ Writing Plans →
OpenSpec Apply（實作）→ Code Review → OpenSpec Archive（歸檔）
```

| 面向 | Superpowers | OpenSpec |
|------|-------------|---------|
| **管理範圍** | 單次開發 session 的流程紀律 | 跨 session 的規格與變更歷史 |
| **產出物** | 設計方案、task list、test、code | proposal、delta specs、design doc |
| **持久性** | 隨 session 結束消失 | 以 Markdown 持久保存在 repo |

---

## 工程效益

### Token 成本 vs. 返工成本

Superpowers 的多 subagent 架構確實增加 token 消耗。但工程決策應比較的是 **total cost**：

- 無紀律的 agent 可能在 10 輪迭代後仍未收斂——每輪都消耗 token
- 有 TDD + verification gate 的 agent 在 2-3 輪內收斂，且產出含完整測試

對於 quality-critical 的 production code，前者的 total token cost 通常高於後者。

### 實戰案例：chardet 7.0.0

chardet 函式庫使用 Superpowers 完成 7.0.0 版本的重構，成果包括：

- **41x 效能提升**
- **96.8% 準確率**
- 覆蓋 2,161 個檔案、99 種編碼的完整測試覆蓋率

這是 enforced TDD 在大規模 codebase 上的直接產出。

---

## 導入建議

1. **從真實專案開始**——不要用 toy project 評估，framework 的價值在複雜場景才會顯現
2. **信任 brainstorming phase**——抵抗「直接寫 code 比較快」的直覺，需求釐清階段的投入會在後續迭代中回收
3. **選擇性啟用**——不需要每次都走完整流程，simple bug fix 可以只用 systematic-debugging + verification
4. **CI 整合**——將 verification-before-completion 的理念延伸到 CI pipeline，確保 agent 的產出通過 automated gate
5. **自定義 skill**——當團隊出現重複性的流程問題，投資撰寫對應的 skill 比反覆在 prompt 中提醒更可靠

> [!warning] 適用場景判斷
> Superpowers 的最大效益出現在 **long-lived、quality-critical 的專案**。對於一次性腳本、快速 prototype、或團隊已有成熟 AI workflow 的場景，導入成本可能高於收益。

---

## 小結

Superpowers 解決的核心問題是：**AI agent 的工程紀律不能依賴 prompt-level 的軟性要求，需要 workflow-level 的硬性閘門。**

它不改變 AI 的能力上限，但顯著提升品質下限——透過 composable skills 將 TDD、systematic debugging、code review 等實踐從「最佳建議」轉變為「強制流程」。對於已經在生產環境中使用 AI coding agent 的團隊，這是在現有工具鏈上附加工程紀律的低摩擦方案。

```bash
# Claude Code
/plugin install superpowers@claude-plugins-official

# Cursor
/add-plugin superpowers
```
