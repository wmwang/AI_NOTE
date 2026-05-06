# 第四堂：擴充 GitAgent 生態 — Skill 開發與內部開源

> **核心命題**：把你的維運工具包成 Skill，全團隊的 AI 都能立刻使用。這就是 AI 時代的「內部開源」。

---

## 📋 本堂摘要

| 項目 | 內容 |
|------|------|
| 🎯 主題 | 防呆 Schema 設計、AI 專屬 Error Handling、憑證安全抽離 |
| 🎬 Demo | 將糟糕的 Shell Script 重構為標準 Skill |
| ⚡ Quick Win | 將 `echo "hello"` 包裝成具備 JSON Schema 的 Skill |
| 📝 作業 | 將私藏維運工具重構為標準 Skill，發 PR 貢獻 |

---

## 一、概念講授（30 mins）

### 1.1 Skill 是什麼？為什麼要封裝？

Skill = 一組「給 AI 看的說明文件 + 可執行的腳本」，讓 AI 獲得特定領域的專業能力。

```
沒有 Skill：
  開發者：「幫我查 ADO 工單 #12345」
  AI：「我無法存取 Azure DevOps...」

有 ado-devops Skill：
  開發者：「幫我查 ADO 工單 #12345」
  AI：自動呼叫 az boards work-item show --id 12345
     → 「工單 #12345：修復訂單 API 500 錯誤，狀態 Active，指派給小明」
```

#### Skill 的標準目錄結構

```
my-awesome-skill/
├── SKILL.md              ← 🔑 核心：給 AI 讀的「說明書」
├── scripts/              ← 可執行的腳本
│   ├── main.sh           ← 主邏輯
│   └── helpers.sh        ← 輔助函式
├── schemas/              ← JSON Schema 定義（選填）
│   └── input.schema.json
├── README.md             ← 給人看的說明（選填）
└── tests/                ← 測試（建議有）
    └── test_main.sh
```

---

### 1.2 SKILL.md：AI 的操作手冊

SKILL.md 是 Skill 的靈魂，AI 會完整讀取這份文件來決定如何使用你的 Skill。

```markdown
# SKILL.md — pod-health-checker

## 觸發條件
當使用者詢問以下相關問題時，啟用此技能：
- Pod 狀態、Pod 健康檢查
- Kubernetes 故障排查
- 服務是否正常運行

## 可用操作

### check-pod-health
檢查指定 namespace 中所有 Pod 的健康狀態。

**參數：**
| 參數 | 必填 | 說明 | 範例 |
|------|:---:|------|------|
| namespace | 是 | K8s namespace | production |
| label | 否 | 標籤選擇器 | app=order |

**執行方式：**
```bash
bash scripts/check-pod-health.sh --namespace <NAMESPACE> [--label <LABEL>]
```

**輸出格式：** JSON
**回傳碼：**
- 0：所有 Pod 健康
- 1：有 Pod 異常
- 2：參數錯誤

### diagnose-crash
診斷處於 CrashLoopBackOff 的 Pod。

**參數：**
| 參數 | 必填 | 說明 |
|------|:---:|------|
| pod-name | 是 | Pod 名稱 |
| namespace | 是 | Namespace |

**執行方式：**
```bash
bash scripts/diagnose-crash.sh --pod <POD_NAME> --namespace <NAMESPACE>
```

## 注意事項
- 所有操作都是唯讀的，不會修改任何資源
- 需要kubectl存取權限
- 輸出都是 JSON 格式
```

---

### 1.3 防呆 Schema 設計

**防呆的核心理念**：讓 AI「不可能傳錯參數」。

#### ❌ 不防呆的設計

```typescript
server.tool(
  "restart_service",
  "重啟服務",
  {
    service: z.string(),      // AI 可能傳 "order service"（有空白）
    env: z.string(),          // AI 可能傳 "prod"（你們用的是 "production"）
    action: z.string(),       // AI 可能傳 "restart" 或 "reboot" 或 "reload"
  },
  ...
);
```

#### ✅ 防呆的設計

