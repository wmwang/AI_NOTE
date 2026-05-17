# Day 1 Content — 全自動化 AI SDLC

**對應大綱**: day1/outline.md
**適用對象**: 已有六堂課基礎的學員，理解 CLAUDE.md、Agentic Loop、Skill 開發、TDD、Clean Architecture

---

## u-1: 完整的 AI SDLC 概念

**對應任務**: d1-u1-t1, d1-u1-t2, d1-u1-t3
**圖片需求 (illustrations)**:
- `day1-u1-sdlc-flow.png` — 流程圖：六環節 + 文件同步循環箭頭 + A2P 審批點標記（AI 生圖，寬屏白底）
- `day1-u1-a2p-model.png` — 概念圖：Agent ↔ Person 審批來回模型（手繪風格 SVG）

### 概念講授（30 分鐘）

#### 1.1 完整的 AI SDLC（Software Development Life Cycle）

AI 全自駕 SDLC 將傳統軟體開發生命週期的每個環節都交給 AI Agent 執行，形成一條完全自動化的交付流水線。

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI 全自駕 SDLC                                │
│                                                                 │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌──────┐ │
│  │ 1.工單  │──→│ 2.分析  │──→│ 3.開發  │──→│ 4.測試  │──→│ 5.PR │ │
│  │ ADO     │   │ Wiki   │   │ TDD    │   │ CI     │   │ Review│ │
│  └────────┘   └────────┘   └────────┘   └────────┘   └──────┘ │
│       ↑                                                    │     │
│       │              ┌──────────────────┐                  │     │
│       └──────────────│ 6.文件同步        │←─────────────────┘     │
│                      │ LLM Wiki Update  │                        │
│                      └──────────────────┘                        │
│                                                                 │
│  🔒 A2P 安全審批：每個破壞性操作都需要人類確認                      │
└─────────────────────────────────────────────────────────────────┘
```

六個環節：
1. **工單（ADO）** — AI 讀取 Azure DevOps 工單，解析需求
2. **分析（Wiki）** — AI 查詢技術文件和架構決策，避免重複踩坑
3. **開發（TDD）** — AI 以測試驅動方式完成功能實作
4. **測試（CI）** — AI 執行單元/整合測試，產出覆蓋率報告
5. **PR Review** — AI 自己做 Code Review 後再發 PR
6. **文件同步** — AI 自動更新 Wiki，形成知識庫閉環

#### 1.2 六大環節詳解

##### 環節一：ADO 工單綁定

透過 `ado-devops` Skill，AI 可以直接讀取 Azure DevOps 工單：

```
claude
> 幫我看一下工單 #12345 的內容

AI 回應：
📋 工單 #12345
  標題：訂單 API 在大量訂單時回應 500 錯誤
  狀態：Active
  指派：小明
  描述：
    - 當同時下單超過 100 筆時，POST /api/v1/orders 回傳 500
    - Log 顯示資料庫連線池耗盡
    - 優先級：High
  Acceptance Criteria：
    - 修正連線池問題
    - 壓測 500 筆同時下單不報錯
```

##### 環節二：Wiki / 知識庫查詢

AI 在開發前先查詢相關的技術文件和架構決策：

```
claude
> 查一下 Wiki 中關於「訂單服務架構」和「資料庫連線池設定」的文件

AI 回應：
📄 相關文件：
  1. 訂單服務架構文件（Wiki/Architecture/Order-Service）
     - 使用 Spring Boot 3.2 + JPA
     - 資料庫：PostgreSQL 15
     - 連線池：HikariCP，maxPoolSize=10

  2. 連線池最佳實務（Wiki/BestPractices/Connection-Pool）
     - 建議公式：poolSize = CPU cores * 2 + disk_spindles
     - PostgreSQL 預設 max_connections=100

  ⚠️ 發現問題：目前 HikariCP maxPoolSize=10，但系統有 20 個 Service 實例
     可能是連線池耗盡的原因
