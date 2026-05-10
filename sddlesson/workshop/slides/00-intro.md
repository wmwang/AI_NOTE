---
marp: true
theme: default
paginate: true
backgroundColor: #0f172a
color: #f1f5f9
style: |
  section {
    font-family: 'Noto Sans TC', sans-serif;
    font-size: 28px;
  }
  h1 { color: #38bdf8; font-size: 2em; }
  h2 { color: #7dd3fc; border-bottom: 2px solid #38bdf8; padding-bottom: 8px; }
  h3 { color: #bae6fd; }
  code { background: #1e293b; color: #a5f3fc; padding: 2px 6px; border-radius: 4px; }
  pre { background: #1e293b; border-left: 4px solid #38bdf8; }
  table { border-collapse: collapse; width: 100%; }
  th { background: #1e3a5f; color: #7dd3fc; }
  td, th { padding: 8px 12px; border: 1px solid #334155; }
  .highlight { color: #fbbf24; font-weight: bold; }
  blockquote { border-left: 4px solid #38bdf8; color: #94a3b8; }
---

# AI 輔助軟體開發實戰工作坊

## 從「用 AI 寫程式」到「用 AI 交付品質」

---

**講師：** [Your Name]
**時長：** 3 小時
**日期：** 2026

---

<!-- _notes:
歡迎大家！這個工作坊的目標不是「怎麼用 AI 更快寫程式」，而是「怎麼用 AI 確保交付的品質」。這兩件事差很多。
今天三小時之後，你們應該能走完一個完整的 AI 輔助開發循環。
-->

---

# 你現在怎麼用 AI 開發？

<br>

舉手調查：

1. 🙋 直接問 AI「幫我寫一個 XXX 功能」
2. 🙋 給 AI 看現有程式碼，問它怎麼改
3. 🙋 先寫測試，再讓 AI 實作
4. 🙋 用 AI 幫我審 code

---

<!-- _notes:
讓大家舉手，不用分析太多，這只是暖場。觀察一下分布。
通常 80% 以上的人在做 1 或 2，也就是「描述需求 → 期待 AI 給答案」這個模式。
這個模式的問題我們接下來會討論。
-->

---

# 大家都遇到的問題

<br>

| 症狀 | 根本原因 |
|------|----------|
| AI 每次生成的程式碼不一樣 | **沒有明確的規格** |
| AI 生的 code 看起來對，但跑起來有 bug | **沒有自動驗證** |
| 改了一個地方，不知道有沒有壞掉其他的 | **沒有測試保護** |
| 需求改了，AI 不知道 | **規格與程式碼分離** |
| 寫了很多 prompt，但結果不穩定 | **Context 給錯了** |

---

<!-- _notes:
這些問題大家應該都很熟悉。我不想花太多時間在痛點上，因為你們都已經感受到了。
重點是：這些問題的根本原因，不是 AI 不夠強，而是「我們沒有給 AI 足夠的結構」。

AI 是一台非常厲害的翻譯機，但你要告訴它：從哪裡翻譯到哪裡。
規格就是那個「從哪裡」。測試就是「驗證翻譯對不對」。
-->

---

# 今天的核心主張

<br>

> **AI 是執行引擎，不是思考引擎。**
> 你提供的結構決定了 AI 輸出的品質。

<br>

```
❌ 舊模式：模糊需求 → AI 腦補 → 你猜對了嗎？
✅ 新模式：可執行規格 → AI 生成 → 測試自動驗證
```

---

<!-- _notes:
這是整個工作坊最核心的一句話。先讓這句話在大家腦子裡落地。
「AI 是執行引擎，不是思考引擎」—— 思考的工作還是人做。
但人的思考結果要能被 AI 讀懂，這就需要「結構」。

接下來三小時，我們會學怎麼建立這個結構。
-->

---

# 今天的學習地圖

<br>

```
M1 規格先行 (30min)
  └─ 把需求寫成 AI 可讀的 Gherkin 規格

M2 AI × TDD (45min)
  └─ 讓 AI 幫你寫測試 → 再讓 AI 寫實作

M3 Context Engineering (25min)
  └─ 設計穩定的 Prompt 模板

M4 完整工作流 (30min)
  └─ API-First 並行開發全流程

M5 企業導入 (15min)
  └─ 帶回去就能用的行動計畫
```

---

<!-- _notes:
快速帶過議程。不需要解釋太多，每個模組開始前會再說明。
告訴大家：今天有三個動手練習，需要電腦。建議打開一個 Claude 視窗和一個編輯器。
-->

---

# 我們用的工具

<br>

| 工具 | 用途 | 替代品 |
|------|------|--------|
| Claude / ChatGPT | AI 助手（主角） | Gemini, Copilot |
| Gherkin | 可執行規格語言 | — |
| Jest (Node.js) | 測試框架 | pytest, JUnit |
| VS Code | 編輯器 | 任何 IDE |
| OpenAPI | API 規格 | — |

<br>

> 重要：工具是容器，方法論是核心。
> 今天學的方法可以用在任何語言、任何 AI 工具。

---

<!-- _notes:
強調這一點：工具會變，但「規格先行 + 測試驅動 + Context Engineering」這三個原則是通用的。
三年後你可能用不同的 AI，但這套思維框架還是一樣有用。
-->

---

# 讓我們開始

<br>

## M1：規格先行

### 為什麼 AI 需要規格？

---

<!-- _notes:
開始 Module 1。可以做一個深呼吸，讓大家進入學習狀態。
告訴大家：M1 是整個工作坊的地基。後面的每個模組都建立在這個基礎上。
-->
