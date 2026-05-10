# 練習 2 參考解答

---

## Step 1：ISA-Level Gherkin（展開版）

```gherkin
Scenario: 會員折扣碼同時存在，取較大折扣 [ISA]
  Given 訂單商品清單：[{ price: 500, qty: 2 }]（共 $1000）
  And   使用者會員等級："Gold"（discount_rate: 0.9）
  And   折扣碼："SAVE15"（discount_rate: 0.85）
  When  calculateDiscount([{ price: 500, qty: 2 }], "Gold", "SAVE15")
  Then  回傳值應為 850（套用較大折扣 SAVE15 = 0.85）
```

---

## Step 2：AI 生成測試（參考輸出）

```typescript
// discount.test.ts

interface OrderItem {
  price: number;
  qty: number;
}

type MemberLevel = 'Gold' | 'Silver' | 'Bronze';

describe('calculateDiscount', () => {
  describe('只有會員折扣', () => {
    it('Gold 會員九折', () => {
      const items: OrderItem[] = [{ price: 500, qty: 2 }];
      const result = calculateDiscount(items, 'Gold');
      expect(result).toBe(900);
    });

    it('Silver 會員九五折', () => {
      const items: OrderItem[] = [{ price: 200, qty: 5 }];
      const result = calculateDiscount(items, 'Silver');
      expect(result).toBe(950);
    });

    it('Bronze 會員無折扣', () => {
      const items: OrderItem[] = [{ price: 100, qty: 3 }];
      const result = calculateDiscount(items, 'Bronze');
      expect(result).toBe(300);
    });
  });

  describe('只有折扣碼', () => {
    it('SAVE10 折扣碼九折', () => {
      const items: OrderItem[] = [{ price: 200, qty: 3 }];
      const result = calculateDiscount(items, 'Bronze', 'SAVE10');
      expect(result).toBe(540);
    });
  });

  describe('會員折扣碼並存，取較大折扣', () => {
    it('折扣碼比會員折扣大時，套用折扣碼', () => {
      const items: OrderItem[] = [{ price: 500, qty: 2 }];
      const result = calculateDiscount(items, 'Gold', 'SAVE15');
      expect(result).toBe(850); // SAVE15=0.85 比 Gold=0.9 更低（更大折扣）
    });

    it('會員折扣比折扣碼大時，套用會員折扣', () => {
      const items: OrderItem[] = [{ price: 500, qty: 2 }];
      // Gold=0.9, SAVE10=0.9 → 相同時任取其一，結果 900
      const result = calculateDiscount(items, 'Gold', 'SAVE10');
      expect(result).toBe(900);
    });
  });

  describe('錯誤情況', () => {
    it('無效折扣碼應拋出錯誤', () => {
      const items: OrderItem[] = [{ price: 100, qty: 1 }];
      expect(() =>
        calculateDiscount(items, 'Gold', 'INVALID_CODE')
      ).toThrow('INVALID_DISCOUNT_CODE');
    });

    it('空訂單應拋出錯誤', () => {
      expect(() =>
        calculateDiscount([], 'Gold')
      ).toThrow('EMPTY_ORDER');
    });
  });
});
```

---

## Step 3：最小實作（參考輸出）

```typescript
// discount.ts

interface OrderItem {
  price: number;
  qty: number;
}

type MemberLevel = 'Gold' | 'Silver' | 'Bronze';

const DISCOUNT_CODES: Record<string, number> = {
  SAVE10: 0.9,
  SAVE15: 0.85,
  VIP20: 0.8,
};

const MEMBER_DISCOUNTS: Record<MemberLevel, number> = {
  Gold: 0.9,
  Silver: 0.95,
  Bronze: 1.0,
};

export function calculateDiscount(
  items: OrderItem[],
  memberLevel: MemberLevel,
  discountCode?: string
): number {
  if (items.length === 0) {
    throw new Error('EMPTY_ORDER');
  }

  const total = items.reduce((sum, item) => sum + item.price * item.qty, 0);

  let bestDiscount = MEMBER_DISCOUNTS[memberLevel];

  if (discountCode !== undefined) {
    const codeDiscount = DISCOUNT_CODES[discountCode];
    if (codeDiscount === undefined) {
      throw new Error('INVALID_DISCOUNT_CODE');
    }
    // 折扣率越低 = 折扣越大，取最低折扣率
    bestDiscount = Math.min(bestDiscount, codeDiscount);
  }

  return Math.round(total * bestDiscount);
}
```

---

## Step 5：Edge Case 挖掘（AI 可能找到的）

常見的 edge case（AI 通常會列出）：

1. **折扣碼大小寫不敏感**："save10" 應等同 "SAVE10" 嗎？
2. **折扣碼有效期**：如果折扣碼已過期？
3. **同一折扣碼只能用一次**：已使用過的折扣碼？
4. **商品數量為 0**：`{ price: 100, qty: 0 }` 應該排除嗎？
5. **負數金額**：`{ price: -50, qty: 1 }` 應該怎麼處理？
6. **折扣後金額小數點**：是四捨五入、無條件捨去，還是無條件進入？
7. **最大折扣上限**：有沒有「最多只能折 X%」的業務規則？
8. **null/undefined 會員等級**：如果 memberLevel 是 null？

這些都值得和 PO 討論，確認業務規則後，再加進 Gherkin。
