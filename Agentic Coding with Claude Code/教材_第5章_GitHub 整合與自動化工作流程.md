# 第5章：GitHub 整合與自動化工作流程

你已經會用 Claude Code 在本機寫程式、debug、重構——但如果讓它也參與 GitHub 的 CI/CD 流程，它就不只是你一個人的助手，而是整個團隊共享的自動化成員。這章就來聊聊怎麼把 Claude Code 接進 GitHub，讓 code review、PR 描述、issue 分類這些事都自動搞定。

---

## 為什麼要把 Claude Code 接到 GitHub？

很多團隊導入 Claude Code 之後，效益只停在「個人開發」這一層：每個人在自己電腦上問 Claude 問題，然後手動把結果貼進去。這樣雖然有幫助，但沒有放大器。

把 Claude Code 接進 GitHub 的好處是：**一次設定，全團隊受益**。

| 自動化任務 | 沒整合前 | 整合後 |
|-----------|---------|--------|
| Code Review | 人工逐行看，時間不一定 | 有新 PR 自動觸發，幾分鐘內給出初步分析 |
| PR 描述 | 開發者自己寫（常常寫得很簡略） | 根據 diff + commit 自動生成結構化描述 |
| Issue 分類 | PM 或 lead 手動貼 label | 新 issue 進來自動判斷類型、嚴重程度 |
| Security Scan | 靠 linter 或人工，可能漏掉 | Claude 在 review 時順帶掃 pattern |

說白了，就是把 Claude Code 從「你的個人工具」升級成「CI/CD pipeline 的一個節點」。

---

## GitHub Actions 怎麼呼叫 Claude Code？

Claude Code 的 CLI 支援 non-interactive 模式，這是接進 CI 環境的關鍵。你不需要讓它開一個互動式 session，只要用 `--print`（或簡寫 `-p`）旗標，它就會執行完畢後直接輸出結果、結束程序。

```bash
# 基本用法：把 prompt 傳進去，把結果印出來
claude -p "幫我 review 以下 code" < diff.txt

# 搭配 --allowedTools 限制它只能用讀取類的工具
claude -p "分析這個 diff" --allowedTools "Read" < diff.txt

# 完全不給工具（純文字推理）
claude -p "用一句話總結這個 commit 做了什麼" --allowedTools ""
```

在 GitHub Actions 的 workflow YAML 裡，你需要先設定好環境變數。Claude Code 支援兩種認證方式：

- **`ANTHROPIC_API_KEY`**：用你自己的 Anthropic API key，按用量計費
- **`CLAUDE_CODE_GITHUB_TOKEN`**：GitHub 官方整合方案，走 GitHub 的帳單，對已訂閱 GitHub Copilot Enterprise 的團隊比較方便

兩種方式都設定在 GitHub repo 的 Settings → Secrets and variables → Actions 裡。

---

## 實際案例一：自動 PR Code Review

當有人開一個新 PR，自動觸發 Claude Code 分析 diff，然後把 review comments 回覆到 PR 上。

完整的 workflow YAML 如下：

```yaml
name: Claude Code PR Review

on:
  pull_request:
    types: [labeled]

jobs:
  code-review:
    # 只在 PR 被貼上 'claude-review' label 時執行
    if: contains(github.event.pull_request.labels.*.name, 'claude-review')
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write  # 需要這個才能留 review 評論
      contents: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # 需要完整 history 才能算 diff

      - name: Install Claude Code CLI
        run: npm install -g @anthropic-ai/claude-code

      - name: Get PR diff
        id: diff
        run: |
          git diff origin/${{ github.base_ref }}...HEAD > pr_diff.txt
          echo "Diff size: $(wc -l < pr_diff.txt) lines"

      - name: Run Claude Code Review
        id: review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          REVIEW=$(claude -p "
          你是一個資深工程師，請 review 以下 Pull Request 的 diff。
          重點關注：
          1. 潛在的 bug 或邏輯錯誤
          2. 安全性問題（SQL injection、XSS、API key 外洩等）
          3. 效能問題
          4. 可讀性和維護性

          如果沒有發現問題，說「整體看起來沒問題，有幾點小建議：」然後給出建議。
          回覆用繁體中文，技術術語保留英文。
          
          PR Diff:
          $(cat pr_diff.txt)
          " --allowedTools "")
          
          echo "REVIEW_CONTENT<<EOF" >> $GITHUB_OUTPUT
          echo "$REVIEW" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const review = `## Claude Code 自動 Review\n\n${{ steps.review.outputs.REVIEW_CONTENT }}\n\n---\n*由 Claude Code 自動生成，建議仍由人工確認後 merge*`;
            
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: review
            });
