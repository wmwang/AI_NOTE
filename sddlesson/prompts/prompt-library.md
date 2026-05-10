# AI x BDD Prompt 範本庫

---

## P01：需求 → DSL-Level Gherkin

```
你是一位 BDD 規格師。
請根據以下需求描述，生成 Gherkin Feature 檔案（DSL-Level）。
要求：
- 涵蓋 Happy Path + 至少 3 個 Edge Cases
- 語言使用繁體中文
- 不要包含技術細節（無 API endpoint、無 DB 欄位）

需求：
[貼入需求描述]
```

---

## P02：DSL-Level → ISA-Level 展開

```
你是一位後端架構師，熟悉 API-First 與 ISA 規格設計。
請將以下 DSL-Level Gherkin Scenario 展開為 ISA-Level。
要求：
- Given：指定具體的 DB 初始資料（表名、欄位值）
- When：指定 HTTP Method + Path + Request Body
- Then：指定 HTTP 狀態碼 + Response Body 結構 + DB 狀態變化

API 基礎路徑：[填入]
DB Schema（相關表）：[填入]

DSL-Level Scenario：
[貼入]
```

---

## P03：ISA Gherkin → Step Definitions

```
你是一位 TypeScript BDD 工程師，使用 Jest-Cucumber。
請根據以下 ISA-Level Gherkin Feature，生成完整的 Step Definitions。
要求：
- 使用 TypeScript
- Given → 初始化 in-memory repository 資料
- When → 呼叫 Service 方法或發送 HTTP 請求（用 supertest）
- Then → expect() assertions
- 外部服務用 jest.mock()
- 不要實作 Service，只生成測試

[貼入 ISA-Level Gherkin]
```

---

## P04：Step Definitions → Service 實作

```
以下是一組測試（Step Definitions），目前所有測試都失敗（Red 狀態）。
請實作 [ServiceName]，讓所有測試通過（Green 狀態）。
要求：
- 最小可運行實作，不過度設計
- 符合測試的介面定義
- 使用 TypeScript

測試程式碼：
[貼入 Step Definitions]

Service 介面（如已定義）：
[貼入 interface]
```

---

## P05：Edge Case 挖掘

```
以下是一個功能的主流程 Gherkin Scenario。
請分析所有可能的邊界條件與 edge cases，並列出：
1. 邊界條件清單（文字描述）
2. 每個邊界條件對應的 Gherkin Scenario

分類方式：
- 輸入驗證（格式錯誤、空值、超長）
- 業務規則（狀態不符、權限不足）
- 系統狀態（資源不存在、資源衝突）
- 外部依賴（第三方 API 失敗、逾時）

主流程 Scenario：
[貼入]
```

---

## P06：Event Storming → Gherkin

```
以下是一個功能的 Event Storming 結果（便利貼清單）。
請將其轉換為 Gherkin Feature 檔案。
規則：
- Actor + Read Model → Given
- Command → When
- Domain Event → Then
- Policy → Edge Case Scenario

Event Storming 結果：
Actor（黃）：[填入]
Commands（藍）：[填入]
Domain Events（橘）：[填入]
Policies（紫）：[填入]
External Systems（粉）：[填入]
```

---

## P07：後端三巨頭規格生成

```
你是一位後端架構師。
根據以下 User Story 和 DSL-Level Gherkin，生成後端三巨頭規格：

1. API Contract（OpenAPI 3.0 格式）
2. DB Schema 變更（新增/修改的 Table/欄位）
3. Domain Events 清單（事件名稱 + Payload 結構）

User Story：
[填入]

Gherkin：
[填入]

現有 DB Schema（相關部分）：
[填入]
```

---

## P08：重構建議

```
以下程式碼的所有測試都通過了。
請在不改變任何行為的前提下提供重構建議，並執行重構。
重構原則：
- 消除重複（DRY）
- 改善命名（可讀性）
- 分離關注點（SRP）
- 每次只做一個重構，確認測試仍通過

程式碼：
[貼入]

對應測試：
[貼入]
```

---

## P09：測試覆蓋率分析

```
請分析以下 Service 程式碼，識別測試覆蓋的盲點：
1. 哪些分支/條件沒有被現有測試覆蓋？
2. 列出缺少的 Gherkin Scenario
3. 優先級排序（高風險的 edge case 優先）

Service 程式碼：
[貼入]

現有 Gherkin：
[貼入]
```

---

## P10：前端 BDD Step Definitions（Playwright）

```
你是一位前端 E2E 測試工程師，使用 Playwright + Jest-Cucumber。
請根據以下 ISA-Level Gherkin，生成前端 Step Definitions。
要求：
- API Mock 使用 Playwright 的 route.fulfill()
- DOM 斷言使用 expect(page.locator())
- 支援 async/await

[貼入 ISA-Level Gherkin]
```
