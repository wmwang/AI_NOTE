# Claude Code Subagents：專業分工，讓 AI 幫你管理 AI

Claude Code 有個你可能沒注意過的功能：它可以把任務「外包」給另一個專門訓練過的小 agent，自己只負責統籌和整合結果。這個機制叫做 **Subagent**，用好了可以讓工作效率大幅提升，同時避免一個很麻煩的問題——context 爆炸。

---

## 先搞清楚一件事：Context Window 會爆

在說 Subagent 之前，得先理解為什麼需要它。

Claude Code 的對話有上限，這個上限叫做 **context window**，目前大約是 200K tokens（大概等於 15 萬個中文字）。聽起來很多，但隨著對話越來越長：

- 你發的每條訊息都在累積
- Claude Code 讀檔案的內容也在累積  
- tool call 的結果也在累積

到最後，context 塞滿了兩個問題：

1. **成本變高**：每次請求要傳送的 token 越來越多
2. **品質變差**：context 裡充滿無關的舊內容，Claude 越來越難專注在當前任務上

```
一個對話的 Context 成長示意：

Turn 1  ████░░░░░░░░░░░░░░░░  10K tokens (5%)
Turn 2  ████████░░░░░░░░░░░░  30K tokens (15%)
Turn 3  ██████████████░░░░░░  90K tokens (45%)
Turn 4  ████████████████████  180K tokens (90%)
Turn 5  ⚠️ CONTEXT LIMIT 接近
```

Subagent 就是為了解決這個問題而生的。

---

## Subagent 怎麼解決這個問題？

概念很簡單：**主 agent 把任務外包給 subagent，subagent 用自己的 context 空間工作，完成後只回傳一份精簡的結果給主 agent**。

類比：你（主 agent）給助理（subagent）一張便條紙寫任務，助理去做完後交一份報告給你。助理做事過程中查了哪些資料、讀了哪些檔案，都不會佔用你的記憶，你只需要看最後的報告。

```
主 Agent                      Subagent
   │                              │
   │── 建立任務 prompt ──────────→│
   │                              │ 用全新的 context
   │                              │ 讀檔、分析、工作
   │                              │ (60K tokens 的工作量)
   │←── 回傳精簡結果 (5K tokens) ─│
   │
   │（主 agent context 只增加 5K，不是 60K）
```

這樣主 agent 的 context 保持精簡，對話品質不會因為累積過多雜訊而下降。

---

## Subagent 的三個核心屬性

每個 subagent 都有三件事你可以控制：

| 屬性 | 說明 | 為什麼重要 |
|------|------|-----------|
| **系統提示 (System Prompt)** | 定義這個 agent 的角色、能力和工作方式 | 決定它怎麼思考、輸出什麼格式 |
| **工具權限 (Tools)** | 指定它能用哪些工具（Read、Write、Bash...） | 遵守最小權限原則，避免 tool pollution |
| **Context 隔離** | 每次呼叫都是全新的 context，不繼承主對話歷史 | 保持主 agent context 精簡 |

---

## Subagent 設定檔長什麼樣？

Subagent 是一個 Markdown 檔案，存在 `.claude/agents/` 目錄下。格式如下：

```markdown
---
name: code-reviewer
description: 當需要 code review 時使用此 agent。
             分析程式碼品質、潛在 bug 和安全問題。
             關鍵字觸發：review、審查、code review
tools: Read, Grep, Glob
model: sonnet
---

你是一位嚴謹的資深工程師，負責 code review。

## 工作流程
1. 讀取指定的程式碼檔案
2. 分析以下面向：
   - 程式碼品質（命名、結構、可讀性）
   - 潛在 bug（邊界條件、錯誤處理）
   - 安全問題（SQL injection、XSS、權限驗證）
3. 依嚴重程度分類輸出（Critical / Warning / Suggestion）

## 輸出格式
每個問題包含：位置、問題說明、影響、建議修正方式
```

**重點說明：**

- **YAML frontmatter（`---` 之間的部分）**：給主 agent 看的，決定何時呼叫這個 subagent、能用什麼工具
- **`---` 之後的內文**：subagent 自己的系統提示，主 agent 看不到這部分
- **`description` 欄位**：這是最關鍵的欄位，下一節會重點說明

---

## Description 欄位：你控制 Subagent 行為的最重要旋鈕

`description` 不只是說明文字，它會被附加到主 agent 的系統提示裡。這意味著：

**主 agent 根據 description 決定：**
1. 什麼時候呼叫這個 subagent
2. 如何構建傳給 subagent 的 prompt

換句話說，description 同時影響「觸發時機」和「任務說明品質」。

**範例：description 的好壞對比**

```markdown
# 差的 description（太模糊）
description: 用於程式碼相關任務

# 好的 description（有觸發時機 + 能力說明 + 範例）
description: 當需要審查程式碼品質、分析潛在 bug 或安全漏洞時使用。
             接收檔案路徑，輸出結構化的審查報告。
             觸發情境：使用者說「review」、「審查」、「幫我看一下這段程式」
```

好的 description 讓主 agent 知道什麼時候該叫誰出來做事，以及要怎麼跟它說清楚任務。

---

## 實際操作：建立一個 Code Reviewer Subagent

