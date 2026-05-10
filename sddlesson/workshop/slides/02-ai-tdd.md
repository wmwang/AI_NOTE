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
  pre { background: #1e293b; border-left: 4px solid #38bdf8; font-size: 0.8em; }
  table { border-collapse: collapse; width: 100%; }
  th { background: #1e3a5f; color: #7dd3fc; }
  td, th { padding: 8px 12px; border: 1px solid #334155; }
  blockquote { border-left: 4px solid #34d399; color: #94a3b8; background: #1e293b; padding: 12px 16px; }
  .red { color: #f87171; }
  .green { color: #34d399; }
  .blue { color: #60a5fa; }
---

# M2：AI × TDD

## Red-Green-Refactor × AI 加速

> 時間：45 分鐘（講授 20 分鐘 + 實作 25 分鐘）

---

<!-- _notes:
Module 2 是整個工作坊最核心的技術模組。
目標：讓大家走完一次完整的 AI x TDD 循環，從 Gherkin 到有測試保護的程式碼。

預計 20 分鐘講，25 分鐘做 Exercise 2（這是主要的動手練習）。
-->

---

# TDD 的核心：先畫靶，後射箭

<br>

```
   🔴 RED         🟢 GREEN       🔵 REFACTOR
   ─────────      ──────────     ──────────
   寫一個          寫最少的        重構程式碼
   會失敗的        程式碼讓        確保測試仍
   測試            測試通過        通過
```

<br>

> **關鍵心態：測試是「規格的可執行形式」**
> 不是「寫完程式再補的東西」

---

<!-- _notes:
TDD 不是新概念，但很多人知道卻不做。
問：「你們團隊有在做 TDD 嗎？」→ 通常大家都搖頭。
原因：寫測試很麻煩，要維護兩份程式碼。

AI 的出現改變了這個等式：AI 可以幫你寫測試。你的工作是「指定目標（Gherkin）」，AI 的工作是「生成測試和實作」。
-->

---

# AI 在 TDD 的哪個位置？

<br>

```
你做的事                    AI 做的事
────────────                ──────────────
Discovery（需求探索）
↓
撰寫 DSL Gherkin ────→      Gherkin 轉 ISA Level（協助）
↓
展開 ISA Gherkin ────→      生成測試程式碼（自動）
↓
執行測試（RED）
↓
                   ←────    生成最小實作（Green Phase）
↓
執行測試（GREEN）
↓
                   ←────    重構建議（Refactor）
↓
程式碼 Review
```

---

<!-- _notes:
這張圖是整個工作坊最重要的圖之一。
強調：你做「策略」（決定要做什麼），AI 做「戰術」（怎麼實現）。

「展開 ISA Gherkin」和「執行測試」這兩步是你必須做的，其他的都可以讓 AI 大量協助。

這樣的分工模式，開發速度可以提升 3-5 倍，但品質不會下降。
-->

---

# Prompt 1：Gherkin → 測試程式碼

<br>

```
你是一位資深 TDD 工程師。
請根據以下 ISA-Level Gherkin Scenario，生成 TypeScript + Jest 的測試程式碼。

規則：
- 只生成測試，不實作被測函式
- Given → Arrange（準備測試資料）
- When  → Act（呼叫被測函式）
- Then  → Assert（用 expect() 驗證）
- 測試函式名稱要清楚描述情境（中文可以）

ISA Gherkin：
[貼入你的 ISA-Level Gherkin]
```

---

<!-- _notes:
現場示範這個 Prompt。把 M1 最後的「個人資料修改」ISA Gherkin 貼進去，讓大家看到 AI 生成的測試。

重點強調：
1. 給角色：「資深 TDD 工程師」→ 讓 AI 知道要用什麼思維
2. 給規則：明確說明 Given/When/Then 的對應方式
3. 只要測試，不要實作：這是 RED Phase，先讓測試存在
-->

---

# Demo：Prompt 1 的輸出

<br>

```typescript
describe('個人資料更新', () => {
  let userService: UserService;

  beforeEach(() => {
    userService = new UserService(new InMemoryUserRepository());
  });

  it('成功更新暱稱', async () => {
    // Arrange
    await userService.createUser({ id: 'u001', nickname: 'alice_old' });

    // Act
    const result = await userService.updateProfile('u001', {
      nickname: 'alice_new',
    });

    // Assert
    expect(result.nickname).toBe('alice_new');
  });

  it('暱稱為空時應拋出驗證錯誤', async () => {
    await userService.createUser({ id: 'u001', nickname: 'alice_old' });

    await expect(
      userService.updateProfile('u001', { nickname: '' })
    ).rejects.toThrow('NICKNAME_REQUIRED');
  });
});
```

---

<!-- _notes:
讓大家看一下這個輸出。注意幾件事：
1. AI 自動推導出 UserService 這個介面（從 Gherkin 的語意）
2. 使用了 in-memory repository（不需要真實 DB）
3. 測試名稱清楚描述情境
4. 錯誤碼是 'NICKNAME_REQUIRED'（具體的錯誤識別符）

這個測試現在是 RED（因為 UserService 還不存在）。
-->

---

# Prompt 2：測試 → 最小實作（GREEN Phase）

<br>

```
以下是一組已存在的 failing 測試（RED Phase）。
請實作最小的程式碼讓這些測試通過。

規則：
- 不要做超過測試要求的任何事
- 不要加測試沒有驗證的功能
- 保持介面簡單（不要過度設計）
- 使用 in-memory 資料結構（不需要真實 DB）

測試程式碼：
[貼入測試檔案的內容]
```

---

<!-- _notes:
這是 GREEN Phase。
強調「最小實作」的概念：只做測試要求的事，其他的之後再說。

這個原則避免了「過度設計」的問題。很多工程師看到需求就想設計完美的架構，但 TDD 要求你先讓測試通過，之後再重構。

AI 在這個 Phase 非常強大，它可以快速生成符合測試的實作。
-->

---

# Prompt 3：Edge Case 挖掘

<br>

```
以下是一個功能的主流程 Gherkin Scenario（Happy Path）。
請列出所有可能的邊界條件與 edge case，
並為每個 edge case 生成對應的 DSL-Level Gherkin Scenario。

分析維度：
- 輸入邊界（空值、null、超長字串、特殊字元）
- 狀態邊界（不存在的 ID、已刪除的資源）
- 業務規則邊界（限額、權限、時間限制）
- 並發情況（同時操作同一資源）

主流程 Gherkin：
[貼入 Happy Path Scenario]
```

---

<!-- _notes:
這個 Prompt 是品質保障的利器。
問大家：「你寫功能的時候，怎麼想到 edge case？」
通常大家是靠經驗、靠 QA 回報、靠線上 bug。

用 AI 系統性地挖掘 edge case，可以在需求階段就把問題找出來，成本比上線後再修便宜 10 倍。

給大家看 AI 可能列出的 edge case：暱稱含有 emoji、暱稱只有空格、暱稱包含 SQL injection 字元...
-->

---

# Prompt 4：Refactor（不改行為的重構）

<br>

```
以下程式碼的測試都通過了（GREEN Phase 完成）。
請在不改變任何行為的前提下重構：

重構目標：
- 消除重複程式碼
- 改善命名（函式名、變數名）
- 減少認知複雜度
- 每次重構後，測試必須仍然通過

程式碼：
[貼入實作程式碼]

對應測試：
[貼入測試程式碼]
```

---

<!-- _notes:
REFACTOR Phase。
強調：重構的安全網就是測試。有了測試，重構就不怕改壞。

這也是為什麼 TDD 的測試要在實作之前寫——因為它是你的安全網，不是事後的文件。

讓大家想一想：如果沒有測試，你敢在自己不熟悉的程式碼上做重構嗎？
-->

---

# 測試金字塔：選對測試層

<br>

```
          [E2E]
        少量・慢・貴
        驗整條使用者流程
       ──────────────────
        [整合測試]
      中量・驗跨模組邊界
      API endpoint 行為
     ──────────────────────
         [單元測試 UT]
       大量・快・便宜
       驗純業務邏輯
     ──────────────────────────
```

**今天的練習 → 單元測試（最快拿到 AI 生成的 ROI）**

---

<!-- _notes:
不要讓大家迷失在「要做哪種測試」。
今天的練習聚焦在單元測試，原因：
1. 速度快，5 分鐘內可以跑完
2. AI 生成最穩定（context 夠小）
3. 最容易看到成效

整合測試和 E2E 在 M4 會稍微帶到，但不是今天的主要重點。
-->

---

# Exercise 2：AI × TDD 全循環實作

<br>

**時間：25 分鐘**

**情境：電商折扣計算引擎**

請完成：
1. 把 Ex1 的 Gherkin 展開成 ISA Level（5 min）
2. 用 Prompt 1 生成測試程式碼（5 min）
3. 用 Prompt 2 生成最小實作（5 min）
4. 執行測試，觀察 RED → GREEN（5 min）
5. 用 Prompt 3 挖出 2 個 Edge Case（5 min）

📄 請使用練習題 `exercises/ex02-ai-tdd.md`

---

<!-- _notes:
這是最重要的練習，給足 25 分鐘。
講師巡場，重點幫助：
1. ISA Level 展開不知道要具體到什麼程度的人
2. 執行測試環境有問題的人

告訴大家：重點不是測試能不能跑起來（環境問題很常見），
而是理解「Gherkin → 測試 → 實作」這個流程。

即使環境有問題，也可以只看 AI 的輸出，理解概念。
-->

---

# Exercise 2 討論

<br>

**3 個問題討論：**

1. AI 生成的測試符合你的預期嗎？
   → 如果不符合，是 Gherkin 寫得不夠清楚，還是 Prompt 不夠明確？

2. 找到了哪些 Edge Case？AI 有沒有想到你沒想到的？

3. 最小實作看起來「夠用」嗎？有沒有不足的地方？

---

<!-- _notes:
花 5 分鐘討論。
這個討論的目的是讓大家反思：
- AI 的輸出品質跟輸入品質高度相關
- Edge case 的挖掘通常 AI 比人更系統化
- 「最小實作」的概念對工程師可能很反直覺，但在 TDD 框架下是正確的

引導大家說：「如果 AI 生的測試不符合預期，問題通常在 Gherkin 或 Prompt，不在 AI。」
-->

---

# M2 總結

<br>

| AI × TDD 的三大 Prompt | |
|----------------------|--|
| Prompt 1 | Gherkin → 測試程式碼（RED） |
| Prompt 2 | 測試 → 最小實作（GREEN） |
| Prompt 3 | Edge Case 挖掘 |
| Prompt 4 | 重構（REFACTOR） |

<br>

**完整循環：Gherkin → RED → GREEN → REFACTOR**

> AI 讓 TDD 的執行成本降低 70%，讓你真的願意做 TDD。

---

<!-- _notes:
休息之前的總結。
強調一個關鍵數字：70%。這不是精確數字，但傳達了「AI 不是取代你，而是降低你不喜歡做的那些重複性工作」。

休息 10 分鐘。提醒大家去上廁所、補水，下半段還有兩個重要模組。
-->

---

# ☕ 休息 10 分鐘

<br>

回來後：**M3：Context Engineering**
→ 為什麼你的 Prompt 不穩定？如何設計可複用的 Prompt？

---

<!-- _notes:
宣布休息。告訴大家時間（例如 10:45 回來）。
趁休息巡一下大家的練習成果，如果有人還沒完成，告訴他下半段有參考解答可以對照。
-->
