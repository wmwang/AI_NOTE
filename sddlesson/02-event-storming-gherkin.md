# Ch2：規格的光譜 — DDD + Event Storming → Gherkin

## 為什麼需要「抽象」？

領域驅動設計（DDD）的核心命題：**沒有抽象就沒有協作**。

- 開發者說「新增一筆 record」，PO 說「建立一張訂單」—— 說的是同一件事，但語言不同
- 共同語言（Ubiquitous Language）是 DDD 解決這個問題的工具
- Event Storming 是建立共同語言最快的方法

---

## Event Storming 基礎

### 便利貼顏色規則

```
橘色  = Domain Event（業務事件）     → 過去式動詞  "訂單已建立"
藍色  = Command（指令）              → 動詞命令式  "建立訂單"
黃色  = Actor（行為者）              → 名詞        "顧客"
綠色  = Read Model（查詢視圖）       → 名詞        "購物車"
紫色  = Policy（業務規則）           → 當...就...  "當庫存不足時，拒絕訂單"
粉紅  = External System（外部系統）  → 名詞        "金流服務"
```

### 電商結帳的 Event Storming 範例

```
[顧客] → 結帳 → 訂單已建立
                    ↓
              庫存已扣減
                    ↓
              付款請求已發送 → [金流服務]
                    ↓
              付款已完成
                    ↓
              確認信已寄出 → [Email 服務]
```

---

## Event Storming → Gherkin 的對應關係

| Event Storming 元素 | 對應 Gherkin |
|--------------------|-------------|
| Actor（黃色）| `Given 已登入的顧客` |
| Read Model（綠色）| `Given 購物車內有 3 件商品` |
| Command（藍色）| `When 顧客點擊「確認結帳」` |
| Domain Event（橘色）| `Then 訂單狀態應為「待付款」` |
| Policy（紫色）| 對應到 Edge Case Scenario |

### 轉換範例

**Event Storming 卡片：**
```
Actor: 已登入顧客
Command: 結帳
Read Model: 購物車（有 2 件商品，總金額 $500）
Domain Event: 訂單已建立
Policy: 若庫存不足 → 顯示錯誤
```

**轉換後的 Gherkin：**
```gherkin
Feature: 電商結帳

  Scenario: 顧客成功結帳
    Given 已登入的顧客 "Alice"
    And   購物車內有商品 "iPhone 殼" 數量 2，每件 $250
    And   商品庫存充足
    When  顧客點擊「確認結帳」
    Then  系統應建立一張訂單
    And   訂單總金額應為 $500
    And   訂單狀態應為「待付款」

  Scenario: 庫存不足時結帳失敗
    Given 已登入的顧客 "Alice"
    And   購物車內有商品 "限量球鞋" 數量 2
    And   商品庫存僅剩 1 件
    When  顧客點擊「確認結帳」
    Then  系統應顯示錯誤訊息「庫存不足，無法完成訂單」
    And   不應建立任何訂單
```

---

## DSL-Level vs. ISA-Level Gherkin

這是課程的核心區分，也是「能不能讓 AI 全自動生成程式碼」的關鍵。

### DSL-Level（業務語言層）

- 給 PO、QA、業務人員看
- 不含技術細節（無 API、無 DB schema）
- 可讀性高，穩定不常變

```gherkin
Scenario: 顧客成功結帳
  Given 已登入的顧客且購物車有商品
  When  顧客確認結帳
  Then  訂單應被建立
```

### ISA-Level（整合規格層）

- 給 AI 生成測試程式碼用
- 含具體參數、API endpoint、DB 欄位
- 是 DSL-Level 的具體化展開

```gherkin
Scenario: 顧客成功結帳 [ISA]
  Given 資料庫中存在使用者 { id: "u001", email: "alice@test.com" }
  And   購物車 { cartId: "c001", userId: "u001" } 含商品 { productId: "p001", qty: 2, price: 250 }
  And   商品 "p001" 庫存為 10
  When  POST /api/orders { cartId: "c001", userId: "u001" }
  Then  HTTP 狀態碼應為 201
  And   回應 body 應包含 { status: "pending_payment", totalAmount: 500 }
  And   資料庫 orders 表應新增一筆 { userId: "u001", status: "pending_payment" }
  And   資料庫 inventory 表中 "p001" 的 stock 應減少 2
```

### 兩層架構的價值

```
DSL-Level  ← 業務人員維護，規格穩定
    ↓ 展開（AI 輔助 or 手動）
ISA-Level  ← 工程師維護，驅動 AI 生成測試
    ↓ AI 自動生成
測試程式碼 + 實作程式碼
```

---

## 練習題

1. 針對「使用者重設密碼」功能，進行 Event Storming（列出所有便利貼）
2. 將 Event Storming 結果轉換為 3 個 Gherkin Scenario（含正常流程 + 2 個 edge case）
3. 選一個 Scenario，把它從 DSL-Level 展開為 ISA-Level
