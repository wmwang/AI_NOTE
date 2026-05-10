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
  pre { background: #1e293b; border-left: 4px solid #34d399; font-size: 0.8em; }
  table { border-collapse: collapse; width: 100%; }
  th { background: #1e3a5f; color: #7dd3fc; }
  td, th { padding: 8px 12px; border: 1px solid #334155; }
  blockquote { border-left: 4px solid #34d399; color: #94a3b8; background: #1e293b; padding: 12px 16px; }
---

# M4：完整工作流程

## 從需求到可交付功能的完整路徑

> 時間：30 分鐘（架構說明 15 分鐘 + 實境 Demo 15 分鐘）

---

<!-- _notes:
Module 4 是把前面三個模組串起來的整合模組。
不需要再做練習，而是帶大家看一個完整的「從需求到程式碼」的流程示範。

15 分鐘說明架構，15 分鐘做 Live Demo（建議準備好 Demo 腳本）。
-->

---

# 完整工作流總覽

<br>

```
① Discovery（三方會議：PO + QA + Dev）
           ↓
② Event Storming → DSL-Level Gherkin
           ↓
③ API-First：定義「後端三巨頭」
   ├─ API Contract（OpenAPI）
   ├─ DB Schema
   └─ Domain Events
           ↓
④ ISA-Level Gherkin（展開具體參數）
           ↓
⑤ 並行開發：
   前端 → Mock Server（依 API Contract）
   後端 → AI × BDD（依 ISA Gherkin）
           ↓
⑥ 整合測試 → ⑦ 驗收 → Done ✓
```

---

<!-- _notes:
帶大家過一遍這個流程。
重點是：每一個步驟都有 AI 可以協助的地方。
而且每個步驟的輸出，都是下一個步驟的輸入——這就是「可執行規格」的威力。

問大家：「你們現在的開發流程最像哪一個步驟是缺失的？」
-->

---

# API-First：前後端解耦的關鍵

<br>

```
傳統模式（阻塞）：
後端開發完 → 前端才能接 → 整合 → 發現不符 → 返工

API-First 模式（並行）：
               ┌─ 前端：用 Mock Server 依 Contract 開發
               │         → 不用等後端，UI 先完成
API Contract → ┤
（共同定義）   │
               └─ 後端：依 Contract 做 TDD
                         → AI 生成測試 + 實作
```

**整合時，Contract 就是驗收標準。差異立刻浮現。**

---

<!-- _notes:
API-First 解決了前後端協作最大的痛點：等待。
前端等後端、後端等需求釐清。

有了 API Contract（OpenAPI 格式），兩邊可以同時進行：
- 前端用 MSW（Mock Service Worker）或 JSON Server 模擬後端
- 後端用 TDD 真正實作

整合時，只需要驗證雙方都符合 Contract。
-->

---

# 後端三巨頭：每個功能的規格清單

<br>

```yaml
# ① API Contract（OpenAPI 格式）
POST /api/orders:
  requestBody:
    cartId: string
    userId: string
  responses:
    201: { orderId: string, status: "pending_payment", totalAmount: number }
    422: { error: "INSUFFICIENT_STOCK" | "CART_EMPTY" }
```

```sql
-- ② DB Schema
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  status VARCHAR(50) DEFAULT 'pending_payment',
  total DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT NOW()
);
```

```json
// ③ Domain Event
{ "event": "OrderCreated", "payload": { "orderId": "...", "totalAmount": 500 }}
```

---

<!-- _notes:
「後端三巨頭」是這個課程裡我最喜歡的概念。
任何一個後端功能，在開始寫程式之前，都要先定義這三份文件：

1. API Contract：這個 endpoint 接收什麼、回傳什麼
2. DB Schema：需要什麼新的 table 或欄位
3. Domain Events：這個功能完成後，會發出什麼事件給其他服務

有了這三份文件，前端、後端、QA 都知道各自要做什麼。AI 也有足夠的 context 生成正確的程式碼。
-->

---

# ISA Gherkin 的威力：從規格到自動化

<br>

```gherkin
# ISA-Level Gherkin（所有參數都具體化）
Scenario: 顧客成功結帳 [ISA]
  Given 使用者 { id: "u001", email: "alice@test.com" } 已登入
  And   購物車 { id: "c001" } 包含商品 { id: "p001", price: 250, qty: 2 }
  And   商品 "p001" 庫存為 10
  When  POST /api/orders { cartId: "c001", userId: "u001" }
        Bearer Token: alice-jwt-token
  Then  HTTP 201
  And   response.body.totalAmount === 500
  And   response.body.status === "pending_payment"
  And   DB orders 表新增一筆 { userId: "u001", total: 500 }
  And   商品 "p001" 庫存減為 8
  And   發出 Domain Event "OrderCreated"
```

---

<!-- _notes:
這是 ISA Level 的完整範例。
注意：所有的「具體參數」都在裡面：
- 使用者 ID、商品 ID、價格、數量
- HTTP 方法和路徑
- 預期的 status code 和 response body
- DB 的變化
- Domain Event

這份 ISA Gherkin 給 AI 之後，它可以生成：
- 測試設置（建立假資料）
- HTTP 請求
- 所有的 assertions
- 而且是 100% 精確的
-->

---

# 從 User Story 到 AC：讓 Gherkin 就是驗收條件

<br>

```markdown
## US-042：顧客可以對已完成的訂單評價

**Story：** 作為顧客，我想要對已完成的訂單留下評價。

**AC1：成功提交評價**
```gherkin
Given 訂單 "o001" 狀態為「已完成」且購買者為當前使用者
When  POST /api/orders/o001/reviews { rating: 5, comment: "很棒！" }
Then  HTTP 201
And   評價儲存至 DB
```

**AC2：不能對未完成訂單評價**
```gherkin
Given 訂單 "o002" 狀態為「待付款」
When  POST /api/orders/o002/reviews { rating: 5 }
Then  HTTP 422，error: "ORDER_NOT_COMPLETED"
```
```

**結果：AC = 測試 = 驗收。沒有模糊地帶。**

---

<!-- _notes:
這是整個工作流最優雅的部分：
User Story 的 Acceptance Criteria 直接用 ISA Gherkin 寫。

好處：
1. PO 寫 AC 的時候就要思考「驗收條件是什麼」
2. QA 看到 AC 就是測試規格，不用再翻譯
3. Dev 實作後，跑一下測試就能知道 AC 有沒有通過
4. Done 的定義非常清楚

傳統流程：需求 → 開發 → QA 測試 → 回報問題 → 修改（很多往返）
SDD 流程：Gherkin AC → AI 實作 → 自動測試 = 驗收（一次到位）
-->

---

# Live Demo：完整走一遍

<br>

**功能：「使用者可以訂閱電子報」**

我們現在做：

1. Discovery 三問（2 min）
2. DSL Gherkin（2 min）
3. 後端三巨頭規格（API + DB + Event）（3 min）
4. ISA Gherkin（2 min）
5. AI 生成測試 → 實作（4 min）
6. 討論：這個流程哪裡可以更快？（2 min）

---

<!-- _notes:
Live Demo 腳本（準備好）：

1. Discovery：
   - Actor：未登入/已登入使用者
   - Context：在首頁或文章底部看到訂閱入口
   - Outcomes：成功訂閱（得到確認信）/ 已訂閱（提示已訂閱）/ Email 格式錯誤

2. DSL Gherkin：現場快速寫出 3 個 Scenario

3. 後端三巨頭：
   - API: POST /api/subscriptions { email: string }
   - DB: subscriptions table（id, email, subscribed_at）
   - Event: UserSubscribed

4. ISA Gherkin：展開參數

5. 用 Claude 生成測試 → 再生成實作（螢幕共享）

建議：提前準備好這個 Demo 的所有內容，Demo 時只是「演示」，不是第一次做。
-->

---

# 常見誤區與解法

<br>

| 誤區 | 解法 |
|------|------|
| ISA Gherkin 寫得太抽象 | 加入真實的 ID、URL、欄位名稱 |
| 一個 Scenario 太長（超過 10 個 step）| 拆開成多個 Scenario |
| 跳過 DSL 直接寫 ISA | 先對齊業務，再具體化 |
| API Contract 不更新 | 把 Contract 放在 Git，PR review |
| 只測 happy path | 用 Prompt 3 系統挖 edge case |
| Prompt 每次都重寫 | 建立 Prompt 模板庫 |

---

<!-- _notes:
這些是工作坊結束後，大家在實際導入時最常碰到的問題。
先說出來，讓大家有心理準備。

最常見的是「ISA Gherkin 太抽象」——大家習慣寫 DSL Level，但 AI 需要 ISA Level 才能生成精確的測試。

第二常見是「只測 happy path」——AI 很擅長挖 edge case，但你要主動問。
-->

---

# M4 總結

<br>

**完整工作流的核心原則：**

1. **API Contract 先行** → 前後端解耦，並行開發
2. **Gherkin 即驗收** → 沒有模糊的 AC
3. **後端三巨頭** → 每個功能開工前的規格檢查清單
4. **ISA 是自動化的入口** → 越具體，AI 越精確

<br>

> 這個流程不是完美的，是迭代的。
> 第一次慢，第十次快。

---

<!-- _notes:
最後那句話很重要：
「第一次慢，第十次快」——導入新流程的 J curve。
一開始會覺得比之前慢（因為要寫 Gherkin、API Contract...），但當這成為習慣後，開發速度和品質都會顯著提升。

告訴大家：不要期待第一週就看到成效，要給自己 4-6 週的適應期。
-->