```

##### 環節三：TDD 開發

使用 Agentic TDD 完成開發（第五、六堂內容）。核心節奏：

```
🔴 寫失敗的測試 → 🟢 實作讓測試通過 → ♻️ 重構
```

##### 環節四：CI 自動測試

```bash
# AI 自動執行
mvn test           # 單元測試
mvn verify          # 整合測試
mvn jacoco:report   # 覆蓋率報告
```

##### 環節五：AI Code Review（PR Reviewer）

AI 在發 PR 前先自己做一次 Code Review：

```
claude
> 請 Review 我這次的改動，檢查是否符合 Clean Architecture 和團隊規範

AI Review 結果：
🔍 Code Review Report

✅ 通過項目：
  - 架構分層正確（Controller → Service → Repository）
  - 測試覆蓋率 92%
  - DTO 轉換完整
  - 錯誤處理使用 GlobalExceptionHandler

⚠️ 建議改善：
  - OrderService.createOrder() 方法過長（45 行），建議拆分
  - HikariCP 設定值建議移至 Configuration Properties

❌ 必須修正：
  - 發現 TODO comment 未處理（第 87 行）
  - 缺少 @Transactional 註解（建立補貨單的操作需要事務保護）
```

##### 環節六：LLM Wiki 動態同步

開發完成後，AI 自動更新 Wiki 文件：

```
claude
> 開發完成，請更新 Wiki 中相關的技術文件

AI 自動更新：
  ✅ 更新「訂單服務架構文件」的連線池設定段落
  ✅ 新增「連線池調校紀錄」到變更日誌
  ✅ 更新 API 文件中的 POST /api/v1/orders 說明
```

#### 1.3 A2P（Agent-to-Person）安全審批

```
A2P 安全模型：

┌──────────┐     請求批准      ┌──────────┐
│   AI      │ ───────────────→ │   人類    │
│  Agent    │                  │  審批者   │
│           │ ←─────────────── │           │
└──────────┘     批准/拒絕     └──────────┘
```

**🔴 必須審批（破壞性操作）**：
- 合併 PR 到 main branch
- 部署到 staging / production
- 修改資料庫 schema
- 變更安全相關設定

**🟡 建議審批（高風險變更）**：
- 新增依賴套件
- 變更 API 介面
- 修改共用模組

**🟢 不需審批（常規工作）**：
- 更新文件
- 新增測試
- Code formatting

> 設計原則：讓 AI 充分發揮，但人類始終握有最終否決權。

---

## u-2: Demo — The Finale

**對應任務**: d1-u2-t1, d1-u2-t2, d1-u2-t3
**圖片需求 (illustrations)**:
- `day1-u2-demo-flow.png` — 截圖：8 步驟執行過渡畫面（8 分屏拼接或 GIF）

### Demo 實演 — The Finale（20 分鐘）

#### 完整的全自駕流程展示

```bash
# 一鍵啟動全流程
claude
> 請幫我完成工單 #12345：訂單 API 在大量訂單時回應 500 錯誤。
>
> 完整流程：
> 1. 讀取工單內容
> 2. 查詢 Wiki 相關文件
> 3. 分析根因
> 4. 使用 TDD 修復
> 5. 執行測試確保通過
> 6. 自行 Code Review
> 7. 更新 Wiki 文件
> 8. 建立 branch 並發 PR
>
> 每個需要審批的步驟，先暫停讓我確認。
```

```
AI 的完整執行過程：

═══════════════════════════════════════════
📋 Step 1/8：讀取工單
═══════════════════════════════════════════
→ 工單 #12345：訂單 API 500 錯誤
→ 優先級：High
→ [ADO] Skill 已啟用

═══════════════════════════════════════════
📚 Step 2/8：查詢 Wiki
═══════════════════════════════════════════
→ 找到「訂單服務架構文件」
→ 找到「連線池設定規範」
→ 發現：HikariCP maxPoolSize=10，但有 20 個 instance

