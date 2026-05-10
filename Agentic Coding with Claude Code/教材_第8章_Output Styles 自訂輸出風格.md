# Claude Code Output Styles：讓 AI 用你想要的方式說話

你有沒有遇過這種狀況：叫 Claude Code 解釋某個問題，它洋洋灑灑寫了五段落，但你只想要一個簡單的條列清單？或者你在寫技術文件，希望它的回答都是結構化的 YAML 格式？Output Styles 就是為了解決這個問題而設計的。

---

## Output Style 是什麼？

Output Style 是一個設定檔，用來修改 Claude Code 的「回應方式」——包括格式、語調、資訊密度，甚至可以嵌入自動化行為（例如：每次回答完自動把結果存成 HTML 檔）。

**它的本質是：把你的設定注入到 Claude Code 的 system prompt 裡。**

一旦選定某個 Output Style，後續所有的對話都會套用那個風格，直到你切換或關閉。

### 內建的三種風格

```bash
/output-style   # 查看目前可用的風格
```

| 風格名稱 | 行為說明 |
|---------|---------|
| **Default** | 預設模式，直接完成任務，給精簡回應 |
| **Explanatory** | 解釋實作選擇和程式碼模式，適合想學習的情境 |
| **Learning** | 讓你自己寫小段程式碼，Claude 從旁引導，練習用 |

除了內建風格，你可以建立完全自訂的風格。

---

## 建立自訂 Output Style

Output Style 的設定檔是一個 Markdown 檔案，存放位置決定它的適用範圍：

| 存放路徑 | 適用範圍 |
|---------|---------|
| `~/.claude/output-styles/` | 全域（所有專案都能用） |
| `.claude/output-styles/` | 僅限當前專案 |

### 最簡單的範例：條列風格

建立 `~/.claude/output-styles/minimal-bullets.md`：

```markdown
---
description: 簡潔條列式回應，直接給答案，不廢話
---

# Communication Style
- 所有回應使用條列清單
- 直接給答案，不需要前言和過渡語
- 不用完整句子，用 key phrase 就好

# Response Format
- 先給答案，再給細節
- 用縮排條列表示層級關係
- 跳過「如您所見」、「值得注意的是」等填充語

# Tone
- 專業、精簡
- 不加保留語和限定詞
```

建立完成後，使用：

```bash
/output-style           # 選擇 minimal-bullets
```

之後的回答全都會變成條列格式，即使你問「解釋一下 output styles 是什麼」，它也會用條列回答。

---

## 進階：YAML 格式的輸出

YAML 特別適合用來描述有層級關係的任務分析。與條列格式相比，YAML 的巢狀結構能自然表達依賴關係和範疇。

建立 `.claude/output-styles/yaml-concise.md`（專案級）：

```markdown
---
description: 結構化 YAML 輸出，用層級表達關係而非序列步驟
---

# Response Format
- 所有回應以有效 YAML 格式輸出
- 用層級和巢狀表達關係
- 值保持簡潔，不用完整句子

# Structure
- 用頂層 key 代表主要區塊
- 子概念放在父層 context 下
- 序列用 list，屬性用 key-value pair

# Tone
- 不寫 prose，不寫過渡語
- 讓 YAML 結構本身傳達意思
- 值盡量用短字串
```

啟用後，同樣一個問題「幫我分析這個 bug 要怎麼修」，回應會長這樣：

```yaml
Task: "修復認證 bug"
Priority: "高"
Complexity: "中"

approach:
  investigate:
    auth_flow: &flow
      - login_endpoint
      - token_validation
      - session_middleware
  debugging:
    logs: "./auth.log"
    reproduce: "invalid_token_scenario"

fix:
  dependencies: [*flow]
  files_to_modify:
    auth.ts:
      scope: "token refresh logic"
      risk: "低"
    middleware.ts:
      scope: "validation checks"
      risk: "高"

verify:
  tests: ["auth_integration", "token_expiry"]
  manual_check: "login flow end-to-end"

metadata:
  estimated_time: "2 hours"
  rollback_plan: "revert commits"
```

這種格式特別適合用在 code review、架構分析、bug 追蹤等需要結構化輸出的場合。

---

## 在 Output Style 裡嵌入工作流程

Output Style 不只能控制格式，還能嵌入**行為指令**，讓 Claude Code 在每次回應後自動執行特定動作。

**實際案例：自動把回答存成 HTML 檔**

