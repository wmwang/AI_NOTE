# AI 輔助開發速查表

> 帶走即用 · 雙面列印

---

## Gherkin 語法

```gherkin
Feature: [功能模組名稱]

  Background:           ← 所有 Scenario 的共用前置條件
    Given [系統狀態]

  Scenario: [具體使用情境名稱]
    Given [前置狀態]    ← 系統現在是什麼狀態？
    When  [觸發動作]    ← 使用者做了什麼？（只有一個動作）
    Then  [預期結果]    ← 系統應有何反應？（可觀察）
    And   [補充結果]    ← 連接多個 Then
```

**DSL Level**（業務語言，給 PO/QA 看）：語意清楚，不含技術細節

**ISA Level**（整合規格，給 AI 生成測試用）：含具體 ID、URL、參數、DB 欄位

---

## Gherkin 撰寫原則

| ✅ 應該這樣 | ❌ 不要這樣 |
|-----------|-----------|
| Given 描述「狀態」 | Given 描述「操作步驟」 |
| When 只有一個核心動作 | When 塞了兩三個動作 |
| Then 描述可觀察結果 | Then 描述實作細節 |
| 每個 Scenario 可獨立閱讀 | Scenario 依賴前一個 Scenario |

---

## Discovery 三問

```
① Actor：誰在做這件事？（使用者角色）
② Context：在什麼前提/狀態下？（Given 的來源）
③ Outcome：做了之後，系統狀態如何改變？（Then 的來源）
```

---

## AI × TDD 四個核心 Prompt

### Prompt 1：Gherkin → 測試

```
你是一位資深 TDD 工程師，熟悉 [語言] 和 [框架]。
根據以下 ISA-Level Gherkin，生成測試程式碼骨架。
規則：
- 只生成測試，不實作被測函式
- Given → Arrange，When → Act，Then → Assert
- 錯誤情境用 expect(...).toThrow()
ISA Gherkin：[貼入]
```

### Prompt 2：測試 → 最小實作

```
以下是 failing 測試（RED Phase）。
請實作最小的程式碼讓這些測試通過。
規則：
- 不做超過測試要求的任何事
- 保持介面簡單
測試程式碼：[貼入]
```

### Prompt 3：Edge Case 挖掘

```
以下是 Happy Path Gherkin。
請列出所有邊界條件和 edge case，
並為每個 edge case 生成 DSL-Level Gherkin Scenario。
分析維度：輸入邊界、狀態邊界、業務規則邊界、並發
主流程：[貼入]
```

### Prompt 4：Refactor

```
以下程式碼測試都通過了。
請在不改變行為的前提下重構。
目標：消除重複、改善命名、減少複雜度。
每次重構後確認測試仍通過。
程式碼：[貼入]  測試：[貼入]
```

---

## Context Engineering 三要素

```
✦ 角色：  "你是一位 [具體角色]，擅長 [技術]"
✦ 格式：  "請輸出 [格式]，不要 [不需要的內容]"
✦ 範例：  貼一個已完成的輸入/輸出對（few-shot）
```

---

## 後端三巨頭（每個功能開工前）

```
✦ API Contract（OpenAPI）
  POST /api/xxx: { request schema } → { response schema }
  Error codes: { ... }

✦ DB Schema
  新增/修改的 Table 或欄位

✦ Domain Events
  { "event": "XxxCreated", "payload": { ... } }
```

---

## 完整工作流

```
Discovery → DSL Gherkin → 後端三巨頭 → ISA Gherkin
         → 前端 Mock Server（API Contract）
         → 後端 AI × TDD（ISA Gherkin）
         → 整合測試 → 驗收（Gherkin AC）
```

---

## TDD 循環

```
🔴 RED    → 寫會失敗的測試（Gherkin → Prompt 1）
🟢 GREEN  → 最小實作讓測試通過（Prompt 2）
🔵 REFACTOR → 重構，確保測試仍通過（Prompt 4）
```

---

*[工作坊：AI 輔助軟體開發實戰]*