```typescript
server.tool(
  "restart_service",
  "重啟指定的微服務。僅限 staging 和 production 環境。",
  {
    service: z.string()
      .regex(/^[a-z][a-z0-9-]*$/, "服務名稱只能包含小寫字母、數字和連字號")
      .describe("微服務名稱，例如 order-service, payment-service"),
    environment: z.enum(["staging", "production"])
      .describe("環境名稱。只允許 staging 或 production"),
    strategy: z.enum(["rolling", "blue-green"])
      .optional()
      .default("rolling")
      .describe("重啟策略：rolling（滾動更新）或 blue-green（藍綠部署）"),
    dryRun: z.boolean()
      .optional()
      .default(true)
      .describe("乾run模式：true 只顯示將要執行的操作，不實際執行"),
  },
  async ({ service, environment, strategy, dryRun }) => {
    // 安全閥：所有破壞性操作預設 dryRun
    if (dryRun) {
      return {
        content: [{
          type: "text",
          text: `[DRY RUN] 將在 ${environment} 環境以 ${strategy} 策略重啟 ${service}。\n` +
                `如果要實際執行，請明確指定 dryRun: false。`,
        }],
      };
    }
    // 實際執行...
  }
);
```

**防呆設計五原則**：

| 原則 | 技術手段 | 效果 |
|------|---------|------|
| **列舉代替自由輸入** | `z.enum(["a", "b"])` | AI 不可能拼錯 |
| **正則表達式驗證** | `.regex(...)` | 防止特殊字元注入 |
| **預設安全值** | `.default(true)` | 破壞性操作預設關閉 |
| **描述清楚** | `.describe("...")` | AI 知道該傳什麼 |
| **乾run 模式** | `dryRun` 參數 | 先看再做的安全閥 |

---

### 1.4 AI 專屬 Error Handling：給 AI 看的 stderr

錯誤訊息的設計直接影響 AI 的 Error Recovery 效率。

```bash
#!/bin/bash
# ❌ 糟糕的錯誤處理
if [ -z "$NAMESPACE" ]; then
  echo "Error" >&2
  exit 1
fi
```

```bash
#!/bin/bash
# ✅ AI-Friendly 的錯誤處理
if [ -z "$NAMESPACE" ]; then
  cat >&2 << EOF
{
  "error": "MISSING_PARAMETER",
  "parameter": "namespace",
  "message": "namespace 參數為必填",
  "suggestion": "請提供 Kubernetes namespace，例如：--namespace production",
  "available_namespaces": ["default", "staging", "production"],
  "example": "bash check-pod.sh --namespace production"
}
EOF
  exit 2  # 用不同的 exit code 區分錯誤類型
fi
```

**Error Message 設計模板**：

```json
{
  "error": "ERROR_CODE_UPPERCASE",
  "parameter": "哪個參數出問題",
  "message": "人類可讀的錯誤描述",
  "suggestion": "AI 應該怎麼修",
  "expected": "正確的格式或值範圍",
  "example": "正確的使用範例"
}
```

---

### 1.5 憑證安全抽離

**絕對不要**把密碼、Token、API Key 寫在 Skill 腳本裡。

```bash
# ❌ 絕對禁止
API_KEY="sk-abc123def456"
az devops login --token "$API_KEY"
```

```bash
# ✅ 正確做法：從環境變數讀取
# 在 ~/.bashrc 或 ~/.zshrc 中設定：
# export ADO_PAT="your-token-here"

: "${ADO_PAT:?Error: ADO_PAT environment variable is not set. Please set it in your shell profile.}"

# 使用時
az devops login --token "$ADO_PAT"
```

```bash
# ✅ 更好的做法：從加密的憑證管理器讀取
ADO_PAT=$(security find-generic-password -s "ado-pat" -w 2>/dev/null)
if [ -z "$ADO_PAT" ]; then
  echo '{"error":"CREDENTIAL_NOT_FOUND","message":"ADO PAT not found in keychain","suggestion":"Run: security add-generic-password -s ado-pat -w YOUR_TOKEN"}' >&2
  exit 1
fi
```

**憑證管理分級**：

