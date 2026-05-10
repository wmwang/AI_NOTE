# Prompt 模板庫

> 直接複製使用 · 根據你的語言和框架調整 `[佔位符]`

---

## 1. 規格轉換類

### 1-A：需求 → DSL Gherkin

```
你是一位 BDD 規格分析師，熟悉 Gherkin 語言和業務分析。

請根據以下使用者需求，執行 Discovery 並輸出 DSL-Level Gherkin。

Discovery 三問：
1. Actor：誰在使用這個功能？
2. Context：在什麼前提下使用？
3. Outcomes：所有可能的結果（Happy Path + Edge Cases）

輸出規則：
- 只輸出 Gherkin Feature，不要其他解釋
- Scenario 名稱要清楚描述情境
- Given 描述狀態，When 只有一個動作，Then 描述可觀察結果
- 至少包含 1 個 Happy Path 和 2 個 Edge Case

需求：
{{REQUIREMENT}}
```

---

### 1-B：DSL Gherkin → ISA Gherkin

```
你是一位後端 API 設計師，熟悉 RESTful API 和 BDD。

請將以下 DSL-Level Gherkin 展開為 ISA-Level（整合規格層級）Gherkin。

展開規則：
- 加入真實的 ID（用 "u001", "p001" 等格式）
- Given 加入具體的資料結構（JSON 格式）
- When 加入 HTTP 方法 + endpoint + request body（如適用）
- Then 加入具體的 HTTP status code 和 response body 欄位
- 加入 DB 狀態變化（如適用）
- 加入 Domain Events（如適用）

DSL Gherkin：
{{DSL_GHERKIN}}

技術棧：
- 語言：{{LANGUAGE}}
- 框架：{{FRAMEWORK}}
- DB：{{DATABASE}}
```

---

### 1-C：需求 → 後端三巨頭規格

```
你是一位後端架構師，熟悉 RESTful API 設計和資料庫設計。

根據以下功能需求，輸出「後端三巨頭」規格文件。

輸出格式（依序輸出，不要其他說明）：

## API Contract（OpenAPI YAML 格式）
[endpoint + request/response schema + error codes]

## DB Schema（SQL 格式）
[新增或修改的 Table / Column]

## Domain Events（JSON 格式）
[事件名稱 + payload 結構]

功能需求：
{{REQUIREMENT}}

現有系統背景（如果有）：
{{CONTEXT}}
```

---

## 2. 測試生成類

### 2-A：ISA Gherkin → Jest 測試（TypeScript）

```
你是一位資深 TDD 工程師，熟悉 TypeScript 和 Jest 測試框架。

請根據以下 ISA-Level Gherkin，生成完整的 Jest 測試程式碼。

規則：
- 只生成測試，不實作被測函式或 class
- 使用 describe/it 結構，中文或英文命名皆可
- Given → beforeEach（Arrange）
- When → Act（呼叫被測函式，結果存入變數）
- Then → expect() assertions
- 錯誤情境用 expect(() => ...).toThrow('ERROR_CODE')
- 使用 in-memory 資料結構，不連接真實 DB
- 每個 it() 應該只測試一個行為

ISA Gherkin：
{{ISA_GHERKIN}}
```

---

### 2-B：ISA Gherkin → pytest 測試（Python）

```
你是一位資深 TDD 工程師，熟悉 Python 和 pytest 測試框架。

請根據以下 ISA-Level Gherkin，生成完整的 pytest 測試程式碼。

規則：
- 只生成測試，不實作被測函式
- 使用 pytest fixture 做資料準備（Given）
- 函式命名：test_[情境描述]（底線分隔）
- 錯誤情境用 pytest.raises()
- 不連接真實 DB（用 in-memory 或 monkeypatch）

ISA Gherkin：
{{ISA_GHERKIN}}
```

---

### 2-C：測試 → 最小實作

```
以下是一組 failing 測試（Red Phase），它們描述了一個函式的預期行為。
請實作這個函式，讓所有測試通過。

實作規則：
- 只做測試要求的事，不做測試沒有驗證的功能
- 保持程式碼簡單（不要過度設計）
- 使用 {{LANGUAGE}} 語言
- 外部依賴（DB、API）用 interface 隔離，不要直接依賴

測試程式碼：
{{TEST_CODE}}
```

---

### 2-D：Edge Case 系統挖掘

