# Context Engineering：AI Agent 真正的核心不是模型，是 Context

很多人學 Claude Code 是從「怎麼下 prompt」開始，但這本書第一章就直接點破：**真正決定 AI agent 好不好用的，不是模型，是 context 的管理方式**。這個概念叫做 Context Engineering（情境工程），理解它會讓你對 Claude Code 的每個設計決策都有更深的領悟。

---

## Prompt Engineering 已經不夠用了

早期用 AI，我們相信「寫好 prompt 就能解決問題」。但現實是：**prompt 是靜態的，工作是動態的**。

當 AI agent 開始長時間執行複雜任務，它需要讀檔案、呼叫工具、查資料、處理錯誤——每一步都產生新的資訊，這些資訊都要塞進 context window 裡。到了某個點，context 會開始爆炸，agent 的表現跟著退化。

Context Engineering 就是在解決這個問題：**不只是「怎麼寫 prompt」，而是「整個對話過程中，什麼資訊要進來、什麼要壓縮、什麼要隔離」**。

---

## Context 失控的三大問題

如果不管理 context，會出現三種讓人崩潰的情況：

| 問題 | 說明 | 常見症狀 |
|------|------|---------|
| **Context Poisoning**（中毒） | 錯誤的資訊進了 context，開始影響後續輸出 | 明明修好的 bug 又出現，Claude 說「根據之前的討論...」但那個討論是錯的 |
| **Context Confusion**（混淆） | 不相關的 context 干擾了當前任務 | 在寫後端 API 時，Claude 突然提到前端的設計規範 |
| **Context Clash**（衝突） | Context 裡不同部分互相矛盾 | CLAUDE.md 說「用 TypeScript」，但對話歷史裡有個範例是用 JavaScript |

---

## Claude Code 的四個 Context 管理策略

### 策略一：寫入 Context（Write Context）— 持久記憶體

Claude Code 有三層記憶體，讓 context 在對話結束後還能留存：

**第一層：專案記憶體 `./CLAUDE.md`**

放在專案根目錄，跟著 git 走，整個團隊共享。適合放：
- 技術棧說明（用什麼框架、資料庫）
- Coding 規範（命名風格、測試規則）
- 特殊注意事項（不要動 legacy-auth 這個資料夾）

```markdown
# Project Context

## Tech Stack
- Node.js + Express（API）
- React + TypeScript（前端）
- PostgreSQL + Prisma（資料庫）

## Coding Standards
- 所有 API 回傳都要有 error handling
- TypeScript 要明確標型別，不用 any
- Commit message 用 Conventional Commits 格式
```

**第二層：使用者記憶體 `~/.claude/CLAUDE.md`**

存在你自己的電腦，不進 git，跨所有專案有效。適合放個人偏好：

```markdown
# 我的個人偏好

## 程式碼風格
- 函式命名用 camelCase
- 變數要有意義，不用 temp、data 這種名字
- 永遠先跑 npm run lint 再問我要不要 commit
```

**第三層：動態記憶體匯入**

在任何 CLAUDE.md 裡用 `@` 引用其他檔案：

```markdown
@./docs/api-spec.md
@./context/database-schema.md
```

這讓你可以把 context 拆成多個檔案，按需組合，不用全部堆在一個大 CLAUDE.md 裡。

---

### 策略二：選取 Context（Select Context）— 只載入需要的

Claude Code 不會把所有東西一次全塞進 context，它會根據任務動態決定要載入什麼。

你可以用 Hooks 讓這個過程自動化。例如，根據 git branch 自動切換 context：

```bash
#!/bin/bash
# context-switcher.sh — 根據 branch 決定要載入什麼 context

CLAUDE_MD="CLAUDE.md"
branch=$(git branch --show-current 2>/dev/null)

add_context() {
  local ref="$1"
  grep -qxF "$ref" "$CLAUDE_MD" || echo "$ref" >> "$CLAUDE_MD"
}

case $branch in
  feature/auth-*)
    add_context "@./context/auth-system.md"
    ;;
  feature/payment-*)
    add_context "@./context/payment-flow.md"
    ;;
  hotfix/*)
    add_context "@./context/production-runbook.md"
    ;;
esac
```

