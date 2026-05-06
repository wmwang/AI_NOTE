# 第三堂：MCP 與 Skill 原理 — 擴充 AI 的手和腦

> **核心命題**：第二堂我們理解了 Agent 的底層循環。這堂課聚焦兩個關鍵擴充機制：**MCP 給 AI 裝「手」**（連接外部系統），**Skill 給 AI 裝「腦」**（注入領域知識）。理解原理，才能在 SDLC 中正確使用。

---

## 📋 本堂摘要

| 項目 | 內容 |
|------|------|
| 🎯 主題 | MCP 協議原理、Skill 載入機制、在 SDLC 中的實際應用 |
| 🎬 Demo | MCP Server 連接 ADO 查工單 → Skill 引導 AI 做 Code Review |
| ⚡ Quick Win | 啟動輕量 MCP Server，用一句話讓 AI 查到系統資訊 |
| 📝 作業 | 設定一個 SDLC 場景的 MCP + Skill，讓 AI 完成一個日常工作流程 |

---

## 一、概念講授（40 mins）

### 1.1 MCP 與 Skill 的定位：手與腦

```
第二堂學到的 Agent Loop：
  while True → LLM 思考 → 呼叫工具 → 觀察結果 → 再思考

這堂課要學的兩個擴充：

┌──────────────────────────────────────────────────────┐
│                    AI Agent                          │
│                                                      │
│   🧠 Skill（腦）          🖐️ MCP（手）               │
│   ┌─────────────┐         ┌─────────────┐           │
│   │ 領域知識     │         │ 外部系統連接 │           │
│   │ 工作流程規範 │         │ API 呼叫     │           │
│   │ 最佳實踐     │         │ 資料查詢     │           │
│   │ Code Review  │         │ ADO / Git    │           │
│   │ 清單         │         │ DB / K8s     │           │
│   └──────┬──────┘         └──────┬──────┘           │
│          │                       │                   │
│          └───────┬───────────────┘                   │
│                  ↓                                   │
│          Agent Loop（s01 的 while True）              │
└──────────────────────────────────────────────────────┘

Skill：AI「知道怎麼做」（知識）
MCP： AI「能夠去做」（能力）
兩者結合：AI「知道要做什麼，而且能實際執行」
```

---

### 1.2 MCP（Model Context Protocol）原理

#### MCP 是什麼？

MCP 是一個開放協議，讓 AI Agent 能連接外部系統。核心概念：

```
┌─────────────┐     MCP Protocol      ┌──────────────────┐
│             │ ←───────────────────→ │                  │
│  AI Agent   │    JSON-RPC 2.0       │   MCP Server     │
│ (Claude)    │    over stdio/SSE     │                  │
│             │                       │   ┌────────────┐ │
│             │    Tools 定義          │   │ 實際系統   │ │
│             │    Resources 定義      │   │ ADO / Git  │ │
│             │    Prompts 定義        │   │ DB / K8s   │ │
│             │                       │   └────────────┘ │
└─────────────┘                       └──────────────────┘
```

#### MCP 的三種能力

| 類型 | 說明 | SDLC 場景舉例 |
|------|------|--------------|
| **Tools** | AI 可呼叫的函式 | 查 ADO 工單、建 PR、跑測試 |
| **Resources** | AI 可讀取的資料來源 | 專案設定檔、API 文件 |
| **Prompts** | 標準化的指令模板 | Code Review 模板、發布清單 |

#### MCP 在 Claude Code 中的運作原理

```
Claude Code 啟動
    │
    ├── 讀取 .claude/settings.json
    │   └── mcpServers: { "ado": { command: "node", args: ["ado-mcp/index.mjs"] } }
    │
    ├── 啟動每個 MCP Server（stdio 通道）
    │   └── MCP Server 註冊其 Tools / Resources / Prompts
    │
    ├── 將 MCP Tools 加入 TOOL_HANDLERS dispatch map
    │   └── 與內建工具（Bash, Read, Write）同等地位
    │
    └── Agent Loop 運行時
        └── LLM 可以選擇呼叫任何已註冊的 MCP Tool
```

