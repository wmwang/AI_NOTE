# Ch3：70% 自動化 — AI x TDD

## TDD 核心循環：先畫靶後射箭

```
Red   → 寫一個會失敗的測試（描述「應該要有」的行為）
Green → 寫最少的程式碼讓測試通過（不多做）
Refactor → 重構程式碼，確保測試仍通過
```

**關鍵心態：** 測試是「規格的可執行形式」，不是「寫完程式再補的東西」。

---

## UT vs. E2E 測試策略

### 測試金字塔

```
        [E2E]          少量、慢、貴、驗整體流程
       [整合測試]       中量、驗跨模組邊界
    [單元測試 UT]      大量、快、便宜、驗邏輯單元
```

### 在 BDD 框架下的選擇

| 情境 | 推薦測試層 | 理由 |
|------|-----------|------|
| 純業務邏輯（折扣計算、狀態機）| UT | 快、隔離好 |
| API endpoint 行為 | 整合測試 | 驗 HTTP contract |
| 跨服務流程（下單→付款→通知）| E2E | 驗整條 happy path |

---

## Gherkin → 測試程式碼的翻譯

### 後端規格一致性要求

ISA-Level Gherkin 的每個 step 必須能 1:1 對應到測試程式碼的 setup/act/assert。

### 範例：從 Gherkin 到 Jest 測試（Node.js）

**ISA-Level Gherkin：**
```gherkin
Scenario: 計算含折扣的訂單總金額
  Given 訂單含商品 [{ price: 100, qty: 3 }, { price: 50, qty: 2 }]
  And   套用折扣碼 "SAVE10"（打九折）
  When  計算訂單總金額
  Then  總金額應為 $360（(300+100) * 0.9）
```

**AI Prompt（生成測試）：**
```
根據以下 ISA-Level Gherkin，生成 Jest 單元測試程式碼。
要求：
- 使用 describe/it 結構
- Given → beforeEach/arrange
- When → act（呼叫被測函式）
- Then → expect assertions
- 不要實作函式本身，只生成測試

[貼上 Gherkin]
```

**生成結果範例：**
```typescript
describe('calculateOrderTotal', () => {
  it('套用九折折扣碼後，總金額正確', () => {
    // Given
    const items = [
      { price: 100, qty: 3 },
      { price: 50,  qty: 2 },
    ];
    const discountCode = 'SAVE10';

    // When
    const total = calculateOrderTotal(items, discountCode);

    // Then
    expect(total).toBe(360);
  });
});
```

---

## AI x TDD 4 大 Prompt 實戰

### Prompt 1：Gherkin → 測試骨架

```
你是一位資深 TDD 工程師。
請根據以下 ISA-Level Gherkin Scenario，生成 [語言/框架] 的測試程式碼骨架。
- 只生成測試，不實作被測程式碼
- Given → Arrange，When → Act，Then → Assert
- 測試函式名稱應清楚描述情境

Gherkin:
[貼入]
```

### Prompt 2：測試 → 實作（TDD Green Phase）

```
以下是一個會失敗的測試，請實作最少的程式碼讓它通過。
- 不要過度設計
- 不要加測試沒要求的功能

測試程式碼:
[貼入]
```

### Prompt 3：Refactor（重構階段）

```
以下程式碼的測試都通過了，請在不改變行為的前提下重構：
- 消除重複
- 改善命名
- 每次重構後確認測試仍能通過

程式碼:
[貼入]

測試:
[貼入]
```

### Prompt 4：Edge Case 挖掘

```
以下是一個功能的主流程 Gherkin Scenario。
請列出所有可能的邊界條件與 edge case，
並為每個 edge case 生成對應的 Gherkin Scenario。

主流程:
[貼入]
```

---

## 後端規格驅動開發的一致性要求

確保以下三層永遠同步：

```
業務規格（DSL Gherkin）
    ↕ 同步
整合規格（ISA Gherkin）
    ↕ 同步
測試程式碼
```

**檢查清單：**
- [ ] 每個 ISA step 都有對應的測試 assertion
- [ ] 每個 edge case scenario 都有對應的測試案例
- [ ] 修改 API 合約時，ISA Gherkin 同步更新
- [ ] 測試失敗時，先看 Gherkin 是否需要更新，再看程式碼

---

## 練習題

1. 為「優惠券驗證」功能撰寫 5 個 ISA-Level Gherkin Scenario
2. 使用 Prompt 1 生成測試骨架
3. 使用 Prompt 2 請 AI 實作讓測試通過
4. 執行 Red-Green-Refactor 完整一輪