```

幾個要注意的地方：
- `fetch-depth: 0` 一定要設，否則 git diff 會不完整
- `permissions: pull-requests: write` 是必要的，GitHub Actions 預設沒有留言權限
- 用 label `claude-review` 控制觸發，避免所有 PR 都燒 API quota
- diff 太大的時候（例如超過 500 行），建議先切割再送，不然 context 會超限

---

## 實際案例二：自動生成 PR 描述

開 PR 的時候，常常開發者隨便打幾個字就送出去了，reviewer 根本不知道這個 PR 在做什麼。這個 workflow 會在 PR 剛開的時候，根據 commit history 和 diff 自動更新 PR 的 description。

```yaml
name: Auto PR Description

on:
  pull_request:
    types: [opened]  # 只在第一次開 PR 時執行

jobs:
  generate-description:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code CLI
        run: npm install -g @anthropic-ai/claude-code

      - name: Collect context
        id: context
        run: |
          git log origin/${{ github.base_ref }}...HEAD --oneline > commits.txt
          git diff origin/${{ github.base_ref }}...HEAD | head -300 > diff_preview.txt

      - name: Generate PR Description
        id: description
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          DESCRIPTION=$(claude -p "
          根據以下資訊，生成一個結構清楚的 Pull Request description。
          
          格式要求（Markdown）：
          ## Summary
          （2-3 句話說明這個 PR 做了什麼）
          
          ## Changes
          （條列主要改動）
          
          ## Testing
          （說明如何測試這些改動，如果從 diff 看不出來就寫「請開發者補充」）
          
          ## Notes
          （任何 reviewer 需要特別注意的事項，沒有就省略這個 section）
          
          Commit messages:
          $(cat commits.txt)
          
          Diff preview (前 300 行):
          $(cat diff_preview.txt)
          " --allowedTools "")
          
          echo "PR_DESCRIPTION<<EOF" >> $GITHUB_OUTPUT
          echo "$DESCRIPTION" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Update PR Description
        uses: actions/github-script@v7
        with:
          script: |
            const currentBody = context.payload.pull_request.body || '';
            // 如果 PR 已經有描述就不要覆蓋（尊重開發者自己寫的）
            if (currentBody && currentBody.trim().length > 20) {
              console.log('PR already has a description, skipping...');
              return;
            }
            
            await github.rest.pulls.update({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              body: `${{ steps.description.outputs.PR_DESCRIPTION }}`
            });
```

---

## GitHub MCP Server：讓 Claude 直接操作 GitHub

除了在 CI 環境裡執行，你也可以在本機開發時讓 Claude Code 直接讀 issue、看 PR、留評論——這就是 GitHub MCP Server 的用途。

安裝方法很簡單：

```bash
claude mcp add github npx @modelcontextprotocol/server-github
```

然後你需要一個 GitHub Personal Access Token（建議用 fine-grained token，只給必要的權限）：

```bash
# 設定環境變數（加進你的 ~/.zshrc 或 ~/.bashrc）
export GITHUB_TOKEN="ghp_你的token"
```

裝好之後，你在 Claude Code 的對話裡就可以直接說：

- 「幫我看一下 issue #123 在講什麼，然後幫我找相關的程式碼」
- 「列出這個 repo 所有 open 的 PR，哪幾個超過兩週沒動？」
- 「把 PR #456 的 diff 拿來，告訴我有沒有可能影響效能的改動」

這跟 CI workflow 不一樣——CI workflow 是「有事件自動觸發」，MCP Server 是「你主動叫它做事」。兩個互補，不衝突。

---

## CI 環境的注意事項

把 AI 接進 CI/CD 有幾個坑要先知道。

**費用問題**

每次 workflow 觸發都會送 API 請求，token 就這樣燒出去了。建議：
- 不要對所有 PR 都觸發，用 label（像 `claude-review`）來控制
- 可以加上 `paths` 篩選，只有特定目錄的改動才觸發
- 加上 diff 行數判斷，太小的改動不值得跑

```yaml
# 只在改動超過 10 行時才執行 Claude review
- name: Check diff size
  id: diff_check
  run: |
    LINES=$(git diff origin/${{ github.base_ref }}...HEAD --stat | tail -1 | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo "0")
    echo "lines=$LINES" >> $GITHUB_OUTPUT
```

**安全性問題**

絕對不要在 workflow log 裡印出 API key。確認：
- 永遠用 `${{ secrets.ANTHROPIC_API_KEY }}` 傳入，不要硬編碼
- 不要在 `run` 區塊裡 `echo $ANTHROPIC_API_KEY`（就算只是 debug 也不行）
- 把 `ANTHROPIC_API_KEY` 加到 repo 的 Secrets，不要加到 Variables（Variables 是明文）

**Non-interactive 模式的限制**

在 CI 裡跑 Claude Code，一定要用 `--allowedTools` 限制它能做的事。如果你只是要它分析程式碼，就不要給它寫檔案或執行 shell 的工具：

```bash
# 只允許讀取，不允許寫入或執行
claude -p "review 這個 diff" --allowedTools "Read"

# 完全不給工具（只用語言推理）
claude -p "summarize this" --allowedTools ""
```

這樣就算 prompt injection 攻擊（有人在 PR 裡偷塞「ignore previous instructions」），Claude 也沒辦法做壞事。

---

## 本篇重點整理

| 概念 | 重點 | 注意事項 |
|------|------|---------|
| Non-interactive 模式 | 用 `-p` / `--print` 旗標，執行完自動結束 | 一定要加 `--allowedTools` 限制操作範圍 |
| 認證方式 | `ANTHROPIC_API_KEY` 或 `CLAUDE_CODE_GITHUB_TOKEN` | 放在 GitHub Secrets，不能硬編碼 |
| 自動 PR Review | 觸發條件用 label 控制，避免所有 PR 都燒 quota | `fetch-depth: 0` 和 `pull-requests: write` 不能少 |
| 自動 PR 描述 | 根據 commits + diff 生成結構化描述 | 先判斷 PR 有沒有現有描述，避免覆蓋開發者自己寫的 |
| GitHub MCP Server | `claude mcp add github npx @modelcontextprotocol/server-github` | 需要 GITHUB_TOKEN，建議用 fine-grained token |
| 費用控制 | 用 label、paths、diff 大小來限制觸發次數 | 每次 CI 觸發都消耗 API token |
| 安全性 | 不印 API key 到 log，用 `--allowedTools ""` 防 prompt injection | Variables 是明文，Secrets 才會加密 |

**三個立即可以做的事：**

1. **今天就試試 `-p` 旗標**：在 terminal 跑 `claude -p "用一句話解釋以下程式碼做什麼" --allowedTools "" < 某個你的檔案.py`，感受一下 non-interactive 模式的感覺，這是接進 CI 的基礎。

2. **建一個最小可行的 workflow**：把本章的「自動 PR 描述」YAML 複製到你的 repo（`.github/workflows/pr-description.yml`），設好 `ANTHROPIC_API_KEY` secret，開一個測試 PR 看看效果。從最無害的自動化開始，熟悉了再往 code review 走。

3. **安裝 GitHub MCP Server**：跑 `claude mcp add github npx @modelcontextprotocol/server-github` 然後設好 `GITHUB_TOKEN`，試著叫 Claude Code「幫我看一下最近三個 open issue 在講什麼」，這種本機互動體驗和 CI 自動化是相輔相成的。
