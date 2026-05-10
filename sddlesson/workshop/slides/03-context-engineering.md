---
marp: true
theme: default
paginate: true
backgroundColor: #0f172a
color: #f1f5f9
style: |
  section { font-family: 'Noto Sans TC', sans-serif; font-size: 26px; }
  h1 { color: #38bdf8; font-size: 1.8em; }
  h2 { color: #7dd3fc; border-bottom: 2px solid #38bdf8; padding-bottom: 8px; }
  h3 { color: #bae6fd; }
  code { background: #1e293b; color: #a5f3fc; padding: 2px 6px; border-radius: 4px; }
  pre { background: #1e293b; border-left: 4px solid #fbbf24; font-size: 0.8em; }
  table { border-collapse: collapse; width: 100%; }
  th { background: #1e3a5f; color: #7dd3fc; }
  td, th { padding: 8px 12px; border: 1px solid #334155; }
  blockquote { border-left: 4px solid #fbbf24; color: #94a3b8; background: #1e293b; padding: 12px 16px; }
---

# M3：Context Engineering

## 設計穩定、可複用的 Prompt

> 時間：25 分鐘（講授 15 分鐘 + 練習 10 分鐘）

---

<!-- _notes:
休息後的第一個模組，可能需要 2 分鐘讓大家回神。
Context Engineering 這個詞是 Addy Osmani 和 Google 工程師提出的，描述「如何有效地給 AI 提供背景資訊」。

這個模組解答了很多人的困惑：「為什麼我用 ChatGPT 每次得到不一樣的答案？」
-->

---

# 為什麼你的 Prompt 不穩定？

<br>

**同樣一個需求，給 AI 不同的 context，結果完全不同：**

```
❌ 不穩定的 Prompt（缺 context）：
"幫我寫一個購物車的測試"

→ 結果：AI 猜測語言、框架、測試風格...
   每次輸出都不同，你花時間修正
```

```
✅ 穩定的 Prompt（有 context）：
"根據以下 ISA-Level Gherkin，使用 TypeScript + Jest 生成
 Step Definitions。格式參考：[範例]。Gherkin：[貼入]"

→ 結果：穩定、可預期、一次就對
```

---

<!-- _notes:
問大家：「你有沒有遇到過，問 AI 同一個問題，今天和昨天的答案不一樣？」

原因不是 AI 變笨了，而是每次對話的 context 不同。AI 在「填補你沒說的部分」時，每次填的不一樣。

解法：把你的 context 結構化，讓 AI 不需要猜。
-->

---

# Context Engineering 三要素

<br>

```
✦ 給角色（Role）
  "你是一位熟悉 BDD 的 TypeScript 資深工程師"
  → 影響：思維框架、使用的術語、輸出風格

✦ 給格式（Format）
  "請輸出 Gherkin + Step Definition，不要其他說明"
  → 影響：輸出結構，避免 AI 加入不需要的內容

✦ 給範例（Examples）
  貼一個已完成的正確範例作為 few-shot
  → 影響：品質下限，讓 AI 對齊你的標準
```

---

<!-- _notes:
這三個要素來自 agent-skills 裡的 context-engineering 技能。
逐一說明：

1. Role：就像你在雇用一個顧問，先告訴他他的背景是什麼。
   "你是一位資深 TDD 工程師" vs "幫我寫測試" → 差很多。

2. Format：AI 默認會加很多解釋文字。你如果只需要程式碼，要明說。
   "只輸出程式碼，不要任何解釋" → 讓輸出直接可用。

3. Examples（Few-shot）：這是最強的工具。
   給一個輸入/輸出的例子，AI 的模仿能力非常強。
   這樣可以把你的「隱性標準」變成「顯性規格」。
-->

---

# 好 Prompt 的結構

<br>

```
[角色]
你是一位 [專業角色]，擅長 [特定技術/方法]。

[任務]
請根據以下 [輸入類型]，[動詞] [輸出類型]。

[規則/限制]
- 規則 1
- 規則 2
- 規則 3

[格式/範例]（選填）
格式參考：[範例輸入] → [範例輸出]

[輸入]
[貼入你的輸入]
```

---

<!-- _notes:
這個結構適用於 80% 的開發用 Prompt。
讓大家把這個結構記下來（或者參考講義的速查表）。

強調：這個結構不是死規定，是思考框架。有時候 [格式/範例] 不需要，有時候規則可以更簡單。
重要的是：每個部分都有它的用途，不要漏掉角色和規則。
-->

---

# 情境化 Prompt vs. 通用 Prompt

<br>

| | 通用 Prompt | 情境化 Prompt |
|--|------------|--------------|
| **角色** | 無 | "資深 TypeScript 工程師" |
| **規格** | 口頭描述 | ISA-Level Gherkin |
| **格式** | 未指定 | "Jest describe/it 結構" |
| **範例** | 無 | 貼一個已完成的測試 |
| **輸出穩定度** | 低 | 高 |
| **需要修改次數** | 3-5 次 | 0-1 次 |

---

<!-- _notes:
讓大家對比這兩種 Prompt 的差異。
「需要修改次數」這個指標很直接：情境化 Prompt 讓你大部分時候第一次就對。

這就是「給 AI 更多 context」的投資報酬率。
花 5 分鐘設計一個好 Prompt，省下 30 分鐘的來回修改。
-->

---

# Prompt 模板化：讓成果可複用

<br>

**把好的 Prompt 存起來，下次直接用：**

```markdown
# Gherkin → Jest 測試模板

## 用途
給定 ISA-Level Gherkin，生成 TypeScript + Jest 測試骨架

## Prompt
---
你是一位資深 TDD 工程師，熟悉 TypeScript 和 Jest 測試框架。
根據以下 ISA-Level Gherkin，生成 Jest 測試程式碼骨架。

規則：
- 只生成測試，不實作被測函式
- Given → beforeEach + 變數宣告
- When → 函式呼叫，結果存入變數
- Then → expect() assertions
- 錯誤情境用 expect(...).rejects.toThrow()

ISA Gherkin：
{{GHERKIN}}
---
```

---

<!-- _notes:
這就是 Prompt 模板化的概念。
建議大家建立一個 prompt-library.md（今天的講義裡有一個起點），把每個常用的 Prompt 存起來。

好處：
1. 不用每次重新思考 Prompt 結構
2. 團隊可以共享同一套 Prompt 庫
3. 可以持續改進 Prompt（版本控制）

建議把 Prompt 存在 Git repo 裡，這樣整個團隊都能用，也能追蹤哪個版本的 Prompt 效果更好。
-->

---

# Agent-Skills 哲學：Source-Driven Development

<br>

> 「每一個框架決策都應該基於官方文件，而不是 AI 的記憶。」
> — Addy Osmani, agent-skills

<br>

**實作：給 AI 看官方文件，而不是讓它靠記憶**

```
# 不夠好的 Prompt
"用 Zod 做表單驗證"

# 更好的 Prompt
"根據以下 Zod v3.22 文件片段，
 為以下 schema 寫驗證邏輯：
 [貼入官方文件]
 Schema 需求：[貼入]"
```

---

<!-- _notes:
這是 agent-skills 裡的 source-driven-development 概念。
AI 的記憶會過時，尤其是 npm 套件的 API 常常改版。
最安全的做法：把官方文件（或 changelog）貼進 Prompt，讓 AI 根據文件生成，而不是靠「我記得這個 API 長這樣」。

這個技巧特別適合：
- 新發布的框架版本
- 你不熟悉的套件
- 有破壞性更新的版本
-->

---

# Exercise 3：改造你的 Prompt

<br>

**時間：10 分鐘**

拿出 Ex2 你用過的 Prompt，用以下框架重新設計：

1. **加入角色**：指定一個具體的工程師身份
2. **加入格式規則**：至少 3 條限制
3. **加入一個 few-shot 範例**（可以用 Ex2 的輸出當範例）
4. 用改造後的 Prompt 重新生成，比較結果

📄 請使用練習題 `exercises/ex03-prompt.md`

---

<!-- _notes:
10 分鐘。
這個練習的目的是讓大家「親手體驗」Prompt 改造前後的差異。
重要提示：告訴大家，如果他們在 Ex2 的 Prompt 已經很好，可以試著設計一個全新情境的 Prompt。

結束後簡短討論：改造前後有什麼差異？輸出品質有提升嗎？
-->

---

# M3 總結

<br>

| 概念 | 實作方式 |
|------|----------|
| 給角色 | "你是一位 [具體角色]" |
| 給格式 | 列出輸出規則和限制 |
| 給範例 | Few-shot：貼一個輸入/輸出對 |
| 源文件驅動 | 貼官方文件，不靠 AI 記憶 |
| Prompt 模板化 | 存在 prompt-library.md，版本控制 |

<br>

> 好的 Prompt 是資產，不是一次性的提問。

---

<!-- _notes:
Context Engineering 的核心就是這些。
最後那句話很重要：好的 Prompt 要存下來、分享出去、持續優化。
把 Prompt 當程式碼一樣對待——它也需要 review、版本控制、和維護。
-->
