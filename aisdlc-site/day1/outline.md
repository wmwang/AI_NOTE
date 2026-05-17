# Day 1: 全自動化 AI SDLC — Workflow 與知識庫閉環

## 學習目標
- 能夠敘述 AI 全自駕 SDLC 的六大環節及其串連邏輯
- 能夠說明 A2P（Agent-to-Person）安全審批模型的應用場景
- 能夠執行完整的工單 → Wiki → TDD → CI → Code Review → PR → 文件同步流程
- 能夠觸發 AI Code Review 並解讀其回饋報告
- 能夠建立並維護知識庫閉環

## 時程
| 時段 | 單元 | 重點 |
|---|---|---|
| 00:00–00:30 | u-1: 完整的 AI SDLC 概念 | 六環節流程圖、A2P 安全模型 |
| 00:30–00:50 | u-2: Demo — The Finale | 一鍵全流程實演（8 分鐘完成傳統 2-4 小時的工作） |
| 00:50–01:00 | u-3: 休息 | |
| 01:00–01:10 | u-4: 六大環節詳解 | ADO 工單綁定、Wiki 查詢、TDD、CI、AI Review、Wiki 同步 |
| 01:10–01:20 | u-5: 知識庫閉環概念 | 開發 → 產出 → 更新 Wiki → 下次引用，形成正向循環 |
| 01:20–01:35 | u-6: Quick Win | 動手：觸發 AI PR Reviewer，觀察它抓出架構違規 |
| 01:35–01:50 | u-7: 回家作業說明 | 結業挑戰：用完整 Agentic Workflow 跑完真實工單 |
| 01:50–02:00 | u-8: 七堂課總回顧 | 三大紀律、結業心法 |

## 單元細部

### u-1: 完整的 AI SDLC 概念
- **學習目標**: 能夠在白板上畫出 AI 全自駕 SDLC 的六大環節流程圖，並標示 A2P 安全審批的插入點
- **任務 (tasks)**:
  - [ ] 觀察六環節流程圖（ADO → 分析 → 開發 → 測試 → PR → Wiki 更新）
  - [ ] 找出循環回饋的位置（文件同步如何回頭影響工單分析）
  - [ ] 標示 A2P 必須審批 vs 建議審批 vs 不需審批的操作
- **素材需求**: 流程圖（可用 draw.io 或 Mermaid），A2P 安全模型圖

### u-2: Demo — The Finale
- **學習目標**: 能夠在看過示範後重現「一鍵啟動 8 分鐘全流程」的步驟
- **任務 (tasks)**:
  - [ ] 觀察 AI 執行 8 步驟的完整過程（不需動手，先理解流程）
  - [ ] 記錄每個步驟耗時與對應的傳統做法耗時
  - [ ] 觀察 A2P 審批點在哪兩個步驟出現
- **素材需求**: Demo 腳本（已在全自動化AI_SDLC.md 中定義）

### u-3: 六大環節詳解
- **學習目標**: 能夠針對每個環節說出對應的工具/Skill 名稱及在流程中的角色
- **任務 (tasks)**:
  - [ ] 環節一：ADO 工單綁定 — 使用 `ado-devops` Skill 讀取工單
  - [ ] 環節二：Wiki / 知識庫查詢 — 查訂單服務架構文件、連線池設定規範
  - [ ] 環節三：TDD 開發 — 參考第五、六堂的 Agentic TDD
  - [ ] 環節四：CI 自動測試 — `mvn test / verify / jacoco:report`
  - [ ] 環節五：AI Code Review — 使用 PR Reviewer Skill
  - [ ] 環節六：LLM Wiki 動態同步 — 自動更新技術文件
- **素材需求**: 六大環節的詳細步驟截圖或 Live Demo

### u-4: 知識庫閉環概念
- **學習目標**: 能夠解釋為何每次開發都會讓 AI 變得更聰明，並能列舉三個形成閉環的關鍵行為
- **任務 (tasks)**:
  - [ ] 畫出知識庫閉環循環圖
  - [ ] 說明 Wiki 文件的累積如何影響下次開發的品質
  - [ ] 討論：哪些知識適合放 Wiki？哪些不適合？
- **素材需求**: 循環圖（可用 Mermaid 或 Excalidraw）

### u-5: Quick Win — 觸發 AI PR Reviewer
- **學習目標**: 能夠對一個故意違規的 Spring Boot 程式碼觸發 AI Code Review，並從報告中揪出全部 5 個架構違規
- **任務 (tasks)**:
  - [ ] 建立一個 `BadController.java`（含 5 個 Clean Architecture 違規）
  - [ ] 對該檔案執行 AI Code Review
  - [ ] 對照檢查清單確認全部 5 個違規都被抓到：
    - ❌ Controller 直接注入 EntityManager
    - ❌ Controller 直接執行 SQL
    - ❌ 沒有 DTO 轉換
    - ❌ 使用 System.out.println
    - ❌ 沒有錯誤處理
- **素材需求**: `BadController.java` 範例檔（已在全自動化AI_SDLC.md 中定義）

### u-6: 回家作業說明 — 結業挑戰
- **學習目標**: 能夠獨立在真實低風險 Backlog 工單上完成從工單到 PR 的全流程，並填寫結業挑戰紀錄表
- **任務 (tasks)**:
  - [ ] 挑選一張低風險 Backlog 工單（bug fix 或小功能）
  - [ ] 完成 7 步驟流程並記錄截圖與耗時
  - [ ] 填寫結業挑戰紀錄表（工單資訊、流程紀錄表、總結）
  - [ ] 自評品質檢查：測試、架構、A2P、Wiki 更新、commit 規範
- **素材需求**: 結業挑戰紀錄表範本（已在全自動化AI_SDLC.md 中定義）

### u-7: 七堂課總回顧
- **學習目標**: 能夠將七堂課的內容串成一條主線，並找出自己最需要加強的環節
- **任務 (tasks)**:
  - [ ] 填寫七堂課核心技能總表
  - [ ] 背誦「AI Coding Agent 三大紀律」
  - [ ] 討論：如何將學到的 Skill 貢獻到團隊 Repo
- **素材需求**: 七堂課總回顧表格（已在全自動化AI_SDLC.md 中定義）

## 圖片需求 (illustrations)
- 全自動化 AI SDLC 流程圖（六環節 + 循環）
- A2P 安全審批模型圖
- 知識庫閉環循環圖
- Demo 截圖（8 步驟執行過程）
- Quick Win：BadController 違規示意圖
- 七堂課總回顧表格