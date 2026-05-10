# Ch4：80% 自動化 — AI x BDD

## BDD 與 TDD 的差異

| | TDD | BDD |
|--|-----|-----|
| 出發點 | 技術行為（函式/類別）| 業務行為（使用者情境）|
| 語言 | 程式碼 | Gherkin（自然語言）|
| 協作對象 | 開發者之間 | PO + QA + 開發者 |
| 測試層 | 主要 UT | UT + E2E 都有 |

**BDD 不是 TDD 的替代，而是 TDD 的上層包裝。**

---

## BDD 工具鏈

### 主流工具

| 語言 | 工具 |
|------|------|
| JavaScript/TypeScript | Cucumber.js, Jest-Cucumber, Vitest |
| Python | Behave, pytest-bdd |
| Java | Cucumber-JVM, JBehave |
| Ruby | Cucumber（原生） |
| Go | Godog |

### 工具鏈架構

```
.feature 檔案（Gherkin）
    ↓
Step Definitions（步驟定義，連結 Gherkin 與程式碼）
    ↓
測試執行（呼叫實際的業務邏輯或 API）
    ↓
測試報告（活文件）
```

---

## AI x BDD 實戰（UT 層級）

### 完整流程

```
1. 撰寫 ISA-Level Gherkin
2. AI 生成 Step Definitions 骨架
3. AI 生成業務邏輯實作
4. 執行測試，修正失敗
```

### 範例：購物車加入商品

**ISA-Level Gherkin：**
```gherkin
Feature: 購物車管理

  Scenario: 加入新商品到空購物車
    Given 一個空的購物車 { cartId: "c001", userId: "u001" }
    And   商品 { productId: "p001", name: "書本", price: 350, stock: 10 }
    When  加入商品 { productId: "p001", qty: 2 } 到購物車 "c001"
    Then  購物車應包含 1 種商品
    And   商品 "p001" 的數量應為 2
    And   購物車小計應為 $700

  Scenario: 加入已存在商品到購物車（累加數量）
    Given 購物車 "c001" 已包含商品 "p001" 數量 1
    When  再加入商品 { productId: "p001", qty: 2 } 到購物車 "c001"
    Then  購物車中商品 "p001" 的數量應為 3
    And   購物車小計應為 $1050

  Scenario: 加入商品但庫存不足
    Given 商品 "p001" 庫存僅剩 1 件
    When  加入商品 { productId: "p001", qty: 5 } 到購物車 "c001"
    Then  應拋出錯誤 "INSUFFICIENT_STOCK"
    And   購物車不應有任何變更
```

**AI Prompt（生成 Step Definitions）：**
```
根據以下 ISA-Level Gherkin Feature，生成 TypeScript + Jest-Cucumber 的 Step Definitions。
要求：
1. 每個 Given/When/Then 對應一個 step definition function
2. Given → 設置測試資料（mock 或 in-memory）
3. When → 呼叫 CartService 的對應方法
4. Then → 用 expect() 驗證結果
5. 使用 in-memory repository，不連接真實 DB

[貼入 Gherkin]
```

---

## AI x BDD 實戰（E2E 層級）

E2E 測試驗證的是「整條 HTTP 請求流程」，包含：
- 真實的 HTTP 請求
- 真實的 DB（可用 test DB）
- 真實的業務邏輯

### E2E Step Definition 範例（Supertest + Node.js）

```typescript
import request from 'supertest';
import { app } from '../../src/app';
import { db } from '../../src/db';

defineFeature(feature, (test) => {
  test('顧客成功結帳', ({ given, and, when, then }) => {
    let response: any;

    given('已登入的顧客 "Alice"', async () => {
      await db.users.create({ id: 'u001', email: 'alice@test.com' });
      // 設置 JWT token for auth
    });

    and('購物車內有商品 "iPhone 殼" 數量 2，每件 $250', async () => {
      await db.carts.create({ id: 'c001', userId: 'u001' });
      await db.cartItems.create({ cartId: 'c001', productId: 'p001', qty: 2 });
      await db.products.create({ id: 'p001', name: 'iPhone 殼', price: 250, stock: 10 });
    });

    when('顧客點擊「確認結帳」', async () => {
      response = await request(app)
        .post('/api/orders')
        .set('Authorization', `Bearer ${aliceToken}`)
        .send({ cartId: 'c001' });
    });

    then('系統應建立一張訂單', () => {
      expect(response.status).toBe(201);
    });

    and('訂單總金額應為 $500', () => {
      expect(response.body.totalAmount).toBe(500);
    });

    and('訂單狀態應為「待付款」', () => {
      expect(response.body.status).toBe('pending_payment');
    });
  });
});
```

---

## BDD-Discovery：撰寫後端三巨頭規格

「後端三巨頭」= **API Contract + DB Schema + Domain Events**

每個功能在進入開發前，必須先定義清楚這三份規格。

### API Contract（OpenAPI 格式）

```yaml
POST /api/orders:
  requestBody:
    cartId: string
    userId: string
  responses:
    201:
      orderId: string
      status: "pending_payment"
      totalAmount: number
    422:
      error: "INSUFFICIENT_STOCK" | "CART_EMPTY" | "INVALID_CART"
```

### DB Schema（新增的 Table/欄位）

```sql
CREATE TABLE orders (
  id         UUID PRIMARY KEY,
  user_id    UUID NOT NULL REFERENCES users(id),
  status     VARCHAR(50) NOT NULL DEFAULT 'pending_payment',
  total      DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Domain Events（發出的事件）

```json
{
  "event": "OrderCreated",
  "payload": {
    "orderId": "uuid",
    "userId": "uuid",
    "totalAmount": 500,
    "items": [...]
  }
}
```

---

## API-First 戰法：前端先 Mock、後端走 AI x BDD

```
1. 前後端共同定義 API Contract（OpenAPI）
       ↓
2. 前端：用 Mock Server（如 MSW）根據 Contract Mock API
   後端：用 ISA Gherkin + AI 驅動 TDD
       ↓
3. 兩邊並行開發，不互相等待
       ↓
4. 整合時，Contract 是驗收標準
```

### Mock Server 設定（MSW 範例）

```typescript
// handlers.ts
import { rest } from 'msw';

export const handlers = [
  rest.post('/api/orders', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        orderId: 'mock-order-001',
        status: 'pending_payment',
        totalAmount: 500,
      })
    );
  }),
];
```

---

## Prompt Engineering 複利技巧

### 讓 AI 輸出穩定的三個原則

1. **給角色**：「你是一位熟悉 BDD 的 TypeScript 工程師」
2. **給格式**：「請輸出 Gherkin + Step Definition，不要其他說明文字」
3. **給範例**：貼一個已完成的正確範例作為 few-shot

### 不穩定的 Prompt vs. 穩定的 Prompt

```
❌ 不穩定
"幫我寫一個購物車的測試"

✓ 穩定
"根據以下 ISA-Level Gherkin，使用 TypeScript + Jest-Cucumber 生成 Step Definitions。
格式參考：[貼入範例]
Gherkin：[貼入]"
```

---

## 練習題

1. 為「使用者忘記密碼 → 發送重設信」功能設計後端三巨頭規格
2. 撰寫 3 個 ISA-Level Gherkin Scenario（正常 + 2 edge cases）
3. 使用 AI 生成對應的 Step Definitions
4. 設計前端 Mock Server handler