### 步驟一：用 /agents 指令建立

```bash
# 在 Claude Code 中輸入
/agents
```

選擇「Create new agent」，依序設定：

1. **描述**：定義角色和觸發時機（這會成為 description 欄位）
2. **工具**：選「Read-only tools」（Read、Grep、Glob）
   - Code reviewer 不需要寫入或執行，給太多工具是 tool pollution
3. **Model**：選 Sonnet（平衡效能和成本）

### 步驟二：確認產出的設定檔

建立完成後，會在 `.claude/agents/code-reviewer.md` 出現：

```markdown
---
name: code-reviewer
description: 當需要進行 code review 或程式碼審查時使用。
             分析程式碼的品質、安全性和效能問題。
             在使用者提到 review、審查、檢查程式碼時觸發。
tools: Read, Grep, Glob
model: sonnet
---

你是一位嚴謹、有豐富實戰經驗的資深工程師...
（以下是系統提示內容）
```

### 步驟三：測試

建一個簡單的測試檔案：

```python
# test_target.py - 這個檔案有一些明顯問題
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL injection 風險
    result = db.execute(query)
    return result

def divide(a, b):
    return a / b  # 沒有處理除以零的情況
```

然後呼叫 subagent：

```
review @test_target.py
```

Claude Code 會自動判斷需要 code review，呼叫 `code-reviewer` subagent，subagent 在自己的 context 裡讀取並分析檔案，最後回傳審查報告給主 agent。

---

## Tool Pollution：別給 Agent 用不到的工具

這是個容易忽略但很重要的概念。

每個工具定義（包含工具名稱、說明）都會佔用 subagent 的 context 空間。如果給了 30 個工具，subagent 的 context 一開始就被工具定義佔去一大塊，真正用來工作的空間就少了。

更重要的是安全性：一個只負責讀程式碼的 code reviewer，如果給了 Bash 工具，就有執行系統指令的能力。這違反了**最小權限原則**。

| Subagent 類型 | 建議工具 | 不需要的工具 |
|--------------|---------|------------|
| Code Reviewer | Read, Grep, Glob | Bash, Write, Edit |
| 文件生成器 | Read, Write | Bash, WebSearch |
| 測試執行器 | Read, Bash | Write, WebFetch |
| 架構分析師 | Read, Grep, WebSearch | Write, Edit, Bash |

---

## 進階：一次派出多個 Subagent 平行工作

Subagent 的真正威力在這裡。不是一個一個呼叫，而是**同時派出多個，每個做不同版本，最後從中選最好的**。

**使用場景：同時生成三種 UI 設計方案**

假設你要設計一個登入頁面的 Hero 區塊，但不確定哪種風格最好：

```
幫我平行生成三個不同風格的 LoginHero 元件：
1. Minimal：極簡白底，重視空白感
2. Dark：深色系，科技感
3. Gradient：漸層背景，現代感

每個輸出到 src/components/hero/ 目錄下，
各自命名為 LoginHeroMinimal.tsx、LoginHeroDark.tsx、LoginHeroGradient.tsx
請用 parallel 方式同時生成，不要一個一個來
```

Claude Code 的主 agent 會同時派出三個 subagent，各自在獨立的 context 空間實作自己的版本。你可以在終端機看到三個 agent 同時執行的進度。

完成後，三個版本都存在了，你可以：
1. 在瀏覽器並排比較
2. 選出最喜歡的一個
3. 刪掉其他兩個

這種「多版本並行 + 人工選優」的工作方式，把 AI 的「可以快速生成多種嘗試」的特性發揮到最大。

> **注意成本**：多個 subagent 並行執行，每個都會消耗獨立的 token。如果任務複雜，token 用量會比較高，執行前確認你的 API 配額。

---

## 本篇重點整理

| 概念 | 核心要點 |
|------|---------|
| **為什麼需要 Subagent** | 主 agent context 有限，subagent 幫你隔離工作的 context 消耗 |
| **Subagent 設定位置** | `.claude/agents/` 目錄（專案級）或 `~/.claude/agents/`（使用者級） |
| **最重要的欄位** | `description`：影響主 agent 何時呼叫、如何描述任務 |
| **工具選擇原則** | 最小權限，只給任務真正需要的工具 |
| **並行執行** | 指示「parallel」或「同時」，主 agent 會同時派出多個 subagent |

**三個立即可以做的事：**

1. 輸入 `/agents` 看看你目前有哪些 subagent（內建有 general-purpose）
2. 建立一個 `code-reviewer` subagent，設定只給 Read-only 工具，下次 review 程式碼時用它
3. 如果有個任務要生成多個版本（例如不同的 commit message 風格、不同設計方案），試試在 prompt 裡加上「平行生成 3 個版本」，體驗一下多 agent 並行的速度

---

## 附錄：Subagent vs 直接用主 Agent

| 情境 | 建議方式 |
|------|---------|
| 簡單、一次性的任務 | 直接用主 agent |
| 需要重複執行的專業任務 | 建立 subagent |
| 對話已經很長、context 快滿 | 用 subagent 隔離後續工作 |
| 想要多個版本讓你選 | 多個 subagent 並行 |
| 任務需要特定限制（只能讀不能寫） | subagent + 指定工具權限 |
