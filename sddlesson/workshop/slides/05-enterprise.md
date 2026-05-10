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
  pre { background: #1e293b; border-left: 4px solid #a78bfa; font-size: 0.8em; }
  table { border-collapse: collapse; width: 100%; }
  th { background: #1e3a5f; color: #7dd3fc; }
  td, th { padding: 8px 12px; border: 1px solid #334155; }
  blockquote { border-left: 4px solid #a78bfa; color: #94a3b8; background: #1e293b; padding: 12px 16px; }
---

# M5：企業導入策略

## 帶回去就能用的行動計畫

> 時間：15 分鐘

---

<!-- _notes:
最後一個模組，15 分鐘。
這個模組的目標是讓大家帶著「明天就能開始的行動計畫」離開。

不需要練習，主要是討論和規劃。
-->

---

# 導入的 J Curve

<br>

```
生產力
  ↑
高 │                              ╭─────────── AI + SDD 成熟期
   │                         ╭───╯
   │─────────────────────────╮  ← 現在（舊流程天花板）
   │                    ╭────╯
低 │               ╭────╯  ← 學習曲線（暫時下降）
   │          ╭────╯
   └──────────────────────────── 時間
         1週  2週  1個月  3個月
```

> **預期第 2-4 週最痛苦，第 6-8 週開始回本**

---

<!-- _notes:
這個 J Curve 圖是任何流程改變都會有的。
告訴大家：暫時的下降不是失敗的訊號，而是學習的訊號。

一些真實的時間線：
- Week 1: 學 Gherkin，感覺很慢
- Week 2-3: ISA Level 不會寫，Prompt 要調很多次
- Week 4: 開始有感覺，第一個功能從 Gherkin 到測試通過
- Week 6-8: 速度開始超過舊方式，品質更高
- Month 3+: 這變成標準流程，新人 onboarding 更快
-->

---

# 三段式導入路徑

<br>

```
第一階段：個人 MVP（Week 1-2）
  ✓ 選一個「下週要開發」的功能
  ✓ 用 Discovery + Gherkin 寫 AC
  ✓ 用 AI × TDD 完成這個功能
  ✓ 記錄時間：比之前快還是慢？

第二階段：雙人協作（Week 3-6）
  ✓ 找一個同事一起，一人寫 Gherkin，一人寫 Prompt
  ✓ 建立團隊 Prompt 模板庫（放在 Git）
  ✓ 在 Sprint 裡加入「Gherkin Review」環節

第三階段：團隊標準化（Month 2-3）
  ✓ 把 Gherkin 放進 User Story AC 模板
  ✓ PR 必須附帶對應的 Gherkin
  ✓ CI 自動跑 BDD 測試
```

---

<!-- _notes:
這個三段式路徑避免了「全面導入失敗」的風險。
很多公司試圖一次性導入所有新流程，結果失敗。

第一階段：只有你自己，沒有風險，學著用
第二階段：找到 early adopter，建立最佳實踐
第三階段：有了成功案例，推廣到全團隊

強調：不要等「準備好了」才開始，第一週就開始用，邊用邊學。
-->

---

# 從哪裡開始？量表評估

<br>

**花 2 分鐘評估你的團隊現狀（1-5 分）：**

| 維度 | 1（無）→ 5（很成熟）| 我的分數 |
|------|---------------------|---------|
| 測試覆蓋率 | 沒有測試 → 80%+ 覆蓋 | |
| 需求文件品質 | 口頭描述 → 完整 AC | |
| Prompt 使用 | 偶爾用 AI → 系統性使用 | |
| API 先行 | 先開發再討論 → Contract First | |
| CI/CD 成熟度 | 手動部署 → 全自動流水線 | |

**最低分的那個維度，就是你的第一優先**

---

<!-- _notes:
讓大家花 2 分鐘真的評估一下，寫在便利貼上。
然後問：「有人想分享自己最低分是哪個維度嗎？」

這個評估的用途：
1. 讓大家知道自己從哪裡開始
2. 避免「我要全部一起改進」的衝動（太貪心，通常失敗）
3. 讓大家帶著具體的行動方向離開
-->

---

# 常見阻力與應對策略

<br>

| 阻力 | 應對 |
|------|------|
| "寫 Gherkin 太花時間" | 先只在複雜功能用，簡單 CRUD 不強制 |
| "PO 不願意參與 Discovery" | 先讓 Dev + QA 寫，事後給 PO 確認 |
| "舊系統沒有測試，不知道從哪裡開始" | 針對新功能導入，舊的不動 |
| "AI 生的 code 品質不穩定" | 建立 Code Review checklist，AI 生成 + 人工審核 |
| "Senior 工程師不信任 AI" | 讓他做 Prompt 設計（最難的那部分），AI 做執行 |

---

<!-- _notes:
這些阻力是真實會碰到的。
不要假裝沒有阻力，而是給大家工具應對。

特別是最後一條：「Senior 工程師不信任 AI」
解法不是說服他信任 AI，而是讓他做最需要經驗的那部分（規格設計、Prompt 工程），AI 做最繁瑣的那部分（程式碼生成）。
Senior 的角色不是被取代，而是被放大。
-->

---

# AI Code Review 清單

<br>

基於 agent-skills 的 `code-review-and-quality` 模組：

```
Review 五個軸度（每個 PR 都要過）：

✦ 功能正確性：測試有沒有覆蓋到所有 Scenario？
✦ 程式碼簡潔性：Chesterton's Fence——為什麼這樣設計？
✦ 安全性：OWASP Top 10 有沒有潛在問題？
✦ 性能：有沒有明顯的 N+1 或記憶體洩漏？
✦ 可維護性：另一個工程師能在 5 分鐘內理解這段程式碼嗎？
```

**每個 PR 建議控制在 ~100 行以下（AI 也更容易 review）**

---

<!-- _notes:
這個 Code Review 清單來自 Addy Osmani 的 agent-skills 專案。
強調：AI 生成的程式碼也需要 Review，不是生出來就直接 merge。

「Chesterton's Fence」概念：不要輕易刪除你不理解用途的程式碼，先理解它為什麼存在。
這個原則防止了「AI 重構把有意義的 workaround 刪掉」的問題。

小 PR（~100 行）不是 AI 的限制，而是 Code Review 品質的要求。大 PR 連人類 reviewer 都無法有效 review。
-->

---

# 你的第一週行動計畫

<br>

**今天結束前，完成這個計畫：**

```
我下週要開發的功能：
_________________________________

我會用 Discovery 三問找出的 edge case：
1. ___
2. ___
3. ___

我會用 AI 做的事（勾選）：
☐ 從 Gherkin 生成測試
☐ 生成最小實作
☐ 挖掘 edge case
☐ Code Review / Refactor 建議

我會分享給 1 個同事的是：
_________________________________
```

---

<!-- _notes:
花 3-5 分鐘讓大家真的寫下來。
「社交承諾」研究顯示：寫下行動計畫並告訴別人，執行率從 20% 提升到 65%。

結束後請 2-3 位學員分享他們的計畫。
-->

---

# ROI：這套方法有多值？

<br>

| 指標 | 傳統模式 | AI × SDD 模式 | 提升 |
|------|---------|--------------|------|
| 功能開發週期 | 2 週 | 1 週 | ~50% |
| Bug 率（上線後） | baseline | 30-50% 減少 | 顯著 |
| Onboarding 時間 | 3-6 個月 | 1-2 個月 | 快 3x |
| 規格變更成本 | 高（重寫程式）| 低（改 Gherkin）| 大幅降低 |
| 技術債累積速度 | 快 | 慢 | 可控 |

> 數據來源：Addy Osmani 的 Google 工程師研究 + 業界案例

---

<!-- _notes:
這些數字是估算值，不要說得太精確（沒有辦法精確）。
但趨勢是對的：
- 功能週期縮短：主要來自「不用等規格討論」和「AI 生成加速」
- Bug 率降低：主要來自「edge case 提前發現」和「測試覆蓋率提升」
- Onboarding 加速：新人可以讀 Gherkin 快速理解系統行為，不用找人問

如果有學員問「這些數字哪裡來的？」：「根據 agent-skills 的工程實踐和業界多個案例的綜合估算，個別結果因團隊而異。」
-->

---

# 總結：今天學了什麼

<br>

```
M1：規格先行
  Gherkin = AI 的輸入格式
  Discovery → Formulation → Automation

M2：AI × TDD
  四個核心 Prompt 完成 Red-Green-Refactor
  Edge Case 系統挖掘

M3：Context Engineering
  三要素：角色 + 格式 + 範例
  Prompt 模板化 = 可複用資產

M4：完整工作流
  API-First 並行開發
  AC = Gherkin = 自動驗收

M5：企業導入
  三段式路徑 + 第一週行動計畫
```

---

<!-- _notes:
快速回顧。
強調：這不是「了解就好」的知識，而是要「實際用」才能得到效果的方法。
最重要的下一步是：今天下班前，找一個下週要開發的功能，用 Gherkin 寫一個 Scenario。

就這樣。不要等到「什麼都準備好了」。
-->

---

# 進階學習資源

<br>

| 資源 | 類型 | 說明 |
|------|------|------|
| [agent-skills](https://github.com/addyosmani/agent-skills) | GitHub | 20 個工程技能的 AI Prompt 模板 |
| [Cucumber / BDD](https://cucumber.io/docs/bdd/) | 官方文件 | BDD 方法論和 Gherkin 語法 |
| [Jest](https://jestjs.io/) | 官方文件 | JavaScript 測試框架 |
| [OpenAPI](https://swagger.io/specification/) | 規格 | API Contract 格式標準 |
| 本課程的 SDD 教材 | 內部資源 | Gherkin → ISA → AI 完整教材 |

<br>

📄 **今天的所有材料：** `sddlesson/workshop/`

---

<!-- _notes:
最後的學習資源。
agent-skills 是今天的主要靈感來源，建議大家回去讀一遍。
每個 Skill 都是一個獨立的文件，可以直接複製 Prompt 使用。

感謝大家的參與，開放 Q&A。
-->

---

# Q&A

<br>

> 沒有蠢問題。只有「問了會學到東西」和「沒問結果帶著疑惑離開」的差別。

<br>

**如果你現在還是不確定怎麼開始：**

→ 找我（或你的同事），一起用你明天要開發的功能練習一次。
   現場走 Discovery + 寫 Gherkin。10 分鐘。

---

<!-- _notes:
Q&A 時間。
如果沒有人問問題（冷場），可以問：
「你覺得今天最難的部分是什麼？」
「你最不確定怎麼應用到你工作上的是哪個部分？」

最後的 CTA（Call to Action）很重要：
不要讓大家帶著「好像理解了但不知道怎麼做」的感覺離開。
邀請他們找你當場練習，降低行動的心理門檻。
-->

---

# 謝謝大家！

<br>

**帶走三件事：**

1. 📋 速查表（cheatsheet.md）— 隨時查 Gherkin 語法
2. 🔧 Prompt 模板庫（prompt-library.md）— 直接複製使用
3. ✅ 第一週行動計畫 — 你剛才寫的那張紙

<br>

> 今天學的方法，明天就能用。
> 一個功能，一個 Gherkin，一個 AI 助理。出發。

---

<!-- _notes:
結尾要有能量。
「今天學的方法，明天就能用」這句話要讓大家相信。

確認大家都有拿到：
1. 速查表（實體講義）
2. Prompt 模板庫（實體講義）
3. 他們自己寫的第一週行動計畫

謝謝大家，結束。
-->