在 `.claude/output-styles/report-generator.md` 加入 `## Workflow` 區塊：

```markdown
---
description: 把所有回答格式化為 HTML 報告，自動存檔並開啟瀏覽器
---

## Workflow
- 產生回答後，將內容存成有意義名稱的 .html 檔案
- 自動在預設瀏覽器中開啟該檔案

## HTML Structure
- 使用完整的 HTML5 文件結構
- 加入清楚的標題和章節
- 使用乾淨的 CSS 樣式
```

之後每次問問題，Claude Code 不只會回答，還會自動建立 HTML 檔案並在瀏覽器開啟。你可以把這個技巧用在產生技術文件、分析報告、或任何你需要固定輸出格式的場合。

---

## 同時跑多個不同風格的 Claude Code

你可以開多個 terminal，每個設定不同的 Output Style，讓它們各自扮演不同角色：

```
Terminal 1 (minimal-bullets)    Terminal 2 (yaml-concise)
━━━━━━━━━━━━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━━━━━━━━━━━━
用於：快速問答、日常任務        用於：架構分析、任務規劃
格式：精簡條列                  格式：YAML 結構化輸出
```

**實際使用場景：**

| Terminal | 風格 | 用途 |
|---------|------|------|
| Terminal 1 | minimal-bullets | 快速查語法、問小問題 |
| Terminal 2 | yaml-concise | 規劃複雜任務、產出分析報告 |
| Terminal 3 | Explanatory | Debug 時讓 Claude 解釋每個決策 |

每個 terminal 各自記得自己的 Output Style，不會互相干擾。

---

## 自訂 Status Line：隨時知道用的是哪個風格

同時跑多個風格時，很容易忘記當前 terminal 是哪個設定。Claude Code 的 status line（畫面最底部那一行）可以顯示這個資訊。

### 最快的方式：用 /statusline 指令自動產生

```bash
/statusline 我想在 status line 顯示目前使用的 output style 名稱
```

Claude Code 會自動：
1. 建立 `~/.claude/statusline.py` 腳本
2. 更新 `~/.claude/settings.json` 的 `statusLine` 設定
3. Status line 馬上開始顯示目前的 output style

你不需要手動寫 Python 或設定 JSON，直接描述你想看什麼，Claude Code 幫你搞定。

### 如果你想自己理解或客製化

Status line 本質上是一個 Python 腳本，透過 stdin 收到 Claude Code 的 session 資料（JSON 格式），輸出什麼就顯示什麼：

```python
import json
import sys

input_data = json.load(sys.stdin)
output_style = input_data.get("output_style", {}).get("name", "default")

# 加顏色（ANSI escape codes）
print(f"\033[1;32mStyle: {output_style}\033[0m")
```

`settings.json` 的設定：

```json
{
  "model": "sonnet",
  "statusLine": {
    "type": "command",
    "command": "uv run ~/.claude/statusline.py"
  }
}
```

### 進階：顯示上一條 prompt

Status line 還可以顯示你剛才輸入的 prompt，方便在多個 terminal 之間切換時快速知道每個 session 在做什麼。Claude Code 把所有對話存在 `~/.claude/projects/` 的 JSONL 檔案裡，直接讀取就能取得：

```bash
/statusline 顯示目前的 output style，以及目前 session 最後一條使用者訊息（不要顯示指令，只顯示一般對話）
```

---

## 本篇重點整理

| 功能 | 指令 / 路徑 | 用途 |
|------|------------|------|
| 查看 / 切換 Output Style | `/output-style` | 選擇回應風格 |
| 建立新 Output Style | `/output-style:new` 或直接建立 .md | 自訂格式、語調、行為 |
| 全域 Style 存放位置 | `~/.claude/output-styles/` | 所有專案都能用 |
| 專案 Style 存放位置 | `.claude/output-styles/` | 只限當前專案 |
| 設定 Status Line | `/statusline` + 描述需求 | 顯示目前風格等資訊 |

**三個馬上可以做的事：**

1. 輸入 `/output-style` 看看內建的三種風格，試試 Explanatory 模式，感受一下它怎麼解釋程式碼
2. 建一個自己的 `minimal-bullets.md` 風格，把上面的範例複製進去，試試看問同樣問題時答案的差異
3. 下次開多個 terminal 工作時，試試各自設定不同風格——一個給快速問答，一個給深度分析
