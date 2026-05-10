# AI 輔助軟體開發實戰工作坊

> 3 小時 · 理論 × 實作 × 帶走即用

---

## 工作坊目標

結束時，學員能夠：

1. 用 Gherkin 把需求轉化為 AI 可讀的可執行規格
2. 走完一次 AI x TDD Red-Green-Refactor 完整循環
3. 設計穩定、可複用的 Prompt 模板
4. 說出完整的 AI 輔助開發工作流（從需求到上線）
5. 制定團隊導入的第一步行動計畫

---

## 議程總覽

| 時段 | 模組 | 內容 | 類型 |
|------|------|------|------|
| 0:00–0:15 | 開場 | 現況痛點 × 今天的解法 | 講授 |
| 0:15–0:45 | **M1：規格先行** | SDD + Gherkin 語言入門 | 講授 + 練習 |
| 0:45–1:30 | **M2：AI × TDD** | Red-Green-Refactor 實戰 | 講授 + 實作 |
| 1:30–1:40 | 休息 | — | — |
| 1:40–2:05 | **M3：Context Engineering** | Prompt 工程精要 | 講授 + 練習 |
| 2:05–2:35 | **M4：完整工作流** | API-First × 全流程 Demo | 講授 + Demo |
| 2:35–2:50 | **M5：企業導入** | 策略 × 常見誤區 × ROI | 講授 |
| 2:50–3:00 | 總結 & Q&A | 行動計畫 | 討論 |

---

## 檔案清單

```
workshop/
├── README.md                  本檔案：工作坊總覽
├── slides/
│   ├── 00-intro.md            開場投影片（Marp 格式）
│   ├── 01-spec-driven.md      M1：規格先行
│   ├── 02-ai-tdd.md           M2：AI × TDD
│   ├── 03-context-engineering.md  M3：Context Engineering
│   ├── 04-full-workflow.md    M4：完整工作流
│   └── 05-enterprise.md       M5：企業導入 + 總結
├── exercises/
│   ├── ex01-gherkin.md        練習 1：撰寫 Gherkin
│   ├── ex02-ai-tdd.md         練習 2：AI × TDD 全循環
│   ├── ex03-prompt.md         練習 3：Prompt 工程
│   └── solutions/             參考解答
│       ├── ex01-solution.md
│       ├── ex02-solution.md
│       └── ex03-solution.md
├── handouts/
│   ├── cheatsheet.md          速查表（帶走即用）
│   └── prompt-library.md      Prompt 模板庫
└── speaker-notes.md           完整講稿（每張投影片對應）
```

---

## 講師準備清單

### 技術環境
- [ ] 備好 Claude / ChatGPT 帳號（建議使用 Claude）
- [ ] Node.js 環境 + Jest 可執行（Demo 用）
- [ ] VS Code + Copilot 或 Cursor（選配）
- [ ] 投影片轉換：安裝 [Marp CLI](https://github.com/marp-team/marp-cli) 或 Marp VS Code 外掛

### 列印材料
- [ ] `handouts/cheatsheet.md` → 每人一份（雙面）
- [ ] `handouts/prompt-library.md` → 每人一份
- [ ] `exercises/ex01-gherkin.md` ~ `ex03-prompt.md` → 每人一份

### 教室設置
- [ ] 白板 + 白板筆（Event Storming 用）
- [ ] 便利貼（橘色/藍色/綠色各一疊）
- [ ] 計時器（練習時間管理）

---

## 參考資源

- [agent-skills by Addy Osmani](https://github.com/addyosmani/agent-skills)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/reference/)
- [Jest 文件](https://jestjs.io/docs/getting-started)
- [OpenAPI Specification](https://swagger.io/specification/)