═══════════════════════════════════════════
🔍 Step 3/8：分析根因
═══════════════════════════════════════════
→ 根因：20 個 instance × 10 connections = 200
→ PostgreSQL max_connections = 100
→ 連線池耗盡導致 500 錯誤
→ 修復方案：調整 maxPoolSize 為 5（20×5=100）
→ 或使用 PgBouncer 做 connection pooling

═══════════════════════════════════════════
🔴 Step 4/8：TDD 開發
═══════════════════════════════════════════
→ 寫測試：ConnectionPoolExhaustionTest
→ 🔴 測試失敗
→ 實作：調整 HikariCP 設定 + 加入等待超時處理
→ 🟢 測試通過
→ ♻️ 重構：抽取連線池設定為 Configuration Properties

═══════════════════════════════════════════
✅ Step 5/8：執行測試
═══════════════════════════════════════════
→ mvn test：24/24 通過 ✅
→ 覆蓋率：89%

═══════════════════════════════════════════
👀 Step 6/8：AI Code Review
═══════════════════════════════════════════
→ ✅ 架構分層正確
→ ✅ 測試完整
→ ⚠️ 建議：加入連線池監控指標
→ 已自動修正

═══════════════════════════════════════════
📝 Step 7/8：更新 Wiki
═══════════════════════════════════════════
→ 更新「訂單服務架構文件」連線池段落
→ 新增「連線池調校紀錄」
→ [需要 A2P 審批] 👤 人類確認：✅ 批准

═══════════════════════════════════════════
🚀 Step 8/8：發 PR
═══════════════════════════════════════════
→ Branch：fix/order-api-connection-pool-#12345
→ Commit：fix(order): adjust HikariCP pool size to prevent connection exhaustion
→ PR 已建立：PR #678
→ [需要 A2P 審批] 👤 人類確認：⏳ 等待審批

═══════════════════════════════════════════
✨ 完成！總耗時：約 8 分鐘（傳統流程約 2-4 小時）
═══════════════════════════════════════════
```

---

## u-4: 六大環節詳解

**對應任務**: d1-u4-t1 ~ d1-u4-t6
**圖片需求 (illustrations)**:
- `day1-u4-ado-workitem.png` — 截圖：ADO 工單內容（標題、狀態、指派、AC）
- `day1-u4-wiki-query.png` — 截圖：Wiki 文件查詢結果（找到 2 篇相關文件）
- `day1-u4-tdd-cycle.png` — 流程圖：🔴→🟢→♻️ 三色 TDD 循環
- `day1-u4-ci-report.png` — 截圖：mvn test + jacoco 覆蓋率報告
- `day1-u4-review-report.png` — 截圖：AI Code Review 報告（✅⚠️❌ 三區）
- `day1-u4-wiki-update.png` — 截圖：Wiki 文件自動更新（✅ 三行）

### 休息後再補充說明

**環節一：ADO 工單綁定**
- Skill：`ado-devops`
- 操作方式：自然語言描述需求，Skill 解析並讀取工單
- 工單內容包含：標題、狀態、指派、優先級、描述、Acceptance Criteria

**環節二：Wiki / 知識庫查詢**
- 查詢維度：架構文件、最佳實務、API 文件、變更日誌
- 查詢結果：用於在开发前了解既有约束，避免重复踩坑

**環節三：TDD 開發**
- 參考第五、六堂的 Agentic TDD 方法
- 核心節奏：🔴 失敗測試 → 🟢 實作 → ♻️ 重構

**環節四：CI 自動測試**
- 三命令：`mvn test` / `mvn verify` / `mvn jacoco:report`
- 覆蓋率門檻：建議 80% 以上

**環節五：AI Code Review**
- 使用 PR Reviewer Skill
- 三類結果：✅ 通過 / ⚠️ 建議改善 / ❌ 必須修正

**環節六：LLM Wiki 動態同步**
- 自動更新技術文件
- 新增變更日誌
- A2P 審批後執行

---

## u-5: 知識庫閉環概念

**對應任務**: d1-u5-t1, d1-u5-t2, d1-u5-t3
**圖片需求 (illustrations)**:
- `day1-u5-closed-loop.png` — 循環圖：開發新功能 → 產出程式碼和文件 → 更新 Wiki → 下次開發讀取（手繪 SVG，暖色風格）

### 知識庫閉環：讓 AI 越來越聰明

```
知識庫閉環循環：

