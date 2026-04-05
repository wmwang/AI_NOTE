---
title: Claude Code + OpenSpec + Superpowers 三工具協同開發實戰指南
date: 2026-04-05
tags:
  - Claude Code
  - OpenSpec
  - Superpowers
  - AI工具
  - 開發效率
aliases:
  - 三工具協同開發
  - AI協同開發指南
---

# Claude Code + OpenSpec + Superpowers：一套讓 AI 真正聽話的開發組合拳

單獨用 Claude Code 寫程式很爽，但你可能也踩過這個坑：跟 AI 說「加個登入功能」，它 5 分鐘後交出一堆程式碼，結果你要的是 JWT，它給你做了 Session。這篇文章介紹一套三工具協同工作流，讓 AI 在有紀律的約束下開發，大幅減少返工。

## 為什麼一個工具不夠用？

說白了，三個工具各有盲點：

| 工具 | 單獨使用的問題 |
|------|--------------|
| **只用 Claude Code** | 需求沒對齊，AI 自由發揮，返工成本高 |
| **只用 OpenSpec** | 有規範文件，但 AI 跑到一半還是會偏離 |
| **只用 Superpowers** | 有工程紀律，但 Plan 基於什麼需求？AI 自己猜的 |

三者搭配起來，分工才清楚：

- **OpenSpec**：負責需求對齊與規格沉澱（事實的唯一來源）
- **Superpowers**：負責工程紀律與流程約束
- **Claude Code**：負責程式碼執行與工具呼叫

---

## 安裝與設定（10 分鐘搞定）

**Claude Code**（macOS/Linux）：
```bash
curl -fsSL https://claude.ai/install.sh | bash
```
> 需要 Claude Pro、Team 或 Enterprise 訂閱，免費版不支援。

**OpenSpec**：
```bash
npm install -g @fission-ai/openspec@latest
cd your-project && openspec init
# 初始化時選擇 Claude Code
```

初始化後會產生 `openspec/` 目錄，包含 `specs/`（規格）、`changes/`（進行中的變更）、`AGENTS.md`（AI 讀取的指令）。

**Superpowers**：
```bash
# 在 Claude Code 中執行
/plugin install superpowers@claude-plugins-official
```

**設定權限**（`/.claude/settings.json`）：
```json
{
  "permissions": {
    "allow": ["Bash:npm:*", "Bash:git:*", "Bash:pnpm:*"],
    "deny": ["Bash:rm -rf *", "Bash:sudo *"]
  }
}
```

---

## 核心工作流：四個階段

### 階段一：OpenSpec 需求對齊

老闆說「加個使用者登入功能」，你的第一步不是開始寫程式，而是：

```
claude
> /opsx:propose 使用者登入功能
```

AI 會生成四個文件：`proposal.md`（為什麼做）、`specs/`（行為變更規格）、`design.md`（技術方案）、`tasks.md`（實作清單）。

**最重要的一個習慣**：在 `proposal.md` 裡寫清楚 **Out of Scope（範圍外）**，例如「不包含第三方登入」、「不包含雙因素驗證」。這一步能防止 AI「過度幫助」。

Review 完後：
```
> 提案確認，繼續
```

---

### 階段二：Superpowers Brainstorming 細化設計

提案確認後，Superpowers 會自動啟動 Brainstorming，用蘇格拉底式問答逐一確認設計細節：

```
1. 使用者資料存哪裡？（現有 PostgreSQL？還是新服務？）
2. 密碼加密用什麼算法？（bcrypt 還是 argon2？）
3. JWT 過期策略：Access Token 多久？Refresh Token 多久？
4. 登入失敗幾次後鎖定帳號？
```

你逐一回答後，AI 會把決策記錄進 `design.md`，包括**選擇了什麼**和**為什麼這樣選**。這份文件在未來維護時非常有用。

---

### 階段三：Superpowers Writing Plans 拆解任務

Brainstorming 完成後，自動進入 Plan 撰寫。生成的 `tasks.md` 會把功能拆成每個 2-5 分鐘可完成的小任務，並明確列出驗收標準與測試要求。

> [!tip] Review Plan 是關鍵步驟
> 直接按確認是最常見的錯誤。執行到一半才發現任務順序錯了（例如應該先建 JWT 工具再做登入 API），代價很高。養成先打開 `tasks.md` 掃一遍的習慣。

```
> 任務 3 和任務 4 順序反了，應該先實作 JWT 再做登入 API
# AI 修改後再確認
> Plan 確認，開始執行
```

---

### 階段四：Subagent 自動執行

確認後，Superpowers 啟動 subagent-driven-development，進入全自動模式：

- **TDD 強制執行**：先寫測試，再寫程式碼
- **兩階段 Review**：Spec 合規性檢查 + 程式碼品質檢查
- **自動修復**：測試失敗時自動調試（例如發現 bcrypt 未安裝，自動補裝）
- **進度追蹤**：即時更新 `tasks.md` 的 checkbox

---

## 三個最常見的踩坑點

**1. 跳過 Brainstorming**：直接叫 AI 寫程式，需求沒對齊，最後返工。正確做法是讓 Superpowers 自動觸發問答流程。

**2. 不 Review Plan**：Plan 生成後直接確認，執行到一半才發現方向不對。

**3. 沒設定權限**：預設允許所有指令，AI 可能執行危險操作。務必在 `settings.json` 中明確設定 `deny` 清單。

---

## 進階技巧：加速與並行

**Fast-Forward 模式**（小功能適用）：
```
> /opsx:ff 使用者登入
# 一次性生成 proposal + specs + design + tasks，跳過逐步確認
```

**並行執行**（獨立任務同時跑）：
```json
// .claude/settings.json
{ "maxSubagents": 3 }
```
「密碼工具」和「JWT 工具」這種互相獨立的任務可以並行，節省時間但會增加 Token 消耗。

---

## 這套工作流適合你嗎？

| 場景 | 適合？ |
|------|--------|
| 中型以上功能（>4 小時） | ✅ 強烈推薦 |
| 多人協作專案 | ✅ 規格文件讓團隊同步 |
| 生產環境程式碼 | ✅ TDD + Code Review 有保障 |
| 快速原型（<1 小時） | ❌ 太重，直接問 AI 就好 |
| 一次性腳本 | ❌ 不值得 |
| 需求完全不明確的探索期 | ❌ 先把需求想清楚再來 |

---

## 下一步

1. **今天就試試看**：找一個你手邊正在開發的中型功能，用 `/opsx:propose` 開始，光是這一步就能讓你想清楚「範圍到底是什麼」。
2. **先不要管並行**：第一次用這套流程，關掉 maxSubagents，專心跑完一個完整的循環，搞懂每個階段在做什麼再說。
3. **留下 design.md**：這套工作流最被低估的價值不是生成程式碼，而是把設計決策記錄下來。三個月後回來看，你會感謝當時的自己。

---

*參考來源：知乎文章《Claude Code + OpenSpec + Superpowers：AI 協同開發實戰指南》（2026-03-27）*
*相關筆記：[[真實C++專案實測_四大Claude_Code工作流比較]]*