把這個腳本接到 `UserPromptSubmit` hook，每次你送 prompt 時就自動根據當前 branch 更新 context。

---

### 策略三：壓縮 Context（Compress Context）— 不讓 context 無限膨脹

對話進行到一半，context window 快滿了怎麼辦？兩個指令：

- **`/clear`**：清掉對話歷史，但保留 CLAUDE.md 的設定。適合「這個對話跑歪了，重新開始」
- **`/compact`**：把對話歷史壓縮成摘要，保留重要決策，捨棄細節。適合「對話很長但還想繼續」

什麼時候該用哪個：

| 情況 | 建議 |
|------|------|
| 對話方向跑歪，想重來 | `/clear` |
| 對話很長，Claude 開始答非所問 | `/compact` |
| 要開始全新的任務 | `/clear` |
| 同一個任務繼續但 context 快滿 | `/compact` |

---

### 策略四：隔離 Context（Isolate Context）— 用 Subagents 切割工作

最強的策略：把不同任務交給不同的 subagent，每個 subagent 有自己乾淨的 context，不會互相污染。

類比：你（主 agent）是專案經理，你不會記住每個細節，你把任務分給不同的工程師（subagents），每個人專注做自己的事，最後向你匯報結果。

```
主 agent（你）
  ├── code-reviewer subagent：專注審查程式碼品質
  ├── test-writer subagent：專注撰寫測試
  └── research subagent：專注查文件和最佳實踐
```

每個 subagent 用自己的 context window 工作，結束後只回傳一份精簡的結果給主 agent。主 agent 的 context 不會被每個 subagent 的工作細節撐爆。

---

## System Prompt 的「金髮女孩區」

原書這個概念很實用，值得單獨說明。

設計 system prompt（包括 CLAUDE.md）時，存在一個甜蜜點，Anthropic 稱之為 **Goldilocks Zone**：

| 過於具體 | 剛剛好 | 過於模糊 |
|---------|-------|---------|
| 「如果使用者說 X，回答 Y；如果說 A，問三個問題」 | 「目標是高效解決問題，使用這個框架思考，這些情況轉給人工」 | 「做正確的事，有需要就升級」 |
| Claude 變成死板的狀態機 | Claude 有智慧地判斷、靈活處理 | Claude 不知道「正確」是什麼 |
| 每個新情況都要改 prompt | 新情況自然處理 | 行為不一致 |

**好的 system prompt 的特徵：**
- 清楚定義角色和範疇（「你是負責訂單的客服，不處理行銷問題」）
- 給原則而不是規則（「選最簡單的解法」而不是列出每種解法）
- 提供思考框架（「先理解問題，再蒐集資訊，再提出方案」）
- 明確說明邊界（「法律問題一律轉人工」）

---

## 本篇重點整理

| 概念 | 核心要點 |
|------|---------|
| **Context Engineering** | 比 Prompt Engineering 更深，管理的是整個對話過程中的資訊流 |
| **三層記憶體** | 專案 CLAUDE.md（共享）、使用者 CLAUDE.md（個人）、動態匯入（彈性） |
| **Context 壓縮** | `/compact` 壓縮歷史，`/clear` 清除重來 |
| **Context 隔離** | Subagents 各自有乾淨 context，避免互相污染 |
| **Goldilocks Zone** | System prompt 要夠具體讓 Claude 知道怎麼做，又要夠靈活讓它能判斷新情況 |

**三個立即可以做的事：**

1. 檢查你的專案有沒有 `CLAUDE.md`，如果沒有，現在就建一個，把技術棧和最重要的規範寫進去
2. 在 `~/.claude/CLAUDE.md` 寫下你的個人偏好，讓 Claude 在所有專案都記得你的習慣
3. 下次對話開始變長、Claude 的回答感覺跑掉時，試試 `/compact` 看看效果
