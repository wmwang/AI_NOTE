# Claude Code Agent Skills：把工作流程封裝成可重用的知識包

你是否遇過這種情況：每次叫 Claude Code 做某件事，它都從頭開始摸索、查資料、自己發明一套流程？下次又做一樣的事，它又重新來一遍，而且做法還不太一樣。**Skills** 就是用來解決這個問題的——把「怎麼做這件事」封裝起來，讓 Claude 每次都用一致、正確的方式執行。

---

## Skills 的核心概念

Skill 是一個資料夾，裡面放著：
- **SKILL.md**：告訴 Claude 這個 skill 是做什麼的、什麼時候用、怎麼用
- **選擇性的腳本**：Bash、Python、JavaScript 等可執行的腳本，讓 Claude 有確定性的工具可以用

**最關鍵的設計：Progressive Disclosure（漸進式揭露）**

Claude Code 不會一次把所有 skill 的內容載入 context。它只會先讀每個 skill 的 YAML frontmatter（大約 100~200 tokens/個），用這些摘要來判斷「現在這個任務需不需要用這個 skill」。只有在決定要用某個 skill 的時候，才把 SKILL.md 的完整內容載入。

類比：你有一本食譜書。平常你只看目錄（YAML frontmatter）。決定要做「紅燒牛肉」之後，才翻到那一頁看完整食譜（SKILL.md 全文）。腳本（scripts）更是只有在真正要執行的那一步才拿出來。

這個設計讓你可以裝很多 skill，而不會一開始就把 context 撐爆。

---

## Skill 的結構

```
.claude/                        ← 專案級 skill（只限此專案）
  skills/
    git-pushing/                ← skill 名稱（資料夾）
      SKILL.md                  ← 定義檔
      scripts/
        smart_commit.sh         ← 輔助腳本

~/.claude/                      ← 使用者級 skill（所有專案都能用）
  skills/
    brand-guidelines/
      SKILL.md
```

### SKILL.md 的結構

```markdown
---
name: git-pushing
description: Stage, commit, and push git changes with conventional commit messages.
             Use when user wants to commit and push changes, mentions pushing to remote,
             or asks to save and push their work.
---

# Git Push Workflow

Stage all changes, create a conventional commit, and push to the remote branch.

## Workflow

**ALWAYS use the script** - do NOT use manual git commands:

\```bash
bash skills/git-pushing/scripts/smart_commit.sh
\```

With custom message:
\```bash
bash skills/git-pushing/scripts/smart_commit.sh "feat: add feature"
\```
```

**重要分界線：`---` 以上 vs 以下**

| 位置 | 可見性 | 功能 |
|------|--------|------|
| YAML frontmatter（`---` 以上） | 永遠載入（輕量） | 決定「何時」呼叫此 skill |
| 正文（`---` 以下） | 只在 skill 被選中後載入 | 定義「如何」執行 |

這個區別非常重要：你想讓 Claude 用來決定「要不要選這個 skill」的觸發條件，必須放在 YAML frontmatter 的 `description` 裡。放在正文裡的任何內容，在 skill 選中之前 Claude 根本看不到。

---

## Skills 解決什麼問題？

### 問題一：每次都重新摸索，做法不一致

**沒有 skill 的情況：**
```
你：幫我 commit 並 push
Claude：好，我來看看你的 git status... 用什麼 commit message 格式？
        讓我用 git add . 再 git commit -m "update"...
```

**有 git-pushing skill 的情況：**
```
你：幫我 commit 並 push
Claude：[選擇 git-pushing skill] → 執行 smart_commit.sh → 完成
```

skill 強迫 Claude 按照你定義的流程走，不讓它自由發揮。這在你有「意見強烈的工作流程」時特別有用——例如：「commit message 必須符合 Conventional Commits 格式」、「一定要先跑 lint 再 commit」。

### 問題二：重複的知識浪費 context

假設你的專案有品牌設計規範，你希望 Claude 做前端修改時都遵守這些規範。

**沒有 skill：** 你每次都要貼一大段設計規範到 prompt 裡，或放進 CLAUDE.md（但這樣每次都佔用 context，即使現在是在寫後端）

**有 brand-guidelines skill：** 設計規範放在 skill 裡，只有在 Claude 判斷任務涉及前端/設計時才載入

---

## 實際操作：安裝現成的 Skills

Anthropic 官方有一個 skills marketplace，直接加進來：

```bash
/plugin add marketplace anthropic/skills
```

安裝後輸入 `/plugins` 查看：
- **Document skills**：Excel、PowerPoint 文件處理
- **Example skills**：brand-guidelines、git-pushing、frontend-design 等

這些 skills 自動更新，下次 Claude Code 啟動會拿最新版。

---

## 實際操作：建立自己的 Skill

以「自動化 git push 流程」為例，自己建一個 skill：

**步驟一：建立目錄結構**

```bash
mkdir -p .claude/skills/git-pushing/scripts
```

**步驟二：建立腳本** `.claude/skills/git-pushing/scripts/smart_commit.sh`

```bash
#!/bin/bash
# 自動 staging、生成 commit message、push

git add -A
git status

# 如果有傳入 commit message 就用，沒有就自動生成
if [ -n "$1" ]; then
  COMMIT_MSG="$1"
else
  # 用 Claude CLI 生成 commit message（非互動模式）
  COMMIT_MSG=$(claude -p "根據以下 git diff 生成一行 conventional commit message：$(git diff --staged)")
fi

git commit -m "$COMMIT_MSG"
git push -u origin HEAD
```