開發新功能 → 產出程式碼和文件 → 更新 Wiki
     ↑                              │
     │                              ▼
  下次開發 ←── AI 讀取 Wiki 知識 ←── 累積知識
```

每次開發都會產生新的知識（架構決策、API 設計、踩過的坑），這些知識存入 Wiki 後，AI 下次開發時就能參考，形成正向循環。

**三個形成閉環的關鍵行為**：
1. **主動記錄**：每次修复 bug，都同步更新 Wiki 的「已知問題」章節
2. **引用積累**：下次遇到類似問題，先查 Wiki 再動手
3. **版本同步**：PR 合併後，自動更新相關技術文件

**哪些知識適合放 Wiki**：
- 架構決策與理由
- API 設計原則
- 常見錯誤與解決方式
- 效能調校參數

**哪些不適合放 Wiki**：
- 純程式碼（程式碼本身在 Git）
- 臨時性備註
- 涉及機密資料的內容

---

## u-6: Quick Win — 觸發 AI PR Reviewer

**對應任務**: d1-u6-t1, d1-u6-t2, d1-u6-t3, d1-u6-t4
**圖片需求 (illustrations)**:
- `day1-u6-bad-controller.png` — 程式碼截圖：BadController.java 六大違規標注（紅色框選 + 序號）

### Quick Win：課堂 10 分鐘動手（10 分鐘）

**任務**：觸發 AI PR Reviewer，觀察它抓出架構違規

#### Step 1：建立一個「故意違規」的 Spring Boot 專案（2 min）

```bash
mkdir pr-review-demo && cd pr-review-demo
git init
```

#### Step 2：建立違規程式碼

```java
import org.springframework.web.bind.annotation.*;
import javax.persistence.*;

@RestController
public class BadController {
    @PersistenceContext
    private EntityManager em;  // ❌ 直接在 Controller 注入 EntityManager

    @PostMapping("/api/orders")
    public String createOrder(@RequestBody String body) {
        // ❌ 直接在 Controller 寫 SQL
        em.createNativeQuery("INSERT INTO orders ...").executeUpdate();
        // ❌ 沒有 DTO 轉換
        // ❌ 沒有錯誤處理
        // ❌ System.out.println
        System.out.println("Order created: " + body);
        return body;  // ❌ 直接回傳 Request Body
    }
}
```

#### Step 3：讓 AI Review（5 min）

```bash
claude
> 請 Code Review 這個改動，以 Clean Architecture 和以下規範檢查：
> - Controller 不可以直接存取 Repository/EntityManager
> - 所有回傳必須使用 DTO
> - 禁止使用 System.out.println
> - 所有資料庫操作必須在 Service 層
> - 必須有錯誤處理
```

#### Step 4：觀察結果（3 min）

確認 AI 抓出以下所有違規：

| 違規項目 | 預期 AI 抓到 |
|---|---|
| 1 | Controller 直接注入 EntityManager |
| 2 | Controller 直接執行 SQL |
| 3 | 沒有 DTO 轉換 |
| 4 | 使用 System.out.println |
| 5 | 沒有錯誤處理 |

---

## u-7: 回家作業說明 — 結業挑戰

**對應任務**: d1-u7-t1, d1-u7-t2, d1-u7-t3, d1-u7-t4
**圖片需求 (illustrations)**:
- `day1-u7-challenge-table.png` — 表格圖：結業挑戰紀錄表範本（步驟 × 工具 × 截圖 × 耗時，寬屏橫式）

### 回家作業（結業挑戰）

**目標**：證明你可以用 AI Agent 完成從工單到 PR 的全流程。

#### 步驟一：挑選工單

- 選一張低風險的 Backlog 工單（bug fix 或小功能）
- 確保不涉及核心業務邏輯或安全相關變更
- 獲得主管同意後開始

#### 步驟二：執行全流程

```
## 結業挑戰紀錄表

