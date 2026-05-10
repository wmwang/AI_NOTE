# 練習 1 參考解答

> 這是參考答案，不是唯一正確答案。Gherkin 有很多種寫法，重點是邏輯清楚、可讀、可測試。

---

## Step 1：Discovery 三問（參考）

**Actor：** 已登入或訪客使用者（搜尋通常不需要登入）

**Context：** 使用者在商品列表頁或首頁，想找特定商品

**Outcomes：**

| 情境 | 結果 |
|------|------|
| 搜尋關鍵字有結果 | 顯示相關商品列表，依相關度排序 |
| 搜尋關鍵字無結果 | 顯示「找不到符合的商品」提示，建議熱門商品 |
| 關鍵字為空 | 不搜尋，或顯示所有商品 / 顯示熱門商品 |
| 篩選條件 | 依價格範圍、評分篩選後更新結果 |

---

## Step 2：DSL-Level Gherkin（參考）

```gherkin
Feature: 商品搜尋

  Background:
    Given 商品資料庫中有以下商品：
      | 名稱       | 價格  | 評分 | 類別     |
      | iPhone 殼 | 250   | 4.5  | 手機配件 |
      | 藍芽耳機  | 1200  | 4.8  | 耳機     |
      | 充電線    | 80    | 3.9  | 配件     |

  Scenario: 搜尋關鍵字有結果，依相關度顯示
    Given 使用者在商品搜尋頁面
    When  使用者搜尋關鍵字 "耳機"
    Then  搜尋結果應包含 "藍芽耳機"
    And   搜尋結果應按相關度排序
    And   每個結果應顯示名稱、價格和評分

  Scenario: 搜尋關鍵字無結果
    Given 使用者在商品搜尋頁面
    When  使用者搜尋關鍵字 "電視"
    Then  畫面應顯示 "找不到符合 '電視' 的商品"
    And   畫面應顯示熱門商品推薦

  Scenario: 搜尋結果套用價格篩選
    Given 使用者已搜尋 "配件" 並看到 2 筆結果（$80 和 $250）
    When  使用者設定篩選條件「價格低於 $200」
    Then  搜尋結果應只顯示 "充電線"（$80）
    And   "iPhone 殼"（$250）不應出現在結果中
```

---

## 評分說明

**Good（上面的範例）：**
- `Given` 描述「使用者在什麼頁面、系統的狀態」
- `When` 只有一個搜尋動作
- `Then` 描述使用者可以看到的結果

**Common Mistakes：**
```gherkin
# ❌ When 太多動作
When  使用者輸入關鍵字 "耳機" 然後點擊搜尋按鈕然後等待結果

# ✅ 應該只有核心動作
When  使用者搜尋關鍵字 "耳機"
```

```gherkin
# ❌ Then 描述實作細節
Then  搜尋服務應呼叫 Elasticsearch 的 match query

# ✅ 應描述可觀察的結果
Then  搜尋結果應包含 "藍芽耳機"
```

---

## Advanced 解答（篩選功能 ISA Level）

```gherkin
Scenario: 套用價格篩選後更新搜尋結果 [ISA]
  Given 商品資料中存在：
    | productId | name      | price | rating |
    | p001      | iPhone 殼 | 250   | 4.5    |
    | p003      | 充電線    | 80    | 3.9    |
  And   使用者已搜尋 keyword: "配件"，結果包含 [p001, p003]
  When  GET /api/search?q=配件&maxPrice=200
  Then  HTTP 200
  And   response.body.results.length === 1
  And   response.body.results[0].productId === "p003"
  And   response.body.results[0].name === "充電線"
```