**步驟三：建立 SKILL.md** `.claude/skills/git-pushing/SKILL.md`

```markdown
---
name: git-pushing
description: Stage, commit, and push git changes with conventional commit messages.
             Use when user wants to commit and push changes, mentions saving to remote,
             or says "push this", "commit and push", "push to github".
---

# Git Push Workflow

Stage all changes, create a conventional commit, and push to the remote branch.

## Workflow

**ALWAYS use the script** - do NOT use manual git commands:

\```bash
bash skills/git-pushing/scripts/smart_commit.sh
\```

With custom message:
\```bash
bash skills/git-pushing/scripts/smart_commit.sh "feat: add feature"
\```
```

**步驟四：測試**

```bash
# 在 Claude Code 中確認 skill 已被識別
List available skills.

# 觸發 skill
push changes
```

Claude 會詢問是否使用 `git-pushing` skill，核准後自動執行腳本。

---

## 三個容易混淆的地方

### 1. 修改觸發條件要改 frontmatter，不是正文

很多人把觸發關鍵字寫在 `## When to Use` 這種正文段落裡，然後發現沒有效果。

原因：正文在 skill 被選中**之後**才載入，Claude 在決定要不要選這個 skill 的時候根本看不到正文。觸發條件**必須**寫在 `description` 欄位（YAML frontmatter）。

```markdown
---
name: git-pushing
description: 寫這裡的內容才有觸發效果  ← ✅ 正確位置
---

## When to Use
寫這裡沒有觸發效果  ← ❌ 沒用
```

### 2. Skill 失敗時 Claude 會自己想辦法

如果腳本執行失敗，Claude 不會直接報錯停下來。它會 fall back 到自己的推理能力，嘗試用原生 git 指令完成任務。這是一個安全網機制。

### 3. 自動核准需要分開設定兩個權限

每次使用 skill 會出現兩次確認：
1. 「是否使用此 skill？」
2. 「是否執行 skill 內的腳本？」

可以在 `settings.local.json` 裡設定自動核准，之後就不需要每次手動確認。

---

## Skills vs. 其他工具：什麼時候用哪個？

這是第9章最有價值的部分，原書放在最後，這裡提到前面：

| 維度 | Skills | MCP | Subagents | Slash Commands |
|------|--------|-----|-----------|----------------|
| **目的** | 標準化工作方式 | 連接外部服務 | 委派隔離任務 | 使用者觸發快捷 |
| **Context 載入** | 漸進式（輕量） | 啟動時全載（可能很重） | 各自獨立 context | 全 prompt 直接注入 |
| **觸發方式** | Agent 自動判斷 | Agent 自動判斷 | Agent 委派 | 使用者輸入 /指令 |
| **執行位置** | 主 agent 內 | MCP server | 獨立 context | 主 agent 內 |
| **最適合** | 重複性工作流程 | 外部 API/服務 | 長時間重型任務 | 快速一次性操作 |
| **Context 效率** | 高（懶載入） | 低（預先全載） | 高（工作隔離） | 低（每次全注入） |

**用哪個的簡單判斷：**

```
這個任務需要連外部服務？ → MCP
這個任務很重，會讓 context 爆炸？ → Subagent
這個任務需要固定流程、避免 Claude 自由發揮？ → Skill
這個任務只是我自己的快捷鍵？ → Slash Command
```

---

## 進階：context: fork

預設情況下 skill 在主 agent 的 context 裡執行。如果你想讓某個 skill 在隔離的 context 跑（像 subagent 那樣），在 frontmatter 加上：

```markdown
---
name: heavy-analysis
description: 深度分析大型程式碼庫
context: fork
agent: Explore
---
```

`context: fork` 讓 skill 在獨立的 context branch 執行，不會污染主對話。`agent: Explore` 指定用哪種 subagent 類型來跑。如果你只想讓這個 skill 透過 slash command 觸發（不要 Claude 自動判斷），加 `disable-model-invocation: true`。

---

## 本篇重點整理

| 概念 | 重點 |
|------|------|
| **Progressive Disclosure** | Frontmatter 永遠載入，正文和腳本在 skill 啟動後才載入，不浪費 context |
| **觸發條件** | 只能放在 YAML frontmatter 的 `description`，正文裡的觸發條件無效 |
| **Skill vs MCP** | Skill = 流程知識，MCP = 外部連結；兩者解決不同問題 |
| **Skill vs Subagent** | Skill 在主 context 跑（輕），Subagent 在隔離 context 跑（適合重型任務） |
| **失敗處理** | 腳本失敗時 Claude 自動 fallback 到原生推理，不會直接報錯停止 |

**三個可以馬上做的事：**

1. 輸入 `/plugin add marketplace anthropic/skills` 安裝官方 skills，然後 `/plugins` 看看有哪些可用
2. 把你最常讓 Claude 做的「有固定流程的事」（例如：寫 commit、產 PR description、跑測試前的清單）整理一下，考慮包成 skill
3. 如果已經有 CLAUDE.md 裡放了大量「永遠需要的知識」，看看哪些其實只在特定任務才需要——那些可以搬到 skill 裡，讓 context 更精簡