| 等級 | 方式 | 適用場景 |
|------|------|---------|
| 🔴 絕對禁止 | 寫死在腳本裡 | 永遠不要這樣做 |
| 🟡 基本安全 | 環境變數 | 個人開發環境 |
| 🟢 推薦做法 | OS Keychain / Vault | 團隊共用環境 |
| 🔵 企業級 | HashiCorp Vault + IAM | 生產環境 |

---

## 二、Demo 實演（20 mins）

### Demo 1：重構一個「寫得很糟」的 Shell Script

```bash
# 這是一個真實常見的「糟糕腳本」
cat > terrible-deploy.sh << 'TERRIBLE'
#!/bin/bash
# deploy stuff
echo "deploying..."
kubectl apply -f ./k8s/
kubectl rollout status deployment/order-service -n prod
echo "done"
TERRIBLE

# 問題清單：
# 1. 沒有錯誤處理
# 2. namespace 寫死
# 3. 沒有確認步驟
# 4. 輸出不是 JSON
# 5. 沒有 dry-run 選項
# 6. 沒有憑證安全處理
```

### Demo 2：一步步重構為標準 Skill

```bash
# 讓 AI 幫我們重構
claude
> 這個 terrible-deploy.sh 有很多問題，請根據以下要求重構為標準 Skill：
> 1. 加上完整的錯誤處理（AI-Friendly 的 JSON 錯誤）
> 2. namespace 和 service 名稱改為參數
> 3. 加上 dry-run 模式（預設開啟）
> 4. 輸出改為 JSON 格式
> 5. 加上 SKILL.md
> 6. 憑證從環境變數讀取

# AI 產出：
# ✅ scripts/deploy.sh — 重構後的腳本
# ✅ SKILL.md — 完整的操作說明
# ✅ schemas/input.schema.json — 參數定義
```

### Demo 3：成功調用重構後的 Skill

```bash
# 安裝 Skill 到 ~/.claude/skills/
cp -r deploy-skill ~/.claude/skills/deploy-skill

# 測試
claude
> 幫我部署 order-service 到 staging 環境

# AI 的回應：
# 「我會使用 deploy-skill 來執行部署。
#  [DRY RUN] 將在 staging 環境部署 order-service。
#  如果要實際執行，請確認。」

> 確認執行

# AI 實際執行部署，並回報結果
```

---

## 三、Quick Win：課堂 10 分鐘動手（10 mins）

### 任務：將 `echo "hello"` 包裝成標準 Skill

```bash
# Step 1：建立 Skill 目錄（1 min）
mkdir -p hello-skill/scripts
cd hello-skill

# Step 2：建立 SKILL.md（3 min）
cat > SKILL.md << 'EOF'
# hello-skill

## 觸發條件
當使用者說「hello」、「打招呼」、「測試 Skill」時啟用。

## 可用操作

### say-hello
向指定對象打招呼。

**參數：**
| 參數 | 必填 | 說明 | 預設 |
|------|:---:|------|------|
| name | 否 | 對象名稱 | World |
| language | 否 | 語言（zh/en/ja） | zh |

**執行方式：**
```bash
bash scripts/hello.sh --name <NAME> --language <LANGUAGE>
```

**輸出格式：** JSON
EOF

# Step 3：建立腳本（4 min）
cat > scripts/hello.sh << 'SCRIPT'
#!/bin/bash
# hello-skill：向指定對象打招呼

# 參數解析
NAME="World"
LANGUAGE="zh"

while [[ "$#" -gt 0 ]]; do
  case $1 in
    --name) NAME="$2"; shift 2 ;;
    --language) LANGUAGE="$2"; shift 2 ;;
    *) echo "{\"error\":\"UNKNOWN_PARAM\",\"parameter\":\"$1\",\"message\":\"未知的參數\",\"suggestion\":\"可用參數：--name, --language\"}" >&2; exit 2 ;;
  esac
done

# 根據語言選擇問候語
case $LANGUAGE in
  zh) GREETING="你好" ;;
  en) GREETING="Hello" ;;
  ja) GREETING="こんにちは" ;;
  *)
    echo "{\"error\":\"INVALID_LANGUAGE\",\"parameter\":\"language\",\"value\":\"$LANGUAGE\",\"message\":\"不支援的語言\",\"suggestion\":\"可用語言：zh, en, ja\"}" >&2
    exit 2
    ;;
esac

# JSON 輸出
echo "{\"greeting\":\"${GREETING}, ${NAME}!\",\"language\":\"${LANGUAGE}\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
SCRIPT

chmod +x scripts/hello.sh

# Step 4：測試（2 min）
bash scripts/hello.sh --name "AI Workshop" --language zh
# 預期輸出：{"greeting":"你好, AI Workshop!","language":"zh","timestamp":"..."}

bash scripts/hello.sh --language xx
# 預期輸出：{"error":"INVALID_LANGUAGE",...}
```

