# 第七堂：全自動化 AI SDLC — Workflow 與知識庫閉環

> **核心命題**：一鍵讀工單 → 查 Wiki → 開發過測 → 更新文件 → 發 PR。這就是全自駕的 AI 軟體交付流程。

---

## 📋 本堂摘要

| 項目 | 內容 |
|------|------|
| 🎯 主題 | ADO 工單綁定、AI Code Review、LLM Wiki 同步、A2P 安全審批 |
| 🎬 Demo | The Finale：一鍵完成從工單到 PR 的全自駕流程 |
| ⚡ Quick Win | 觸發 AI PR Reviewer，觀察它抓出架構違規 |
| 📝 作業 | 結業挑戰：用完整 Agentic Workflow 跑完一張真實工單 |

---

## 一、概念講授（30 mins）

### 1.1 完整的 AI SDLC（Software Development Life Cycle）

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

### 1.2 六大環節詳解

#### 環節一：ADO 工單綁定

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

#### 環節二：Wiki / 知識庫查詢

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

#### 環節三：TDD 開發（第五、六堂的內容）

使用 Agentic TDD 完成開發，確保測試通過。

#### 環節四：CI 自動測試

```bash
# AI 自動執行
mvn test           # 單元測試
mvn verify          # 整合測試
mvn jacoco:report   # 覆蓋率報告

# 確認通過後進入下一步
```

#### 環節五：AI Code Review（PR Reviewer）

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

#### 環節六：LLM Wiki 動態同步

開發完成後，AI 自動更新 Wiki 文件：

```
claude
> 開發完成，請更新 Wiki 中相關的技術文件

AI 自動更新：
  ✅ 更新「訂單服務架構文件」的連線池設定段落
  ✅ 新增「連線池調校紀錄」到變更日誌
  ✅ 更新 API 文件中的 POST /api/v1/orders 說明
```

### 1.3 A2P（Agent-to-Person）安全審批

```
A2P 安全模型：

┌──────────┐     請求批准      ┌──────────┐
│   AI      │ ───────────────→ │   人類    │
│  Agent    │                  │  審批者   │
│           │ ←─────────────── │           │
└──────────┘     批准/拒絕     └──────────┘

需要 A2P 審批的操作：
  🔴 必須審批：
    - 合併 PR 到 main branch
    - 部署到 staging / production
    - 修改資料庫 schema
    - 變更安全相關設定
  
  🟡 建議審批：
    - 新增依賴套件
    - 變更 API 介面
    - 修改共用模組
  
  🟢 不需審批：
    - 更新文件
    - 新增測試
    - Code formatting
```

### 1.4 知識庫閉環：讓 AI 越來越聰明

```
知識庫閉環循環：

開發新功能 → 產出程式碼和文件 → 更新 Wiki
     ↑                              │
     │                              ▼
  下次開發 ←── AI 讀取 Wiki 知識 ←── 累積知識
```

每次開發都會產生新的知識（架構決策、API 設計、踩過的坑），這些知識存入 Wiki 後，AI 下次開發時就能參考，形成正向循環。

---

## 二、Demo 實演 — The Finale（20 mins）

### 完整的全自駕流程展示

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

## 三、Quick Win：課堂 10 分鐘動手（10 mins）

### 任務：觸發 AI PR Reviewer，觀察它抓出架構違規

```bash
# Step 1：建立一個「故意違規」的 Spring Boot 專案（2 min）
mkdir pr-review-demo && cd pr-review-demo
git init

# Step 2：建立違規程式碼
cat > src/main/java/BadController.java << 'JAVA'
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
JAVA

git add .
git commit -m "bad: violation of clean architecture"

# Step 3：讓 AI Review（5 min）
claude
> 請 Code Review 這個改動，以 Clean Architecture 和以下規範檢查：
> - Controller 不可以直接存取 Repository/EntityManager
> - 所有回傳必須使用 DTO
> - 禁止使用 System.out.println
> - 所有資料庫操作必須在 Service 層
> - 必須有錯誤處理

# Step 4：觀察結果（3 min）
# AI 應該抓出所有 5 個違規項目
# 並提供具體的修正建議
```

### 檢查點

```bash
# 確認 AI 抓出以下違規：
# ✅ Controller 直接注入 EntityManager
# ✅ Controller 直接執行 SQL
# ✅ 沒有 DTO 轉換
# ✅ 使用 System.out.println
# ✅ 沒有錯誤處理
```

---

## 四、回家作業（結業挑戰）

### 作業：挑選一張真實的低風險 Backlog 工單，用完整 Agentic Workflow 跑完

**目標**：證明你可以用 AI Agent 完成從工單到 PR 的全流程。

#### 步驟

1. **挑選工單**：
   - 選一張低風險的 Backlog 工單（bug fix 或小功能）
   - 確保不涉及核心業務邏輯或安全相關變更
   - 獲得主管同意後開始

2. **執行全流程**：

```markdown
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

3. **品質檢查**：
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

## 五、七堂課總回顧

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

*上一堂：[AI 架構重構實戰](06_AI架構重構實戰.md) | [回到課程總覽](README.md)*