**關鍵洞察**：MCP Tool 在 Agent Loop 中的地位跟內建工具完全一樣！還記得 s02 的 dispatch map 嗎？MCP Tool 只是多加了幾個 handler 而已。

#### MCP 配置方式

```json
// .claude/settings.json
{
  "mcpServers": {
    "ado-devops": {
      "command": "node",
      "args": ["./mcp-servers/ado-devops/index.mjs"],
      "env": {
        "ADO_ORG": "https://dev.azure.com/mycompany",
        "ADO_PAT": "${ADO_PAT}"  // 從環境變數讀取
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

---

### 1.3 MCP Server 實戰範例：ADO 工單查詢

一個連接 Azure DevOps 的 MCP Server：

```typescript
// ado-mcp/index.mjs
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "ado-devops", version: "1.0.0" });

const ADO_ORG = process.env.ADO_ORG;
const ADO_PAT = process.env.ADO_PAT;

// Tool 1：查詢工單
server.tool(
  "get_work_item",
  "查詢 Azure DevOps 工單的詳細資訊",
  {
    id: z.number().describe("工單 ID"),
  },
  async ({ id }) => {
    const response = await fetch(
      `${ADO_ORG}/_apis/wit/workitems/${id}?api-version=7.0`,
      {
        headers: {
          Authorization: `Basic ${Buffer.from(`:${ADO_PAT}`).toString("base64")}`,
        },
      }
    );
    const item = await response.json();
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          id: item.id,
          title: item.fields["System.Title"],
          state: item.fields["System.State"],
          assignedTo: item.fields["System.AssignedTo"]?.displayName,
          description: item.fields["System.Description"],
          type: item.fields["System.WorkItemType"],
        }, null, 2),
      }],
    };
  }
);

