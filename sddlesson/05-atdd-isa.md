# Ch5：最後一哩路 — ATDD + ISA 規格

## ATDD：驗收測試驅動開發

ATDD（Acceptance Test-Driven Development）是在 BDD 之上，加入了**「驗收」的概念**。

### BDD vs. ATDD

| | BDD | ATDD |
|--|-----|------|
| 誰定義測試？| 開發者 + QA | PO + QA + 開發者（三方） |
| 測試的目的 | 驗證行為 | 驗收「功能是否完成」|
| 測試層 | UT + E2E | 主要 E2E + 系統邊界 |
| 完成定義 | 測試通過 | 驗收條件 100% 通過 |

### ATDD 循環

```
PO 定義驗收條件（AC）
       ↓
三方將 AC 轉化為 Gherkin Scenario
       ↓
開發者用 AI x BDD 實作
       ↓
QA 執行驗收測試
       ↓
全部通過 → Done
```

---

## User Story + AC → Gherkin

### 標準 User Story 格式

```
作為 [角色]
我想要 [功能]
以便 [業務價值]
```

### 驗收條件（Acceptance Criteria）轉換

**User Story：**
```
作為 已登入的顧客
我想要 追蹤我的訂單狀態
以便 知道商品何時會到貨
```

**AC（Given-When-Then 格式）：**
```
AC1: 訂單狀態追蹤 - 正常情況
  Given 顧客有一筆訂單 #001，狀態為「配送中」
  When  顧客查詢訂單 #001 的狀態
  Then  系統回傳訂單狀態「配送中」與預計到達時間

AC2: 訂單不存在
  Given 顧客查詢不存在的訂單 #999
  When  發送查詢請求
  Then  系統回傳 404 錯誤

AC3: 查詢他人訂單（權限錯誤）
  Given 顧客 Alice 嘗試查詢 Bob 的訂單
  When  發送查詢請求
  Then  系統回傳 403 錯誤
```

---

## ISA（Integration Specification Architecture）

ISA 是「讓 AI 能夠全自動生成測試程式碼」的規格層次。

### ISA 的組成

```
ISA = DSL-Level Gherkin 的具體展開
    + 明確的技術邊界（API、DB、Event）
    + 可被工具解析的格式
```

### ISA 撰寫規則

#### Rule 1：Given 必須指定確切的資料狀態

```gherkin
# ❌ DSL-Level（太抽象）
Given 顧客有一筆訂單

# ✓ ISA-Level（可執行）
Given 資料庫 orders 表有一筆記錄:
  | orderId | userId | status      | totalAmount |
  | "o001"  | "u001" | "shipping"  | 500         |
```

#### Rule 2：When 必須是明確的系統操作

```gherkin
# ❌ DSL-Level
When 顧客查詢訂單狀態

# ✓ ISA-Level
When GET /api/orders/o001
     Headers: { Authorization: "Bearer {u001_token}" }
```

#### Rule 3：Then 必須指定可驗證的輸出

```gherkin
# ❌ DSL-Level
Then 系統回傳訂單資訊

# ✓ ISA-Level
Then HTTP 狀態碼為 200
And  回應 body 為:
  {
    "orderId": "o001",
    "status": "shipping",
    "estimatedArrival": "2024-01-15"
  }
```

---

## BDD Analysis：高測試覆蓋率的 QA 思維

### 邊界設計原則

**透過「測試複雜度」決定邊界：**

如果一個服務/函式需要超過 5 個 Scenario 才能覆蓋，考慮拆分。

```
訂單服務（太大）
├── 建立訂單
├── 計算折扣
├── 驗證優惠券
├── 扣減庫存
└── 發送通知

→ 拆分：
  ┌──────────────────────┐
  │  OrderService        │ 建立訂單（協調者）
  └──────────────────────┘
         ↓ 呼叫
  ┌──────────────────────┐
  │  DiscountCalculator  │ 計算折扣（純業務邏輯）
  │  CouponValidator     │ 驗證優惠券
  │  InventoryService    │ 扣減庫存
  │  NotificationService │ 發送通知
  └──────────────────────┘
```

### 「抓大放小」測試策略

- **大**（ATDD/E2E）：驗收最重要的完整流程（happy path + critical edge cases）
- **小**（UT）：細節業務邏輯（折扣計算、狀態機轉換）

```
E2E 測試覆蓋率目標：主要流程 100%，次要流程 80%
UT 覆蓋率目標：業務邏輯 > 90%
```

---

## 前端的 AI x BDD

前端 BDD 的特殊性：
- Given = 頁面狀態 + API Mock 狀態
- When = 使用者互動（點擊、輸入）
- Then = DOM 狀態變化 + API 呼叫驗證

### 前端 BDD 工具鏈

```
Gherkin Feature 檔案
    ↓
Step Definitions（連結 Gherkin 與 UI 操作）
    ↓
Playwright / Cypress（瀏覽器自動化）
    + MSW（API Mock）
```

### 前端 ISA-Level Gherkin 範例

```gherkin
Scenario: 顯示購物車商品清單
  Given API GET /api/cart/c001 回傳:
    { items: [{ name: "iPhone 殼", qty: 2, price: 250 }], total: 500 }
  When  使用者訪問 /cart
  Then  頁面應顯示商品 "iPhone 殼"
  And   頁面應顯示數量 "2"
  And   頁面應顯示小計 "NT$500"
  And   「結帳」按鈕應為可點擊狀態
```

---

## 練習題

1. 為「訂閱電子報」功能撰寫 User Story + 3 個 AC
2. 將 AC 轉換為 DSL-Level + ISA-Level Gherkin
3. 識別這個功能應使用哪些測試層（UT/整合/E2E）
4. 用「邊界設計原則」評估是否需要拆分服務
