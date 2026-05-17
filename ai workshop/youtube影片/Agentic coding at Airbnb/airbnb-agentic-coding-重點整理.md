# Airbnb Agentic Coding 實戰重點整理

> Airbnb 兩位工程師 Szczepan 和 Mike 分享了他們在 2025 年推動 Agentic Coding 的完整歷程——從願景設定、工具策略、技術架構到組織變革。以下是把 40 分鐘演講提煉出的核心重點。

---

## 一、願景與類比：從 Driver 變成 Navigator

Airbnb 用 **Pair Programming** 來類比 Agentic Coding：

| 角色 | 傳統 Pair Programming | Agentic Coding |
|------|----------------------|----------------|
| **Driver**（戰術） | 人類工程師拿鍵盤寫程式 | AI Agent 負責產出程式碼 |
| **Navigator**（策略） | 人在旁邊看全局、指引方向 | **人類工程師變成永久 Navigator** |

重點不是 AI 取代人，而是人類從「一行一行寫程式碼」升級為「同時駕馭多個 Agent Session」。

## 二、關鍵數據

| 指標 | 數據 |
|------|------|
| Agentic Coding 佔 PR 比例 | **64%**（原預測年底才 20-40%） |
| 開發者情緒調查 | 連續 4 次「最佳工程生產力工具」 |
| 採用曲線 | 幾乎垂直成長，20 年來僅見 |
| 強制使用 | **無**，純自願採用 |
| 超級使用者 | 同時開 5 個平行 Agentic Session |

## 三、Agentic Coding 的定義

```
工程師寫 prompt → 啟動 Agentic Loop
                    ├── 多次呼叫 LLM（次數未知）
                    ├── 呼叫各種工具 / MCP（哪些未知）
                    ├── 載入配置（system prompt、agents.md、cursor rules）
                    └── 有自主性決定執行流程
                 → 產出程式碼變更
                 → 人類審查後才提交 PR
```

關鍵特徵：工程師不知道 Agent 會用幾次 LLM、會用哪些工具、會怎麼跑流程。它有自主性，這就是「Agentic」。

## 四、技能養成四階段

| 等級 | 描述 | 重點 |
|------|------|------|
| Level 1 | 初步接觸 | 大多數人已通過 |
| Level 2 | 逐一批准操作 | 學習階段，正常 |
| Level 3 | 開啟 auto-approve | **信任自己的 prompting 技能，而非信任 AI** |
| Level 4 | 整合建設工具 | 建構 MCP、推動轉型 |

注意：太快跳到 auto-approve 會產生大量未審查的 PR。給工程師時間學習。

## 五、Airbnb 的工具策略演進

### 三個策略的比較

| 策略 | 優勢 | 劣勢 |
|------|------|------|
| **IDE First** | 美觀 UX、上下文整合、RAG pipeline | 缺乏 Agentic 能力 |
| **CLI First** | 市場最佳答案、豐富工具、可遠端執行 | 無 Airbnb 內部知識 |
| **兩者兼得** | CLI 品質 + Airbnb 知識 + MCP 標準 | 需要投入建設 |

### 最終方案：Airchat + MCP

Airbnb 的解法是建一個叫 **Airchat** 的 wrapper 抽象層：

```
Airchat（統一入口）
├── 管理多個 CLI Agent 引擎（Aider、Claude Code、Codex、Gemini...）
├── 自動更新與部署
├── MCP Server（暴露內部工具給 Agent）
├── MCP Client（讓 IDE 也能用 MCP 工具）
└── 配置同步機制
```

核心邏輯：**不重新發明輪子，用 wrapper 整合市場上最好的 Agent，再透過 MCP 把公司內部知識注入。**

## 六、MCP 是關鍵基礎建設

MCP（Model Context Protocol）= **給 LLM 用的 REST API**

Airbnb 全面投入 MCP 的做法：

| 層面 | 具體作為 |
|------|---------|
| **MCP Server** | 把 IDE 工具功能包裝成 MCP server，CLI 也能用 |
| **MCP Client** | IDE 插件內建 MCP client，統一工具存取 |
| **Auth** | 自動注入使用者認證的框架 |
| **安全** | 建立標準化鋪路，免兩週安全審查 |
| **模板** | 專案模板讓團隊低成本實驗 |
| **SDK** | 標準化 client 開發框架 |

目前內部超過 **12 個 MCP server**，由各團隊自發貢獻。

## 七、知識注入：Tool Calling Is All You Need

Airbnb 的核心觀點：**不需要 fine-tune 或訓練自己的模型**。

| 舊方式 | 新方式 |
|--------|--------|
| RAG pipeline 一次性猜測搜尋 | MCP server 包裝知識庫 endpoint |
| 線性、單次 | Agentic、可反覆搜尋 |
| 人類決定搜尋詞 | LLM 自己決定怎麼搜、搜什麼 |

效果：幾乎免費得到 Agentic Search + Deep Research。例如問「怎麼在 Airbnb 設定 S3」，Agent 會搜尋公司內部文件並給出 Airbnb 特定的做法。

## 八、IDE 整合策略：打不過就加入

Airbnb 一開始想自己建 Orchestrator（planning agent → coding agent → validation agent），但：

> AI 發展太快，我們還在規劃，市場就領先五步了。團隊太小，沒有肌肉建這些 agent。

最終策略：**IDE 只做薄薄的 shim 層，委派給 Airchat CLI 處理**。保持單向資料流和單一職責。

## 九、六個核心教訓

| 教訓 | 說明 |
|------|------|
| **需要全村的力量** | 不是幾個專家在暗房裡就能搞定。賦能在地專家，建立 champion program |
| **不要輕視 CLI** | 80% 工程師偏好 CLI agent 工具。Mike 自己從 IDE 派變成 CLI 派 |
| **移除障礙** | 一鍵啟動、放在開發者所在的地方。不要強迫換 IDE |
| **必須標準化** | 不要每個新趨勢都跟，觀察產業穩定方向再下注 |
| **衡量所有事情** | 量化 + 質化並行。很多傳統生產力指標仍適用 |
| **不要降低標準** | 測試程式碼品質要等同 production code。審查 AI 產出時要勇於質疑 |

## 十、最重要的一句話

> **你的 Agentic 工具本身是不夠的。你需要在它周圍有很多配套技術——遠端 IDE、沙盒環境、好的 code review 工具和文化。也許未來的軟體工程就是全部都是 code review。**

## 下一步

1. **評估你的 MCP 就緒度**：你的內部工具是否能透過 MCP server 暴露給 Agent？
2. **建立沙盒環境**：支援平行 Agentic Session 的隔離 workspace 是必備基礎建設
3. **強化 code review 文化**：當程式碼產出量暴增，review 品質是守住品質的最後防線
