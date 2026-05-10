# AI x BDD：規格驅動全自動開發術 自學資源

> 涵蓋 Gherkin、Event Storming、TDD、BDD、ATDD、API-First 與 AI 輔助開發工作流

## 學習地圖

| 章節 | 主題 | 檔案 |
|------|------|------|
| Ch1 | 規格驅動開發的前提 | [01-sdd-foundation.md](01-sdd-foundation.md) |
| Ch2 | 規格的光譜：DDD + Event Storming | [02-event-storming-gherkin.md](02-event-storming-gherkin.md) |
| Ch3 | 70% 自動化：AI x TDD | [03-ai-tdd.md](03-ai-tdd.md) |
| Ch4 | 80% 自動化：AI x BDD | [04-ai-bdd.md](04-ai-bdd.md) |
| Ch5 | 最後一哩路：ATDD + ISA | [05-atdd-isa.md](05-atdd-isa.md) |
| Ch6 | API-First 敏捷開發工作流 | [06-api-first-workflow.md](06-api-first-workflow.md) |
| 附錄 | Prompt 範本庫 | [prompts/](prompts/) |

## 核心概念速查

```
規格層次
├── DSL-Level Gherkin   ← 業務語言，給 PO/QA 看
│     Given/When/Then (抽象)
└── ISA-Level Gherkin   ← 整合規格，給 AI 生成測試程式碼用
      Given/When/Then (具體參數、API、DB 狀態)

自動化程度進階
TDD (70%) → BDD (80%) → ATDD + ISA (100%)
```