// Tool 2：查詢 Sprint 工單列表
server.tool(
  "list_sprint_items",
  "列出當前 Sprint 中指定狀態的工單",
  {
    project: z.string().describe("ADO 專案名稱"),
    state: z.enum(["To Do", "In Progress", "Done", "All"]).default("All")
           .describe("工單狀態篩選"),
  },
  async ({ project, state }) => {
    const wiql = state === "All"
      ? "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.IterationPath] = @CurrentIteration"
      : `SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.IterationPath] = @CurrentIteration AND [System.State] = '${state}'`;

    const response = await fetch(
      `${ADO_ORG}/${project}/_apis/wit/wiql?api-version=7.0`,
      {
        method: "POST",
        headers: {
          Authorization: `Basic ${Buffer.from(`:${ADO_PAT}`).toString("base64")}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: wiql }),
      }
    );
    const result = await response.json();
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          project,
          sprint: "current",
          totalItems: result.workItems?.length ?? 0,
          items: result.workItems?.map(wi => ({ id: wi.id, url: wi.url })) ?? [],
        }, null, 2),
      }],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

---

### 1.4 Skill 原理：AI 的領域知識注入

#### Skill 是什麼？

還記得第二堂的 s05（Skill Loading）嗎？Skill 就是**按需載入的領域知識**。

```
Layer 1 — System Prompt（便宜）：
│ Skills available:
│   - code-review: Code Review 最佳實踐
│   - spring-boot: Spring Boot 開發規範
│   - git-flow: Git 工作流程

Layer 2 — 按需載入（AI 需要時才載入完整內容）：
│ <skill name="code-review">
│   1. 檢查是否有硬編碼的憑證
│   2. 檢查是否有未處理的例外
│   3. 檢查 Clean Architecture 分層
│   ...
│ </skill>
```

#### Skill 的目錄結構

```
.claude/skills/
├── code-review/
│   └── SKILL.md          ← AI 讀這個檔案獲得知識
├── spring-boot/
│   └── SKILL.md
├── git-flow/
│   └── SKILL.md
└── testing/
    └── SKILL.md
```

#### SKILL.md 的完整範例

```markdown
---
name: code-review
description: 團隊 Code Review 最佳實踐與檢查清單
---

# Code Review Skill

## 觸發條件
當使用者要求 Review 程式碼、檢查 PR、或提到 Code Review 時啟用。

## Review 檢查清單

### 安全性（最高優先級）
1. **憑證洩漏**：檢查是否有硬編碼的密碼、API Key、Token
2. **SQL Injection**：檢查是否有字串拼接的 SQL
3. **XSS**：檢查是否有未轉義的使用者輸入

### 架構（高優先級）
4. **分層違規**：Controller 不應直接存取 DB，Service 不應回傳 HTTP Response
5. **依賴方向**：外層可以依賴內層，內層不能依賴外層
6. **單一職責**：一個類別只有一個修改的原因

### 品質（中優先級）
7. **命名**：方法名稱應該描述「做什麼」而非「怎麼做」
8. **例外處理**：不應吞掉例外而不處理
9. **重複程式碼**：DRY 原則

### 測試（建議）
10. **測試覆蓋**：新功能是否有對應的測試
11. **邊界條件**：null、空字串、極端值是否有處理

## Review 輸出格式

對每個發現的問題，使用以下格式：

**嚴重程度**：🔴 Critical / 🟡 Warning / 🔵 Info
**檔案**：`path/to/file.java`
**行號**：L42-L45
**問題**：描述
**建議**：如何修復
**範例程式碼**：
```java
// 修正後的程式碼
```

## 團隊特定規則
- Spring Boot 專案使用 Constructor Injection，禁止 @Autowired
- 所有 API 必須有 Swagger 文件
- 資料庫操作必須透過 Repository 層
```

#### Skill 在 Agent Loop 中的運作

```
使用者：「幫我 Review 這個 PR」

Agent Loop:
  Iteration 1:
    LLM 思考 → 我需要 code-review 的知識
    tool_call: load_skill("code-review")
    tool_result: <skill name="code-review">...完整內容...</skill>

  Iteration 2:
    LLM 思考 → 我有 Review 清單了，先看 PR 改了什麼
    tool_call: bash("git diff main...feature-branch")

  Iteration 3:
    LLM 思考 → 根據清單逐項檢查，發現安全性問題
    → 產出結構化的 Review 報告
    stop_reason: "end_turn"
```

---

### 1.5 Skill 與 MCP 的協同：SDLC 全場景

| SDLC 階段 | Skill（知道怎麼做） | MCP（能夠去做） |
|-----------|-------------------|----------------|
| **需求** | 需求分析 Skill | ADO 查工單 MCP |
| **設計** | 架構規範 Skill | Wiki 讀取 MCP |
| **開發** | Spring Boot Skill | Git 操作 MCP |
| **測試** | TDD Skill | 測試執行 MCP |
| **Review** | Code Review Skill | PR 建立 MCP |
| **部署** | 部署清單 Skill | K8s 操作 MCP |

**核心公式**：`Skill（知識）+ MCP（能力）+ Agent Loop（執行）= 自動化 SDLC`

---

### 1.6 Skill 的進階用法

#### 多 Skill 組合

AI 可以在一次任務中載入多個 Skill：

```
使用者：「從 ADO 工單 #12345 開始，完成開發並發 PR」

AI 的執行流程：
1. load_skill("git-flow")        → 學會團隊的 Git 工作流
2. MCP: get_work_item(12345)     → 讀取工單內容
3. load_skill("spring-boot")     → 學會開發規範
4. 開發程式碼...
5. load_skill("testing")         → 學會測試規範
6. 撰寫測試...
7. load_skill("code-review")     → 學會 Review 清單
8. 自我 Review...
9. MCP: create_pull_request()    → 發 PR
```

#### Skill 的繼承與覆蓋

```
skills/
├── base-java/           ← 基礎 Java 規範
│   └── SKILL.md
├── spring-boot/         ← 繼承 base-java，加上 Spring 特定規範
│   └── SKILL.md
└── spring-boot-ai/      ← 繼承 spring-boot，加上 AI 模組特定規範
    └── SKILL.md
```

SKILL.md 中可以聲明依賴：

```markdown
---
name: spring-boot
description: Spring Boot 開發規範
depends_on: [base-java]
---

# Spring Boot Skill

繼承 base-java 的所有規範，並加上以下 Spring Boot 特定規則...
```

#### Skill 作為 System Prompt 的一部分

你也可以把關鍵 Skill 直接寫進 CLAUDE.md，讓它永遠存在：

```markdown
# CLAUDE.md

## 核心紀律（永遠遵守）
- 禁止直接操作 production 環境
- 所有 API 必須有錯誤處理
- 測試必須先於實作（TDD）

## 可用 Skills
- code-review: PR Review 時載入
- spring-boot: 開發時載入
- testing: 寫測試時載入
```

---

## 二、Demo 實演（10 mins）

### Demo 1：MCP 連接 ADO — 用自然語言查工單

```bash
# 啟動帶有 ADO MCP 的 Claude Code
claude

> 查一下工單 #12345

# AI 的執行：
# 1. MCP tool_call: get_work_item({ id: 12345 })
# 2. 回傳：工單 #12345「修復訂單 API 500 錯誤」，狀態 Active，指派給小明

> 這個 Sprint 有哪些 In Progress 的工單？

# AI 的執行：
# 1. MCP tool_call: list_sprint_items({ project: "myproject", state: "In Progress" })
# 2. 回傳工單列表
```

### Demo 2：Skill 引導 Code Review

```bash
# 不使用 Skill
> Review 這段程式碼：[貼上程式碼]
# AI 給出泛泛的建議

# 使用 Skill
> 載入 code-review skill，然後 Review 這個 PR
# AI 根據團隊的 Review 清單逐項檢查
# 輸出結構化的 Review 報告，包含嚴重程度分級
```

### Demo 3：MCP + Skill 協同

```bash
> 從工單 #12345 到發 PR，完整走一遍

# AI 的完整流程：
# 1. MCP 讀工單 → 2. Skill 載入開發規範 → 3. 開發
# 4. Skill 載入測試規範 → 5. 寫測試 → 6. MCP 發 PR
```

---

## 三、Quick Win：課堂 10 分鐘動手（10 mins）

### 任務：啟動 MCP Server + 建立 Code Review Skill

```bash
# Part A：建立輕量 MCP Server（5 min）
mkdir my-first-mcp && cd my-first-mcp
npm init -y && npm install @modelcontextprotocol/sdk zod

cat > index.mjs << 'EOF'
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { execSync } from "child_process";

const server = new McpServer({ name: "dev-toolkit", version: "1.0.0" });

server.tool(
  "get_git_status",
  "查詢當前 Git Repository 的狀態（分支、未提交變更）",
  {},
  async () => {
    const branch = execSync("git branch --show-current").toString().trim();
    const status = execSync("git status --short").toString().trim();
    const log = execSync("git log --oneline -5").toString().trim();
    return {
      content: [{ type: "text", text: JSON.stringify({
        currentBranch: branch,
        uncommittedChanges: status.split("\n").filter(Boolean),
        recentCommits: log.split("\n"),
      }, null, 2) }],
    };
  }
);

server.tool(
  "run_tests",
  "執行專案測試並回報結果",
  {
    path: z.string().optional().describe("測試路徑，預設為當前目錄"),
    command: z.string().optional().default("npm test").describe("測試指令"),
  },
  async ({ path: dir, command }) => {
    try {
      const result = execSync(command, { cwd: dir, timeout: 30000 }).toString();
      return { content: [{ type: "text", text: `✅ Tests passed\n${result}` }] };
    } catch (e) {
      return { content: [{ type: "text", text: `❌ Tests failed\n${e.stdout?.toString() || e.message}` }] };
    }
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
EOF
```

```bash
# Part B：建立 Code Review Skill（5 min）
mkdir -p ~/.claude/skills/code-review

cat > ~/.claude/skills/code-review/SKILL.md << 'EOF'
---
name: code-review
description: 團隊 Code Review 檢查清單
---

# Code Review Skill

## 觸發條件
當使用者要求 Review 程式碼、檢查 PR 時啟用。

## 檢查清單
1. 🔴 硬編碼的憑證或敏感資訊
2. 🟡 未處理的例外或空指標
3. 🟡 Clean Architecture 分層違規
4. 🔵 命名不清或魔術數字
5. 🔵 缺少必要的測試

## 輸出格式
每個問題標示：嚴重程度、檔案、行號、建議修復方式
EOF
```

```bash
# 配置 MCP Server
# 加入到 .claude/settings.json：
```

```json
{
  "mcpServers": {
    "dev-toolkit": {
      "command": "node",
      "args": ["./index.mjs"],
      "cwd": "/absolute/path/to/my-first-mcp"
    }
  }
}
```

```bash
# 測試
claude
> 現在的 Git 狀態？
# ✅ AI 呼叫 get_git_status 工具

> 幫我 Review 最近一次 commit 的程式碼
# ✅ AI 載入 code-review Skill，根據清單逐項檢查
```

---

## 四、回家作業

### 作業：設定 SDLC 場景的 MCP + Skill 組合

**目標**：選擇一個你日常工作中的重複流程，用 MCP + Skill 讓 AI 自動化完成。

#### 步驟

1. **選擇場景**（擇一）：
   - 從 ADO 工單 → 建分支 → 開發 → 發 PR
   - Code Review 流程：收到 PR → 逐項檢查 → 產出 Review 意見
   - 測試流程：跑測試 → 分析失敗原因 → 修正建議
   - 文件更新：程式碼變更 → 同步更新 API 文件

2. **建立對應的 SKILL.md**：
   ```markdown
   ---
   name: your-skill-name
   description: 一句話描述
   ---

   # Your Skill Name

   ## 觸發條件
   ...

   ## 工作流程
   1. Step 1: ...
   2. Step 2: ...

   ## 輸出格式
   ...
   ```

3. **配置 MCP Server**（如果場景需要外部系統）：
   - 在 `.claude/settings.json` 中設定
   - 或使用現成的 MCP Server（如 @modelcontextprotocol/server-github）

4. **測試並記錄**：
   ```markdown
   ## 測試報告

   ### 場景描述
   ...

   ### AI 執行過程
   | Step | AI 做了什麼 | 使用的工具/Skill |
   |------|-----------|-----------------|
   | 1 | | |
   | 2 | | |

   ### 效果對比
   - 手動執行時間：___ 分鐘
   - AI 輔助時間：___ 分鐘
   ```

#### 評分標準

| 項目 | 比重 |
|------|:---:|
| 場景選擇的真實性與價值 | 25% |
| SKILL.md 的完整度與清晰度 | 25% |
| MCP 配置的正確性 | 25% |
| 測試報告與效果對比 | 25% |

---

## 五、關鍵 Takeaway

> 💡 **MCP + Skill 的核心公式**：
> ```
> Skill（知道怎麼做）+ MCP（能夠去做）+ Agent Loop（持續執行）= 自動化 SDLC
> ```
>
> - **MCP** = 給 AI 裝「手」：讓它能查工單、建 PR、跑測試
> - **Skill** = 給 AI 裝「腦」：讓它知道團隊的規範、清單、最佳實踐
> - **兩者結合** = AI 不只能做，還能做對

### 延伸閱讀

- [MCP 官方文件](https://modelcontextprotocol.io/)
- [Claude Code Skills 說明](https://docs.anthropic.com/en/docs/claude-code/skills)
- [MCP Server 範例合集](https://github.com/modelcontextprotocol/servers)
- [第二堂 s05 Skill Loading 原理](02_解構大廠Agent底層.md)

---

*上一堂：[解構大廠 Agent 底層](02_解構大廠Agent底層.md) | 下一堂：[擴充 GitAgent 生態](04_擴充GitAgent生態.md)*