```
你是一位資深 QA 工程師，擅長找到系統的邊界條件。

以下是一個功能的主流程 Gherkin Scenario（Happy Path）。
請系統性地列出所有可能的邊界條件和 edge case，
並為每個 edge case 生成 DSL-Level Gherkin Scenario。

分析維度（每個維度都要考慮）：
- 輸入邊界：null、空值、空字串、空陣列、負數、零、極大值、特殊字元
- 狀態邊界：不存在的資源 ID、已刪除的資源、未授權的使用者
- 業務規則邊界：限額、到期日、次數限制、狀態機轉換
- 並發情況：同時操作同一資源、重複提交

輸出格式：
對每個 edge case 說明「為什麼這是邊界」，然後輸出 Gherkin Scenario。

主流程：
{{HAPPY_PATH_GHERKIN}}
```

---

## 3. 程式碼品質類

### 3-A：Code Review（五軸）

```
你是一位資深工程師，正在做 Code Review。

請從以下五個軸度審查這段程式碼，每個軸度都要有具體的發現和建議：

① 功能正確性：邏輯有沒有 bug？邊界條件處理了嗎？
② 簡潔性：有沒有不必要的複雜度？Chesterton's Fence——為什麼這樣設計？
③ 安全性：有沒有 OWASP Top 10 的潛在問題？（SQL injection、XSS、未授權存取等）
④ 性能：有沒有明顯的性能問題？（N+1、記憶體洩漏、不必要的計算）
⑤ 可維護性：另一個工程師 5 分鐘內能理解這段程式碼嗎？命名清楚嗎？

輸出格式：
- 對每個軸度：「發現」和「建議」（如果沒有問題就說「OK」）
- 最後：「必須修改」和「建議修改」的清單

程式碼：
{{CODE}}
```

---

### 3-B：安全性掃描（OWASP Top 10）

```
你是一位資安工程師。

請掃描以下程式碼，檢查是否有 OWASP Top 10 的安全漏洞，特別關注：
- A01: 存取控制（Authorization checks）
- A02: 密碼學失效（明文密碼、弱加密）
- A03: Injection（SQL、XSS、Command Injection）
- A05: 安全配置錯誤
- A07: 身份驗證問題

對每個發現的問題：
1. 描述漏洞
2. 說明攻擊情境（攻擊者可以做什麼）
3. 提供修正後的程式碼

程式碼：
{{CODE}}
```

---

### 3-C：重構（不改行為）

```
以下程式碼的測試都通過了。
請在不改變任何外部行為的前提下重構程式碼。

重構目標（按優先序）：
1. 消除重複程式碼（DRY 原則）
2. 改善命名（函式名、變數名要能表達意圖）
3. 減少函式複雜度（每個函式只做一件事）
4. 減少認知複雜度（巢狀層數、magic numbers）

約束：
- 每次重構一個小步驟，不要一次改太多
- 重構後必須說明「改了什麼、為什麼這樣改」
- 對應測試不應該需要修改

程式碼：
{{CODE}}

對應測試：
{{TEST_CODE}}
```

---

## 4. API 設計類

### 4-A：功能需求 → OpenAPI Contract

```
你是一位 API 設計師，熟悉 RESTful API 和 OpenAPI 3.0。

根據以下功能需求，設計 API Contract（OpenAPI YAML 格式）。

設計原則：
- 遵循 RESTful 資源命名（名詞複數）
- HTTP 方法語意正確（GET/POST/PUT/PATCH/DELETE）
- 錯誤回應要有具體的 error code（字串），不只是 HTTP status
- 需要分頁的列表要加 pagination 參數
- 需要認證的 endpoint 要標記 security

輸出格式：OpenAPI 3.0 YAML

功能需求：
{{REQUIREMENT}}
```

---

## 5. 文件類

### 5-A：程式碼 → Architecture Decision Record (ADR)

```
根據以下程式碼或設計決策，產生一份 Architecture Decision Record（ADR）。

ADR 格式：
# ADR-[編號]：[決策標題]

## 狀態
[提議 / 已接受 / 已棄用]

## 背景
[為什麼需要做這個決策？]

## 決策
[我們決定做什麼？]

## 後果
### 正面影響
### 負面影響 / 取捨
### 風險

程式碼或設計：
{{CODE_OR_DESIGN}}
```

---

*更新這個模板庫：把用過效果好的 Prompt 加進來*
*存在 Git repo，和程式碼一起版本控制*