### 安裝並讓 AI 呼叫

```bash
# 安裝到 Claude Code skills 目錄
cp -r hello-skill ~/.claude/skills/hello-skill

# 測試
claude
> 跟我打招呼

# AI 會讀取 SKILL.md，找到 say-hello 操作，執行腳本
```

### 檢查點

```bash
# 確認 Skill 結構完整
find hello-skill -type f
# 預期：
# hello-skill/SKILL.md
# hello-skill/scripts/hello.sh

# 確認腳本可執行
bash scripts/hello.sh --name "Test" --language en
# 預期：{"greeting":"Hello, Test!","language":"en",...}
```

---

## 四、回家作業（貢獻大會）

### 作業：將私藏維運工具重構為標準 Skill，發 PR 貢獻

**目標**：把你日常使用的某個好工具，按照標準格式封裝為 Skill，發 PR 到團隊的 gitagent-protocol Repo。

#### 步驟

1. **挑選工具**：選一個你私藏的維運工具
   - 例如：快速查 Log 的腳本、批次重啟服務的腳本、檢查憑證有效期的腳本
   - 例如：DB 備份狀態檢查、Redis 記憶體分析、Nginx 設定驗證

2. **重構為標準格式**：
   ```
   your-skill/
   ├── SKILL.md              ← 必填
   ├── scripts/
   │   └── main.sh           ← 必填
   ├── schemas/              ← 建議
   └── README.md             ← 建議
   ```

3. **品質檢查清單**：
   - [ ] SKILL.md 觸發條件清楚
   - [ ] 所有參數有 zod 或手動驗證
   - [ ] 錯誤訊息是 AI-Friendly JSON
   - [ ] 憑證從環境變數讀取（不在腳本中寫死）
   - [ ] 破壞性操作有 dry-run 模式
   - [ ] 輸出為 JSON 格式
   - [ ] 腳本有執行權限

4. **發 PR**：
   ```bash
   git checkout -b skill/your-skill-name
   cp -r your-skill Skills/your-skill-name/
   git add .
   git commit -m "feat(skill): add your-skill-name"
   git push origin skill/your-skill-name
   # 然後在 ADO/GitHub 發 PR
   ```

#### PR Description 模板

```markdown
## 新增 Skill：your-skill-name

### 功能說明
這個 Skill 可以做什麼...

### 使用場景
- 場景 1：...
- 場景 2：...

### 測試方式
```bash
bash scripts/main.sh --param value
```

### 截圖
（AI 成功呼叫此 Skill 的截圖）

### 檢查清單
- [x] SKILL.md 完整
- [x] 參數驗證
- [x] AI-Friendly 錯誤處理
- [x] 憑證安全
- [x] JSON 輸出
```

#### 評分標準

| 項目 | 比重 |
|------|:---:|
| 工具的實用性與原創性 | 25% |
| SKILL.md 的清晰度 | 20% |
| 防呆 Schema 設計 | 20% |
| Error Handling 品質 | 15% |
| PR 完整度（含測試截圖） | 20% |

---

## 五、關鍵 Takeaway

> 💡 **Skill 開發的三大紀律**：
> 1. **AI-Friendly 優先** — 你不是在寫給人用的 CLI，你是在寫給 AI 看的 API
> 2. **安全預設** — 破壞性操作永遠預設 dry-run，憑證永遠外部化
> 3. **可組合** — 一個 Skill 做一件事，AI 會把多個 Skill 組合起來完成複雜任務

---

*上一堂：[專屬 SRE 兵器庫](03_專屬SRE兵器庫.md) | 下一堂：[AI 系統分析實戰](05_AI系統分析實戰.md)*