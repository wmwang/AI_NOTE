# 練習 2：AI × TDD 全循環實作

> **時間：25 分鐘**
> **模組：M2 — AI × TDD**
> **需要：** 電腦 + Claude/ChatGPT + Node.js（選配）

---

## 情境說明

你要開發一個「折扣計算引擎」，需求如下：

> 訂單系統支援兩種折扣：
> 1. **折扣碼**：特定代碼對應特定折扣率（例如 SAVE10 = 九折）
> 2. **會員等級折扣**：Gold 九折、Silver 九五折、Bronze 無折扣
>
> 若兩種折扣同時存在，取**折扣較大者**。
> 折扣碼無效時應拋出錯誤，訂單金額為 0 或負數時應拋出錯誤。

---

## Step 1：展開 ISA-Level Gherkin（5 分鐘）

以下是 DSL-Level Gherkin，請展開成 ISA-Level（加入具體參數）：

**DSL Level（已給）：**
```gherkin
Scenario: 會員折扣碼同時存在，取較大折扣
  Given 訂單金額為 $1000
  And   使用者是 Gold 會員（九折）
  And   套用折扣碼 SAVE15（85 折）
  When  計算折扣後金額
  Then  最終金額應套用較大折扣（85 折）
```

**請展開為 ISA Level（填入具體參數）：**
```gherkin
Scenario: 會員折扣碼同時存在，取較大折扣 [ISA]
  Given 訂單商品清單：[___________________]
  And   使用者會員等級：[_______]（discount_rate: [_____]）
  And   折扣碼：[_______]（discount_rate: [_____]）
  When  呼叫 [__________________]([___________])
  Then  回傳值應為 [_______]
```

---

## Step 2：生成測試程式碼（5 分鐘）

把你展開的 ISA Gherkin，搭配以下 Prompt 貼給 AI：

```
你是一位資深 TDD 工程師，熟悉 TypeScript 和 Jest 測試框架。
請根據以下 ISA-Level Gherkin，生成完整的 Jest 測試程式碼。

規則：
- 只生成測試，不實作 calculateDiscount 函式本身
- 測試文件結構：describe → it（中文命名）
- Given → Arrange（準備測試資料）
- When → Act（呼叫 calculateDiscount）
- Then → Assert（用 expect() 驗證）
- 錯誤情境用 expect(...).toThrow()
- 函式簽章建議：calculateDiscount(items, memberLevel, discountCode?)

ISA Gherkin：
[貼入你展開的 ISA Gherkin + 下面提供的額外 Scenarios]
```

**額外需要測試的 Scenarios（一起貼給 AI）：**

```gherkin
Scenario: 只有折扣碼，無會員折扣 [ISA]
  Given 訂單：[{ price: 200, qty: 3 }]（共 $600）
  And   折扣碼："SAVE10"（discount_rate: 0.9）
  And   使用者會員等級："Bronze"（無折扣）
  When  calculateDiscount([{ price: 200, qty: 3 }], "Bronze", "SAVE10")
  Then  回傳值應為 540

Scenario: 無效折扣碼應拋出錯誤 [ISA]
  Given 折扣碼："INVALID_CODE" 不存在於折扣碼表
  When  calculateDiscount([{ price: 100, qty: 1 }], "Gold", "INVALID_CODE")
  Then  應拋出錯誤 "INVALID_DISCOUNT_CODE"

Scenario: 訂單金額為零應拋出錯誤 [ISA]
  Given 訂單商品清單為空陣列 []
  When  calculateDiscount([], "Gold")
  Then  應拋出錯誤 "EMPTY_ORDER"
```

---

## Step 3：生成最小實作（5 分鐘）

把 AI 生成的測試程式碼，搭配以下 Prompt 貼給 AI：

```
以下是一組 failing 測試（RED Phase）。
請實作 calculateDiscount 函式，讓所有測試通過。

規則：
- 只做測試要求的事，不做多餘的功能
- 折扣碼表可以用硬編碼 Map（不需要 DB）：
  "SAVE10" → 0.9, "SAVE15" → 0.85, "VIP20" → 0.8
- 使用 TypeScript，純函式（不需要 class）
- 函式簽章：calculateDiscount(items, memberLevel, discountCode?)

測試程式碼：
[貼入 Step 2 生成的測試]
```

---

## Step 4：執行測試（5 分鐘）

**如果有 Node.js 環境：**

```bash
# 建立專案（如果還沒有）
mkdir discount-engine && cd discount-engine
npm init -y
npm install jest ts-jest @types/jest typescript --save-dev

# 建立 tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "strict": true
  }
}
EOF

# 建立 jest.config.js
cat > jest.config.js << 'EOF'
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node'
}
EOF

# 把 AI 生成的測試存為 discount.test.ts
# 把 AI 生成的實作存為 discount.ts
npm test
```

**如果沒有環境（也可以）：**
→ 只閱讀 AI 生成的測試和實作，確認邏輯是否正確。
→ 觀察：測試有沒有覆蓋所有 Scenario？實作有沒有超出測試的要求？

---

## Step 5：挖掘 Edge Case（5 分鐘）

把以下 Prompt 貼給 AI：

```
以下是折扣計算引擎的主流程 Gherkin（Happy Path）。
請系統性地列出所有可能的邊界條件和 edge case，
並為每個 edge case 生成對應的 DSL-Level Gherkin Scenario。

分析維度：
- 輸入邊界（null、空值、負數、極大值）
- 折扣碼相關（過期碼、已使用碼、大小寫敏感）
- 會員相關（無效等級、null）
- 業務規則（折扣後金額如何取整？有沒有最低折扣限制？）

主流程：
[貼入你的 Happy Path Scenario]
```

**記錄：AI 提出了哪些你沒想到的 edge case？**

| Edge Case | 你有想到嗎？ | 是否重要？ |
|-----------|------------|-----------|
| | | |
| | | |
| | | |

---

## 反思問題

完成後，思考以下問題（不需要交出，個人反思）：

1. AI 生成的測試有多接近你預期的？哪裡不符合，是 Gherkin 的問題還是 Prompt 的問題？

2. 從 Gherkin 到有測試的程式碼，這個過程花了多少時間？跟你平常直接寫測試比呢？

3. 如果你要把這個 `calculateDiscount` 的 Gherkin 放進 User Story 的 AC，你會怎麼調整？