### 工單資訊
- 工單號碼：
- 標題：
- 風險等級：低

### 流程紀錄

| 步驟 | 工具/Skill | 截圖 | 耗時 |
|------|-----------|------|------|
| 1. 讀取工單 | ado-devops | | |
| 2. 查詢 Wiki | | | |
| 3. TDD 開發 | | | |
| 4. 測試通過 | mvn test | | |
| 5. Code Review | | | |
| 6. 更新文件 | | | |
| 7. 發 PR | git | | |

### 總結
- 傳統預估耗時：___ 小時
- 實際 AI 輔助耗時：___ 分鐘
- AI 節省的時間比例：___%
- 遇到的問題和解決方式：
- 心得與建議：
```

#### 步驟三：品質檢查

- [ ] PR 的程式碼有對應的測試
- [ ] 測試全部通過
- [ ] 沒有跳過 A2P 審批
- [ ] Wiki 文件已更新
- [ ] commit message 符合規範

#### 評分標準

| 項目 | 比重 |
|------|:---:|
| 流程完整度（7 個步驟是否都執行） | 30% |
| 程式碼品質（測試、架構、規範） | 25% |
| 文件更新完整度 | 15% |
| 效率提升數據 | 15% |
| 心得反思的深度 | 15% |

---

## u-8: 七堂課總回顧

**對應任務**: d1-u8-t1, d1-u8-t2, d1-u8-t3
**圖片需求 (illustrations)**:
- `day1-u8-seven-days.png` — 表格圖：七堂課總表（堂數 × 主題 × 核心技能，寬屏橫式）

### 七堂課總回顧

| 堂數 | 主題 | 核心技能 |
|:---:|------|---------|
| 1 | 企業級 AI 基礎建設 | CLAUDE.md、架構邊界 |
| 2 | 解構大廠 Agent 底層 | Agentic Loop、Error Recovery |
| 3 | 專屬 SRE 兵器庫 | MCP Server、AI-Friendly 腳本 |
| 4 | 擴充 GitAgent 生態 | Skill 開發、防呆 Schema |
| 5 | AI 系統分析實戰 | 逆向工程、規格萃取 |
| 6 | AI 架構重構實戰 | Agentic TDD、Clean Architecture |
| 7 | 全自動化 AI SDLC | 端到端 Workflow、知識庫閉環 |

### 最終心法

> 🏆 **AI Coding Agent 的三大紀律**：
> 1. **架構先行** — 用 CLAUDE.md 定義邊界，讓 AI 在框架內發揮
> 2. **規格驅動** — 先有規格再寫程式，測試是規格的可執行版本
> 3. **人機協作** — AI 做重複性工作，人類做決策和審批

> 🎓 **結業不是結束**：把你學到的 Skill 貢獻到團隊 Repo，讓全團隊的 AI 都能受益。這才是 AI 時代的工程文化。

---

## 參考素材

| 素材 | 對象 | 備註 |
|---|---|---|
| 全自動化AI_SDLC.md | 學員 | 原始講義（備查，不納入 SPA） |
| BadController.java | 學員 | Quick Win 範例程式碼 |
| 結業挑戰紀錄表.md | 學員 | 回家作業填寫範本 |
| 七堂課總回顧表格.md | 學員 | 參考用 |