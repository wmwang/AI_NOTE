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
  pre { background: #1e293b; border-left: 4px solid #38bdf8; font-size: 0.85em; }
  table { border-collapse: collapse; width: 100%; }
  th { background: #1e3a5f; color: #7dd3fc; }
  td, th { padding: 8px 12px; border: 1px solid #334155; }
  blockquote { border-left: 4px solid #fbbf24; color: #94a3b8; background: #1e293b; padding: 12px 16px; }
---

# M1：規格先行

## 把需求轉化為 AI 可執行的規格

> 時間：30 分鐘（講授 20 分鐘 + 練習 10 分鐘）

---

<!-- _notes:
Module 1 開始。這個模組的目標是讓大家理解：
1. 為什麼規格必須是「可執行的」
2. 什麼是 Gherkin，如何寫
3. DSL Level 和 ISA Level 的差異

預計 20 分鐘講，10 分鐘做 Exercise 1。
-->

---

# 規格的問題不是「寫得不夠詳細」

<br>

| 傳統規格的問題 | 後果 |
|--------------|------|
| 寫在 Notion / Confluence | AI 讀不懂（也不會主動去讀）|
| 用自然語言描述 | 每個人理解不同 |
| 靜態文件 | 改了需求，文件滯後 |
| 沒有驗收條件 | 「完成」的定義不清楚 |

<br>

> **真正的問題：規格沒有跟程式碼綁在一起**

---

<!-- _notes:
這是從你們公司的 Notion 文件說起。問一下：你們公司的需求文件存在哪裡？
大部分都是 Notion / Confluence / Jira。AI 能讀嗎？即使能讀，它怎麼知道哪個是最新版本？

重點不是「寫得更詳細」，而是「換一種 AI 能對齊的格式」。
-->

---

# 可執行規格（Executable Specification）

<br>

```
傳統規格：
"使用者可以用 Google 帳號登入系統"
（模糊、不可驗證）

可執行規格（Gherkin）：
Given 使用者尚未登入
When  使用者點擊「用 Google 登入」並完成授權
Then  使用者應被導向首頁
And   頂部導航列應顯示使用者名稱
```

**差別：後者可以直接被轉換成測試程式碼**

---

<!-- _notes:
把這兩段並排讓大家看。
傳統規格給 AI 的問題：AI 不知道要從哪裡開始、不知道「完成」是什麼樣子。
Gherkin 給 AI：清楚的前置條件、清楚的動作、清楚的預期結果 → 可以直接生成測試。
-->

---

# Discovery → Formulation → Automation

<br>

```
Discovery（探索）
  問三個問題：
  ① Actor：誰在做這件事？
  ② Context：在什麼前提下？
  ③ Outcome：做了之後，系統怎麼改變？
        ↓
Formulation（形式化）
  把探索結果寫成 Gherkin Scenario
        ↓
Automation（自動化）
  AI 根據 Gherkin 生成測試程式碼 + 實作程式碼
```

---

<!-- _notes:
這是 BDD 的核心循環，改編自 Cucumber 的 Three Amigos 概念。
Discovery 是 PO + QA + Dev 一起做的。
Formulation 是 Dev/QA 做的。
Automation 是 AI + Dev 一起做的。

重點是：人負責「Discovery」，AI 負責「Automation」，Gherkin 是中間的橋樑。
-->

---

# Gherkin 語言入門

<br>

```gherkin
Feature: 使用者登入

  Background:
    Given 系統中存在帳號 "alice@example.com"

  Scenario: 正確密碼登入成功
    Given 使用者在登入頁面
    When  使用者輸入正確的帳號與密碼
    Then  使用者應被導向首頁
    And   頂部應顯示 "歡迎回來，Alice"

  Scenario: 密碼錯誤三次帳號鎖定
    Given 使用者在登入頁面
    When  使用者連續輸入錯誤密碼 3 次
    Then  帳號應被鎖定 30 分鐘
    And   畫面應顯示 "帳號已鎖定，請 30 分鐘後再試"
```

---

<!-- _notes:
一字一字帶過 Gherkin 語法。
Feature：一個功能模組
Background：所有 Scenario 的共同前置條件
Scenario：一個具體的使用情境
Given：前置狀態（Before the action）
When：觸發動作（The action）
Then：預期結果（The assertion）
And：連接多個條件

問學員：這個格式看起來像什麼？（答：自然語言）對，這就是 Gherkin 的設計目標：讓非工程師也能讀懂，讓 AI 也能解析。
-->

---

# Gherkin 關鍵字速查

<br>

| 關鍵字 | 用途 | 對應問題 |
|--------|------|---------|
| `Feature` | 功能模組名稱 | 這個功能是什麼？ |
| `Background` | 共用前置條件 | 所有情境的共同前提？ |
| `Scenario` | 單一使用情境 | 一個具體的「例子」 |
| `Given` | 前置狀態 | 系統現在是什麼狀態？ |
| `When` | 觸發動作 | 使用者做了什麼？ |
| `Then` | 預期結果 | 系統應有何反應？ |
| `And` / `But` | 連接多個條件 | 補充說明 |

---

<!-- _notes:
不需要死記，拿講義的速查表就可以了。
重點是理解 Given/When/Then 的語意。
-->

---

# DSL Level vs. ISA Level

<br>

```gherkin
# DSL Level（業務語言，給 PO / QA 看）
Scenario: 含折扣碼的訂單總金額計算
  Given 訂單含 3 件 $100 的商品和 2 件 $50 的商品
  And   套用折扣碼 "SAVE10"（九折）
  When  顧客確認訂單
  Then  訂單總金額應為 $360

# ISA Level（整合規格，給 AI 生成測試用）
Scenario: 含折扣碼的訂單總金額計算 [ISA]
  Given 訂單含商品 [{ price: 100, qty: 3 }, { price: 50, qty: 2 }]
  And   套用折扣碼 "SAVE10"（discount_rate: 0.9）
  When  呼叫 calculateOrderTotal(items, discountCode)
  Then  回傳值應為 360
```

---

<!-- _notes:
這是本模組最重要的概念之一。
DSL Level：抽象，讓業務人員可以讀懂、可以討論
ISA Level：具體，含有真實參數、API endpoint、資料結構

AI 需要 ISA Level 才能生成精確的測試程式碼。
DSL Level 用於對齊業務理解，ISA Level 用於自動化。

兩個 Level 都要維護，但工作流是先寫 DSL，再展開成 ISA。
-->

---

# 現場 Demo：需求 → Gherkin

<br>

**需求：「用戶可以修改自己的個人資料」**

<br>

**Step 1：Discovery 三問**

```
Actor：已登入的使用者
Context：在個人資料頁面，有現有資料
Outcomes：
  ✓ 成功儲存 → 顯示成功訊息
  ✗ 暱稱為空 → 顯示驗證錯誤
  ✗ 圖片超過 5MB → 顯示大小限制錯誤
```

---

<!-- _notes:
這個 Demo 現場示範，花 3-4 分鐘。
從需求開始，帶著大家一起做 Discovery，然後寫出 DSL Gherkin。
目的是讓大家看到從「模糊需求」到「結構化規格」的過程。

可以邀請學員幫你想 edge case。
-->

---

# 現場 Demo：需求 → Gherkin（續）

<br>

**Step 2：Formulation（DSL Gherkin）**

```gherkin
Feature: 個人資料管理

  Background:
    Given 已登入使用者 "Alice"
    And   Alice 的現有暱稱為 "alice_old"

  Scenario: 成功更新暱稱
    When  Alice 修改暱稱為 "alice_new" 並儲存
    Then  畫面應顯示 "個人資料已更新"
    And   暱稱應顯示為 "alice_new"

  Scenario: 暱稱為空不允許儲存
    When  Alice 清空暱稱欄位並點擊儲存
    Then  應顯示錯誤 "暱稱不能為空"
    And   個人資料不應有任何變更
```

---

<!-- _notes:
完成後，問大家：還有什麼 edge case 我們沒想到？
可能的答案：暱稱有特殊字元、暱稱太長、網路錯誤...
每個 edge case 都是一個新的 Scenario。

這就是「先畫靶，再射箭」的思維。
-->

---

# Exercise 1：撰寫你的第一個 Gherkin

<br>

**時間：10 分鐘**

**情境：「電商平台的商品搜尋功能」**

請完成：
1. Discovery 三問（Actor / Context / Outcomes）
2. 寫出 **3 個** DSL Level Gherkin Scenario
   - 1 個 Happy Path
   - 2 個 Edge Cases

📄 請使用練習題 `exercises/ex01-gherkin.md`

---

<!-- _notes:
計時 10 分鐘。
巡場看大家的進度，幫助卡住的學員。
常見問題：「Given 要寫多細？」→ 答：DSL Level 不用太細，業務人員能懂就行。

結束後，請 2-3 位學員分享，簡短討論。
-->

---

# 關鍵提醒

<br>

**一個好的 Gherkin Scenario 的特徵：**

✅ Given 描述「系統狀態」而非「操作步驟」
✅ When 只有一個核心動作（不要塞兩件事）
✅ Then 描述可觀察的結果（不是實作細節）
✅ 每個 Scenario 可以獨立閱讀、獨立理解

<br>

**常見錯誤：**

❌ `When 使用者登入然後去到購物車然後結帳`（太多動作）
✅ 拆成三個 Scenario 分別描述

---

<!-- _notes:
這是 Exercise 1 之後的總結。
花 2-3 分鐘強調這些原則，為下一個模組做準備。

特別強調：「每個 Scenario 可以獨立閱讀」→ 這樣 AI 才能精確地針對單一 Scenario 生成測試。
如果一個 Scenario 寫了十個步驟，AI 很容易搞混。
-->

---

# M1 總結

<br>

| 學到了 | 下一步 |
|--------|--------|
| Discovery → Formulation → Automation 流程 | M2 的 Automation |
| Gherkin 語言：Given / When / Then | 練習轉成 ISA Level |
| DSL Level vs. ISA Level | 讓 AI 生成測試 |

<br>

> 規格是 AI 的輸入格式。有了可執行規格，AI 才能自動驗證。

**→ 下一個模組：讓 AI 幫你走 Red-Green-Refactor**

---

<!-- _notes:
快速總結，過渡到 Module 2。
如果有人問：「ISA Level 怎麼寫？」可以說：「我們在 M2 會帶大家用 AI 來轉換。」
-->
