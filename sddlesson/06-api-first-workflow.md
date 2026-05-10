# Ch6：AI x BDD-API-First 敏捷開發工作流

## 完整工作流總覽

```
[需求/User Story]
       ↓
① Discovery（三方會議）
       ↓
② Event Storming → DSL-Level Gherkin
       ↓
③ API-First：定義後端三巨頭規格
   - API Contract（OpenAPI）
   - DB Schema
   - Domain Events
       ↓
④ ISA-Level Gherkin（展開具體參數）
       ↓
⑤ 並行開發：
   前端 → Mock Server（依 API Contract）
   後端 → AI x BDD（依 ISA Gherkin）
       ↓
⑥ 整合測試（驗證 Contract 一致性）
       ↓
⑦ ATDD 驗收（PO 確認 AC 通過）
       ↓
Done ✓
```

---

## 活動圖建模（流程分析工具）

活動圖用於理解「使用者的行為流程」，再從流程推導出系統行為。

### 活動圖 vs. Event Storming

| | 活動圖 | Event Storming |
|--|--------|---------------|
| 焦點 | 流程順序（How）| 業務事件（What）|
| 適合 | 複雜流程、有分支決策 | 多 Actor 協作、事件驅動 |
| 輸出 | 步驟序列 | Domain Events 清單 |

**使用建議：**
- 複雜流程 → 先畫活動圖，再做 Event Storming
- 簡單 CRUD → 直接 Event Storming

### 電商結帳活動圖

```
開始
  ↓
檢查購物車是否為空
  ├─ 是 → 顯示「購物車為空」→ 結束
  └─ 否 ↓
驗證庫存
  ├─ 庫存不足 → 顯示錯誤 → 結束
  └─ 庫存充足 ↓
選擇付款方式
  ↓
送出訂單
  ↓
呼叫金流 API
  ├─ 付款失敗 → 顯示錯誤，訂單取消 → 結束
  └─ 付款成功 ↓
扣減庫存
  ↓
發送確認信
  ↓
顯示訂單成立頁面
  ↓
結束
```

### 活動圖 → API + ISA 建模思維

每個「決策點」→ 對應一個 edge case Scenario
每個「外部系統呼叫」→ 對應一個需要 Mock 的依賴

---

## Discovery → Formulation → Automation 完整演練

### 功能：使用者完成社群登入（Google OAuth）

#### Step 1：Discovery（三個問題）

```
Actor: 未登入的使用者
Context: 使用者選擇「用 Google 登入」
Events: 
  - Google 授權成功 → 用戶登入/新增帳號
  - Google 授權失敗 → 顯示錯誤
  - 用戶取消授權 → 回到登入頁
```

#### Step 2：DSL-Level Gherkin（Formulation）

```gherkin
Feature: Google OAuth 登入

  Scenario: 新用戶首次 Google 登入
    Given 未在系統中註冊的使用者
    When  使用者完成 Google 授權
    Then  系統應自動建立帳號
    And   使用者應被導向歡迎頁面

  Scenario: 既有用戶 Google 登入
    Given 已在系統中的使用者（曾用 Google 登入過）
    When  使用者完成 Google 授權
    Then  使用者應被導向首頁

  Scenario: Google 授權失敗
    Given 使用者嘗試 Google 登入
    When  Google 回傳授權錯誤
    Then  系統應顯示「登入失敗，請稍後再試」
```

#### Step 3：後端三巨頭規格

```yaml
# API Contract
GET /auth/google/callback:
  query:
    code: string     # Google 授權碼
    state: string
  responses:
    302:             # 成功：重導向
      Location: /welcome  # 新用戶
      Location: /         # 既有用戶
    302:             # 失敗：重導向到錯誤頁
      Location: /login?error=oauth_failed
```

```sql
-- DB Schema（若需要新欄位）
ALTER TABLE users ADD COLUMN google_id VARCHAR(255) UNIQUE;
ALTER TABLE users ADD COLUMN avatar_url TEXT;
```

```json
// Domain Event
{
  "event": "UserLoggedIn",
  "payload": { "userId": "uuid", "method": "google", "isNewUser": true }
}
```

#### Step 4：ISA-Level Gherkin（Automation 準備）

```gherkin
Scenario: 新用戶首次 Google 登入 [ISA]
  Given Google OAuth Mock 回傳成功授權碼 "valid_code_001"
  And   Google User Info API 回傳 { googleId: "g001", email: "new@gmail.com", name: "New User" }
  And   資料庫中不存在 google_id = "g001" 的使用者
  When  GET /auth/google/callback?code=valid_code_001&state=csrf_token
  Then  HTTP 回應應為 302 重導向
  And   Location header 應為 "/welcome"
  And   資料庫 users 表應新增一筆 { email: "new@gmail.com", google_id: "g001" }
  And   回應應包含 Set-Cookie session token
  And   應發出 Domain Event "UserLoggedIn" { isNewUser: true }
```

---

## 超高速敏捷：User Story AC 直接綁定情境

### 傳統流程 vs. SDD 流程

```
傳統流程（慢）：
User Story → 口頭討論 → 開發 → QA 測試 → 發現問題 → 修改
（每個步驟都可能因理解不同而返工）

SDD 流程（快）：
User Story → AC = Gherkin → AI 實作 → 自動測試 = 驗收
（規格即測試，沒有詮釋空間）
```

### User Story Card 範例（AC 直接用 Gherkin 寫）

```markdown
## US-042：顧客可以對訂單評價

**Story：** 作為顧客，我想要對已完成的訂單留下評價，以便幫助其他顧客。

**AC1：成功提交評價**
```gherkin
Given 訂單 "o001" 狀態為「已完成」
And   顧客 "Alice" 是該訂單的購買者
When  POST /api/orders/o001/reviews { rating: 5, comment: "很棒！" }
Then  HTTP 201
And   評價應儲存至資料庫
And   訂單 "o001" 的平均評分應更新
```

**AC2：不能對未完成訂單評價**
```gherkin
Given 訂單 "o002" 狀態為「待付款」
When  POST /api/orders/o002/reviews { rating: 5 }
Then  HTTP 422，錯誤碼 "ORDER_NOT_COMPLETED"
```
```

---

## 從 ISA Gherkin 到完整自動化的 Prompt

```
你是一位 BDD 自動化工程師。請根據以下 ISA-Level Gherkin Feature，
完成以下任務（依序輸出）：

1. Step Definitions（TypeScript + Jest-Cucumber）
2. 被測服務的介面定義（TypeScript interface）
3. 被測服務的實作（最小可通過測試的實作）
4. 任何需要的 Mock/Stub（外部服務、DB）

注意：
- 使用 in-memory repository
- 外部 API 用 jest.mock()
- 每個 step 必須有明確的 assert

[貼入 ISA-Level Gherkin]
```

---

## 學習路徑建議

```
Week 1-2：Gherkin 語言 + Event Storming
  → 練習為現有功能撰寫 Gherkin，熟悉語法

Week 3-4：DSL vs. ISA Level 區分
  → 每天把 1 個 DSL Scenario 展開為 ISA

Week 5-6：AI x TDD 基礎循環
  → Red-Green-Refactor，加入 AI 輔助

Week 7-10：AI x BDD UT 層級
  → 建立完整的 Feature File + Step Definitions

Week 11-14：AI x BDD E2E 層級
  → Supertest/Playwright 整合，真實 HTTP 測試

Week 15-20：API-First 完整工作流
  → 完成一個真實功能的從 Discovery 到 Done
```
