# Claude Code 整合指南

# Claude Code 如何運作

> 了解代理迴圈、內建工具，以及 Claude Code 如何與您的專案互動。

Claude Code 是在您的終端機中執行的代理助手。雖然它在編碼方面表現出色，但它可以幫助您從命令列執行的任何操作：撰寫文件、執行建置、搜尋檔案、研究主題等。

本指南涵蓋核心架構、內建功能，以及[有效使用 Claude Code 的提示](#work-effectively-with-claude-code)。如需逐步說明，請參閱[常見工作流程](/zh-TW/common-workflows)。如需擴展功能（如 skills、MCP 和 hooks），請參閱[擴展 Claude Code](/zh-TW/features-overview)。

## 代理迴圈

當您給 Claude 一項任務時，它會經歷三個階段：**收集上下文**、**採取行動**和**驗證結果**。這些階段相互融合。Claude 始終使用工具，無論是搜尋檔案以了解您的程式碼、編輯以進行變更，還是執行測試以檢查其工作。

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/agentic-loop.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=5f1827dec8539f38adee90ead3a85a38" alt="代理迴圈：您的提示導致 Claude 收集上下文、採取行動、驗證結果，並重複直到任務完成。您可以在任何時刻中斷。" width="720" height="280" data-path="images/agentic-loop.svg" />

迴圈會根據您的要求進行調整。關於您程式碼庫的問題可能只需要收集上下文。錯誤修復會反覆循環所有三個階段。重構可能涉及廣泛的驗證。Claude 根據從上一步學到的內容決定每一步需要什麼，將數十個操作鏈接在一起，並沿途進行課程修正。

您也是這個迴圈的一部分。您可以在任何時刻中斷以引導 Claude 朝不同方向發展、提供額外上下文，或要求它嘗試不同的方法。Claude 自主工作，但對您的輸入保持回應。

代理迴圈由兩個元件提供動力：[模型](#models)進行推理，[工具](#tools)採取行動。Claude Code 充當 Claude 周圍的**代理工具**：它提供工具、上下文管理和執行環境，將語言模型轉變為能力強大的編碼代理。

### 模型

Claude Code 使用 Claude 模型來理解您的程式碼並推理任務。Claude 可以讀取任何語言的程式碼、理解元件如何連接，以及找出需要改變什麼來完成您的目標。對於複雜任務，它將工作分解為步驟、執行它們，並根據學到的內容進行調整。

[多個模型](/zh-TW/model-config)可用，具有不同的權衡。Sonnet 可以很好地處理大多數編碼任務。Opus 為複雜的架構決策提供更強的推理能力。在會話期間使用 `/model` 切換，或使用 `claude --model <name>` 開始。

當本指南說「Claude 選擇」或「Claude 決定」時，是模型在進行推理。

### 工具

工具是使 Claude Code 成為代理的原因。沒有工具，Claude 只能用文字回應。有了工具，Claude 可以採取行動：讀取您的程式碼、編輯檔案、執行命令、搜尋網路，以及與外部服務互動。每個工具使用都會返回資訊，反饋到迴圈中，告知 Claude 的下一個決定。

內建工具通常分為五個類別，每個類別代表不同類型的代理能力。

| 類別        | Claude 可以做什麼                                                                      |
| --------- | --------------------------------------------------------------------------------- |
| **檔案操作**  | 讀取檔案、編輯程式碼、建立新檔案、重新命名和重新組織                                                        |
| **搜尋**    | 按模式查找檔案、使用正規表達式搜尋內容、探索程式碼庫                                                        |
| **執行**    | 執行 shell 命令、啟動伺服器、執行測試、使用 git                                                     |
| **網路**    | 搜尋網路、擷取文件、查詢錯誤訊息                                                                  |
| **程式碼智能** | 編輯後查看類型錯誤和警告、跳轉到定義、查找參考（需要[程式碼智能外掛程式](/zh-TW/discover-plugins#code-intelligence)） |

這些是主要功能。Claude 還具有用於生成 subagents、詢問您問題和其他編排任務的工具。請參閱[Claude 可用的工具](/zh-TW/tools-reference)以取得完整清單。

Claude 根據您的提示和沿途學到的內容選擇使用哪些工具。當您說「修復失敗的測試」時，Claude 可能會：

1. 執行測試套件以查看失敗的內容
2. 讀取錯誤輸出
3. 搜尋相關的原始檔案
4. 讀取這些檔案以理解程式碼
5. 編輯檔案以修復問題
6. 再次執行測試以驗證

每個工具使用都會給 Claude 新資訊，告知下一步。這就是代理迴圈的實際運作。

**擴展基本功能：** 內建工具是基礎。您可以使用 [skills](/zh-TW/skills) 擴展 Claude 知道的內容、使用 [MCP](/zh-TW/mcp) 連接到外部服務、使用 [hooks](/zh-TW/hooks) 自動化工作流程，以及將任務卸載給 [subagents](/zh-TW/sub-agents)。這些擴展形成了核心代理迴圈之上的一層。請參閱[擴展 Claude Code](/zh-TW/features-overview) 以獲得有關為您的需求選擇正確擴展的指導。

## Claude 可以存取什麼

本指南重點介紹終端機。Claude Code 也在 [VS Code](/zh-TW/vs-code)、[JetBrains IDE](/zh-TW/jetbrains) 和其他環境中執行。

當您在目錄中執行 `claude` 時，Claude Code 可以存取：

* **您的專案。** 您目錄和子目錄中的檔案，以及其他地方經您許可的檔案。
* **您的終端機。** 您可以執行的任何命令：建置工具、git、套件管理器、系統公用程式、指令碼。如果您可以從命令列執行，Claude 也可以。
* **您的 git 狀態。** 目前分支、未提交的變更和最近的提交歷史。
* **您的 [CLAUDE.md](/zh-TW/memory)。** 一個 markdown 檔案，您可以在其中儲存專案特定的指示、慣例和 Claude 應該在每個會話中知道的上下文。
* **[自動記憶](/zh-TW/memory#auto-memory)。** Claude 在您工作時自動儲存的學習內容，例如專案模式和您的偏好。MEMORY.md 的前 200 行或 25KB（以先到者為準）在每個會話開始時載入。
* **您設定的擴展。** 用於外部服務的 [MCP servers](/zh-TW/mcp)、用於工作流程的 [skills](/zh-TW/skills)、用於委派工作的 [subagents](/zh-TW/sub-agents)，以及用於瀏覽器互動的 [Claude in Chrome](/zh-TW/chrome)。

因為 Claude 看到您的整個專案，它可以跨越它工作。當您要求 Claude「修復身份驗證錯誤」時，它會搜尋相關檔案、讀取多個檔案以理解上下文、跨它們進行協調編輯、執行測試以驗證修復，以及在您要求時提交變更。這與只看到目前檔案的內聯程式碼助手不同。

## 環境和介面

上述代理迴圈、工具和功能在您使用 Claude Code 的任何地方都是相同的。改變的是程式碼執行的位置以及您與它互動的方式。

### 執行環境

Claude Code 在三個環境中執行，每個環境對程式碼執行位置有不同的權衡。

| 環境       | 程式碼執行位置          | 使用案例              |
| -------- | ---------------- | ----------------- |
| **本機**   | 您的機器             | 預設。完全存取您的檔案、工具和環境 |
| **雲端**   | Anthropic 管理的 VM | 卸載任務、處理您本機沒有的儲存庫  |
| **遠端控制** | 您的機器，從瀏覽器控制      | 使用網路 UI，同時保持一切本機  |

### 介面

您可以透過終端機、[桌面應用程式](/zh-TW/desktop)、[IDE 擴展](/zh-TW/vs-code)、[claude.ai/code](https://claude.ai/code)、[遠端控制](/zh-TW/remote-control)、[Slack](/zh-TW/slack) 和 [CI/CD 管道](/zh-TW/github-actions)存取 Claude Code。介面決定了您如何看到和與 Claude 互動，但底層代理迴圈是相同的。請參閱[在任何地方使用 Claude Code](/zh-TW/overview#use-claude-code-everywhere) 以取得完整清單。

## 使用會話

Claude Code 在您工作時將您的對話儲存在本機為純文字 JSONL 檔案，位於 `~/.claude/projects/` 下，這使得[重新開始](#undo-changes-with-checkpoints)、[恢復和分叉](#resume-or-fork-sessions)會話成為可能。在 Claude 進行程式碼變更之前，它還會快照受影響的檔案，以便您在需要時可以還原。如需路徑、保留期和如何清除此資料，請參閱[`~/.claude` 中的應用程式資料](/zh-TW/claude-directory#application-data)。

**會話是獨立的。** 每個新會話都以新的上下文視窗開始，沒有來自先前會話的對話歷史。Claude 可以使用[自動記憶](/zh-TW/memory#auto-memory)跨會話保留學習內容，您可以在 [CLAUDE.md](/zh-TW/memory) 中新增自己的持久指示。

### 跨分支工作

每個 Claude Code 對話都是綁定到您目前目錄的會話。`/resume` 選擇器預設顯示目前 worktree 中的會話，並具有鍵盤快捷鍵以擴展清單到其他 worktrees 或專案。請參閱[管理會話](/zh-TW/sessions#use-the-session-picker)以取得完整的選擇器快捷鍵清單以及名稱解析的工作方式。

Claude 看到您目前分支的檔案。當您切換分支時，Claude 看到新分支的檔案，但您的對話歷史保持不變。Claude 記得您討論過的內容，即使在切換後也是如此。

由於會話綁定到目錄，您可以使用 [git worktrees](/zh-TW/worktrees) 執行平行 Claude 會話，這會為個別分支建立單獨的目錄。

### 恢復或分叉會話

使用 `claude --continue` 或 `claude --resume` 恢復會話會在相同的會話 ID 下重新開啟它，並將新訊息附加到現有對話。使用 `--fork-session` 或 `/branch` 分叉會將歷史複製到新的會話 ID 中，保持原始不變。

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/session-continuity.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=fa41d12bfb57579cabfeece907151d30" alt="會話連續性：恢復繼續相同的會話，分叉使用新 ID 建立新分支。" width="560" height="280" data-path="images/session-continuity.svg" />

如需恢復旗標、`/resume` 選擇器、命名，以及當相同會話在兩個終端機中開啟時會發生什麼，請參閱[管理會話](/zh-TW/sessions)。

### 上下文視窗

Claude 的上下文視窗保存您的對話歷史、檔案內容、命令輸出、[CLAUDE.md](/zh-TW/memory)、[自動記憶](/zh-TW/memory#auto-memory)、載入的 skills 和系統指示。當您工作時，上下文會填滿。Claude 會自動壓縮，但對話早期的指示可能會丟失。將持久規則放在 CLAUDE.md 中，並執行 `/context` 以查看什麼在使用空間。

如需互動式逐步說明，請參閱[探索上下文視窗](/zh-TW/context-window)。

#### 當上下文填滿時

Claude Code 在您接近限制時自動管理上下文。它首先清除較舊的工具輸出，然後在需要時總結對話。您的請求和關鍵程式碼片段被保留；對話早期的詳細指示可能會丟失。將持久規則放在 CLAUDE.md 中，而不是依賴對話歷史。

要控制在壓縮期間保留的內容，請在 CLAUDE.md 中新增「Compact Instructions」部分或使用焦點執行 `/compact`（如 `/compact focus on the API changes`）。

如果單個檔案或工具輸出非常大，以至於在每次摘要後上下文立即重新填滿，Claude Code 會在幾次嘗試後停止自動壓縮，並顯示錯誤而不是迴圈。請參閱[自動壓縮停止並出現 thrashing 錯誤](/zh-TW/troubleshooting#auto-compaction-stops-with-a-thrashing-error)以取得恢復步驟。

執行 `/context` 以查看什麼在使用空間。MCP 工具定義預設會延遲，並透過[工具搜尋](/zh-TW/mcp#scale-with-mcp-tool-search)按需載入，因此只有工具名稱會消耗上下文，直到 Claude 使用特定工具。執行 `/mcp` 以檢查每個伺服器的成本。

#### 使用 skills 和 subagents 管理上下文

除了壓縮，您可以使用其他功能來控制什麼載入到上下文中。

[Skills](/zh-TW/skills) 按需載入。Claude 在會話開始時看到 skill 描述，但完整內容只在使用 skill 時載入。對於您手動呼叫的 skills，設定 `disable-model-invocation: true` 以將描述保留在上下文之外，直到您需要它們。對於您沒有撰寫的 skills，使用 [`skillOverrides`](/zh-TW/skills#override-skill-visibility-from-settings) 從設定中執行相同操作。

[Subagents](/zh-TW/sub-agents) 獲得自己的新上下文，完全與您的主要對話分開。他們的工作不會使您的上下文膨脹。完成後，他們返回摘要。這種隔離是 subagents 在長會話中有幫助的原因。

請參閱[上下文成本](/zh-TW/features-overview#understand-context-costs)以了解每個功能的成本，以及[減少令牌使用](/zh-TW/costs#reduce-token-usage)以獲得管理上下文的提示。

## 使用檢查點和許可保持安全

Claude 有兩個安全機制：檢查點讓您撤銷檔案變更，許可控制 Claude 可以在不詢問的情況下執行的操作。

### 使用檢查點撤銷變更

**每個檔案編輯都是可逆的。** 在 Claude 編輯任何檔案之前，它會快照目前內容。如果出現問題，按 `Esc` 兩次以重新開始到先前狀態，或要求 Claude 撤銷。

檢查點是會話本機的，與 git 分開。它們只涵蓋檔案變更。影響遠端系統的操作（資料庫、API、部署）無法檢查點，這就是為什麼 Claude 在執行具有外部副作用的命令之前詢問。

### 控制 Claude 可以做什麼

按 `Shift+Tab` 循環通過許可模式：

* **預設**：Claude 在檔案編輯和 shell 命令之前詢問
* **自動接受編輯**：Claude 編輯檔案並執行常見的檔案系統命令（如 `mkdir` 和 `mv`）而不詢問，仍然詢問其他命令
* **Plan Mode**：Claude 僅使用唯讀工具，建立您可以在執行前批准的計畫
* **Auto mode**：Claude 使用背景安全檢查評估所有操作。目前是研究預覽

您也可以在 `.claude/settings.json` 中允許特定命令，以便 Claude 不會每次都詢問。這對於受信任的命令（如 `npm test` 或 `git status`）很有用。設定可以從組織範圍的政策範圍到個人偏好。請參閱[許可](/zh-TW/permissions)以取得詳細資訊。

***

## 有效使用 Claude Code

這些提示可幫助您從 Claude Code 獲得更好的結果。

### 向 Claude Code 尋求幫助

Claude Code 可以教您如何使用它。提出問題，例如「我如何設定 hooks？」或「構建我的 CLAUDE.md 的最佳方式是什麼？」，Claude 會解釋。

內建命令也會引導您完成設定：

* `/init` 引導您為您的專案建立 CLAUDE.md
* `/agents` 幫助您設定自訂 subagents
* `/doctor` 診斷您的安裝的常見問題

### 這是一個對話

Claude Code 是對話式的。您不需要完美的提示。從您想要的開始，然後細化：

```text theme={null}
修復登入錯誤
```

\[Claude 調查，嘗試一些東西]

```text theme={null}
這不太對。問題在於會話處理。
```

\[Claude 調整方法]

當第一次嘗試不正確時，您不會重新開始。您進行迭代。

#### 中斷和引導

您可以在任何時刻中斷 Claude。如果它走錯了路，只需輸入您的更正並按 Enter。Claude 將停止正在執行的操作，並根據您的輸入調整其方法。您不必等待它完成或重新開始。

### 預先具體

您的初始提示越精確，您需要的更正就越少。參考特定檔案、提及約束，並指出範例模式。

```text theme={null}
結帳流程對於具有過期卡的使用者已損壞。
檢查 src/payments/ 以查找問題，特別是令牌刷新。
先寫一個失敗的測試，然後修復它。
```

模糊的提示有效，但您會花更多時間引導。像上面這樣的具體提示通常在第一次嘗試時成功。

### 給 Claude 一些東西來驗證

Claude 在能夠檢查自己的工作時表現更好。包括測試案例、貼上預期 UI 的螢幕截圖，或定義您想要的輸出。

```text theme={null}
實現 validateEmail。測試案例：'user@example.com' → true，
'invalid' → false，'user@.com' → false。之後執行測試。
```

對於視覺工作，貼上設計的螢幕截圖，並要求 Claude 將其實現與其進行比較。

### 在實現之前探索

對於複雜的問題，將研究與編碼分開。使用計畫模式（按 `Shift+Tab` 兩次）首先分析程式碼庫：

```text theme={null}
讀取 src/auth/ 並理解我們如何處理會話。
然後為新增 OAuth 支援建立計畫。
```

檢查計畫，透過對話細化它，然後讓 Claude 實現。這種兩階段方法比直接跳到程式碼產生更好的結果。

### 委派，不要指示

想像委派給一位能力強大的同事。提供上下文和方向，然後相信 Claude 會找出詳細資訊：

```text theme={null}
結帳流程對於具有過期卡的使用者已損壞。
相關程式碼在 src/payments/ 中。您可以調查並修復它嗎？
```

您不需要指定要讀取哪些檔案或執行哪些命令。Claude 會找出來。

## 接下來

<CardGroup cols={2}>
  <Card title="使用功能擴展" icon="puzzle-piece" href="/zh-TW/features-overview">
    新增 Skills、MCP 連接和自訂命令
  </Card>

  <Card title="常見工作流程" icon="graduation-cap" href="/zh-TW/common-workflows">
    典型任務的逐步指南
  </Card>
</CardGroup>


---

# Choose a permission mode

> Control whether Claude asks before editing files or running commands. Cycle modes with Shift+Tab in the CLI or use the mode selector in VS Code, Desktop, and claude.ai.

When Claude wants to edit a file, run a shell command, or make a network request, it pauses and asks you to approve the action. Permission modes control how often that pause happens. The mode you pick shapes the flow of a session: default mode has you review each action as it comes, while looser modes let Claude work in longer uninterrupted stretches and report back when done. Pick more oversight for sensitive work, or fewer interruptions when you trust the direction.

## Available modes

Each mode makes a different tradeoff between convenience and oversight. The table below shows what Claude can do without a permission prompt in each mode.

| Mode                                                                | What runs without asking                                                               | Best for                                |
| :------------------------------------------------------------------ | :------------------------------------------------------------------------------------- | :-------------------------------------- |
| `default`                                                           | Reads only                                                                             | Getting started, sensitive work         |
| [`acceptEdits`](#auto-approve-file-edits-with-acceptedits-mode)     | Reads, file edits, and common filesystem commands (`mkdir`, `touch`, `mv`, `cp`, etc.) | Iterating on code you're reviewing      |
| [`plan`](#analyze-before-you-edit-with-plan-mode)                   | Reads only                                                                             | Exploring a codebase before changing it |
| [`auto`](#eliminate-prompts-with-auto-mode)                         | Everything, with background safety checks                                              | Long tasks, reducing prompt fatigue     |
| [`dontAsk`](#allow-only-pre-approved-tools-with-dontask-mode)       | Only pre-approved tools                                                                | Locked-down CI and scripts              |
| [`bypassPermissions`](#skip-all-checks-with-bypasspermissions-mode) | Everything                                                                             | Isolated containers and VMs only        |

In every mode except `bypassPermissions`, writes to [protected paths](#protected-paths) are never auto-approved, guarding repository state and Claude's own configuration against accidental corruption.

Modes set the baseline. Layer [permission rules](/en/permissions#manage-permissions) on top to pre-approve or block specific tools in any mode except `bypassPermissions`, which skips the permission layer entirely.

## Switch permission modes

You can switch modes mid-session, at startup, or as a persistent default. The mode is set through these controls, not by asking Claude in chat. Select your interface below to see how to change it.

<Tabs>
  <Tab title="CLI">
    **During a session**: press `Shift+Tab` to cycle `default` → `acceptEdits` → `plan`. The current mode appears in the status bar. Not every mode is in the default cycle:

    * `auto`: appears when your account meets the [auto mode requirements](#eliminate-prompts-with-auto-mode); cycling to auto shows an opt-in prompt until you accept it, or select **No, don't ask again** to remove auto from the cycle
    * `bypassPermissions`: appears after you start with `--permission-mode bypassPermissions`, `--dangerously-skip-permissions`, or `--allow-dangerously-skip-permissions`; the `--allow-` variant adds the mode to the cycle without activating it
    * `dontAsk`: never appears in the cycle; set it with `--permission-mode dontAsk`

    Enabled optional modes slot in after `plan`, with `bypassPermissions` first and `auto` last. If you have both enabled, you will cycle through `bypassPermissions` on the way to `auto`.

    **At startup**: pass the mode as a flag.

    ```bash theme={null}
    claude --permission-mode plan
    ```

    **As a default**: set `defaultMode` in [settings](/en/settings#settings-files).

    ```json theme={null}
    {
      "permissions": {
        "defaultMode": "acceptEdits"
      }
    }
    ```

    The same `--permission-mode` flag works with `-p` for [non-interactive runs](/en/headless).
  </Tab>

  <Tab title="VS Code">
    **During a session**: click the mode indicator at the bottom of the prompt box.

    **As a default**: set `claudeCode.initialPermissionMode` in VS Code settings, or use the Claude Code extension settings panel.

    The mode indicator shows these labels, mapped to the mode each one applies:

    | UI label           | Mode                |
    | :----------------- | :------------------ |
    | Ask before edits   | `default`           |
    | Edit automatically | `acceptEdits`       |
    | Plan mode          | `plan`              |
    | Auto mode          | `auto`              |
    | Bypass permissions | `bypassPermissions` |

    Auto mode appears in the mode indicator after you enable **Allow dangerously skip permissions** in the extension settings, but it stays unavailable until your account meets every requirement listed in the [auto mode section](#eliminate-prompts-with-auto-mode). The `claudeCode.initialPermissionMode` setting does not accept `auto`; to start in auto mode by default, set `defaultMode` in your Claude Code [`settings.json`](/en/settings#settings-files) instead.

    Bypass permissions also requires the **Allow dangerously skip permissions** toggle before it appears in the mode indicator.

    See the [VS Code guide](/en/vs-code) for extension-specific details.
  </Tab>

  <Tab title="JetBrains">
    The JetBrains plugin runs Claude Code in the IDE terminal, so switching modes works the same as in the CLI: press `Shift+Tab` to cycle, or pass `--permission-mode` when launching.
  </Tab>

  <Tab title="Desktop">
    Use the mode selector next to the send button. Auto and Bypass permissions appear only after you enable them in Desktop settings. See the [Desktop guide](/en/desktop#choose-a-permission-mode).
  </Tab>

  <Tab title="Web and mobile">
    Use the mode dropdown next to the prompt box on [claude.ai/code](https://claude.ai/code) or in the mobile app. Permission prompts appear in claude.ai for approval. Which modes appear depends on where the session runs:

    * **Cloud sessions** on [Claude Code on the web](/en/claude-code-on-the-web): Auto accept edits and Plan mode. Ask permissions, Auto, and Bypass permissions are not available.
    * **[Remote Control](/en/remote-control) sessions** on your local machine: Ask permissions, Auto accept edits, and Plan mode. Auto and Bypass permissions are not available.

    For Remote Control, you can also set the starting mode when launching the host:

    ```bash theme={null}
    claude remote-control --permission-mode acceptEdits
    ```
  </Tab>
</Tabs>

## Auto-approve file edits with acceptEdits mode

`acceptEdits` mode lets Claude create and edit files in your working directory without prompting. The status bar shows `⏵⏵ accept edits on` while this mode is active.

In addition to file edits, `acceptEdits` mode auto-approves common filesystem Bash commands: `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, and `sed`. These commands are also auto-approved when prefixed with safe environment variables such as `LANG=C` or `NO_COLOR=1`, or process wrappers such as `timeout`, `nice`, or `nohup`. Like file edits, auto-approval applies only to paths inside your working directory or `additionalDirectories`. Paths outside that scope, writes to [protected paths](#protected-paths), and all other Bash commands still prompt.

When the [PowerShell tool](/en/tools-reference#powershell-tool) is enabled, `acceptEdits` mode also auto-approves `Set-Content`, `Add-Content`, `Clear-Content`, and `Remove-Item` on in-scope paths, along with their common aliases. The same scope and protected-path rules apply.

Use `acceptEdits` when you want to review changes in your editor or via `git diff` after the fact rather than approving each edit inline. Press `Shift+Tab` once from default mode to enter it, or start with it directly:

```bash theme={null}
claude --permission-mode acceptEdits
```

## Analyze before you edit with plan mode

Plan mode tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source. Permission prompts still apply the same as default mode.

Enter plan mode by pressing `Shift+Tab` or prefixing a single prompt with `/plan`. You can also start in plan mode from the CLI:

```bash theme={null}
claude --permission-mode plan
```

Press `Shift+Tab` again to leave plan mode without approving a plan.

### Review and approve a plan

When the plan is ready, Claude presents it and asks how to proceed. From that prompt you can:

* Approve and start in auto mode
* Approve and accept edits
* Approve and review each edit manually
* Keep planning with feedback
* Refine with [Ultraplan](/en/ultraplan) for browser-based review

Press `Ctrl+G` to open the proposed plan in your default text editor and edit it directly before Claude proceeds. When [`showClearContextOnPlanAccept`](/en/settings#available-settings) is enabled, each approve option also offers to clear the planning context first.

Accepting a plan also names the session from the plan content automatically, unless you've already set a name with `--name` or `/rename`.

### Set plan mode as the default

To make plan mode the default for a project, set `defaultMode` in `.claude/settings.json`:

```json theme={null}
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

## Eliminate prompts with auto mode

<Note>
  Auto mode requires Claude Code v2.1.83 or later.
</Note>

Auto mode lets Claude execute without permission prompts. A separate classifier model reviews actions before they run, blocking anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content Claude read.

<Warning>
  Auto mode is a research preview. It reduces prompts but does not guarantee safety. Use it for tasks where you trust the general direction, not as a replacement for review on sensitive operations.
</Warning>

Auto mode is available only when your account meets all of these requirements:

* **Plan**: Max, Team, Enterprise, or API. Not available on Pro.
* **Admin**: on Team and Enterprise, an admin must enable it in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code) before users can turn it on. Admins can also lock it off by setting `permissions.disableAutoMode` to `"disable"` in [managed settings](/en/permissions#managed-settings).
* **Model**: Claude Sonnet 4.6, Opus 4.6, or Opus 4.7 on Team, Enterprise, and API plans; Claude Opus 4.7 only on Max plans. Other models, including Haiku and claude-3 models, are not supported.
* **Provider**: Anthropic API only. Not available on Bedrock, Vertex, or Foundry.

If Claude Code reports auto mode as unavailable, one of these requirements is unmet; this is not a transient outage. A separate message that names a model and says auto mode "cannot determine the safety" of an action is a transient classifier outage; see the [error reference](/en/errors#auto-mode-cannot-determine-the-safety-of-an-action).

### What the classifier blocks by default

The classifier trusts your working directory and your repo's configured remotes. Everything else is treated as external until you [configure trusted infrastructure](/en/auto-mode-config).

**Blocked by default**:

* Downloading and executing code, like `curl | bash`
* Sending sensitive data to external endpoints
* Production deploys and migrations
* Mass deletion on cloud storage
* Granting IAM or repo permissions
* Modifying shared infrastructure
* Irreversibly destroying files that existed before the session
* Force push, or pushing directly to `main`

**Allowed by default**:

* Local file operations in your working directory
* Installing dependencies declared in your lock files or manifests
* Reading `.env` and sending credentials to their matching API
* Read-only HTTP requests
* Pushing to the branch you started on or one Claude created

Sandbox network access requests are routed through the classifier rather than allowed by default. Run `claude auto-mode defaults` to see the full rule lists. If routine actions get blocked, an administrator can add trusted repos, buckets, and services via the `autoMode.environment` setting: see [Configure auto mode](/en/auto-mode-config).

### Boundaries you state in conversation

The classifier treats boundaries you state in the conversation as a block signal. If you tell Claude "don't push" or "wait until I review before deploying", the classifier blocks matching actions even when the default rules would allow them. A boundary stays in force until you lift it in a later message. Claude's own judgment that a condition was met does not lift it.

Boundaries are not stored as rules. The classifier re-reads them from the transcript on each check, so a boundary can be lost if [context compaction](/en/costs#reduce-token-usage) removes the message that stated it. For a hard guarantee, add a [deny rule](/en/permissions#permission-rule-syntax) instead.

### When auto mode falls back

Each denied action shows a notification and appears in `/permissions` under the Recently denied tab, where you can press `r` to retry it with a manual approval.

If the classifier blocks an action 3 times in a row or 20 times total, auto mode pauses and Claude Code resumes prompting. Approving the prompted action resumes auto mode. These thresholds are not configurable. Any allowed action resets the consecutive counter, while the total counter persists for the session and resets only when its own limit triggers a fallback.

In [non-interactive mode](/en/headless) with the `-p` flag, repeated blocks abort the session since there is no user to prompt.

Repeated blocks usually mean the classifier is missing context about your infrastructure. Use `/feedback` to report false positives, or have an administrator [configure trusted infrastructure](/en/auto-mode-config).

<AccordionGroup>
  <Accordion title="How the classifier evaluates actions">
    Each action goes through a fixed decision order. The first matching step wins:

    1. Actions matching your [allow or deny rules](/en/permissions#manage-permissions) resolve immediately
    2. Read-only actions and file edits in your working directory are auto-approved, except writes to [protected paths](#protected-paths)
    3. Everything else goes to the classifier
    4. If the classifier blocks, Claude receives the reason and tries an alternative

    On entering auto mode, broad allow rules that grant arbitrary code execution are dropped:

    * Blanket `Bash(*)` or `PowerShell(*)`
    * Wildcarded interpreters like `Bash(python*)`
    * Package-manager run commands
    * `Agent` allow rules

    Narrow rules like `Bash(npm test)` carry over. Dropped rules are restored when you leave auto mode.

    The classifier sees user messages, tool calls, and your CLAUDE.md content. Tool results are stripped, so hostile content in a file or web page cannot manipulate it directly. A separate server-side probe scans incoming tool results and flags suspicious content before Claude reads it. For more on how these layers work together, see the [auto mode announcement](https://claude.com/blog/auto-mode) and the [engineering deep dive](https://www.anthropic.com/engineering/claude-code-auto-mode).
  </Accordion>

  <Accordion title="How auto mode handles subagents">
    The classifier checks [subagent](/en/sub-agents) work at three points:

    1. Before a subagent starts, the delegated task description is evaluated, so a dangerous-looking task is blocked at spawn time.
    2. While the subagent runs, each of its actions goes through the classifier with the same rules as the parent session, and any `permissionMode` in the subagent's frontmatter is ignored.
    3. When the subagent finishes, the classifier reviews its full action history; if that return check flags a concern, a security warning is prepended to the subagent's results.
  </Accordion>

  <Accordion title="Cost and latency">
    The classifier runs on a server-configured model that is independent of your `/model` selection, so switching models does not change classifier availability. Classifier calls count toward your token usage. Each check sends a portion of the transcript plus the pending action, adding a round-trip before execution. Reads and working-directory edits outside protected paths skip the classifier, so the overhead comes mainly from shell commands and network operations.
  </Accordion>
</AccordionGroup>

## Allow only pre-approved tools with dontAsk mode

`dontAsk` mode auto-denies every tool call that would otherwise prompt. Only actions matching your `permissions.allow` rules and [read-only Bash commands](/en/permissions#read-only-commands) can execute; explicit `ask` rules are denied rather than prompting. This makes the mode fully non-interactive for CI pipelines or restricted environments where you pre-define exactly what Claude may do.

Set it at startup with the flag:

```bash theme={null}
claude --permission-mode dontAsk
```

## Skip all checks with bypassPermissions mode

`bypassPermissions` mode disables permission prompts and safety checks so tool calls execute immediately. As of v2.1.126 this includes writes to [protected paths](#protected-paths), which earlier versions still prompted for. Removals targeting the filesystem root or home directory, such as `rm -rf /` and `rm -rf ~`, still prompt as a circuit breaker against model error. Only use this mode in isolated environments like containers, VMs, or dev containers without internet access, where Claude Code cannot damage your host system.

You cannot enter `bypassPermissions` from a session that was started without one of the enabling flags; restart with one to enable it:

```bash theme={null}
claude --permission-mode bypassPermissions
```

The `--dangerously-skip-permissions` flag is equivalent.

<Warning>
  `bypassPermissions` offers no protection against prompt injection or unintended actions. For background safety checks without prompts, use [auto mode](#eliminate-prompts-with-auto-mode) instead. Administrators can block this mode by setting `permissions.disableBypassPermissionsMode` to `"disable"` in [managed settings](/en/permissions#managed-settings).
</Warning>

## Protected paths

Writes to a small set of paths are never auto-approved, in every mode except `bypassPermissions`. This prevents accidental corruption of repository state and Claude's own configuration. In `default`, `acceptEdits`, and `plan` these writes prompt; in `auto` they route to the classifier; in `dontAsk` they are denied; in `bypassPermissions` they are allowed.

Protected directories:

* `.git`
* `.vscode`
* `.idea`
* `.husky`
* `.claude`, except for `.claude/commands`, `.claude/agents`, `.claude/skills`, and `.claude/worktrees` where Claude routinely creates content

Protected files:

* `.gitconfig`, `.gitmodules`
* `.bashrc`, `.bash_profile`, `.zshrc`, `.zprofile`, `.profile`
* `.ripgreprc`
* `.mcp.json`, `.claude.json`

## See also

* [Permissions](/en/permissions): allow, ask, and deny rules; managed policies
* [Configure auto mode](/en/auto-mode-config): tell the classifier which infrastructure your organization trusts
* [Hooks](/en/hooks): custom permission logic via `PreToolUse` and `PermissionRequest` hooks
* [Ultraplan](/en/ultraplan): run plan mode in a Claude Code on the web session with browser-based review
* [Security](/en/security): safeguards and best practices
* [Sandboxing](/en/sandboxing): filesystem and network isolation for Bash commands
* [Non-interactive mode](/en/headless): run Claude Code with the `-p` flag


---

# Common workflows

> Step-by-step guides for exploring codebases, fixing bugs, refactoring, testing, and other everyday tasks with Claude Code.

This page collects short recipes for everyday development. For higher-level guidance on prompting and context management, see [Best practices](/en/best-practices).

This page covers:

* [Prompt recipes](#prompt-recipes) for exploring code, fixing bugs, refactoring, testing, PRs, and documentation
* [Resume previous conversations](#resume-previous-conversations) so a task can span multiple sittings
* [Run parallel sessions with worktrees](#run-parallel-sessions-with-worktrees) so concurrent edits don't collide
* [Plan before editing](#plan-before-editing) to review changes before they touch disk
* [Delegate research to subagents](#delegate-research-to-subagents) to keep your main context clean
* [Pipe Claude into scripts](#pipe-claude-into-scripts) for CI and batch processing

## Prompt recipes

These are prompt patterns for everyday tasks like exploring unfamiliar code, debugging, refactoring, writing tests, and creating PRs. Each works in any Claude Code surface; adapt the wording to your project.

### Understand new codebases

#### Get a quick codebase overview

Suppose you've just joined a new project and need to understand its structure quickly.

<Steps>
  <Step title="Navigate to the project root directory">
    ```bash theme={null}
    cd /path/to/project 
    ```
  </Step>

  <Step title="Start Claude Code">
    ```bash theme={null}
    claude 
    ```
  </Step>

  <Step title="Ask for a high-level overview">
    ```text theme={null}
    give me an overview of this codebase
    ```
  </Step>

  <Step title="Dive deeper into specific components">
    ```text theme={null}
    explain the main architecture patterns used here
    ```

    ```text theme={null}
    what are the key data models?
    ```

    ```text theme={null}
    how is authentication handled?
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Start with broad questions, then narrow down to specific areas
  * Ask about coding conventions and patterns used in the project
  * Request a glossary of project-specific terms
</Tip>

#### Find relevant code

Suppose you need to locate code related to a specific feature or functionality.

<Steps>
  <Step title="Ask Claude to find relevant files">
    ```text theme={null}
    find the files that handle user authentication
    ```
  </Step>

  <Step title="Get context on how components interact">
    ```text theme={null}
    how do these authentication files work together?
    ```
  </Step>

  <Step title="Understand the execution flow">
    ```text theme={null}
    trace the login process from front-end to database
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Be specific about what you're looking for
  * Use domain language from the project
  * Install a [code intelligence plugin](/en/discover-plugins#code-intelligence) for your language to give Claude precise "go to definition" and "find references" navigation
</Tip>

***

### Fix bugs efficiently

Suppose you've encountered an error message and need to find and fix its source.

<Steps>
  <Step title="Share the error with Claude">
    ```text theme={null}
    I'm seeing an error when I run npm test
    ```
  </Step>

  <Step title="Ask for fix recommendations">
    ```text theme={null}
    suggest a few ways to fix the @ts-ignore in user.ts
    ```
  </Step>

  <Step title="Apply the fix">
    ```text theme={null}
    update user.ts to add the null check you suggested
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Tell Claude the command to reproduce the issue and get a stack trace
  * Mention any steps to reproduce the error
  * Let Claude know if the error is intermittent or consistent
</Tip>

***

### Refactor code

Suppose you need to update old code to use modern patterns and practices.

<Steps>
  <Step title="Identify legacy code for refactoring">
    ```text theme={null}
    find deprecated API usage in our codebase
    ```
  </Step>

  <Step title="Get refactoring recommendations">
    ```text theme={null}
    suggest how to refactor utils.js to use modern JavaScript features
    ```
  </Step>

  <Step title="Apply the changes safely">
    ```text theme={null}
    refactor utils.js to use ES2024 features while maintaining the same behavior
    ```
  </Step>

  <Step title="Verify the refactoring">
    ```text theme={null}
    run tests for the refactored code
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Ask Claude to explain the benefits of the modern approach
  * Request that changes maintain backward compatibility when needed
  * Do refactoring in small, testable increments
</Tip>

***

### Work with tests

Suppose you need to add tests for uncovered code.

<Steps>
  <Step title="Identify untested code">
    ```text theme={null}
    find functions in NotificationsService.swift that are not covered by tests
    ```
  </Step>

  <Step title="Generate test scaffolding">
    ```text theme={null}
    add tests for the notification service
    ```
  </Step>

  <Step title="Add meaningful test cases">
    ```text theme={null}
    add test cases for edge conditions in the notification service
    ```
  </Step>

  <Step title="Run and verify tests">
    ```text theme={null}
    run the new tests and fix any failures
    ```
  </Step>
</Steps>

Claude can generate tests that follow your project's existing patterns and conventions. When asking for tests, be specific about what behavior you want to verify. Claude examines your existing test files to match the style, frameworks, and assertion patterns already in use.

For comprehensive coverage, ask Claude to identify edge cases you might have missed. Claude can analyze your code paths and suggest tests for error conditions, boundary values, and unexpected inputs that are easy to overlook.

***

### Create pull requests

You can create pull requests by asking Claude directly ("create a pr for my changes"), or guide Claude through it step-by-step:

<Steps>
  <Step title="Summarize your changes">
    ```text theme={null}
    summarize the changes I've made to the authentication module
    ```
  </Step>

  <Step title="Generate a pull request">
    ```text theme={null}
    create a pr
    ```
  </Step>

  <Step title="Review and refine">
    ```text theme={null}
    enhance the PR description with more context about the security improvements
    ```
  </Step>
</Steps>

When you create a PR using `gh pr create`, the session is automatically linked to that PR. To return to it later, run `claude --from-pr <number>` or paste the PR URL into the [`/resume` picker](/en/sessions#use-the-session-picker) search.

<Tip>
  Review Claude's generated PR before submitting and ask Claude to highlight potential risks or considerations.
</Tip>

### Handle documentation

Suppose you need to add or update documentation for your code.

<Steps>
  <Step title="Identify undocumented code">
    ```text theme={null}
    find functions without proper JSDoc comments in the auth module
    ```
  </Step>

  <Step title="Generate documentation">
    ```text theme={null}
    add JSDoc comments to the undocumented functions in auth.js
    ```
  </Step>

  <Step title="Review and enhance">
    ```text theme={null}
    improve the generated documentation with more context and examples
    ```
  </Step>

  <Step title="Verify documentation">
    ```text theme={null}
    check if the documentation follows our project standards
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Specify the documentation style you want (JSDoc, docstrings, etc.)
  * Ask for examples in the documentation
  * Request documentation for public APIs, interfaces, and complex logic
</Tip>

***

### Work in notes and non-code folders

Claude Code works in any directory. Run it inside a notes vault, a documentation folder, or any collection of markdown files to search, edit, and reorganize content the same way you would code.

The `.claude/` directory and `CLAUDE.md` sit alongside other tools' config directories without conflict. Claude reads files fresh on each tool call, so it sees edits you make in another application the next time it reads that file.

***

### Work with images

Suppose you need to work with images in your codebase, and you want Claude's help analyzing image content.

<Steps>
  <Step title="Add an image to the conversation">
    You can use any of these methods:

    1. Drag and drop an image into the Claude Code window
    2. Copy an image and paste it into the CLI with ctrl+v (Do not use cmd+v)
    3. Provide an image path to Claude. E.g., "Analyze this image: /path/to/your/image.png"
  </Step>

  <Step title="Ask Claude to analyze the image">
    ```text theme={null}
    What does this image show?
    ```

    ```text theme={null}
    Describe the UI elements in this screenshot
    ```

    ```text theme={null}
    Are there any problematic elements in this diagram?
    ```
  </Step>

  <Step title="Use images for context">
    ```text theme={null}
    Here's a screenshot of the error. What's causing it?
    ```

    ```text theme={null}
    This is our current database schema. How should we modify it for the new feature?
    ```
  </Step>

  <Step title="Get code suggestions from visual content">
    ```text theme={null}
    Generate CSS to match this design mockup
    ```

    ```text theme={null}
    What HTML structure would recreate this component?
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Use images when text descriptions would be unclear or cumbersome
  * Include screenshots of errors, UI designs, or diagrams for better context
  * You can work with multiple images in a conversation
  * Image analysis works with diagrams, screenshots, mockups, and more
  * When Claude references images (for example, `[Image #1]`), `Cmd+Click` (Mac) or `Ctrl+Click` (Windows/Linux) the link to open the image in your default viewer
</Tip>

***

### Reference files and directories

Use @ to quickly include files or directories without waiting for Claude to read them.

<Steps>
  <Step title="Reference a single file">
    ```text theme={null}
    Explain the logic in @src/utils/auth.js
    ```

    This includes the full content of the file in the conversation.
  </Step>

  <Step title="Reference a directory">
    ```text theme={null}
    What's the structure of @src/components?
    ```

    This provides a directory listing with file information.
  </Step>

  <Step title="Reference MCP resources">
    ```text theme={null}
    Show me the data from @github:repos/owner/repo/issues
    ```

    This fetches data from connected MCP servers using the format @server:resource. See [MCP resources](/en/mcp#use-mcp-resources) for details.
  </Step>
</Steps>

<Tip>
  Tips:

  * File paths can be relative or absolute
  * @ file references add `CLAUDE.md` in the file's directory and parent directories to context
  * Directory references show file listings, not contents
  * You can reference multiple files in a single message (for example, "@file1.js and @file2.js")
</Tip>

***

### Run Claude on a schedule

Suppose you want Claude to handle a task automatically on a recurring basis, like reviewing open PRs every morning, auditing dependencies weekly, or checking for CI failures overnight.

Pick a scheduling option based on where you want the task to run:

| Option                                                 | Where it runs                     | Best for                                                                                                                                                                                                 |
| :----------------------------------------------------- | :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Routines](/en/routines)                               | Anthropic-managed infrastructure  | Tasks that should run even when your computer is off. Can also trigger on API calls or GitHub events in addition to a schedule. Configure at [claude.ai/code/routines](https://claude.ai/code/routines). |
| [Desktop scheduled tasks](/en/desktop-scheduled-tasks) | Your machine, via the desktop app | Tasks that need direct access to local files, tools, or uncommitted changes.                                                                                                                             |
| [GitHub Actions](/en/github-actions)                   | Your CI pipeline                  | Tasks tied to repo events like opened PRs, or cron schedules that should live alongside your workflow config.                                                                                            |
| [`/loop`](/en/scheduled-tasks)                         | The current CLI session           | Quick polling while a session is open. Tasks stop when you start a new conversation; `--resume` and `--continue` restore unexpired ones.                                                                 |

<Tip>
  When writing prompts for scheduled tasks, be explicit about what success looks like and what to do with results. The task runs autonomously, so it can't ask clarifying questions. For example: "Review open PRs labeled `needs-review`, leave inline comments on any issues, and post a summary in the `#eng-reviews` Slack channel."
</Tip>

***

### Ask Claude about its capabilities

Claude has built-in access to its documentation and can answer questions about its own features and limitations.

#### Example questions

```text theme={null}
can Claude Code create pull requests?
```

```text theme={null}
how does Claude Code handle permissions?
```

```text theme={null}
what skills are available?
```

```text theme={null}
how do I use MCP with Claude Code?
```

```text theme={null}
how do I configure Claude Code for Amazon Bedrock?
```

```text theme={null}
what are the limitations of Claude Code?
```

<Note>
  Claude provides documentation-based answers to these questions. For hands-on demonstrations, run `/powerup` for interactive lessons with animated demos, or refer to the specific workflow sections above.
</Note>

<Tip>
  Tips:

  * Claude always has access to the latest Claude Code documentation, regardless of the version you're using
  * Ask specific questions to get detailed answers
  * Claude can explain complex features like MCP integration, enterprise configurations, and advanced workflows
</Tip>

***

## Resume previous conversations

When a task spans multiple sittings, pick up where you left off instead of re-explaining context. Claude Code saves every conversation locally.

```bash theme={null}
claude --continue
```

This resumes the most recent session in the current directory; if there isn't one yet, it prints `No conversation found to continue` and exits. Use `claude --resume` to choose from a list, or `/resume` from inside a running session. See [Manage sessions](/en/sessions) for naming, branching, and the full picker reference.

## Run parallel sessions with worktrees

Work on a feature in one terminal while Claude fixes a bug in another, without the edits colliding. Each worktree is a separate checkout on its own branch.

```bash theme={null}
claude --worktree feature-auth
```

Run the same command with a different name in a second terminal to start an isolated parallel session. See [Worktrees](/en/worktrees) for cleanup, `.worktreeinclude`, and non-git VCS support.

## Plan before editing

For changes you want to review before they touch disk, switch to plan mode. Claude reads files and proposes a plan but makes no edits until you approve.

```bash theme={null}
claude --permission-mode plan
```

You can also press `Shift+Tab` mid-session to toggle into plan mode. See [Plan mode](/en/permission-modes#analyze-before-you-edit-with-plan-mode) for the approval flow and editing the plan in your text editor.

## Delegate research to subagents

Exploring a large codebase fills your context with file reads. Delegate the exploration so only the findings come back.

```text theme={null}
use a subagent to investigate how our auth system handles token refresh
```

The subagent reads files in its own context window and reports a summary. See [Subagents](/en/sub-agents) for defining custom agents with their own tools and prompts.

## Pipe Claude into scripts

Run Claude non-interactively for CI, pre-commit hooks, or batch processing. Stdin and stdout work like any Unix tool.

```bash theme={null}
git log --oneline -20 | claude -p "summarize these recent commits"
```

See [Non-interactive mode](/en/headless) for output formats, permission flags, and fan-out patterns.

## Next steps

<CardGroup cols={2}>
  <Card title="Best practices" icon="lightbulb" href="/en/best-practices">
    Patterns for getting the most out of Claude Code
  </Card>

  <Card title="Manage sessions" icon="rotate-left" href="/en/sessions">
    Resume, name, and branch conversations
  </Card>

  <Card title="Worktrees" icon="code-branch" href="/en/worktrees">
    Run isolated parallel sessions
  </Card>

  <Card title="Extend Claude Code" icon="puzzle-piece" href="/en/features-overview">
    Add skills, hooks, MCP, subagents, and plugins
  </Card>
</CardGroup>


---

# Best practices for Claude Code

> Tips and patterns for getting the most out of Claude Code, from configuring your environment to scaling across parallel sessions.

Claude Code is an agentic coding environment. Unlike a chatbot that answers questions and waits, Claude Code can read your files, run commands, make changes, and autonomously work through problems while you watch, redirect, or step away entirely.

This changes how you work. Instead of writing code yourself and asking Claude to review it, you describe what you want and Claude figures out how to build it. Claude explores, plans, and implements.

But this autonomy still comes with a learning curve. Claude works within certain constraints you need to understand.

This guide covers patterns that have proven effective across Anthropic's internal teams and for engineers using Claude Code across various codebases, languages, and environments. For how the agentic loop works under the hood, see [How Claude Code works](/en/how-claude-code-works).

***

Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills.

Claude's context window holds your entire conversation, including every message, every file Claude reads, and every command output. However, this can fill up fast. A single debugging session or codebase exploration might generate and consume tens of thousands of tokens.

This matters since LLM performance degrades as context fills. When the context window is getting full, Claude may start "forgetting" earlier instructions or making more mistakes. The context window is the most important resource to manage. To see how a session fills up in practice, [watch an interactive walkthrough](/en/context-window) of what loads at startup and what each file read costs. Track context usage continuously with a [custom status line](/en/statusline), and see [Reduce token usage](/en/costs#reduce-token-usage) for strategies on reducing token usage.

***

## Give Claude a way to verify its work

<Tip>
  Include tests, screenshots, or expected outputs so Claude can check itself. This is the single highest-leverage thing you can do.
</Tip>

Claude performs dramatically better when it can verify its own work, like run tests, compare screenshots, and validate outputs.

Without clear success criteria, it might produce something that looks right but actually doesn't work. You become the only feedback loop, and every mistake requires your attention.

| Strategy                              | Before                                                  | After                                                                                                                                                                                                   |
| ------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Provide verification criteria**     | *"implement a function that validates email addresses"* | *"write a validateEmail function. example test cases: [user@example.com](mailto:user@example.com) is true, invalid is false, [user@.com](mailto:user@.com) is false. run the tests after implementing"* |
| **Verify UI changes visually**        | *"make the dashboard look better"*                      | *"\[paste screenshot] implement this design. take a screenshot of the result and compare it to the original. list differences and fix them"*                                                            |
| **Address root causes, not symptoms** | *"the build is failing"*                                | *"the build fails with this error: \[paste error]. fix it and verify the build succeeds. address the root cause, don't suppress the error"*                                                             |

UI changes can be verified using the [Claude in Chrome extension](/en/chrome). It opens new tabs in your browser, tests the UI, and iterates until the code works.

Your verification can also be a test suite, a linter, or a Bash command that checks output. Invest in making your verification rock-solid.

***

## Explore first, then plan, then code

<Tip>
  Separate research and planning from implementation to avoid solving the wrong problem.
</Tip>

Letting Claude jump straight to coding can produce code that solves the wrong problem. Use [plan mode](/en/permission-modes#analyze-before-you-edit-with-plan-mode) to separate exploration from execution.

The recommended workflow has four phases:

<Steps>
  <Step title="Explore">
    Enter plan mode. Claude reads files and answers questions without making changes.

    ```txt claude (plan mode) theme={null}
    read /src/auth and understand how we handle sessions and login.
    also look at how we manage environment variables for secrets.
    ```
  </Step>

  <Step title="Plan">
    Ask Claude to create a detailed implementation plan.

    ```txt claude (plan mode) theme={null}
    I want to add Google OAuth. What files need to change?
    What's the session flow? Create a plan.
    ```

    Press `Ctrl+G` to open the plan in your text editor for direct editing before Claude proceeds.
  </Step>

  <Step title="Implement">
    Switch out of plan mode and let Claude code, verifying against its plan.

    ```txt claude (default mode) theme={null}
    implement the OAuth flow from your plan. write tests for the
    callback handler, run the test suite and fix any failures.
    ```
  </Step>

  <Step title="Commit">
    Ask Claude to commit with a descriptive message and create a PR.

    ```txt claude (default mode) theme={null}
    commit with a descriptive message and open a PR
    ```
  </Step>
</Steps>

<Callout>
  Plan mode is useful, but also adds overhead.

  For tasks where the scope is clear and the fix is small (like fixing a typo, adding a log line, or renaming a variable) ask Claude to do it directly.

  Planning is most useful when you're uncertain about the approach, when the change modifies multiple files, or when you're unfamiliar with the code being modified. If you could describe the diff in one sentence, skip the plan.
</Callout>

***

## Provide specific context in your prompts

<Tip>
  The more precise your instructions, the fewer corrections you'll need.
</Tip>

Claude can infer intent, but it can't read your mind. Reference specific files, mention constraints, and point to example patterns.

| Strategy                                                                                         | Before                                               | After                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------ | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Scope the task.** Specify which file, what scenario, and testing preferences.                  | *"add tests for foo.py"*                             | *"write a test for foo.py covering the edge case where the user is logged out. avoid mocks."*                                                                                                                                                                                                                                                                    |
| **Point to sources.** Direct Claude to the source that can answer a question.                    | *"why does ExecutionFactory have such a weird api?"* | *"look through ExecutionFactory's git history and summarize how its api came to be"*                                                                                                                                                                                                                                                                             |
| **Reference existing patterns.** Point Claude to patterns in your codebase.                      | *"add a calendar widget"*                            | *"look at how existing widgets are implemented on the home page to understand the patterns. HotDogWidget.php is a good example. follow the pattern to implement a new calendar widget that lets the user select a month and paginate forwards/backwards to pick a year. build from scratch without libraries other than the ones already used in the codebase."* |
| **Describe the symptom.** Provide the symptom, the likely location, and what "fixed" looks like. | *"fix the login bug"*                                | *"users report that login fails after session timeout. check the auth flow in src/auth/, especially token refresh. write a failing test that reproduces the issue, then fix it"*                                                                                                                                                                                 |

Vague prompts can be useful when you're exploring and can afford to course-correct. A prompt like `"what would you improve in this file?"` can surface things you wouldn't have thought to ask about.

### Provide rich content

<Tip>
  Use `@` to reference files, paste screenshots/images, or pipe data directly.
</Tip>

You can provide rich data to Claude in several ways:

* **Reference files with `@`** instead of describing where code lives. Claude reads the file before responding.
* **Paste images directly**. Copy/paste or drag and drop images into the prompt.
* **Give URLs** for documentation and API references. Use `/permissions` to allowlist frequently-used domains.
* **Pipe in data** by running `cat error.log | claude` to send file contents directly.
* **Let Claude fetch what it needs**. Tell Claude to pull context itself using Bash commands, MCP tools, or by reading files.

***

## Configure your environment

A few setup steps make Claude Code significantly more effective across all your sessions. For a full overview of extension features and when to use each one, see [Extend Claude Code](/en/features-overview).

### Write an effective CLAUDE.md

<Tip>
  Run `/init` to generate a starter CLAUDE.md file based on your current project structure, then refine over time.
</Tip>

CLAUDE.md is a special file that Claude reads at the start of every conversation. Include Bash commands, code style, and workflow rules. This gives Claude persistent context it can't infer from code alone.

The `/init` command analyzes your codebase to detect build systems, test frameworks, and code patterns, giving you a solid foundation to refine.

There's no required format for CLAUDE.md files, but keep it short and human-readable. For example:

```markdown CLAUDE.md theme={null}
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

CLAUDE.md is loaded every session, so only include things that apply broadly. For domain knowledge or workflows that are only relevant sometimes, use [skills](/en/skills) instead. Claude loads them on demand without bloating every conversation.

Keep it concise. For each line, ask: *"Would removing this cause Claude to make mistakes?"* If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!

| ✅ Include                                            | ❌ Exclude                                          |
| ---------------------------------------------------- | -------------------------------------------------- |
| Bash commands Claude can't guess                     | Anything Claude can figure out by reading code     |
| Code style rules that differ from defaults           | Standard language conventions Claude already knows |
| Testing instructions and preferred test runners      | Detailed API documentation (link to docs instead)  |
| Repository etiquette (branch naming, PR conventions) | Information that changes frequently                |
| Architectural decisions specific to your project     | Long explanations or tutorials                     |
| Developer environment quirks (required env vars)     | File-by-file descriptions of the codebase          |
| Common gotchas or non-obvious behaviors              | Self-evident practices like "write clean code"     |

If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost. If Claude asks you questions that are answered in CLAUDE.md, the phrasing might be ambiguous. Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts.

You can tune instructions by adding emphasis (e.g., "IMPORTANT" or "YOU MUST") to improve adherence. Check CLAUDE.md into git so your team can contribute. The file compounds in value over time.

CLAUDE.md files can import additional files using `@path/to/import` syntax:

```markdown CLAUDE.md theme={null}
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

You can place CLAUDE.md files in several locations:

* **Home folder (`~/.claude/CLAUDE.md`)**: applies to all Claude sessions
* **Project root (`./CLAUDE.md`)**: check into git to share with your team
* **Project root (`./CLAUDE.local.md`)**: personal project-specific notes; add this file to your `.gitignore` so it isn't shared with your team
* **Parent directories**: useful for monorepos where both `root/CLAUDE.md` and `root/foo/CLAUDE.md` are pulled in automatically
* **Child directories**: Claude pulls in child CLAUDE.md files on demand when working with files in those directories

### Configure permissions

<Tip>
  Use [auto mode](/en/permission-modes#eliminate-prompts-with-auto-mode) to let a classifier handle approvals, `/permissions` to allowlist specific commands, or `/sandbox` for OS-level isolation. Each reduces interruptions while keeping you in control.
</Tip>

By default, Claude Code requests permission for actions that might modify your system: file writes, Bash commands, MCP tools, etc. This is safe but tedious. After the tenth approval you're not really reviewing anymore, you're just clicking through. There are three ways to reduce these interruptions:

* **Auto mode**: a separate classifier model reviews commands and blocks only what looks risky: scope escalation, unknown infrastructure, or hostile-content-driven actions. Best when you trust the general direction of a task but don't want to click through every step
* **Permission allowlists**: permit specific tools you know are safe, like `npm run lint` or `git commit`
* **Sandboxing**: enable OS-level isolation that restricts filesystem and network access, allowing Claude to work more freely within defined boundaries

Read more about [permission modes](/en/permission-modes), [permission rules](/en/permissions), and [sandboxing](/en/sandboxing).

### Use CLI tools

<Tip>
  Tell Claude Code to use CLI tools like `gh`, `aws`, `gcloud`, and `sentry-cli` when interacting with external services.
</Tip>

CLI tools are the most context-efficient way to interact with external services. If you use GitHub, install the `gh` CLI. Claude knows how to use it for creating issues, opening pull requests, and reading comments. Without `gh`, Claude can still use the GitHub API, but unauthenticated requests often hit rate limits.

Claude is also effective at learning CLI tools it doesn't already know. Try prompts like `Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.`

### Connect MCP servers

<Tip>
  Run `claude mcp add` to connect external tools like Notion, Figma, or your database.
</Tip>

With [MCP servers](/en/mcp), you can ask Claude to implement features from issue trackers, query databases, analyze monitoring data, integrate designs from Figma, and automate workflows.

### Set up hooks

<Tip>
  Use hooks for actions that must happen every time with zero exceptions.
</Tip>

[Hooks](/en/hooks-guide) run scripts automatically at specific points in Claude's workflow. Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens.

Claude can write hooks for you. Try prompts like *"Write a hook that runs eslint after every file edit"* or *"Write a hook that blocks writes to the migrations folder."* Edit `.claude/settings.json` directly to configure hooks by hand, and run `/hooks` to browse what's configured.

### Create skills

<Tip>
  Create `SKILL.md` files in `.claude/skills/` to give Claude domain knowledge and reusable workflows.
</Tip>

[Skills](/en/skills) extend Claude's knowledge with information specific to your project, team, or domain. Claude applies them automatically when relevant, or you can invoke them directly with `/skill-name`.

Create a skill by adding a directory with a `SKILL.md` to `.claude/skills/`:

```markdown .claude/skills/api-conventions/SKILL.md theme={null}
---
name: api-conventions
description: REST API design conventions for our services
---
# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

Skills can also define repeatable workflows you invoke directly:

```markdown .claude/skills/fix-issue/SKILL.md theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

Run `/fix-issue 1234` to invoke it. Use `disable-model-invocation: true` for workflows with side effects that you want to trigger manually.

### Create custom subagents

<Tip>
  Define specialized assistants in `.claude/agents/` that Claude can delegate to for isolated tasks.
</Tip>

[Subagents](/en/sub-agents) run in their own context with their own set of allowed tools. They're useful for tasks that read many files or need specialized focus without cluttering your main conversation.

```markdown .claude/agents/security-reviewer.md theme={null}
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

Tell Claude to use subagents explicitly: *"Use a subagent to review this code for security issues."*

### Install plugins

<Tip>
  Run `/plugin` to browse the marketplace. Plugins add skills, tools, and integrations without configuration.
</Tip>

[Plugins](/en/plugins) bundle skills, hooks, subagents, and MCP servers into a single installable unit from the community and Anthropic. If you work with a typed language, install a [code intelligence plugin](/en/discover-plugins#code-intelligence) to give Claude precise symbol navigation and automatic error detection after edits.

For guidance on choosing between skills, subagents, hooks, and MCP, see [Extend Claude Code](/en/features-overview#match-features-to-your-goal).

***

## Communicate effectively

The way you communicate with Claude Code significantly impacts the quality of results.

### Ask codebase questions

<Tip>
  Ask Claude questions you'd ask a senior engineer.
</Tip>

When onboarding to a new codebase, use Claude Code for learning and exploration. You can ask Claude the same sorts of questions you would ask another engineer:

* How does logging work?
* How do I make a new API endpoint?
* What does `async move { ... }` do on line 134 of `foo.rs`?
* What edge cases does `CustomerOnboardingFlowImpl` handle?
* Why does this code call `foo()` instead of `bar()` on line 333?

Using Claude Code this way is an effective onboarding workflow, improving ramp-up time and reducing load on other engineers. No special prompting required: ask questions directly.

### Let Claude interview you

<Tip>
  For larger features, have Claude interview you first. Start with a minimal prompt and ask Claude to interview you using the `AskUserQuestion` tool.
</Tip>

Claude asks about things you might not have considered yet, including technical implementation, UI/UX, edge cases, and tradeoffs.

```text theme={null}
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

Once the spec is complete, start a fresh session to execute it. The new session has clean context focused entirely on implementation, and you have a written spec to reference.

***

## Manage your session

Conversations are persistent and reversible. Use this to your advantage!

### Course-correct early and often

<Tip>
  Correct Claude as soon as you notice it going off track.
</Tip>

The best results come from tight feedback loops. Though Claude occasionally solves problems perfectly on the first attempt, correcting it quickly generally produces better solutions faster.

* **`Esc`**: stop Claude mid-action with the `Esc` key. Context is preserved, so you can redirect.
* **`Esc + Esc` or `/rewind`**: press `Esc` twice or run `/rewind` to open the rewind menu and restore previous conversation and code state, or summarize from a selected message.
* **`"Undo that"`**: have Claude revert its changes.
* **`/clear`**: reset context between unrelated tasks. Long sessions with irrelevant context can reduce performance.

If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run `/clear` and start fresh with a more specific prompt that incorporates what you learned. A clean session with a better prompt almost always outperforms a long session with accumulated corrections.

### Manage context aggressively

<Tip>
  Run `/clear` between unrelated tasks to reset context.
</Tip>

Claude Code automatically compacts conversation history when you approach context limits, which preserves important code and decisions while freeing space.

During long sessions, Claude's context window can fill with irrelevant conversation, file contents, and commands. This can reduce performance and sometimes distract Claude.

* Use `/clear` frequently between tasks to reset the context window entirely
* When auto compaction triggers, Claude summarizes what matters most, including code patterns, file states, and key decisions
* For more control, run `/compact <instructions>`, like `/compact Focus on the API changes`
* To compact only part of the conversation, use `Esc + Esc` or `/rewind`, select a message checkpoint, and choose **Summarize from here**. This condenses messages from that point forward while keeping earlier context intact.
* Customize compaction behavior in CLAUDE.md with instructions like `"When compacting, always preserve the full list of modified files and any test commands"` to ensure critical context survives summarization
* For quick questions that don't need to stay in context, use [`/btw`](/en/interactive-mode#side-questions-with-%2Fbtw). The answer appears in a dismissible overlay and never enters conversation history, so you can check a detail without growing context.

### Use subagents for investigation

<Tip>
  Delegate research with `"use subagents to investigate X"`. They explore in a separate context, keeping your main conversation clean for implementation.
</Tip>

Since context is your fundamental constraint, subagents are one of the most powerful tools available. When Claude researches a codebase it reads lots of files, all of which consume your context. Subagents run in separate context windows and report back summaries:

```text theme={null}
Use subagents to investigate how our authentication system handles token
refresh, and whether we have any existing OAuth utilities I should reuse.
```

The subagent explores the codebase, reads relevant files, and reports back with findings, all without cluttering your main conversation.

You can also use subagents for verification after Claude implements something:

```text theme={null}
use a subagent to review this code for edge cases
```

### Rewind with checkpoints

<Tip>
  Every action Claude makes creates a checkpoint. You can restore conversation, code, or both to any previous checkpoint.
</Tip>

Claude automatically checkpoints before changes. Double-tap `Escape` or run `/rewind` to open the rewind menu. You can restore conversation only, restore code only, restore both, or summarize from a selected message. See [Checkpointing](/en/checkpointing) for details.

Instead of carefully planning every move, you can tell Claude to try something risky. If it doesn't work, rewind and try a different approach. Checkpoints persist across sessions, so you can close your terminal and still rewind later.

<Warning>
  Checkpoints only track changes made *by Claude*, not external processes. This isn't a replacement for git.
</Warning>

### Resume conversations

<Tip>
  Name sessions with `/rename` and treat them like branches: each workstream gets its own persistent context.
</Tip>

Claude Code saves conversations locally, so when a task spans multiple sittings you don't have to re-explain the context. Run `claude --continue` to pick up the most recent session, or `claude --resume` to choose from a list. Give sessions descriptive names like `oauth-migration` so you can find them later. See [Manage sessions](/en/sessions) for the full set of resume, branch, and naming controls.

***

## Automate and scale

Once you're effective with one Claude, multiply your output with parallel sessions, non-interactive mode, and fan-out patterns.

Everything so far assumes one human, one Claude, and one conversation. But Claude Code scales horizontally. The techniques in this section show how you can get more done.

### Run non-interactive mode

<Tip>
  Use `claude -p "prompt"` in CI, pre-commit hooks, or scripts. Add `--output-format stream-json` for streaming JSON output.
</Tip>

With `claude -p "your prompt"`, you can run Claude non-interactively, without a session. [Non-interactive mode](/en/headless) is how you integrate Claude into CI pipelines, pre-commit hooks, or any automated workflow. The output formats let you parse results programmatically: plain text, JSON, or streaming JSON.

```bash theme={null}
# One-off queries
claude -p "Explain what this project does"

# Structured output for scripts
claude -p "List all API endpoints" --output-format json

# Streaming for real-time processing
claude -p "Analyze this log file" --output-format stream-json
```

### Run multiple Claude sessions

<Tip>
  Run multiple Claude sessions in parallel to speed up development, run isolated experiments, or start complex workflows.
</Tip>

Pick the parallel approach that fits how much coordination you want to do yourself:

* [Worktrees](/en/worktrees): run separate CLI sessions in isolated git checkouts so edits don't collide
* [Desktop app](/en/desktop#work-in-parallel-with-sessions): manage multiple local sessions visually, each in its own worktree
* [Claude Code on the web](/en/claude-code-on-the-web): run sessions on Anthropic-managed cloud infrastructure in isolated VMs
* [Agent teams](/en/agent-teams): automated coordination of multiple sessions with shared tasks, messaging, and a team lead

Beyond parallelizing work, multiple sessions enable quality-focused workflows. A fresh context improves code review since Claude won't be biased toward code it just wrote.

For example, use a Writer/Reviewer pattern:

| Session A (Writer)                                                      | Session B (Reviewer)                                                                                                                                                     |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Implement a rate limiter for our API endpoints`                        |                                                                                                                                                                          |
|                                                                         | `Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases, race conditions, and consistency with our existing middleware patterns.` |
| `Here's the review feedback: [Session B output]. Address these issues.` |                                                                                                                                                                          |

You can do something similar with tests: have one Claude write tests, then another write code to pass them.

### Fan out across files

<Tip>
  Loop through tasks calling `claude -p` for each. Use `--allowedTools` to scope permissions for batch operations.
</Tip>

For large migrations or analyses, you can distribute work across many parallel Claude invocations:

<Steps>
  <Step title="Generate a task list">
    Have Claude list all files that need migrating (e.g., `list all 2,000 Python files that need migrating`)
  </Step>

  <Step title="Write a script to loop through the list">
    ```bash theme={null}
    for file in $(cat files.txt); do
      claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
        --allowedTools "Edit,Bash(git commit *)"
    done
    ```
  </Step>

  <Step title="Test on a few files, then run at scale">
    Refine your prompt based on what goes wrong with the first 2-3 files, then run on the full set. The `--allowedTools` flag restricts what Claude can do, which matters when you're running unattended.
  </Step>
</Steps>

You can also integrate Claude into existing data/processing pipelines:

```bash theme={null}
claude -p "<your prompt>" --output-format json | your_command
```

Use `--verbose` for debugging during development, and turn it off in production.

### Run autonomously with auto mode

For uninterrupted execution with background safety checks, use [auto mode](/en/permission-modes#eliminate-prompts-with-auto-mode). A classifier model reviews commands before they run, blocking scope escalation, unknown infrastructure, and hostile-content-driven actions while letting routine work proceed without prompts.

```bash theme={null}
claude --permission-mode auto -p "fix all lint errors"
```

For non-interactive runs with the `-p` flag, auto mode aborts if the classifier repeatedly blocks actions, since there is no user to fall back to. See [when auto mode falls back](/en/permission-modes#when-auto-mode-falls-back) for thresholds.

***

## Avoid common failure patterns

These are common mistakes. Recognizing them early saves time:

* **The kitchen sink session.** You start with one task, then ask Claude something unrelated, then go back to the first task. Context is full of irrelevant information.
  > **Fix**: `/clear` between unrelated tasks.
* **Correcting over and over.** Claude does something wrong, you correct it, it's still wrong, you correct again. Context is polluted with failed approaches.
  > **Fix**: After two failed corrections, `/clear` and write a better initial prompt incorporating what you learned.
* **The over-specified CLAUDE.md.** If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise.
  > **Fix**: Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook.
* **The trust-then-verify gap.** Claude produces a plausible-looking implementation that doesn't handle edge cases.
  > **Fix**: Always provide verification (tests, scripts, screenshots). If you can't verify it, don't ship it.
* **The infinite exploration.** You ask Claude to "investigate" something without scoping it. Claude reads hundreds of files, filling the context.
  > **Fix**: Scope investigations narrowly or use subagents so the exploration doesn't consume your main context.

***

## Develop your intuition

The patterns in this guide aren't set in stone. They're starting points that work well in general, but might not be optimal for every situation.

Sometimes you *should* let context accumulate because you're deep in one complex problem and the history is valuable. Sometimes you should skip planning and let Claude figure it out because the task is exploratory. Sometimes a vague prompt is exactly right because you want to see how Claude interprets the problem before constraining it.

Pay attention to what works. When Claude produces great output, notice what you did: the prompt structure, the context you provided, the mode you were in. When Claude struggles, ask why. Was the context too noisy? The prompt too vague? The task too big for one pass?

Over time, you'll develop intuition that no guide can capture. You'll know when to be specific and when to be open-ended, when to plan and when to explore, when to clear context and when to let it accumulate.

## Related resources

* [How Claude Code works](/en/how-claude-code-works): the agentic loop, tools, and context management
* [Extend Claude Code](/en/features-overview): skills, hooks, MCP, subagents, and plugins
* [Common workflows](/en/common-workflows): step-by-step recipes for debugging, testing, PRs, and more
* [CLAUDE.md](/en/memory): store project conventions and persistent context


---

# How Claude remembers your project

> Give Claude persistent instructions with CLAUDE.md files, and let Claude accumulate learnings automatically with auto memory.

Each Claude Code session begins with a fresh context window. Two mechanisms carry knowledge across sessions:

* **CLAUDE.md files**: instructions you write to give Claude persistent context
* **Auto memory**: notes Claude writes itself based on your corrections and preferences

This page covers how to:

* [Write and organize CLAUDE.md files](#claude-md-files)
* [Scope rules to specific file types](#organize-rules-with-claude/rules/) with `.claude/rules/`
* [Configure auto memory](#auto-memory) so Claude takes notes automatically
* [Troubleshoot](#troubleshoot-memory-issues) when instructions aren't being followed

## CLAUDE.md vs auto memory

Claude Code has two complementary memory systems. Both are loaded at the start of every conversation. Claude treats them as context, not enforced configuration. The more specific and concise your instructions, the more consistently Claude follows them.

|                      | CLAUDE.md files                                   | Auto memory                                                      |
| :------------------- | :------------------------------------------------ | :--------------------------------------------------------------- |
| **Who writes it**    | You                                               | Claude                                                           |
| **What it contains** | Instructions and rules                            | Learnings and patterns                                           |
| **Scope**            | Project, user, or org                             | Per working tree                                                 |
| **Loaded into**      | Every session                                     | Every session (first 200 lines or 25KB)                          |
| **Use for**          | Coding standards, workflows, project architecture | Build commands, debugging insights, preferences Claude discovers |

Use CLAUDE.md files when you want to guide Claude's behavior. Auto memory lets Claude learn from your corrections without manual effort.

Subagents can also maintain their own auto memory. See [subagent configuration](/en/sub-agents#enable-persistent-memory) for details.

## CLAUDE.md files

CLAUDE.md files are markdown files that give Claude persistent instructions for a project, your personal workflow, or your entire organization. You write these files in plain text; Claude reads them at the start of every session.

### When to add to CLAUDE.md

Treat CLAUDE.md as the place you write down what you'd otherwise re-explain. Add to it when:

* Claude makes the same mistake a second time
* A code review catches something Claude should have known about this codebase
* You type the same correction or clarification into chat that you typed last session
* A new teammate would need the same context to be productive

Keep it to facts Claude should hold in every session: build commands, conventions, project layout, "always do X" rules. If an entry is a multi-step procedure or only matters for one part of the codebase, move it to a [skill](/en/skills) or a [path-scoped rule](#organize-rules-with-claude/rules/) instead. The [extension overview](/en/features-overview#build-your-setup-over-time) covers when to use each mechanism.

### Choose where to put CLAUDE.md files

CLAUDE.md files can live in several locations, each with a different scope. More specific locations take precedence over broader ones.

| Scope                    | Location                                                                                                                                                                | Purpose                                                    | Use case examples                                                    | Shared with                     |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------- |
| **Managed policy**       | • macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />• Linux and WSL: `/etc/claude-code/CLAUDE.md`<br />• Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Organization-wide instructions managed by IT/DevOps        | Company coding standards, security policies, compliance requirements | All users in organization       |
| **Project instructions** | `./CLAUDE.md` or `./.claude/CLAUDE.md`                                                                                                                                  | Team-shared instructions for the project                   | Project architecture, coding standards, common workflows             | Team members via source control |
| **User instructions**    | `~/.claude/CLAUDE.md`                                                                                                                                                   | Personal preferences for all projects                      | Code styling preferences, personal tooling shortcuts                 | Just you (all projects)         |
| **Local instructions**   | `./CLAUDE.local.md`                                                                                                                                                     | Personal project-specific preferences; add to `.gitignore` | Your sandbox URLs, preferred test data                               | Just you (current project)      |

CLAUDE.md and CLAUDE.local.md files in the directory hierarchy above the working directory are loaded in full at launch. Files in subdirectories load on demand when Claude reads files in those directories. See [How CLAUDE.md files load](#how-claude-md-files-load) for the full resolution order.

For large projects, you can break instructions into topic-specific files using [project rules](#organize-rules-with-claude/rules/). Rules let you scope instructions to specific file types or subdirectories.

### Set up a project CLAUDE.md

A project CLAUDE.md can be stored in either `./CLAUDE.md` or `./.claude/CLAUDE.md`. Create this file and add instructions that apply to anyone working on the project: build and test commands, coding standards, architectural decisions, naming conventions, and common workflows. These instructions are shared with your team through version control, so focus on project-level standards rather than personal preferences.

<Tip>
  Run `/init` to generate a starting CLAUDE.md automatically. Claude analyzes your codebase and creates a file with build commands, test instructions, and project conventions it discovers. If a CLAUDE.md already exists, `/init` suggests improvements rather than overwriting it. Refine from there with instructions Claude wouldn't discover on its own.

  Set `CLAUDE_CODE_NEW_INIT=1` to enable an interactive multi-phase flow. `/init` asks which artifacts to set up: CLAUDE.md files, skills, and hooks. It then explores your codebase with a subagent, fills in gaps via follow-up questions, and presents a reviewable proposal before writing any files.
</Tip>

### Write effective instructions

CLAUDE.md files are loaded into the context window at the start of every session, consuming tokens alongside your conversation. The [context window visualization](/en/context-window) shows where CLAUDE.md loads relative to the rest of the startup context. Because they're context rather than enforced configuration, how you write instructions affects how reliably Claude follows them. Specific, concise, well-structured instructions work best.

**Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence. If your instructions are growing large, use [path-scoped rules](#path-specific-rules) so instructions load only when Claude works with matching files. You can also split content into [imports](#import-additional-files) for organization, though imported files still load and enter the context window at launch.

**Structure**: use markdown headers and bullets to group related instructions. Claude scans structure the same way readers do: organized sections are easier to follow than dense paragraphs.

**Specificity**: write instructions that are concrete enough to verify. For example:

* "Use 2-space indentation" instead of "Format code properly"
* "Run `npm test` before committing" instead of "Test your changes"
* "API handlers live in `src/api/handlers/`" instead of "Keep files organized"

**Consistency**: if two rules contradict each other, Claude may pick one arbitrarily. Review your CLAUDE.md files, nested CLAUDE.md files in subdirectories, and [`.claude/rules/`](#organize-rules-with-claude/rules/) periodically to remove outdated or conflicting instructions. In monorepos, use [`claudeMdExcludes`](#exclude-specific-claude-md-files) to skip CLAUDE.md files from other teams that aren't relevant to your work.

### Import additional files

CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them.

Both relative and absolute paths are allowed. Relative paths resolve relative to the file containing the import, not the working directory. Imported files can recursively import other files, with a maximum depth of five hops.

To pull in a README, package.json, and a workflow guide, reference them with `@` syntax anywhere in your CLAUDE.md:

```text theme={null}
See @README for project overview and @package.json for available npm commands for this project.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

For private per-project preferences that shouldn't be checked into version control, create a `CLAUDE.local.md` at the project root. It loads alongside `CLAUDE.md` and is treated the same way. Add `CLAUDE.local.md` to your `.gitignore` so it isn't committed; running `/init` and choosing the personal option does this for you.

If you work across multiple git worktrees of the same repository, a gitignored `CLAUDE.local.md` only exists in the worktree where you created it. To share personal instructions across worktrees, import a file from your home directory instead:

```text theme={null}
# Individual Preferences
- @~/.claude/my-project-instructions.md
```

<Warning>
  The first time Claude Code encounters external imports in a project, it shows an approval dialog listing the files. If you decline, the imports stay disabled and the dialog does not appear again.
</Warning>

For a more structured approach to organizing instructions, see [`.claude/rules/`](#organize-rules-with-claude/rules/).

### AGENTS.md

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If your repository already uses `AGENTS.md` for other coding agents, create a `CLAUDE.md` that imports it so both tools read the same instructions without duplicating them. You can also add Claude-specific instructions below the import. Claude loads the imported file at session start, then appends the rest:

```markdown CLAUDE.md theme={null}
@AGENTS.md

## Claude Code

Use plan mode for changes under `src/billing/`.
```

A symlink also works if you don't need to add Claude-specific content:

```bash theme={null}
ln -s AGENTS.md CLAUDE.md
```

On Windows, creating a symlink requires Administrator privileges or Developer Mode, so use the `@AGENTS.md` import instead.

Running [`/init`](/en/commands) in a repo that already has an `AGENTS.md` reads it and incorporates the relevant parts into the generated `CLAUDE.md`. It also reads other tool configs like `.cursorrules` and `.windsurfrules`.

### How CLAUDE.md files load

Claude Code reads CLAUDE.md files by walking up the directory tree from your current working directory, checking each directory along the way for `CLAUDE.md` and `CLAUDE.local.md` files. This means if you run Claude Code in `foo/bar/`, it loads instructions from `foo/bar/CLAUDE.md`, `foo/CLAUDE.md`, and any `CLAUDE.local.md` files alongside them.

All discovered files are concatenated into context rather than overriding each other. Across the directory tree, content is ordered from the filesystem root down to your working directory. For the `foo/bar/` example, `foo/CLAUDE.md` appears in context before `foo/bar/CLAUDE.md`, so instructions closer to where you launched Claude are read last. Within each directory, `CLAUDE.local.md` is appended after `CLAUDE.md`, so your personal notes are the last thing Claude reads at that level.

Claude also discovers `CLAUDE.md` and `CLAUDE.local.md` files in subdirectories under your current working directory. Instead of loading them at launch, they are included when Claude reads files in those subdirectories.

If you work in a large monorepo where other teams' CLAUDE.md files get picked up, use [`claudeMdExcludes`](#exclude-specific-claude-md-files) to skip them.

Block-level HTML comments (`<!-- maintainer notes -->`) in CLAUDE.md files are stripped before the content is injected into Claude's context. Use them to leave notes for human maintainers without spending context tokens on them. Comments inside code blocks are preserved. When you open a CLAUDE.md file directly with the Read tool, comments remain visible.

#### Load from additional directories

The `--add-dir` flag gives Claude access to additional directories outside your main working directory. By default, CLAUDE.md files from these directories are not loaded.

To also load memory files from additional directories, set the `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` environment variable:

```bash theme={null}
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

This loads `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md`, and `CLAUDE.local.md` from the additional directory. `CLAUDE.local.md` is skipped if you exclude `local` from [`--setting-sources`](/en/cli-reference).

### Organize rules with `.claude/rules/`

For larger projects, you can organize instructions into multiple files using the `.claude/rules/` directory. This keeps instructions modular and easier for teams to maintain. Rules can also be [scoped to specific file paths](#path-specific-rules), so they only load into context when Claude works with matching files, reducing noise and saving context space.

<Note>
  Rules load into context every session or when matching files are opened. For task-specific instructions that don't need to be in context all the time, use [skills](/en/skills) instead, which only load when you invoke them or when Claude determines they're relevant to your prompt.
</Note>

#### Set up rules

Place markdown files in your project's `.claude/rules/` directory. Each file should cover one topic, with a descriptive filename like `testing.md` or `api-design.md`. All `.md` files are discovered recursively, so you can organize rules into subdirectories like `frontend/` or `backend/`:

```text theme={null}
your-project/
├── .claude/
│   ├── CLAUDE.md           # Main project instructions
│   └── rules/
│       ├── code-style.md   # Code style guidelines
│       ├── testing.md      # Testing conventions
│       └── security.md     # Security requirements
```

Rules without [`paths` frontmatter](#path-specific-rules) are loaded at launch with the same priority as `.claude/CLAUDE.md`.

#### Path-specific rules

Rules can be scoped to specific files using YAML frontmatter with the `paths` field. These conditional rules only apply when Claude is working with files matching the specified patterns.

```markdown theme={null}
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
- Include OpenAPI documentation comments
```

Rules without a `paths` field are loaded unconditionally and apply to all files. Path-scoped rules trigger when Claude reads files matching the pattern, not on every tool use.

Use glob patterns in the `paths` field to match files by extension, directory, or any combination:

| Pattern                | Matches                                  |
| ---------------------- | ---------------------------------------- |
| `**/*.ts`              | All TypeScript files in any directory    |
| `src/**/*`             | All files under `src/` directory         |
| `*.md`                 | Markdown files in the project root       |
| `src/components/*.tsx` | React components in a specific directory |

You can specify multiple patterns and use brace expansion to match multiple extensions in one pattern:

```markdown theme={null}
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

#### Share rules across projects with symlinks

The `.claude/rules/` directory supports symlinks, so you can maintain a shared set of rules and link them into multiple projects. Symlinks are resolved and loaded normally, and circular symlinks are detected and handled gracefully.

This example links both a shared directory and an individual file:

```bash theme={null}
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

#### User-level rules

Personal rules in `~/.claude/rules/` apply to every project on your machine. Use them for preferences that aren't project-specific:

```text theme={null}
~/.claude/rules/
├── preferences.md    # Your personal coding preferences
└── workflows.md      # Your preferred workflows
```

User-level rules are loaded before project rules, giving project rules higher priority.

### Manage CLAUDE.md for large teams

For organizations deploying Claude Code across teams, you can centralize instructions and control which CLAUDE.md files are loaded.

#### Deploy organization-wide CLAUDE.md

Organizations can deploy a centrally managed CLAUDE.md that applies to all users on a machine. This file cannot be excluded by individual settings.

<Steps>
  <Step title="Create the file at the managed policy location">
    * macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
    * Linux and WSL: `/etc/claude-code/CLAUDE.md`
    * Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`
  </Step>

  <Step title="Deploy with your configuration management system">
    Use MDM, Group Policy, Ansible, or similar tools to distribute the file across developer machines. See [managed settings](/en/permissions#managed-settings) for other organization-wide configuration options.
  </Step>
</Steps>

A managed CLAUDE.md and [managed settings](/en/settings#settings-files) serve different purposes. Use settings for technical enforcement and CLAUDE.md for behavioral guidance:

| Concern                                        | Configure in                                              |
| :--------------------------------------------- | :-------------------------------------------------------- |
| Block specific tools, commands, or file paths  | Managed settings: `permissions.deny`                      |
| Enforce sandbox isolation                      | Managed settings: `sandbox.enabled`                       |
| Environment variables and API provider routing | Managed settings: `env`                                   |
| Authentication method and organization lock    | Managed settings: `forceLoginMethod`, `forceLoginOrgUUID` |
| Code style and quality guidelines              | Managed CLAUDE.md                                         |
| Data handling and compliance reminders         | Managed CLAUDE.md                                         |
| Behavioral instructions for Claude             | Managed CLAUDE.md                                         |

Settings rules are enforced by the client regardless of what Claude decides to do. CLAUDE.md instructions shape Claude's behavior but are not a hard enforcement layer.

#### Exclude specific CLAUDE.md files

In large monorepos, ancestor CLAUDE.md files may contain instructions that aren't relevant to your work. The `claudeMdExcludes` setting lets you skip specific files by path or glob pattern.

This example excludes a top-level CLAUDE.md and a rules directory from a parent folder. Add it to `.claude/settings.local.json` so the exclusion stays local to your machine:

```json theme={null}
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Patterns are matched against absolute file paths using glob syntax. You can configure `claudeMdExcludes` at any [settings layer](/en/settings#settings-files): user, project, local, or managed policy. Arrays merge across layers.

Managed policy CLAUDE.md files cannot be excluded. This ensures organization-wide instructions always apply regardless of individual settings.

## Auto memory

Auto memory lets Claude accumulate knowledge across sessions without you writing anything. Claude saves notes for itself as it works: build commands, debugging insights, architecture notes, code style preferences, and workflow habits. Claude doesn't save something every session. It decides what's worth remembering based on whether the information would be useful in a future conversation.

<Note>
  Auto memory requires Claude Code v2.1.59 or later. Check your version with `claude --version`.
</Note>

### Enable or disable auto memory

Auto memory is on by default. To toggle it, open `/memory` in a session and use the auto memory toggle, or set `autoMemoryEnabled` in your project settings:

```json theme={null}
{
  "autoMemoryEnabled": false
}
```

To disable auto memory via environment variable, set `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

### Storage location

Each project gets its own memory directory at `~/.claude/projects/<project>/memory/`. The `<project>` path is derived from the git repository, so all worktrees and subdirectories within the same repo share one auto memory directory. Outside a git repo, the project root is used instead.

To store auto memory in a different location, set `autoMemoryDirectory` in your user settings at `~/.claude/settings.json`:

```json theme={null}
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

The value must be an absolute path or start with `~/`. This setting is accepted from policy and user settings, and from the `--settings` flag. It is not accepted from project or local settings, since both files live inside the project directory and a cloned repository could supply either to redirect auto memory writes to sensitive locations.

The directory contains a `MEMORY.md` entrypoint and optional topic files:

```text theme={null}
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index, loaded into every session
├── debugging.md       # Detailed notes on debugging patterns
├── api-conventions.md # API design decisions
└── ...                # Any other topic files Claude creates
```

`MEMORY.md` acts as an index of the memory directory. Claude reads and writes files in this directory throughout your session, using `MEMORY.md` to keep track of what's stored where.

Auto memory is machine-local. All worktrees and subdirectories within the same git repository share one auto memory directory. Files are not shared across machines or cloud environments.

### How it works

The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start. Claude keeps `MEMORY.md` concise by moving detailed notes into separate topic files.

This limit applies only to `MEMORY.md`. CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence.

Topic files like `debugging.md` or `patterns.md` are not loaded at startup. Claude reads them on demand using its standard file tools when it needs the information.

Claude reads and writes memory files during your session. When you see "Writing memory" or "Recalled memory" in the Claude Code interface, Claude is actively updating or reading from `~/.claude/projects/<project>/memory/`.

### Audit and edit your memory

Auto memory files are plain markdown you can edit or delete at any time. Run [`/memory`](#view-and-edit-with-memory) to browse and open memory files from within a session.

## View and edit with `/memory`

The `/memory` command lists all CLAUDE.md, CLAUDE.local.md, and rules files loaded in your current session, lets you toggle auto memory on or off, and provides a link to open the auto memory folder. Select any file to open it in your editor.

When you ask Claude to remember something, like "always use pnpm, not npm" or "remember that the API tests require a local Redis instance," Claude saves it to auto memory. To add instructions to CLAUDE.md instead, ask Claude directly, like "add this to CLAUDE.md," or edit the file yourself via `/memory`.

## Troubleshoot memory issues

These are the most common issues with CLAUDE.md and auto memory, along with steps to debug them.

### Claude isn't following my CLAUDE.md

CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. Claude reads it and tries to follow it, but there's no guarantee of strict compliance, especially for vague or conflicting instructions.

To debug:

* Run `/memory` to verify your CLAUDE.md and CLAUDE.local.md files are being loaded. If a file isn't listed, Claude can't see it.
* Check that the relevant CLAUDE.md is in a location that gets loaded for your session (see [Choose where to put CLAUDE.md files](#choose-where-to-put-claude-md-files)).
* Make instructions more specific. "Use 2-space indentation" works better than "format code nicely."
* Look for conflicting instructions across CLAUDE.md files. If two files give different guidance for the same behavior, Claude may pick one arbitrarily.

If the instruction is something that must run at a specific point, such as before every commit or after each file edit, write it as a [hook](/en/hooks-guide) instead. Hooks execute as shell commands at fixed lifecycle events and apply regardless of what Claude decides to do.

For instructions you want at the system prompt level, use [`--append-system-prompt`](/en/cli-reference#system-prompt-flags). This must be passed every invocation, so it's better suited to scripts and automation than interactive use.

<Tip>
  Use the [`InstructionsLoaded` hook](/en/hooks#instructionsloaded) to log exactly which instruction files are loaded, when they load, and why. This is useful for debugging path-specific rules or lazy-loaded files in subdirectories.
</Tip>

### I don't know what auto memory saved

Run `/memory` and select the auto memory folder to browse what Claude has saved. Everything is plain markdown you can read, edit, or delete.

### My CLAUDE.md is too large

Files over 200 lines consume more context and may reduce adherence. Use [path-scoped rules](#path-specific-rules) to load instructions only when Claude works with matching files, or trim content that isn't needed in every session. Splitting into [`@path` imports](#import-additional-files) helps organization but does not reduce context, since imported files load at launch.

### Instructions seem lost after `/compact`

Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it into the session. Nested CLAUDE.md files in subdirectories are not re-injected automatically; they reload the next time Claude reads a file in that subdirectory.

If an instruction disappeared after compaction, it was either given only in conversation or lives in a nested CLAUDE.md that hasn't reloaded yet. Add conversation-only instructions to CLAUDE.md to make them persist. See [What survives compaction](/en/context-window#what-survives-compaction) for the full breakdown.

See [Write effective instructions](#write-effective-instructions) for guidance on size, structure, and specificity.

## Related resources

* [Debug your configuration](/en/debug-your-config): diagnose why CLAUDE.md or settings aren't taking effect
* [Skills](/en/skills): package repeatable workflows that load on demand
* [Settings](/en/settings): configure Claude Code behavior with settings files
* [Subagent memory](/en/sub-agents#enable-persistent-memory): let subagents maintain their own auto memory


---

# 探索 .claude 目錄

> Claude Code 讀取 CLAUDE.md、settings.json、hooks、skills、commands、subagents、rules 和自動記憶的位置。探索您專案中的 .claude 目錄和主目錄中的 ~/.claude。

export const ClaudeExplorer = () => {
  const A = useMemo(() => ({href, children}) => <a href={href} style={{
    color: 'var(--ce-accent)',
    textDecoration: 'none',
    borderBottom: '1px dotted var(--ce-accent)'
  }}>{children}</a>, []);
  const C = useMemo(() => ({children}) => <code style={{
    fontFamily: 'var(--ce-mono)',
    fontSize: '0.92em',
    padding: '1px 4px',
    borderRadius: '3px',
    background: 'var(--ce-surface)',
    border: '0.5px solid var(--ce-border-subtle)'
  }}>{children}</code>, []);
  const commandsNote = useMemo(() => <>Commands and skills are now the same mechanism. For new workflows, use <A href="/en/skills">skills/</A> instead: same <C>/name</C> invocation, plus you can bundle supporting files.</>, []);
  const FILE_TREE = useMemo(() => ({
    project: {
      label: 'your-project/',
      children: [{
        id: 'claude-md',
        label: 'CLAUDE.md',
        type: 'file',
        icon: 'md',
        color: '#6A9BCC',
        badge: 'committed',
        oneLiner: 'Project instructions Claude reads every session',
        when: 'Loaded into context at the start of every session',
        description: 'Project-specific instructions that shape how Claude works in this repository. Put your conventions, common commands, and architectural context here so Claude operates with the same assumptions your team does.',
        tips: ['Target under 200 lines. Longer files still load in full but may reduce adherence', <>CLAUDE.md loads into every session. If something only matters for specific tasks, move it to a <A href="/en/skills">skill</A> or a path-scoped <A href="/en/memory#organize-rules-with-claude/rules/">rule</A> so it loads only when needed</>, 'List the commands you run most, like build, test, and format, so Claude knows them without you spelling them out each time', <>Run <C>/memory</C> to open and edit CLAUDE.md from within a session</>, <>Also works at <C>.claude/CLAUDE.md</C> if you prefer to keep the project root clean</>],
        exampleIntro: 'This example is for a TypeScript and React project. It lists the build and test commands, the framework conventions Claude should follow, and project-specific rules like export style and file layout.',
        example: `# Project conventions

## Commands
- Build: \`npm run build\`
- Test: \`npm test\`
- Lint: \`npm run lint\`

## Stack
- TypeScript with strict mode
- React 19, functional components only

## Rules
- Named exports, never default exports
- Tests live next to source: \`foo.ts\` -> \`foo.test.ts\`
- All API routes return \`{ data, error }\` shape`,
        docsLink: '/en/memory'
      }, {
        id: 'mcp-json',
        label: '.mcp.json',
        type: 'file',
        icon: 'json',
        color: '#9B7BC4',
        badge: 'committed',
        oneLiner: 'Project-scoped MCP servers, shared with your team',
        when: <>Servers connect when the session begins. Tool schemas are deferred by default and load on demand via <A href="/en/mcp#scale-with-mcp-tool-search">tool search</A></>,
        description: <>Configures Model Context Protocol (MCP) servers that give Claude access to external tools: databases, APIs, browsers, and more. This file holds the project-scoped servers your whole team uses. Personal servers you want to keep to yourself go in <C>~/.claude.json</C> instead.</>,
        tips: [<>Use environment variable references for secrets: <C>{'${GITHUB_TOKEN}'}</C></>, <>Lives at the project root, not inside <C>.claude/</C></>, <>For servers only you need, run <C>claude mcp add --scope user</C>. This writes to <C>~/.claude.json</C> instead of <C>.mcp.json</C></>],
        exampleIntro: <>This example configures the GitHub MCP server so Claude can read issues and open pull requests. The <C>{'${GITHUB_TOKEN}'}</C> reference is read from your shell environment when Claude Code starts the server, so the token never lands in the file.</>,
        example: `{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "\${GITHUB_TOKEN}"
      }
    }
  }
}`,
        docsLink: '/en/mcp'
      }, {
        id: 'worktreeinclude',
        label: '.worktreeinclude',
        type: 'file',
        icon: 'md',
        color: '#8FA876',
        badge: 'committed',
        oneLiner: 'Gitignored files to copy into new worktrees',
        when: <>Read when Claude creates a git worktree via <C>--worktree</C>, the <C>EnterWorktree</C> tool, or subagent <C>isolation: worktree</C></>,
        description: <>Lists gitignored files to copy from your main repository into each new worktree. Worktrees are fresh checkouts, so untracked files like <C>.env</C> are missing by default. Patterns here use <C>.gitignore</C> syntax. Only files that match a pattern and are also gitignored get copied, so tracked files are never duplicated.</>,
        tips: [<>Lives at the project root, not inside <C>.claude/</C></>, <>Git-only: if you configure a <A href="/en/hooks#worktreecreate">WorktreeCreate hook</A> for a different VCS, this file is not read. Copy files inside your hook script instead</>, <>Also applies to parallel sessions in the <A href="/en/desktop#work-in-parallel-with-sessions">desktop app</A></>],
        exampleIntro: 'This example copies your local environment files and a secrets config into every worktree Claude creates. Comments start with # and blank lines are ignored, same as .gitignore.',
        example: `# Local environment
.env
.env.local

# API credentials
config/secrets.json`,
        docsLink: '/en/worktrees#copy-gitignored-files-into-worktrees'
      }, {
        id: 'dot-claude',
        label: '.claude/',
        type: 'folder',
        icon: 'folder',
        color: 'var(--ce-accent)',
        oneLiner: 'Project-level configuration, rules, and extensions',
        description: 'Everything Claude Code reads that is specific to this project. If you use git, commit most files here so your team shares them; a few, like settings.local.json, are automatically gitignored. Each file badge shows which.',
        children: [{
          id: 'settings-json',
          label: 'settings.json',
          type: 'file',
          icon: 'json',
          color: 'var(--ce-text-3)',
          badge: 'committed',
          oneLiner: 'Permissions, hooks, and configuration',
          when: <>Overrides global <C>~/.claude/settings.json</C>. Local settings, CLI flags, and managed settings override this</>,
          description: 'Settings that Claude Code applies directly. Permissions control which commands and tools Claude can use; hooks run your scripts at specific points in a session. Unlike CLAUDE.md, which Claude reads as guidance, these are enforced whether Claude follows them or not.',
          contains: [<><A href="/en/permissions">permissions</A>: allow, deny, or prompt before Claude uses specific tools or commands</>, <><A href="/en/hooks">hooks</A>: run your own scripts on events like before a tool call or after a file edit</>, <><A href="/en/statusline">statusLine</A>: customize the line shown at the bottom while Claude works</>, <><A href="/en/settings#available-settings">model</A>: pick a default model for this project</>, <><A href="/en/settings#environment-variables">env</A>: environment variables set in every session</>, <><A href="/en/output-styles">outputStyle</A>: select a custom system-prompt style from output-styles/</>],
          tips: [<>Bash permission patterns support wildcards: <C>Bash(npm test *)</C> matches any command starting with <C>npm test</C></>, <>Array settings like <C>permissions.allow</C> combine across all scopes; scalar settings like <C>model</C> use the most specific value</>],
          exampleIntro: <>This example allows <C>npm test</C> and <C>npm run</C> commands without prompting, blocks <C>rm -rf</C>, and runs Prettier on files after Claude edits or writes them.</>,
          example: `{
  "permissions": {
    "allow": [
      "Bash(npm test *)",
      "Bash(npm run *)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  },
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
      }]
    }]
  }
}`,
          docsLink: '/en/settings'
        }, {
          id: 'settings-local-json',
          label: 'settings.local.json',
          type: 'file',
          icon: 'json',
          color: 'var(--ce-text-3)',
          badge: 'gitignored',
          oneLiner: 'Your personal settings overrides for this project',
          when: 'Highest of the user-editable settings files; CLI flags and managed settings still take precedence',
          description: 'Personal settings that take precedence over the project defaults. Same JSON format as settings.json, but not committed. Use this when you need different permissions or defaults than the team config.',
          tips: [<>Same schema as settings.json. Array settings like <C>permissions.allow</C> combine across scopes; scalar settings like <C>model</C> use the local value</>, <>Claude Code adds this file to <C>~/.config/git/ignore</C> the first time it writes one. If you use a custom <C>core.excludesFile</C>, add the pattern there too. To share the ignore rule with your team, also add it to the project <C>.gitignore</C></>],
          exampleIntro: 'This example adds Docker permissions on top of whatever the team settings.json allows.',
          example: `{
  "permissions": {
    "allow": [
      "Bash(docker *)"
    ]
  }
}`,
          docsLink: '/en/settings'
        }, {
          id: 'rules',
          label: 'rules/',
          type: 'folder',
          icon: 'folder',
          color: '#9B7BC4',
          oneLiner: 'Topic-scoped instructions, optionally gated by file paths',
          when: <>Rules without <C>paths:</C> load at session start. Rules with <C>paths:</C> load when a matching file enters context</>,
          description: [<>Project instructions split into topic files that can load conditionally based on file paths. A rule without <C>paths:</C> frontmatter loads at session start like CLAUDE.md; a rule with <C>paths:</C> loads only when Claude reads a matching file.</>, <>Like CLAUDE.md, rules are guidance Claude reads, not configuration Claude Code enforces. For guaranteed behavior use <A href="/en/hooks">hooks</A> or <A href="/en/permissions">permissions</A>.</>],
          tips: [<>Use <C>paths:</C> frontmatter with globs to scope rules to directories or file types</>, <>Subdirectories work: <C>.claude/rules/frontend/react.md</C> is discovered automatically</>, 'When CLAUDE.md approaches 200 lines, start splitting into rules'],
          docsLink: '/en/memory#organize-rules-with-claude/rules/',
          children: [{
            id: 'rule-testing',
            label: 'testing.md',
            type: 'file',
            icon: 'md',
            color: '#9B7BC4',
            badge: 'committed',
            oneLiner: 'Test conventions scoped to test files',
            when: <>Loaded when Claude reads a file matching the <C>paths:</C> globs below</>,
            description: <>An example rule that only loads when Claude is working on test files. The <C>paths:</C> globs in the frontmatter define which files trigger it; here, anything ending in .test.ts or .test.tsx. For other files, this rule is not loaded into context.</>,
            example: `---
paths:
  - "**/*.test.ts"
  - "**/*.test.tsx"
---

# Testing Rules

- Use descriptive test names: "should [expected] when [condition]"
- Mock external dependencies, not internal modules
- Clean up side effects in afterEach`
          }, {
            id: 'rule-api',
            label: 'api-design.md',
            type: 'file',
            icon: 'md',
            color: '#9B7BC4',
            badge: 'committed',
            oneLiner: 'API conventions scoped to backend code',
            when: <>Loaded when Claude reads a file matching the <C>paths:</C> glob below</>,
            description: <>A second example showing a rule scoped to backend code. The <C>paths:</C> glob matches files under src/api/, so these conventions load only when Claude is editing API routes.</>,
            example: `---
paths:
  - "src/api/**/*.ts"
---

# API Design Rules

- All endpoints must validate input with Zod schemas
- Return shape: { data: T } | { error: string }
- Rate limit all public endpoints`
          }]
        }, {
          id: 'skills',
          label: 'skills/',
          type: 'folder',
          icon: 'folder',
          color: '#D4A843',
          oneLiner: 'Reusable prompts you or Claude invoke by name',
          when: <>Invoked with <C>/skill-name</C> or when Claude matches the task to a skill</>,
          description: <>Each skill is a folder with a SKILL.md file plus any supporting files it needs. By default, both you and Claude can invoke a skill. Use frontmatter to control that: <C>disable-model-invocation: true</C> for user-only workflows like <C>/deploy</C>, or <C>user-invocable: false</C> to hide from the <C>/</C> menu while Claude can still invoke it.</>,
          tips: [<>Skills accept arguments: <C>/deploy staging</C> passes "staging" as <C>$ARGUMENTS</C>. Use <C>$0</C>, <C>$1</C>, and so on for positional access</>, <>The <C>description</C> frontmatter determines when Claude auto-invokes the skill</>, 'Bundle reference docs alongside SKILL.md. Claude knows the skill directory path and can read supporting files when you mention them'],
          docsLink: '/en/skills',
          children: [{
            id: 'skill-review',
            label: 'security-review/',
            type: 'folder',
            icon: 'folder',
            color: '#D4A843',
            oneLiner: 'A skill bundling SKILL.md with supporting files',
            children: [{
              id: 'skill-review-md',
              label: 'SKILL.md',
              type: 'file',
              icon: 'md',
              color: '#D4A843',
              badge: 'committed',
              oneLiner: 'Entrypoint: trigger, invocability, instructions',
              when: <>User types <C>/security-review &lt;target&gt;</C>; Claude cannot auto-invoke this skill</>,
              description: [<>This skill uses <C>disable-model-invocation: true</C> so only you can trigger it; Claude never invokes it on its own.</>, <>The <C>!`...`</C> line runs a shell command and injects its output into the prompt. <C>$ARGUMENTS</C> substitutes whatever you typed after the skill name. Claude sees the skill directory path, so mentioning a bundled file like checklist.md lets Claude read it.</>],
              example: `---
description: Reviews code changes for security vulnerabilities, authentication gaps, and injection risks
disable-model-invocation: true
argument-hint: <branch-or-path>
---

## Diff to review

!\`git diff $ARGUMENTS\`

Audit the changes above for:

1. Injection vulnerabilities (SQL, XSS, command)
2. Authentication and authorization gaps
3. Hardcoded secrets or credentials

Use checklist.md in this skill directory for the full review checklist.

Report findings with severity ratings and remediation steps.`
            }, {
              id: 'skill-checklist',
              label: 'checklist.md',
              type: 'file',
              icon: 'md',
              color: '#D4A843',
              badge: 'committed',
              oneLiner: 'Supporting file bundled with the skill',
              when: 'Claude reads it on demand while running the skill',
              description: <>Skills can bundle any supporting files: reference docs, templates, scripts. The skill directory path is prepended to SKILL.md, so Claude can read bundled files by name. For scripts in bash injection commands, use the <C>{'${CLAUDE_SKILL_DIR}'}</C> placeholder.</>,
              example: `# Security Review Checklist

## Input Validation
- [ ] All user input sanitized before DB queries
- [ ] File upload MIME types validated
- [ ] Path traversal prevented on file operations

## Authentication
- [ ] JWT tokens expire after 24 hours
- [ ] API keys stored in environment variables
- [ ] Passwords hashed with bcrypt or argon2`
            }]
          }]
        }, {
          id: 'commands',
          label: 'commands/',
          type: 'folder',
          icon: 'folder',
          color: '#788C5D',
          oneLiner: <>Single-file prompts invoked with <C>/name</C></>,
          note: commandsNote,
          when: <>User types <C>/command-name</C></>,
          description: <>A file at <C>commands/deploy.md</C> creates <C>/deploy</C> the same way a skill at <C>skills/deploy/SKILL.md</C> does, and both can be auto-invoked by Claude. Skills use a directory with SKILL.md, letting you bundle reference docs, templates, or scripts alongside the prompt.</>,
          tips: [<>Use <C>$ARGUMENTS</C> in the file to accept parameters: <C>/fix-issue 123</C></>, 'If a skill and command share a name, the skill takes precedence', 'New commands should usually be skills instead; commands remain supported'],
          docsLink: '/en/skills',
          children: [{
            id: 'cmd-example',
            label: 'fix-issue.md',
            type: 'file',
            icon: 'md',
            color: '#788C5D',
            badge: 'committed',
            oneLiner: <>Invoked as <C>/fix-issue &lt;number&gt;</C></>,
            note: commandsNote,
            description: [<>An example command for fixing a GitHub issue. Type <C>/fix-issue 123</C> and the <C>!`...`</C> line runs <C>gh issue view 123</C> in your shell, injecting the output into the prompt before Claude sees it.</>, <><C>$ARGUMENTS</C> substitutes whatever you typed after the command name. For positional access, use <C>$0</C> <C>$1</C> and so on.</>],
            example: `---
argument-hint: <issue-number>
---

!\`gh issue view $ARGUMENTS\`

Investigate and fix the issue above.

1. Trace the bug to its root cause
2. Implement the fix
3. Write or update tests
4. Summarize what you changed and why`
          }]
        }, {
          id: 'output-styles',
          label: 'output-styles/',
          type: 'folder',
          icon: 'folder',
          color: '#5AA7A7',
          oneLiner: 'Project-scoped output styles, if your team shares any',
          when: 'Applied at session start when selected via the outputStyle setting',
          description: <>Output styles are usually personal, so most live in <C>~/.claude/output-styles/</C>. Put one here if your team shares a style, like a review mode everyone uses. See <A href="#ce-global-output-styles">the Global tab</A> for the full explanation and example.</>,
          docsLink: '/en/output-styles',
          children: []
        }, {
          id: 'agents',
          label: 'agents/',
          type: 'folder',
          icon: 'folder',
          color: '#C46686',
          oneLiner: 'Specialized subagents with their own context window',
          when: 'Runs in its own context window when you or Claude invoke it',
          description: 'Each markdown file defines a subagent with its own system prompt, tool access, and optionally its own model. Subagents run in a fresh context window, keeping the main conversation clean. Useful for parallel work or isolated tasks.',
          tips: ['Each agent gets a fresh context window, separate from your main session', <>Restrict tool access per agent with the <C>tools:</C> frontmatter field</>, 'Type @ and pick an agent from the autocomplete to delegate directly'],
          docsLink: '/en/sub-agents',
          children: [{
            id: 'agent-reviewer',
            label: 'code-reviewer.md',
            type: 'file',
            icon: 'md',
            color: '#C46686',
            badge: 'committed',
            oneLiner: 'Subagent for isolated code review',
            when: 'Claude spawns it for review tasks, or you @-mention it from the autocomplete',
            description: <>An example subagent restricted to read-only tools. The <C>description</C> frontmatter tells Claude when to delegate to it automatically; <C>tools:</C> limits it to Read, Grep, and Glob so it can inspect code but never edit. The body becomes the subagent's system prompt.</>,
            example: `---
name: code-reviewer
description: Reviews code for correctness, security, and maintainability
tools: Read, Grep, Glob
---

You are a senior code reviewer. Review for:

1. Correctness: logic errors, edge cases, null handling
2. Security: injection, auth bypass, data exposure
3. Maintainability: naming, complexity, duplication

Every finding must include a concrete fix.`
          }]
        }, {
          id: 'agent-memory',
          label: 'agent-memory/',
          type: 'folder',
          icon: 'folder',
          color: '#C46686',
          badge: 'committed',
          autogen: true,
          oneLiner: 'Subagent persistent memory, separate from your main session auto memory',
          when: 'First 200 lines (capped at 25KB) of MEMORY.md loaded into the subagent system prompt when it runs',
          description: <>Subagents with <C>memory: project</C> in their frontmatter get a dedicated memory directory here. This is distinct from your <A href="/en/memory#auto-memory">main session auto memory</A> at <C>~/.claude/projects/</C>: each subagent reads and writes its own MEMORY.md, not yours.</>,
          tips: [<>Only created for subagents that set the <C>memory:</C> frontmatter field</>, <>This directory holds project-scoped subagent memory, meant to be shared with your team. To keep memory out of version control use <C>memory: local</C>, which writes to <C>.claude/agent-memory-local/</C> instead. For cross-project memory use <C>memory: user</C>, which writes to <C>~/.claude/agent-memory/</C></>, <>The main session auto memory is a different feature; see <C>~/.claude/projects/</C> in the Global tab</>],
          docsLink: '/en/sub-agents#enable-persistent-memory',
          children: [{
            id: 'agent-memory-sub',
            label: '<agent-name>/',
            type: 'folder',
            icon: 'folder',
            color: '#C46686',
            autogen: true,
            children: [{
              id: 'agent-memory-md',
              label: 'MEMORY.md',
              type: 'file',
              icon: 'md',
              color: '#C46686',
              badge: 'committed',
              autogen: true,
              oneLiner: 'The subagent writes and maintains this file automatically',
              when: 'Loaded into the subagent system prompt when the subagent starts',
              description: <>Works the same as your <A href="/en/memory#auto-memory">main auto memory</A>: the subagent creates and updates this file itself. You do not write it. The subagent reads it at the start of each task and writes back what it learns.</>,
              example: `# code-reviewer memory

## Patterns seen
- Project uses custom Result<T, E> type, not exceptions
- Auth middleware expects Bearer token in Authorization header
- Tests use factory functions in test/factories/

## Recurring issues
- Missing null checks on API responses (src/api/*)
- Unhandled promise rejections in background jobs`
            }]
          }]
        }]
      }]
    },
    global: {
      label: '~/',
      children: [{
        id: 'claude-json',
        label: '.claude.json',
        type: 'file',
        icon: 'json',
        color: 'var(--ce-text-3)',
        badge: 'local',
        oneLiner: 'App state and UI preferences',
        when: <>Read at session start for your preferences and MCP servers. Claude Code writes back to it when you change settings in <C>/config</C> or approve trust prompts</>,
        description: <>Holds state that does not belong in settings.json: theme, OAuth session, per-project trust decisions, your personal MCP servers, and UI toggles. Mostly managed through <C>/config</C> rather than editing directly.</>,
        tips: [<>IDE toggles like <C>autoConnectIde</C> and <C>externalEditorContext</C> live here, not in settings.json</>, <>The <C>projects</C> key tracks per-project state like trust-dialog acceptance and last-session metrics. Permission rules you approve in-session go to <C>.claude/settings.local.json</C> instead</>, <>MCP servers here are yours only: user scope applies across all projects, local scope is per-project but not committed. Team-shared servers go in <C>.mcp.json</C> at the project root instead</>],
        example: `{
  "autoConnectIde": true,
  "externalEditorContext": true,
  "mcpServers": {
    "my-tools": {
      "command": "npx",
      "args": ["-y", "@example/mcp-server"]
    }
  }
}`,
        docsLink: '/en/settings#global-config-settings'
      }, {
        id: 'global-dot-claude',
        label: '.claude/',
        type: 'folder',
        icon: 'folder',
        color: 'var(--ce-accent)',
        oneLiner: 'Your personal configuration across all projects',
        description: 'The global counterpart to your project .claude/ directory. Files here apply to every project you work in and are never committed to any repository.',
        children: [{
          id: 'global-claude-md',
          label: 'CLAUDE.md',
          type: 'file',
          icon: 'md',
          color: '#6A9BCC',
          badge: 'local',
          oneLiner: 'Personal preferences across every project',
          when: 'Loaded at the start of every session, in every project',
          description: 'Your global instruction file. Loaded alongside the project CLAUDE.md at session start, so both are in context together. When instructions conflict, project-level instructions take priority. Keep this to preferences that apply everywhere: response style, commit format, personal conventions.',
          tips: ['Keep it short since it loads into context for every project, alongside that project\'s own CLAUDE.md', 'Good for response style, commit format, and personal conventions'],
          example: `# Global preferences

- Keep explanations concise
- Use conventional commit format
- Show the terminal command to verify changes
- Prefer composition over inheritance`,
          docsLink: '/en/memory'
        }, {
          id: 'global-settings',
          label: 'settings.json',
          type: 'file',
          icon: 'json',
          color: 'var(--ce-text-3)',
          badge: 'local',
          oneLiner: 'Default settings for all projects',
          when: 'Your defaults. Project and local settings.json override any keys you also set there',
          description: [<>Same keys as project <C>settings.json</C>: permissions, hooks, model, environment variables, and the rest. Put settings here that you want in every project, like permissions you always allow, a preferred model, or a notification hook that runs regardless of which project you're in.</>, <>Settings follow a precedence order: project <C>settings.json</C> overrides any matching keys you set here. This is different from CLAUDE.md, where global and project files are both loaded into context rather than merged key by key.</>],
          example: `{
  "permissions": {
    "allow": [
      "Bash(git log *)",
      "Bash(git diff *)"
    ]
  }
}`,
          docsLink: '/en/settings'
        }, {
          id: 'keybindings',
          label: 'keybindings.json',
          type: 'file',
          icon: 'json',
          color: 'var(--ce-text-3)',
          badge: 'local',
          oneLiner: 'Custom keyboard shortcuts',
          when: 'Read at session start and hot-reloaded when you edit the file',
          description: <>Rebind keyboard shortcuts in the interactive CLI. Run <C>/keybindings</C> to create or open this file with a schema reference. Ctrl+C, Ctrl+D, Ctrl+M, and Caps Lock are reserved and cannot be rebound.</>,
          exampleIntro: <>This example binds <C>Ctrl+E</C> to open your external editor and unbinds <C>Ctrl+U</C> by setting it to <C>null</C>. The <C>context</C> field scopes bindings to a specific part of the CLI, here the main chat input.</>,
          example: `{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/en/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}`,
          docsLink: '/en/keybindings'
        }, {
          id: 'themes',
          label: 'themes/',
          type: 'folder',
          icon: 'folder',
          color: '#5AA7A7',
          oneLiner: 'Custom color themes',
          when: <>Read at session start and hot-reloaded when files change. Listed in <C>/theme</C></>,
          description: <>Each <C>.json</C> file defines a custom color theme: a built-in <C>base</C> preset plus an <C>overrides</C> map of color tokens. Create one interactively with <C>/theme</C> or write the JSON by hand. Selecting a custom theme stores <C>custom:&lt;slug&gt;</C> as your theme preference.</>,
          example: `{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}`,
          docsLink: '/en/terminal-config#create-a-custom-theme',
          children: []
        }, {
          id: 'global-projects',
          label: 'projects/',
          type: 'folder',
          icon: 'folder',
          color: '#E8A45C',
          autogen: true,
          oneLiner: "Auto memory: Claude's notes to itself, per project",
          when: 'MEMORY.md loaded at session start; topic files read on demand',
          description: 'Auto memory lets Claude accumulate knowledge across sessions without you writing anything. Claude saves notes as it works: build commands, debugging insights, architecture notes. Each project gets its own memory directory keyed by the repository path.',
          tips: [<>On by default. Toggle with <C>/memory</C> or <C>autoMemoryEnabled</C> in settings</>, 'MEMORY.md is the index loaded each session. The first 200 lines, or 25KB, whichever comes first, are read', 'Topic files like debugging.md are read on demand, not at startup', 'These are plain markdown. Edit or delete them anytime'],
          docsLink: '/en/memory#auto-memory',
          children: [{
            id: 'memory-dir',
            label: '<project>/memory/',
            type: 'folder',
            icon: 'folder',
            color: '#E8A45C',
            autogen: true,
            oneLiner: "Claude's accumulated knowledge for one project",
            children: [{
              id: 'memory-md',
              label: 'MEMORY.md',
              type: 'file',
              icon: 'md',
              color: '#E8A45C',
              badge: 'local',
              autogen: true,
              oneLiner: 'Claude writes and maintains this file automatically',
              when: 'First 200 lines (capped at 25KB) loaded at session start',
              description: 'Claude creates and updates this file as it works; you do not write it yourself. It acts as an index that Claude reads at the start of every session, pointing to topic files for detail. You can edit or delete it, but Claude will keep updating it.',
              example: `# Memory Index

## Project
- [build-and-test.md](build-and-test.md): npm run build (~45s), Vitest, dev server on 3001
- [architecture.md](architecture.md): API client singleton, refresh-token auth

## Reference
- [debugging.md](debugging.md): auth token rotation and DB connection troubleshooting`,
              docsLink: '/en/memory'
            }, {
              id: 'memory-topic',
              label: 'debugging.md',
              type: 'file',
              icon: 'md',
              color: '#E8A45C',
              badge: 'local',
              autogen: true,
              oneLiner: 'Topic notes Claude writes when MEMORY.md gets long',
              when: 'Claude reads this when a related task comes up',
              description: 'An example of a topic file Claude creates when MEMORY.md grows too long. Claude picks the filename based on what it splits out: debugging.md, architecture.md, build-commands.md, or similar. You never create these yourself. Claude reads a topic file back only when the current task relates to it.',
              example: `---
name: Debugging patterns
description: Auth token rotation and database connection troubleshooting for this project
type: reference
---

## Auth Token Issues
- Refresh token rotation: old token invalidated immediately
- If 401 after refresh: check clock skew between client and server

## Database Connection Drops
- Connection pool: max 10 in dev, 50 in prod
- Always check \`docker compose ps\` first`
            }]
          }]
        }, {
          id: 'global-rules',
          label: 'rules/',
          type: 'folder',
          icon: 'folder',
          color: '#9B7BC4',
          oneLiner: 'User-level rules that apply to every project',
          when: <>Rules without <C>paths:</C> load at session start. Rules with <C>paths:</C> load when a matching file enters context</>,
          description: 'Same as project .claude/rules/ but applies everywhere. Use this for conventions you want across all your work, like personal code style or commit message format.',
          docsLink: '/en/memory#organize-rules-with-claude/rules/',
          children: []
        }, {
          id: 'global-skills',
          label: 'skills/',
          type: 'folder',
          icon: 'folder',
          color: '#D4A843',
          oneLiner: 'Personal skills available in every project',
          when: <>Invoked with <C>/skill-name</C> in any project</>,
          description: 'Skills you built for yourself that work everywhere. Same structure as project skills: each is a folder with SKILL.md, scoped to your user account instead of a single project.',
          docsLink: '/en/skills',
          children: []
        }, {
          id: 'global-commands',
          label: 'commands/',
          type: 'folder',
          icon: 'folder',
          color: '#788C5D',
          oneLiner: 'Personal single-file commands available in every project',
          note: commandsNote,
          when: <>User types <C>/command-name</C> in any project</>,
          description: 'Same as project commands/ but scoped to your user account. Each markdown file becomes a command available everywhere.',
          docsLink: '/en/skills',
          children: []
        }, {
          id: 'global-output-styles',
          label: 'output-styles/',
          type: 'folder',
          icon: 'folder',
          color: '#5AA7A7',
          oneLiner: 'Custom system-prompt sections that adjust how Claude works',
          when: 'Applied at session start when selected via the outputStyle setting',
          description: [<>Each markdown file defines an output style: a section appended to the system prompt that, by default, also drops the built-in software-engineering task instructions. Use this to adapt Claude Code for uses beyond coding, or to add teaching or review modes.</>, <>Select a built-in or custom style with <C>/config</C> or the <C>outputStyle</C> key in settings. Styles here are available in every project; project-level styles with the same name take precedence.</>],
          tips: ['Built-in styles Explanatory and Learning are included with Claude Code; custom styles go here', <>Set <C>keep-coding-instructions: true</C> in frontmatter to keep the default task instructions alongside your additions</>, 'Changes take effect on the next session since the system prompt is fixed at startup for caching'],
          docsLink: '/en/output-styles',
          children: [{
            id: 'output-style-example',
            label: 'teaching.md',
            type: 'file',
            icon: 'md',
            color: '#5AA7A7',
            badge: 'local',
            oneLiner: 'Example style that adds explanations and leaves small changes for you',
            when: <>Active when <C>outputStyle</C> in settings is set to <C>teaching</C></>,
            description: <>This style appends instructions to the system prompt: Claude adds a "Why this approach" note after each task and leaves TODO(human) markers for changes under 10 lines instead of writing them itself. Select it by setting <C>outputStyle</C> to the filename without .md, or to the <C>name</C> field if you set one in frontmatter.</>,
            example: `---
description: Explains reasoning and asks you to implement small pieces
keep-coding-instructions: true
---

After completing each task, add a brief "Why this approach" note
explaining the key design decision.

When a change is under 10 lines, ask the user to implement it
themselves by leaving a TODO(human) marker instead of writing it.`
          }]
        }, {
          id: 'global-agents',
          label: 'agents/',
          type: 'folder',
          icon: 'folder',
          color: '#C46686',
          oneLiner: 'Personal subagents available in every project',
          when: 'Claude delegates or you @-mention in any project',
          description: 'Subagents defined here are available across all your projects. Same format as project agents.',
          docsLink: '/en/sub-agents',
          children: []
        }, {
          id: 'global-agent-memory',
          label: 'agent-memory/',
          type: 'folder',
          icon: 'folder',
          color: '#C46686',
          autogen: true,
          oneLiner: <>Persistent memory for subagents with <C>memory: user</C></>,
          when: 'Loaded into the subagent system prompt when the subagent starts',
          description: <>Subagents with <C>memory: user</C> in their frontmatter store knowledge here that persists across all projects. For project-scoped subagent memory, see <C>.claude/agent-memory/</C> instead.</>,
          docsLink: '/en/sub-agents#enable-persistent-memory',
          children: []
        }]
      }]
    }
  }), []);
  const BADGE_STYLES = useMemo(() => ({
    committed: {
      bg: 'rgba(85,138,66,0.08)',
      color: 'var(--ce-badge-committed)',
      border: 'rgba(85,138,66,0.15)',
      label: 'committed'
    },
    gitignored: {
      bg: 'rgba(217,119,87,0.06)',
      color: 'var(--ce-badge-gitignored)',
      border: 'rgba(217,119,87,0.15)',
      label: 'gitignored'
    },
    local: {
      bg: 'rgba(115,114,108,0.06)',
      color: 'var(--ce-badge-local)',
      border: 'rgba(115,114,108,0.12)',
      label: 'local only'
    },
    autogen: {
      bg: 'rgba(232,164,92,0.1)',
      color: 'var(--ce-badge-autogen)',
      border: 'rgba(232,164,92,0.2)',
      label: 'Claude writes'
    }
  }), []);
  const allNodes = useMemo(() => {
    const flatten = (nodes, acc, path, parentId) => {
      for (const node of nodes) {
        const nextPath = [...path, node.label];
        acc[node.id] = {
          ...node,
          path: nextPath,
          parentId
        };
        if (node.children) flatten(node.children, acc, nextPath, node.id);
      }
      return acc;
    };
    const project = flatten(FILE_TREE.project.children, {}, [FILE_TREE.project.label]);
    const global = flatten(FILE_TREE.global.children, {}, [FILE_TREE.global.label]);
    for (const id in project) project[id].root = 'project';
    for (const id in global) global[id].root = 'global';
    return {
      ...project,
      ...global
    };
  }, [FILE_TREE]);
  const allFolderIds = useMemo(() => Object.keys(allNodes).filter(id => allNodes[id].type === 'folder'), [allNodes]);
  const DEFAULT_EXPANDED = ['dot-claude', 'rules', 'skills', 'skill-review', 'commands', 'agents', 'agent-memory', 'agent-memory-sub', 'global-dot-claude', 'global-output-styles', 'global-projects', 'memory-dir'];
  const [mounted, setMounted] = useState(false);
  const [activeRoot, setActiveRoot] = useState('project');
  const [selectedId, setSelectedId] = useState('claude-md');
  const [expandedFolders, setExpandedFolders] = useState(() => new Set(DEFAULT_EXPANDED));
  const [forceMobile, setForceMobile] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const copyTimeoutRef = useRef(null);
  const rootRef = useRef(null);
  useEffect(() => {
    setMounted(true);
    const applyHash = scroll => {
      const hash = window.location.hash.slice(1);
      if (!hash.startsWith('ce-')) return;
      const id = hash.slice(3);
      const node = allNodes[id];
      if (!node) return;
      setActiveRoot(node.root);
      setSelectedId(id);
      setExpandedFolders(new Set(allFolderIds));
      if (scroll && rootRef.current) rootRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    };
    applyHash(false);
    const onHashChange = () => applyHash(true);
    const onFsChange = () => setIsFullscreen(!!document.fullscreenElement);
    window.addEventListener('hashchange', onHashChange);
    document.addEventListener('fullscreenchange', onFsChange);
    return () => {
      if (copyTimeoutRef.current) clearTimeout(copyTimeoutRef.current);
      window.removeEventListener('hashchange', onHashChange);
      document.removeEventListener('fullscreenchange', onFsChange);
    };
  }, []);
  useEffect(() => {
    if (!mounted || !rootRef.current) return;
    const hash = window.location.hash.slice(1);
    if (hash.startsWith('ce-') && allNodes[hash.slice(3)]) {
      rootRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  }, [mounted]);
  if (!mounted) return null;
  const selected = allNodes[selectedId];
  const tree = FILE_TREE[activeRoot];
  const isCopied = copiedId === selected.id;
  const toggleFolder = id => {
    const next = new Set(expandedFolders);
    next.has(id) ? next.delete(id) : next.add(id);
    setExpandedFolders(next);
  };
  const switchRoot = root => {
    if (root === activeRoot) return;
    setActiveRoot(root);
    const firstId = FILE_TREE[root].children[0].id;
    setSelectedId(firstId);
    try {
      history.replaceState(null, '', '#ce-' + firstId);
    } catch (e) {}
  };
  const toggleFullscreen = () => {
    if (!rootRef.current) return;
    if (document.fullscreenElement) document.exitFullscreen(); else rootRef.current.requestFullscreen().catch(() => {});
  };
  const selectNode = n => {
    setSelectedId(n.id);
    if (n.type === 'folder' && !expandedFolders.has(n.id)) toggleFolder(n.id);
    try {
      history.replaceState(null, '', '#ce-' + n.id);
    } catch (e) {}
  };
  const iconBtn = {
    width: 28,
    flexShrink: 0,
    borderRadius: '6px',
    border: 'none',
    cursor: 'pointer',
    background: 'transparent',
    color: 'var(--ce-text-4)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  };
  const visibleFolderIds = allFolderIds.filter(id => allNodes[id].root === activeRoot);
  const allExpanded = visibleFolderIds.every(id => expandedFolders.has(id));
  const toggleAllFolders = () => {
    const next = new Set(expandedFolders);
    visibleFolderIds.forEach(id => allExpanded ? next.delete(id) : next.add(id));
    setExpandedFolders(next);
  };
  const onTreeKeyDown = e => {
    if (!['ArrowDown', 'ArrowUp', 'ArrowRight', 'ArrowLeft'].includes(e.key)) return;
    const visible = [];
    const walk = nodes => {
      for (const n of nodes) {
        visible.push(n.id);
        if (n.children && expandedFolders.has(n.id)) walk(n.children);
      }
    };
    walk(tree.children);
    const i = visible.indexOf(selectedId);
    if (i === -1) return;
    e.preventDefault();
    if (e.key === 'ArrowDown' && i < visible.length - 1) selectNode(allNodes[visible[i + 1]]); else if (e.key === 'ArrowUp' && i > 0) selectNode(allNodes[visible[i - 1]]); else if (e.key === 'ArrowRight' && selected.type === 'folder') {
      if (!expandedFolders.has(selectedId)) toggleFolder(selectedId); else if (selected.children && selected.children.length) selectNode(allNodes[selected.children[0].id]);
    } else if (e.key === 'ArrowLeft') {
      if (selected.type === 'folder' && expandedFolders.has(selectedId)) toggleFolder(selectedId); else if (selected.parentId) selectNode(allNodes[selected.parentId]);
    }
  };
  const copyExample = (id, text) => {
    const done = () => {
      setCopiedId(id);
      if (copyTimeoutRef.current) clearTimeout(copyTimeoutRef.current);
      copyTimeoutRef.current = setTimeout(() => setCopiedId(null), 2000);
    };
    const fallback = () => {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try {
        if (document.execCommand('copy')) done();
      } catch (e) {}
      document.body.removeChild(ta);
    };
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else {
      fallback();
    }
  };
  const renderIcon = (icon, color, size) => {
    const sz = size || 14;
    if (icon === 'folder') {
      return <svg width={sz} height={sz} viewBox="0 0 14 14" fill="none">
          <path d="M1.5 3.5a1 1 0 0 1 1-1h2.6l1 1.2h5.4a1 1 0 0 1 1 1v5.8a1 1 0 0 1-1 1h-9a1 1 0 0 1-1-1V3.5z" fill={color} fillOpacity="0.15" stroke={color} strokeWidth="1" />
        </svg>;
    }
    if (icon === 'json') {
      return <svg width={sz} height={sz} viewBox="0 0 14 14" fill="none">
          <rect x="2" y="1.5" width="10" height="11" rx="1.5" fill={color} fillOpacity="0.15" stroke={color} strokeWidth="1" />
          <text x="7" y="9" fontSize="6" fontFamily="monospace" fill={color} textAnchor="middle" fontWeight="700">{'{}'}</text>
        </svg>;
    }
    return <svg width={sz} height={sz} viewBox="0 0 14 14" fill="none">
        <rect x="2" y="1.5" width="10" height="11" rx="1.5" fill={color} fillOpacity="0.15" stroke={color} strokeWidth="1" />
        <line x1="4.5" y1="5" x2="9.5" y2="5" stroke={color} strokeWidth="1" />
        <line x1="4.5" y1="7" x2="9.5" y2="7" stroke={color} strokeWidth="1" />
        <line x1="4.5" y1="9" x2="8" y2="9" stroke={color} strokeWidth="1" />
      </svg>;
  };
  const renderNode = (node, depth) => {
    const isFolder = node.type === 'folder';
    const isExpanded = expandedFolders.has(node.id);
    const isSelected = selectedId === node.id;
    return <div key={node.id}>
        <button role="treeitem" tabIndex={-1} onClick={() => selectNode(node)} aria-selected={isSelected} aria-expanded={isFolder ? isExpanded : undefined} style={{
      display: 'flex',
      alignItems: 'center',
      gap: '5px',
      width: '100%',
      padding: `4px 8px 4px ${8 + depth * 16}px`,
      background: isSelected ? 'var(--ce-accent-bg)' : 'transparent',
      borderTop: 'none',
      borderRight: 'none',
      borderBottom: 'none',
      borderLeft: isSelected ? '2px solid var(--ce-accent)' : '2px solid transparent',
      outline: 'none',
      cursor: 'pointer',
      textAlign: 'left',
      fontFamily: 'var(--ce-mono)',
      fontSize: '13.5px',
      color: isSelected ? 'var(--ce-accent)' : 'var(--ce-text-2)',
      fontWeight: isSelected ? 550 : 400,
      transition: 'all 0.1s'
    }}>
          {isFolder ? <span onClick={e => {
      e.stopPropagation();
      toggleFolder(node.id);
    }} style={{
      fontSize: '14px',
      color: 'var(--ce-text-4)',
      width: '20px',
      height: '20px',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      cursor: 'pointer',
      borderRadius: '4px',
      marginLeft: '-6px',
      flexShrink: 0
    }} onMouseEnter={e => {
      e.currentTarget.style.background = 'var(--ce-arrow-hover)';
      e.currentTarget.style.color = 'var(--ce-text-2)';
    }} onMouseLeave={e => {
      e.currentTarget.style.background = 'transparent';
      e.currentTarget.style.color = 'var(--ce-text-4)';
    }}>{isExpanded ? '▾' : '▸'}</span> : <span style={{
      width: '14px',
      flexShrink: 0
    }} />}
          {renderIcon(node.icon, node.color)}
          <span style={{
      flex: 1,
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap'
    }}>{node.label}</span>
          {node.badge && BADGE_STYLES[node.badge] && <span title={BADGE_STYLES[node.badge].label} style={{
      width: 6,
      height: 6,
      borderRadius: '50%',
      background: BADGE_STYLES[node.badge].color,
      flexShrink: 0,
      opacity: 0.7
    }} />}
        </button>
        {isFolder && isExpanded && node.children && <div role="group">{node.children.map(child => renderNode(child, depth + 1))}</div>}
      </div>;
  };
  return <>
    <style>{`
      .ce-root {
        --ce-mono: var(--font-mono, ui-monospace, monospace);
        --ce-accent: #D97757;
        --ce-accent-bg: rgba(217,119,87,0.06);
        --ce-accent-border: rgba(217,119,87,0.12);
        --ce-bg: #fff;
        --ce-surface: #FAFAF7;
        --ce-surface-hover: #F0EEE6;
        --ce-border: #E8E6DC;
        --ce-border-subtle: #F0EEE6;
        --ce-text: #141413;
        --ce-text-2: #5E5D59;
        --ce-text-3: #73726C;
        --ce-text-4: #9C9A92;
        --ce-text-5: #B8B6AE;
        --ce-sep: #D1CFC5;
        --ce-code-header: #F5F4ED;
        --ce-code-bg: #1A1918;
        --ce-arrow-hover: rgba(0,0,0,0.08);
        --ce-badge-committed: #3d6b2e;
        --ce-badge-gitignored: #b85c3a;
        --ce-badge-local: #5e5d59;
        --ce-badge-autogen: #b07520;
        --ce-when-text: #4a7fb5;
      }
      .dark .ce-root {
        --ce-bg: #1a1918;
        --ce-surface: #232221;
        --ce-surface-hover: #2e2d2b;
        --ce-border: #3a3936;
        --ce-border-subtle: #2e2d2b;
        --ce-text: #e8e6dc;
        --ce-text-2: #c4c2b8;
        --ce-text-3: #9c9a92;
        --ce-text-4: #73726c;
        --ce-text-5: #5e5d59;
        --ce-sep: #4a4946;
        --ce-code-header: #2e2d2b;
        --ce-code-bg: #0d0d0c;
        --ce-arrow-hover: rgba(255,255,255,0.08);
        --ce-badge-committed: #6fa85c;
        --ce-badge-gitignored: #e08a60;
        --ce-badge-local: #9c9a92;
        --ce-badge-autogen: #e8a45c;
        --ce-when-text: #8bb4e0;
      }
      .ce-mobile-fallback { display: none; border: 1px solid rgba(0,0,0,0.1); background: rgba(0,0,0,0.03); }
      .dark .ce-mobile-fallback { border-color: rgba(255,255,255,0.15); background: rgba(255,255,255,0.04); }
      @media (max-width: 700px) {
        .ce-root:not(.ce-force) { display: none !important; }
        .ce-mobile-fallback { display: block; }
      }
    `}</style>
    {!forceMobile && <div className="ce-mobile-fallback" style={{
    padding: '14px 16px',
    borderRadius: '8px',
    fontSize: '14px'
  }}>
      The interactive explorer works best on a larger screen. See the <a href="#file-reference" style={{
    color: '#D97757'
  }}>file reference table</a> below, or <button onClick={() => setForceMobile(true)} style={{
    border: 'none',
    background: 'none',
    padding: 0,
    color: '#D97757',
    textDecoration: 'underline',
    cursor: 'pointer',
    font: 'inherit'
  }}>show the explorer anyway</button>.
    </div>}
    <div ref={rootRef} className={forceMobile ? 'ce-root ce-force' : 'ce-root'} style={{
    borderRadius: isFullscreen ? 0 : '12px',
    border: '1px solid var(--ce-border)',
    background: 'var(--ce-bg)',
    display: 'flex',
    alignItems: 'stretch',
    overflow: 'hidden',
    fontFamily: 'var(--font-sans, -apple-system, sans-serif)',
    ...isFullscreen && ({
      height: '100vh'
    })
  }}>
      {}
      <div style={{
    width: 'min(240px, 35%)',
    minWidth: '180px',
    flexShrink: 0,
    borderRight: '1px solid var(--ce-border-subtle)',
    background: 'var(--ce-surface)',
    display: 'flex',
    flexDirection: 'column'
  }}>
        <div style={{
    padding: '8px 8px 4px',
    borderBottom: '1px solid var(--ce-border-subtle)',
    display: 'flex',
    gap: '4px'
  }}>
          {['project', 'global'].map(root => <button key={root} onClick={() => switchRoot(root)} style={{
    flex: 1,
    padding: '6px 0',
    borderRadius: '6px',
    border: 'none',
    cursor: 'pointer',
    fontFamily: 'var(--ce-mono)',
    fontSize: '11.5px',
    background: activeRoot === root ? 'var(--ce-accent-bg)' : 'transparent',
    color: activeRoot === root ? 'var(--ce-accent)' : 'var(--ce-text-4)',
    fontWeight: activeRoot === root ? 600 : 430
  }}>
              {root === 'project' ? 'Project' : 'Global (~/)'}
            </button>)}
          <button onClick={toggleAllFolders} title={allExpanded ? 'Collapse all' : 'Expand all'} style={{
    ...iconBtn,
    fontSize: 11
  }}>
            {allExpanded ? '⊟' : '⊞'}
          </button>
          <button onClick={toggleFullscreen} title={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'} style={{
    ...iconBtn,
    fontSize: 13
  }}>
            {isFullscreen ? '⤡' : '⛶'}
          </button>
        </div>
        <div role="tree" aria-label="Configuration files" tabIndex={0} onKeyDown={onTreeKeyDown} style={{
    padding: '6px 0',
    overflowY: 'auto',
    flex: 1,
    outline: 'none'
  }}>
          {tree.children.map(node => renderNode(node, 0))}
        </div>
      </div>

      {}
      <div style={{
    flex: 1,
    minWidth: 0,
    padding: '20px 24px',
    minHeight: '400px',
    overflowY: 'auto'
  }}>
            <span aria-live="polite" style={{
    position: 'absolute',
    width: 1,
    height: 1,
    overflow: 'hidden',
    clip: 'rect(0 0 0 0)'
  }}>{selected.label} selected</span>
            {}
            <div style={{
    fontFamily: 'var(--ce-mono)',
    fontSize: '11px',
    color: 'var(--ce-text-4)',
    marginBottom: '10px',
    cursor: 'default'
  }}>
              {selected.path.map((seg, i) => <span key={i}>
                  <span style={{
    color: i === selected.path.length - 1 ? 'var(--ce-accent)' : 'var(--ce-text-4)'
  }}>{seg.replace(/\/$/, '')}</span>
                  {i < selected.path.length - 1 && <span style={{
    color: 'var(--ce-sep)'
  }}> / </span>}
                </span>)}
            </div>

            {}
            <div style={{
    display: 'flex',
    alignItems: 'flex-start',
    gap: '10px',
    marginBottom: '10px'
  }}>
              <span style={{
    flexShrink: 0,
    display: 'flex'
  }}>{renderIcon(selected.icon, selected.color, 24)}</span>
              <div style={{
    flex: 1,
    minWidth: 0
  }}>
                <div style={{
    fontSize: '22px',
    fontWeight: 600,
    color: 'var(--ce-text)',
    letterSpacing: '-0.3px',
    lineHeight: '26px'
  }}>{selected.label}</div>
                {selected.oneLiner && <div style={{
    fontSize: '15px',
    color: 'var(--ce-text-3)',
    marginTop: '3px'
  }}>{selected.oneLiner}</div>}
              </div>
              <div style={{
    display: 'flex',
    gap: '4px',
    flexShrink: 0
  }}>
                {[selected.autogen && 'autogen', selected.badge].filter(Boolean).map(k => {
    const s = BADGE_STYLES[k];
    if (!s) return null;
    return <span key={k} style={{
      fontFamily: 'var(--ce-mono)',
      fontSize: '10px',
      fontWeight: 600,
      textTransform: 'uppercase',
      letterSpacing: '0.3px',
      padding: '2px 6px',
      borderRadius: '4px',
      background: s.bg,
      color: s.color,
      border: `0.5px solid ${s.border}`
    }}>{s.label}</span>;
  })}
              </div>
            </div>

            {}
            {selected.note && <div style={{
    padding: '10px 12px',
    borderRadius: '8px',
    marginBottom: '14px',
    background: 'rgba(217,119,87,0.06)',
    border: '1px solid rgba(217,119,87,0.2)',
    borderLeft: '3px solid var(--ce-accent)',
    fontSize: '15px',
    color: 'var(--ce-text-2)',
    lineHeight: 1.6
  }}>
                {selected.note}
              </div>}

            {}
            {selected.when && <div style={{
    padding: '8px 12px',
    borderRadius: '6px',
    background: 'rgba(106,155,204,0.06)',
    border: '0.5px solid rgba(106,155,204,0.12)',
    fontSize: '15px',
    color: 'var(--ce-when-text)',
    marginBottom: '16px'
  }}>
                <div style={{
    fontSize: '10px',
    fontWeight: 700,
    textTransform: 'uppercase',
    letterSpacing: '0.4px',
    opacity: 0.65,
    marginBottom: '3px'
  }}>When it loads</div>
                <div style={{
    fontWeight: 500
  }}>{selected.when}</div>
              </div>}

            {}
            {selected.description && <div style={{
    fontSize: '16px',
    color: 'var(--ce-text-2)',
    lineHeight: 1.65,
    marginBottom: '16px'
  }}>
                {Array.isArray(selected.description) ? selected.description.map((para, i) => <div key={i} style={{
    marginBottom: i < selected.description.length - 1 ? '12px' : 0
  }}>{para}</div>) : selected.description}
              </div>}

            {}
            {selected.contains && selected.contains.length > 0 && <div style={{
    marginBottom: '16px'
  }}>
                <div style={{
    fontSize: '11px',
    fontWeight: 700,
    color: 'var(--ce-text-4)',
    textTransform: 'uppercase',
    letterSpacing: '0.4px',
    marginBottom: '8px'
  }}>Common keys</div>
                {selected.contains.map((item, i) => <div key={i} style={{
    display: 'flex',
    gap: '7px',
    fontSize: '15px',
    color: 'var(--ce-text-2)',
    lineHeight: 1.5,
    marginBottom: '5px'
  }}>
                    <span style={{
    fontSize: '7px',
    color: 'var(--ce-text-4)',
    marginTop: '6px'
  }}>●</span>
                    <span>{item}</span>
                  </div>)}
              </div>}

            {}
            {selected.tips && selected.tips.length > 0 && <div style={{
    padding: '12px 14px',
    borderRadius: '8px',
    background: 'var(--ce-surface)',
    border: '1px solid var(--ce-border-subtle)',
    marginBottom: '16px'
  }}>
                <div style={{
    fontSize: '11px',
    fontWeight: 700,
    color: 'var(--ce-accent)',
    textTransform: 'uppercase',
    letterSpacing: '0.4px',
    marginBottom: '6px'
  }}>Tips</div>
                {selected.tips.map((tip, i) => <div key={i} style={{
    display: 'flex',
    gap: '7px',
    fontSize: '14.5px',
    color: 'var(--ce-text-2)',
    marginBottom: i < selected.tips.length - 1 ? '5px' : 0
  }}>
                    <span style={{
    fontSize: '7px',
    color: 'var(--ce-accent)',
    marginTop: '6px'
  }}>●</span>
                    <span>{tip}</span>
                  </div>)}
              </div>}

            {}
            {selected.example && <div style={{
    marginBottom: '16px'
  }}>
                {selected.exampleIntro && <div style={{
    fontSize: '15px',
    color: 'var(--ce-text-2)',
    lineHeight: 1.6,
    marginBottom: '10px'
  }}>
                    {selected.exampleIntro}
                  </div>}
                <div style={{
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '6px 10px',
    background: 'var(--ce-code-header)',
    border: '1px solid var(--ce-border)',
    borderRadius: '8px 8px 0 0'
  }}>
                  <span style={{
    fontFamily: 'var(--ce-mono)',
    fontSize: '11px',
    fontWeight: 600,
    color: 'var(--ce-text-3)'
  }}>{selected.label}</span>
                  <button onClick={() => copyExample(selected.id, selected.example)} style={{
    padding: '3px 8px',
    borderRadius: '4px',
    fontSize: '11px',
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'all 0.15s',
    background: isCopied ? 'rgba(85,138,66,0.08)' : 'var(--ce-code-header)',
    border: isCopied ? '0.5px solid rgba(85,138,66,0.2)' : '0.5px solid var(--ce-border)',
    color: isCopied ? '#558A42' : 'var(--ce-text-3)'
  }}>
                    {isCopied ? '✓ Copied' : 'Copy'}
                  </button>
                </div>
                <pre style={{
    margin: 0,
    padding: '12px 14px',
    background: 'var(--ce-code-bg)',
    color: '#E8E6DC',
    fontFamily: 'var(--ce-mono)',
    fontSize: '13px',
    lineHeight: 1.65,
    borderRadius: '0 0 8px 8px',
    overflowX: 'auto',
    whiteSpace: 'pre'
  }}>{selected.example}</pre>
              </div>}

            {}
            {selected.docsLink && <a href={selected.docsLink} style={{
    display: 'inline-flex',
    padding: '5px 12px',
    borderRadius: '6px',
    background: 'var(--ce-accent-bg)',
    border: '1px solid var(--ce-accent-border)',
    color: 'var(--ce-accent)',
    fontSize: '12px',
    fontWeight: 600,
    textDecoration: 'none'
  }}>Full docs →</a>}

            {}
            {selected.children && selected.children.length > 0 && <div style={{
    marginTop: '20px'
  }}>
                <div style={{
    fontSize: '11px',
    fontWeight: 700,
    color: 'var(--ce-text-4)',
    textTransform: 'uppercase',
    letterSpacing: '0.4px',
    marginBottom: '8px'
  }}>Contents</div>
                <div style={{
    display: 'flex',
    flexDirection: 'column',
    gap: '4px'
  }}>
                  {selected.children.map(child => <button key={child.id} onClick={() => selectNode(child)} style={{
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '6px 8px',
    width: '100%',
    background: 'var(--ce-surface)',
    borderRadius: '6px',
    border: 'none',
    cursor: 'pointer',
    textAlign: 'left',
    transition: 'background 0.1s'
  }} onMouseEnter={e => e.currentTarget.style.background = 'var(--ce-surface-hover)'} onMouseLeave={e => e.currentTarget.style.background = 'var(--ce-surface)'}>
                      {renderIcon(child.icon, child.color, 13)}
                      <span style={{
    fontFamily: 'var(--ce-mono)',
    fontSize: '12px',
    color: 'var(--ce-text-2)'
  }}>{child.label}</span>
                      {child.oneLiner && <span style={{
    fontSize: '11px',
    color: 'var(--ce-text-4)',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap'
  }}>{child.oneLiner}</span>}
                    </button>)}
                </div>
              </div>}
      </div>
    </div>
    </>;
};

Claude Code 從您的專案目錄和主目錄中的 `~/.claude` 讀取指令、設定、skills、subagents 和記憶。將專案檔案提交到 git 以與您的團隊共享；`~/.claude` 中的檔案是個人設定，適用於您的所有專案。

在 Windows 上，`~/.claude` 解析為 `%USERPROFILE%\.claude`。如果您設定了 [`CLAUDE_CONFIG_DIR`](/zh-TW/env-vars)，此頁面上的每個 `~/.claude` 路徑都會改為位於該目錄下。

大多數使用者只編輯 `CLAUDE.md` 和 `settings.json`。目錄的其餘部分是可選的：根據需要新增 skills、rules 或 subagents。

## 探索目錄

點擊樹中的檔案以查看每個檔案的功能、何時載入以及範例。

<ClaudeExplorer />

## 未顯示的內容

探索器涵蓋您編寫和編輯的檔案。一些相關檔案位於其他位置：

| 檔案                      | 位置                  | 用途                                                                                                                                                                    |
| ----------------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `managed-settings.json` | 系統級別，因作業系統而異        | 企業強制執行的設定，您無法覆蓋。請參閱[伺服器管理的設定](/zh-TW/server-managed-settings)。                                                                                                        |
| `CLAUDE.local.md`       | 專案根目錄               | 您對此專案的私人偏好設定，與 CLAUDE.md 一起載入。手動建立並將其新增到 `.gitignore`。                                                                                                                |
| 已安裝的 plugins            | `~/.claude/plugins` | 複製的市場、已安裝的 plugin 版本和每個 plugin 的資料，由 `claude plugin` 命令管理。孤立版本在 plugin 更新或解除安裝後 7 天內被刪除。請參閱 [plugin 快取](/zh-TW/plugins-reference#plugin-caching-and-file-resolution)。 |

`~/.claude` 還保存 Claude Code 在您工作時寫入的資料：文字記錄、提示歷史記錄、檔案快照、快取和日誌。請參閱下方的[應用程式資料](#application-data)。

## 選擇正確的檔案

不同類型的自訂設定位於不同的檔案中。使用此表格找到變更應該位於何處。

| 您想要                    | 編輯                                      | 範圍    | 參考                                                      |
| :--------------------- | :-------------------------------------- | :---- | :------------------------------------------------------ |
| 為 Claude 提供專案上下文和慣例    | `CLAUDE.md`                             | 專案或全域 | [Memory](/zh-TW/memory)                                 |
| 允許或阻止特定工具呼叫            | `settings.json` `permissions` 或 `hooks` | 專案或全域 | [Permissions](/zh-TW/permissions)、[Hooks](/zh-TW/hooks) |
| 在工具呼叫之前或之後執行指令碼        | `settings.json` `hooks`                 | 專案或全域 | [Hooks](/zh-TW/hooks)                                   |
| 為工作階段設定環境變數            | `settings.json` `env`                   | 專案或全域 | [Settings](/zh-TW/settings#available-settings)          |
| 將個人覆蓋保留在 git 之外        | `settings.local.json`                   | 僅專案   | [Settings scopes](/zh-TW/settings#settings-files)       |
| 新增您使用 `/name` 叫用的提示或功能 | `skills/<name>/SKILL.md`                | 專案或全域 | [Skills](/zh-TW/skills)                                 |
| 定義具有自己工具的專門 subagent   | `agents/*.md`                           | 專案或全域 | [Subagents](/zh-TW/sub-agents)                          |
| 透過 MCP 連接外部工具          | `.mcp.json`                             | 僅專案   | [MCP](/zh-TW/mcp)                                       |
| 變更 Claude 格式化回應的方式     | `output-styles/*.md`                    | 專案或全域 | [Output styles](/zh-TW/output-styles)                   |

## 檔案參考

此表列出探索器涵蓋的每個檔案。專案範圍的檔案位於您的儲存庫中的 `.claude/` 下（或 `CLAUDE.md`、`.mcp.json` 和 `.worktreeinclude` 的根目錄）。全域範圍的檔案位於 `~/.claude/` 中，適用於所有專案。

<Note>
  有幾件事可以覆蓋您在這些檔案中放入的內容：

  * 您的組織部署的[受管設定](/zh-TW/server-managed-settings)優先於所有內容
  * CLI 旗標（如 `--permission-mode` 或 `--settings`）會覆蓋該工作階段的 `settings.json`
  * 某些環境變數優先於其等效設定，但這會有所不同：檢查[環境變數參考](/zh-TW/env-vars)以了解每個變數

  請參閱[設定優先順序](/zh-TW/settings#settings-precedence)以了解完整順序。
</Note>

點擊檔案名稱以在上方的探索器中開啟該節點。

| 檔案                                                  | 範圍    | 提交 | 功能                            | 參考                                                                      |
| --------------------------------------------------- | ----- | -- | ----------------------------- | ----------------------------------------------------------------------- |
| [`CLAUDE.md`](#ce-claude-md)                        | 專案和全域 | ✓  | 每個工作階段載入的指令                   | [Memory](/zh-TW/memory)                                                 |
| [`rules/*.md`](#ce-rules)                           | 專案和全域 | ✓  | 主題範圍的指令，可選擇路徑限制               | [Rules](/zh-TW/memory#organize-rules-with-claude/rules/)                |
| [`settings.json`](#ce-settings-json)                | 專案和全域 | ✓  | 權限、hooks、環境變數、模型預設值           | [Settings](/zh-TW/settings)                                             |
| [`settings.local.json`](#ce-settings-local-json)    | 僅專案   |    | 您的個人覆蓋，自動 gitignored          | [Settings scopes](/zh-TW/settings#settings-files)                       |
| [`.mcp.json`](#ce-mcp-json)                         | 僅專案   | ✓  | 團隊共享的 MCP 伺服器                 | [MCP scopes](/zh-TW/mcp#mcp-installation-scopes)                        |
| [`.worktreeinclude`](#ce-worktreeinclude)           | 僅專案   | ✓  | Gitignored 檔案以複製到新的 worktrees | [Worktrees](/zh-TW/common-workflows#copy-gitignored-files-to-worktrees) |
| [`skills/<name>/SKILL.md`](#ce-skills)              | 專案和全域 | ✓  | 可重複使用的提示，使用 `/name` 叫用或自動叫用   | [Skills](/zh-TW/skills)                                                 |
| [`commands/*.md`](#ce-commands)                     | 專案和全域 | ✓  | 單檔案提示；與 skills 相同的機制          | [Skills](/zh-TW/skills)                                                 |
| [`output-styles/*.md`](#ce-output-styles)           | 專案和全域 | ✓  | 自訂系統提示部分                      | [Output styles](/zh-TW/output-styles)                                   |
| [`agents/*.md`](#ce-agents)                         | 專案和全域 | ✓  | Subagent 定義及其自己的提示和工具         | [Subagents](/zh-TW/sub-agents)                                          |
| [`agent-memory/<name>/`](#ce-agent-memory)          | 專案和全域 | ✓  | Subagents 的持久記憶               | [Persistent memory](/zh-TW/sub-agents#enable-persistent-memory)         |
| [`~/.claude.json`](#ce-claude-json)                 | 僅全域   |    | 應用程式狀態、OAuth、UI 切換、個人 MCP 伺服器 | [Global config](/zh-TW/settings#global-config-settings)                 |
| [`projects/<project>/memory/`](#ce-global-projects) | 僅全域   |    | 自動記憶：Claude 在工作階段間對自己的筆記      | [Auto memory](/zh-TW/memory#auto-memory)                                |
| [`keybindings.json`](#ce-keybindings)               | 僅全域   |    | 自訂快捷鍵                         | [Keybindings](/zh-TW/keybindings)                                       |
| [`themes/*.json`](#ce-themes)                       | 僅全域   |    | 自訂色彩主題                        | [Custom themes](/zh-TW/terminal-config#create-a-custom-theme)           |

## 檢查已載入的內容

探索器顯示可以存在的檔案。若要查看在您目前工作階段中實際載入的內容，請使用這些命令：

| 命令             | 顯示                                    |
| -------------- | ------------------------------------- |
| `/context`     | 按類別的權杖使用情況：系統提示、記憶檔案、skills、MCP 工具和訊息 |
| `/memory`      | 載入了哪些 CLAUDE.md 和 rules 檔案，加上自動記憶項目   |
| `/agents`      | 已設定的 subagents 及其設定                   |
| `/hooks`       | 作用中的 hook 設定                          |
| `/mcp`         | 已連接的 MCP 伺服器及其狀態                      |
| `/skills`      | 來自專案、使用者和 plugin 來源的可用 skills         |
| `/permissions` | 目前的允許和拒絕規則                            |
| `/doctor`      | 安裝和設定診斷                               |

首先執行 `/context` 以取得概觀，然後執行特定命令以調查您想要的區域。

## 應用程式資料

除了您編寫的設定外，`~/.claude` 還保存 Claude Code 在工作階段期間寫入的資料。這些檔案是純文字。任何通過工具的內容都會在磁碟上的文字記錄中結束：檔案內容、命令輸出、貼上的文字。

### 自動清理

下列路徑中的檔案在啟動時被刪除，一旦它們的年齡超過 [`cleanupPeriodDays`](/zh-TW/settings#available-settings)。預設值為 30 天。

| `~/.claude/` 下的路徑                            | 內容                                                                                      |
| -------------------------------------------- | --------------------------------------------------------------------------------------- |
| `projects/<project>/<session>.jsonl`         | 完整對話文字記錄：每條訊息、工具呼叫和工具結果                                                                 |
| `projects/<project>/<session>/tool-results/` | 溢出到單獨檔案的大型工具輸出                                                                          |
| `file-history/<session>/`                    | Claude 變更的檔案的編輯前快照，用於[檢查點還原](/zh-TW/checkpointing)                                      |
| `plans/`                                     | 在 [Plan Mode](/zh-TW/permission-modes#analyze-before-you-edit-with-plan-mode) 期間寫入的計畫檔案 |
| `debug/`                                     | 每個工作階段的偵錯日誌，僅在您使用 `--debug` 啟動或執行 `/debug` 時寫入                                          |
| `paste-cache/`、`image-cache/`                | 大型貼上和附加影像的內容                                                                            |
| `session-env/`                               | 每個工作階段的環境中繼資料                                                                           |
| `tasks/`                                     | 由 task tools 寫入的每個工作階段任務清單                                                              |
| `shell-snapshots/`                           | Bash tool 使用的擷取 shell 環境。在正常退出時移除。掃描會清除任何在當機後遺留的檔案。                                     |
| `backups/`                                   | 在設定遷移前取得的 `~/.claude.json` 的時間戳記副本                                                      |

### 保留直到您刪除它們

以下路徑不受自動清理覆蓋，並無限期保留。

| `~/.claude/` 下的路徑  | 內容                             |
| ------------------ | ------------------------------ |
| `history.jsonl`    | 您輸入的每個提示，帶有時間戳記和專案路徑。用於向上箭頭回憶。 |
| `stats-cache.json` | 由 `/usage` 顯示的彙總權杖和成本計數        |
| `todos/`           | 舊版每個工作階段的任務清單。不再由目前版本寫入；可安全刪除。 |

其他小型快取和鎖定檔案會根據您使用的功能而出現，可安全刪除。

### 純文字儲存

文字記錄和歷史記錄在靜止時未加密。作業系統檔案權限是唯一的保護。如果工具讀取 `.env` 檔案或命令列印認證，該值會寫入 `projects/<project>/<session>.jsonl`。若要減少暴露：

* 降低 `cleanupPeriodDays` 以縮短文字記錄的保留時間
* 設定 [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/zh-TW/env-vars) 環境變數以跳過在任何模式中寫入文字記錄和提示歷史記錄。在非互動模式中，您可以改為在 `-p` 旁邊傳遞 `--no-session-persistence`，或在 Agent SDK 中設定 `persistSession: false`。
* 使用[權限規則](/zh-TW/permissions)拒絕讀取認證檔案

### 清除本機資料

執行 `claude project purge` 以刪除 Claude Code 為一個專案保存的狀態：

* `projects/` 下的文字記錄和自動記憶
* 每個工作階段的 `tasks/`、`debug/` 和 `file-history/` 項目
* `history.jsonl` 中的匹配提示行
* 專案在 `~/.claude.json` 中的項目

該命令會列印完整的刪除計畫，並在移除任何內容之前要求確認。

預覽計畫而不刪除任何內容：

```bash theme={null}
claude project purge ~/work/my-repo --dry-run
```

透過單一確認提示刪除：

```bash theme={null}
claude project purge ~/work/my-repo
```

省略路徑以從互動式清單中選擇專案。

跳過確認提示以在指令碼中使用：

```bash theme={null}
claude project purge ~/work/my-repo --yes
```

傳遞 `--all` 而不是路徑以一次清除所有專案的狀態，這會直接刪除 `history.jsonl` 而不是篩選它。傳遞 `-i` 以逐項逐步執行刪除計畫。

該命令會單獨保留 `shell-snapshots/` 和 `backups/`，因為這些不是專案範圍的，並在計畫輸出中警告它們。如果沒有狀態與給定路徑相符，它會以狀態 1 退出。

您也可以手動刪除上述任何應用程式資料路徑。新工作階段不受影響。下表顯示您對過去工作階段失去的內容。

| 刪除                                                                                                                                                                                    | 您失去                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `~/.claude/projects/`                                                                                                                                                                 | 過去工作階段的繼續、繼續和倒帶    |
| `~/.claude/history.jsonl`                                                                                                                                                             | 向上箭頭提示回憶           |
| `~/.claude/file-history/`                                                                                                                                                             | 過去工作階段的檢查點還原       |
| `~/.claude/stats-cache.json`                                                                                                                                                          | 由 `/usage` 顯示的歷史總計 |
| `~/.claude/debug/`、`~/.claude/plans/`、`~/.claude/paste-cache/`、`~/.claude/image-cache/`、`~/.claude/session-env/`、`~/.claude/tasks/`、`~/.claude/shell-snapshots/`、`~/.claude/backups/` | 沒有面向使用者的內容         |
| `~/.claude/todos/`                                                                                                                                                                    | 無。舊版目錄不由目前版本寫入。    |

不要刪除 `~/.claude.json`、`~/.claude/settings.json` 或 `~/.claude/plugins/`：這些保存您的驗證、偏好設定和已安裝的 plugins。

## 相關資源

* [管理 Claude 的記憶](/zh-TW/memory)：寫入和組織 CLAUDE.md、rules 和自動記憶
* [設定設定](/zh-TW/settings)：設定權限、hooks、環境變數和模型預設值
* [建立 skills](/zh-TW/skills)：建立可重複使用的提示和工作流程
* [設定 subagents](/zh-TW/sub-agents)：定義具有自己上下文的專門代理


---

# Explore the context window

> An interactive simulation of how Claude Code's context window fills during a session. See what loads automatically, what each file read costs, and when rules and hooks fire.

export const ContextWindow = () => {
  const MAX = 200000;
  const STARTUP_END = 0.2;
  {}
  const EVENTS = useMemo(() => [{}, {
    t: 0.015,
    kind: 'auto',
    label: 'System prompt',
    tokens: 4200,
    color: '#6B6964',
    vis: 'hidden',
    desc: 'Core instructions for behavior, tool use, and response formatting. Always loaded first. You never see it.',
    link: null
  }, {
    t: 0.035,
    kind: 'auto',
    label: 'Auto memory (MEMORY.md)',
    tokens: 680,
    color: '#E8A45C',
    vis: 'hidden',
    desc: "Claude's notes to itself from previous sessions: build commands it learned, patterns it noticed, mistakes to avoid. The first 200 lines or 25KB, whichever comes first, are loaded into the conversation context.",
    link: '/en/memory#auto-memory'
  }, {
    t: 0.06,
    kind: 'auto',
    label: 'Environment info',
    tokens: 280,
    color: '#6B6964',
    vis: 'hidden',
    desc: 'Working directory, platform, shell, OS version, and whether this is a git repo. Git branch, status, and recent commits load as a separate block at the very end of the system prompt.',
    link: null
  }, {
    t: 0.08,
    kind: 'auto',
    label: 'MCP tools (deferred)',
    tokens: 120,
    color: '#9B7BC4',
    vis: 'hidden',
    desc: 'MCP tool names listed so Claude knows what is available. By default, full schemas stay deferred and Claude loads specific ones on demand via tool search when a task needs them. Set `ENABLE_TOOL_SEARCH=auto` to load schemas upfront when they fit within 10% of the context window, or `ENABLE_TOOL_SEARCH=false` to load everything.',
    link: '/en/mcp#scale-with-mcp-tool-search'
  }, {
    t: 0.1,
    kind: 'auto',
    label: 'Skill descriptions',
    tokens: 450,
    color: '#D4A843',
    vis: 'hidden',
    noSurviveCompact: true,
    desc: 'One-line descriptions of available skills so Claude knows what it can invoke. Full skill content loads only when Claude actually uses one. Skills with `disable-model-invocation: true` are not in this list. They stay completely out of context until you invoke them with `/name`. Unlike the rest of the startup content, this listing is not re-injected after `/compact`. Only skills you actually invoked get preserved.',
    link: '/en/skills'
  }, {
    t: 0.12,
    kind: 'auto',
    label: '~/.claude/CLAUDE.md',
    tokens: 320,
    color: '#6A9BCC',
    vis: 'hidden',
    desc: 'Your global preferences. Applies to every project. Loaded alongside project instructions at the start of every conversation.',
    link: '/en/memory#choose-where-to-put-claude-md-files'
  }, {
    t: 0.14,
    kind: 'auto',
    label: 'Project CLAUDE.md',
    tokens: 1800,
    color: '#6A9BCC',
    vis: 'hidden',
    desc: 'Project conventions, build commands, architecture notes. The most important file you can create. Lives in your project root, so your whole team gets the same instructions.',
    tip: 'Keep it under 200 lines. Move reference content to skills or path-scoped rules so it only loads when needed.',
    link: '/en/memory'
  }, {}, {
    t: 0.22,
    kind: 'user',
    label: 'Your prompt',
    tokens: 45,
    color: '#558A42',
    vis: 'full',
    desc: '"Fix the auth bug where users get 401 after token refresh"',
    link: null
  }, {}, {
    t: 0.28,
    kind: 'claude',
    label: 'Read src/api/auth.ts',
    tokens: 2400,
    color: '#8A8880',
    vis: 'brief',
    desc: 'Main auth file. You see "Read auth.ts" in your terminal, but the 2,400 tokens of file content only Claude sees.',
    tip: 'File reads dominate context usage. Be specific in prompts ("fix the bug in auth.ts") so Claude reads fewer files. For research-heavy tasks, use a subagent.',
    link: null
  }, {
    t: 0.32,
    kind: 'claude',
    label: 'Read src/lib/tokens.ts',
    tokens: 1100,
    color: '#8A8880',
    vis: 'brief',
    desc: 'Following imports to the token module. Shown as a one-liner in your terminal.',
    link: null
  }, {
    t: 0.35,
    kind: 'auto',
    label: 'Rule: api-conventions.md',
    tokens: 380,
    color: '#4A9B8E',
    vis: 'brief',
    desc: 'This rule in `.claude/rules/` has a `paths:` pattern matching `src/api/**`. It loaded automatically when Claude read a file in that directory. You see "Loaded .claude/rules/api-conventions.md" in your terminal, but not the rule content.',
    link: '/en/memory#path-specific-rules'
  }, {
    t: 0.38,
    kind: 'claude',
    label: 'Read middleware.ts',
    tokens: 1800,
    color: '#8A8880',
    vis: 'brief',
    desc: 'Tracing the auth flow deeper.',
    link: null
  }, {
    t: 0.41,
    kind: 'claude',
    label: 'Read auth.test.ts',
    tokens: 1600,
    color: '#8A8880',
    vis: 'brief',
    desc: 'Checking existing tests for expected behavior.',
    link: null
  }, {
    t: 0.44,
    kind: 'auto',
    label: 'Rule: testing.md',
    tokens: 290,
    color: '#4A9B8E',
    vis: 'brief',
    desc: 'Another path-scoped rule, this one matching `*.test.ts` files. Triggered when Claude read auth.test.ts. Shown as a one-line "Loaded" notice.',
    link: '/en/memory#path-specific-rules'
  }, {
    t: 0.47,
    kind: 'claude',
    label: 'grep "refreshToken"',
    tokens: 600,
    color: '#A09E96',
    vis: 'brief',
    desc: 'Search results across the codebase. You see the command ran, not the full output.',
    link: null
  }, {}, {
    t: 0.53,
    kind: 'claude',
    label: "Claude's analysis",
    tokens: 800,
    color: '#D97757',
    vis: 'full',
    desc: 'Explains the bug: token invalidated too early in the rotation. This text appears in your terminal.',
    link: null
  }, {
    t: 0.57,
    kind: 'claude',
    label: 'Edit auth.ts',
    tokens: 400,
    color: '#D97757',
    vis: 'full',
    desc: 'Fixes the token rotation order. The diff appears in your terminal.',
    link: null
  }, {
    t: 0.59,
    kind: 'hook',
    label: 'Hook: prettier',
    tokens: 120,
    color: '#B8860B',
    vis: 'hidden',
    desc: 'A PostToolUse hook in `settings.json` runs prettier after every file edit and reports back via `hookSpecificOutput.additionalContext`. That field enters Claude\'s context. Plain stdout on exit 0 does not. It is written to the debug log only.',
    tip: 'Output JSON with `additionalContext` to send info to Claude. For PostToolUse hooks, exit code 2 surfaces stderr as an error but cannot block since the tool already ran. Keep output concise since it enters context without truncation.',
    link: '/en/hooks-guide'
  }, {
    t: 0.62,
    kind: 'claude',
    label: 'Edit auth.test.ts',
    tokens: 600,
    color: '#D97757',
    vis: 'full',
    desc: 'Adds a regression test for the fix. The diff appears in your terminal.',
    link: null
  }, {
    t: 0.64,
    kind: 'hook',
    label: 'Hook: prettier',
    tokens: 100,
    color: '#B8860B',
    vis: 'hidden',
    desc: 'The same hook fires again for the test file. Every matching tool event triggers it.',
    link: '/en/hooks-guide'
  }, {
    t: 0.67,
    kind: 'claude',
    label: 'npm test output',
    tokens: 1200,
    color: '#A09E96',
    vis: 'brief',
    desc: 'Runs the test suite. You see "Running npm test..." and the pass count, not the full 1,200 tokens of output.',
    link: null
  }, {
    t: 0.70,
    kind: 'claude',
    label: 'Summary',
    tokens: 400,
    color: '#D97757',
    vis: 'full',
    desc: '"Fixed token rotation. Added regression test. All tests pass."',
    link: null
  }, {}, {
    t: 0.72,
    kind: 'user',
    label: 'Your follow-up',
    tokens: 40,
    color: '#558A42',
    vis: 'full',
    desc: '"Use a subagent to research session timeout handling, then fix it"',
    tip: 'Follow-ups add to the same context. Delegating research to a subagent keeps large file reads out of your main window.',
    link: null
  }, {
    t: 0.79,
    kind: 'claude',
    label: 'Spawn research subagent',
    tokens: 80,
    color: '#D97757',
    vis: 'brief',
    desc: "Claude delegates the research to a subagent with a fresh, separate context window. It loads CLAUDE.md and the same MCP and skill setup, but starts without your conversation history or the main session's auto memory.",
    link: '/en/sub-agents'
  }, {
    t: 0.795,
    kind: 'sub',
    label: 'System prompt',
    tokens: 0,
    subTokens: 900,
    color: '#6B6964',
    vis: 'hidden',
    desc: "The subagent gets its own system prompt, shorter than the main session's. For the general-purpose agent, it's a brief prompt plus environment details. The main session's auto memory is not included. If a custom agent has memory: in its frontmatter, it loads its own separate MEMORY.md here instead.",
    link: '/en/sub-agents#enable-persistent-memory'
  }, {
    t: 0.80,
    kind: 'sub',
    label: 'Project CLAUDE.md (own copy)',
    tokens: 0,
    subTokens: 1800,
    color: '#6A9BCC',
    vis: 'hidden',
    desc: "The subagent loads CLAUDE.md too. Same file, same content, but it counts against the subagent's context, not yours. The built-in Explore and Plan agents skip this for a smaller context.",
    link: '/en/sub-agents'
  }, {
    t: 0.805,
    kind: 'sub',
    label: 'MCP tools + skills',
    tokens: 0,
    subTokens: 970,
    color: '#9B7BC4',
    vis: 'hidden',
    desc: "The subagent has access to the same MCP servers and skills. It gets most of the parent's tools, minus several that don't apply in a nested context, including plan-mode controls, background-task tools, and by default the Agent tool itself to prevent recursion.",
    link: '/en/sub-agents'
  }, {
    t: 0.81,
    kind: 'sub',
    label: 'Task prompt from main',
    tokens: 0,
    subTokens: 120,
    color: '#558A42',
    vis: 'hidden',
    desc: "Instead of a user prompt, the subagent receives the task Claude wrote for it: 'Research session timeout handling in this codebase.'",
    link: '/en/sub-agents'
  }, {
    t: 0.82,
    kind: 'sub',
    label: 'Read session.ts',
    tokens: 0,
    subTokens: 2200,
    color: '#8A8880',
    vis: 'hidden',
    desc: "Now the subagent does its work. This file read fills the subagent's context, not yours.",
    link: '/en/sub-agents'
  }, {
    t: 0.825,
    kind: 'sub',
    label: 'Read timeouts.ts',
    tokens: 0,
    subTokens: 800,
    color: '#8A8880',
    vis: 'hidden',
    desc: "Another file read in the subagent's separate context.",
    link: '/en/sub-agents'
  }, {
    t: 0.83,
    kind: 'sub',
    label: 'Read config/*.ts',
    tokens: 0,
    subTokens: 3100,
    color: '#8A8880',
    vis: 'hidden',
    desc: "The subagent can read as many files as it needs. None of this touches your main context.",
    link: '/en/sub-agents'
  }, {
    t: 0.85,
    kind: 'claude',
    label: 'Subagent returns summary',
    tokens: 420,
    color: '#D97757',
    vis: 'brief',
    desc: "Only the subagent's final text response comes back to your context, plus a small metadata trailer with token counts and duration. The subagent read 6,100 tokens of files. You got a 420-token result. That's the context savings.",
    link: '/en/sub-agents'
  }, {
    t: 0.86,
    kind: 'claude',
    label: "Claude's response",
    tokens: 1200,
    color: '#D97757',
    vis: 'full',
    desc: 'Analysis and fix for session timeouts. This text appears in your terminal.',
    link: null
  }, {}, {
    t: 0.875,
    kind: 'user',
    label: '!git status',
    tokens: 180,
    color: '#558A42',
    vis: 'full',
    desc: "You ran a shell command with the ! prefix to see which files Claude modified. The command and its output both enter context as part of your message. Useful for grounding Claude in command output without Claude running it.",
    link: '/en/interactive-mode#bash-mode-with-prefix'
  }, {
    t: 0.89,
    kind: 'user',
    label: '/commit-push',
    tokens: 620,
    color: '#558A42',
    vis: 'brief',
    desc: 'You invoked a skill that has `disable-model-invocation: true`. Its description was not in the skill index at startup, so it cost zero context until this moment. Now the full skill content loads and Claude follows its instructions to stage, commit, and push your changes.',
    tip: 'Set `disable-model-invocation: true` on skills with side effects like committing, deploying, or sending messages. They stay out of context entirely until you need them.',
    link: '/en/skills#control-who-invokes-a-skill'
  }, {}, {
    t: 0.93,
    kind: 'compact',
    label: '/compact',
    tokens: 0,
    color: '#D97757',
    vis: 'brief',
    desc: 'Replaces the conversation with a structured summary. You see a "Conversation compacted" message. The summarization happens without appearing in your terminal.',
    link: '/en/how-claude-code-works#the-context-window'
  }].filter(e => e.t !== undefined), []);
  const VIS_META = {
    hidden: {
      label: 'Invisible in your terminal',
      sub: 'This content does not appear in your terminal.'
    },
    brief: {
      label: 'One-liner in your terminal',
      sub: 'You see a brief mention, not the full content.'
    },
    full: {
      label: 'Shown in your terminal',
      sub: 'The actual content appears in your terminal.'
    }
  };
  {}
  const GATES = [{
    at: 0.18,
    kind: 'prompt',
    text: 'Fix the auth bug where users get 401 after token refresh',
    resumeTo: 0.22
  }, {
    at: 0.705,
    kind: 'prompt',
    text: 'Use a subagent to research session timeout handling, then fix it',
    resumeTo: 0.72
  }, {
    at: 0.865,
    kind: 'bang',
    text: '!git status',
    resumeTo: 0.875
  }, {
    at: 0.88,
    kind: 'slash',
    text: '/commit-push',
    resumeTo: 0.89
  }, {
    at: 0.90,
    kind: 'compact',
    text: '/compact',
    resumeTo: 1
  }];
  const KIND_META = {
    auto: {
      badge: 'auto',
      detail: 'Auto-loaded',
      badgeBg: 'rgba(94,93,89,0.15)',
      badgeColor: '#8A8880'
    },
    user: {
      badge: 'you',
      detail: 'You typed this',
      badgeBg: 'rgba(85,138,66,0.15)',
      badgeColor: '#6BA656'
    },
    claude: {
      badge: 'claude',
      detail: "Claude's work",
      badgeBg: 'rgba(217,119,87,0.12)',
      badgeColor: '#D97757'
    },
    hook: {
      badge: 'hook',
      detail: 'Hook (automatic)',
      badgeBg: 'rgba(184,134,11,0.15)',
      badgeColor: '#CCA020'
    },
    compact: {
      badge: 'compact',
      detail: 'Compaction',
      badgeBg: 'rgba(217,119,87,0.12)',
      badgeColor: '#D97757'
    },
    sub: {
      badge: 'subagent',
      detail: "In subagent's context",
      badgeBg: 'rgba(155,123,196,0.12)',
      badgeColor: '#9B7BC4'
    }
  };
  const LEGEND = [{
    c: '#6B6964',
    l: 'System'
  }, {
    c: '#6A9BCC',
    l: 'CLAUDE.md'
  }, {
    c: '#E8A45C',
    l: 'Memory'
  }, {
    c: '#D4A843',
    l: 'Skills'
  }, {
    c: '#9B7BC4',
    l: 'MCP'
  }, {
    c: '#4A9B8E',
    l: 'Rules'
  }, {
    c: '#558A42',
    l: 'You'
  }, {
    c: '#8A8880',
    l: 'Files'
  }, {
    c: '#A09E96',
    l: 'Output'
  }, {
    c: '#D97757',
    l: 'Claude'
  }, {
    c: '#B8860B',
    l: 'Hooks'
  }];
  const fmt = n => n >= 1000 ? (n / 1000).toFixed(1).replace(/\.0$/, '') + 'K' : n + '';
  const [time, setTime] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [hovIdx, setHovIdx] = useState(null);
  const [selIdx, setSelIdx] = useState(null);
  const [hovCat, setHovCat] = useState(null);
  const [gatesPassed, setGatesPassed] = useState(0);
  const [mounted, setMounted] = useState(false);
  const [hasInteracted, setHasInteracted] = useState(false);
  const lastRef = useRef(null);
  const scrollRef = useRef(null);
  const detailRef = useRef(null);
  useEffect(() => setMounted(true), []);
  const activeGate = GATES.find((g, i) => i >= gatesPassed && time >= g.at && time < g.resumeTo);
  useEffect(() => {
    if (!playing) return;
    let raf;
    let stopped = false;
    const tick = ts => {
      if (stopped) return;
      if (!lastRef.current) lastRef.current = ts;
      const dt = (ts - lastRef.current) / 1000;
      lastRef.current = ts;
      setTime(prev => {
        const next = prev + dt * 0.032;
        const gate = GATES.find((g, i) => i >= gatesPassed && next >= g.at && prev < g.resumeTo);
        if (gate) {
          stopped = true;
          setPlaying(false);
          return gate.at;
        }
        if (next >= 1) {
          stopped = true;
          setPlaying(false);
          return 1;
        }
        return next;
      });
      if (!stopped) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => {
      stopped = true;
      cancelAnimationFrame(raf);
      lastRef.current = null;
    };
  }, [playing, gatesPassed]);
  const sendPrompt = () => {
    if (!activeGate) return;
    const isCompact = activeGate.kind === 'compact';
    setGatesPassed(n => n + 1);
    setTime(activeGate.resumeTo);
    setSelIdx(null);
    setHovIdx(null);
    if (!isCompact) setPlaying(true);
  };
  const visibleCount = EVENTS.filter(e => e.t <= time).length;
  const preCompactVisible = useMemo(() => EVENTS.slice(0, visibleCount), [EVENTS, visibleCount]);
  const compactGateIdx = GATES.length - 1;
  const isCompacted = gatesPassed > compactGateIdx && preCompactVisible.some(e => e.kind === 'compact');
  const {visible, preCompactTotal} = useMemo(() => {
    const nonCompact = preCompactVisible.filter(e => e.kind !== 'compact');
    if (!isCompacted) {
      return {
        visible: preCompactVisible,
        preCompactTotal: 0
      };
    }
    {}
    const autoLoads = nonCompact.filter(e => e.kind === 'auto' && e.t < STARTUP_END && !e.noSurviveCompact);
    const summarized = nonCompact.filter(e => e.t >= STARTUP_END && e.kind !== 'sub');
    const sumTokens = summarized.reduce((s, e) => s + e.tokens, 0);
    const summaryBlock = {
      t: STARTUP_END,
      kind: 'compact',
      label: 'Conversation summary',
      tokens: Math.round(sumTokens * 0.12),
      color: '#A09E96',
      vis: 'hidden',
      desc: `All ${summarized.length} conversation events condensed into one structured summary. The summary keeps: your requests and intent, key technical concepts, files examined or modified with important code snippets, errors and how they were fixed, pending tasks, and current work. It replaces the verbatim conversation: full tool outputs and intermediate reasoning are gone. Claude can still reference the work but won't have the exact code it read earlier.`,
      link: '/en/how-claude-code-works#the-context-window'
    };
    return {
      visible: [...autoLoads, summaryBlock],
      preCompactTotal: nonCompact.reduce((s, e) => s + e.tokens, 0)
    };
  }, [preCompactVisible, isCompacted]);
  const {blocks, totalTokens} = useMemo(() => {
    const bl = visible.map((e, visIdx) => ({
      ...e,
      id: e.label + e.t,
      visIdx
    })).filter(e => e.tokens > 0 || e.label === 'Conversation summary');
    return {
      blocks: bl,
      totalTokens: bl.reduce((s, b) => s + b.tokens, 0)
    };
  }, [visible]);
  const subTotal = useMemo(() => visible.filter(e => e.kind === 'sub').reduce((s, e) => s + (e.subTokens || 0), 0), [visible]);
  useEffect(() => {
    if (!scrollRef.current) return;
    if (isCompacted) scrollRef.current.scrollTo({
      top: 0,
      behavior: 'smooth'
    }); else if (playing || activeGate) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [visible.length, !!activeGate, isCompacted]);
  const rootRef = useRef(null);
  const keyStateRef = useRef({});
  const [isFullscreen, setIsFullscreen] = useState(false);
  keyStateRef.current = {
    time,
    activeGate,
    sendPrompt,
    hasInteracted
  };
  useEffect(() => {
    const onFsChange = () => setIsFullscreen(!!document.fullscreenElement);
    document.addEventListener('fullscreenchange', onFsChange);
    return () => document.removeEventListener('fullscreenchange', onFsChange);
  }, []);
  const toggleFullscreen = () => {
    if (!rootRef.current) return;
    if (document.fullscreenElement) document.exitFullscreen(); else rootRef.current.requestFullscreen().catch(() => {});
  };
  useEffect(() => {
    const onKey = e => {
      const tag = e.target.tagName;
      if (tag === 'INPUT' || tag === 'BUTTON' || tag === 'TEXTAREA' || tag === 'SELECT' || e.target.isContentEditable) return;
      if (!rootRef.current) return;
      const rect = rootRef.current.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) return;
      if (rect.bottom < 0 || rect.top > window.innerHeight) return;
      if (e.code === 'Space') {
        const {time: t, activeGate: g, sendPrompt: send, hasInteracted: hi} = keyStateRef.current;
        if (!hi) return;
        e.preventDefault();
        if (t === 0) setPlaying(true); else if (g) send(); else if (t >= 1) {
          setTime(0);
          setGatesPassed(0);
          setSelIdx(null);
          setHovIdx(null);
          setPlaying(true);
        } else setPlaying(p => !p);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);
  const pct = totalTokens / MAX * 100;
  const barColor = pct > 75 ? '#D97757' : pct > 50 ? '#B8860B' : '#558A42';
  const activeIdx = selIdx !== null ? selIdx : hovIdx;
  const hovEvent = activeIdx !== null ? visible[activeIdx] : null;
  useEffect(() => {
    if (detailRef.current) detailRef.current.scrollTop = 0;
  }, [hovEvent]);
  const focusT = hovEvent ? hovEvent.t : time;
  const takeaway = isCompacted ? 'Compaction replaces the conversation with a structured summary. System prompt, CLAUDE.md, memory, and MCP tools reload automatically. The skill listing is the one exception. Only skills you actually invoked are preserved.' : focusT < STARTUP_END ? 'A lot loads before you type anything. CLAUDE.md, memory, skills, and MCP tools are all in context before your first prompt.' : focusT < 0.28 ? "Your prompt is tiny compared to what's already loaded. Most of Claude's context is project knowledge, not your words." : focusT < 0.50 ? 'Each file Claude reads grows the context. Path-scoped rules load automatically alongside matching files.' : focusT < 0.71 ? 'Hooks fire automatically on tool events. Output reaches Claude via additionalContext JSON. Exit code 2 surfaces stderr to Claude. Plain stdout on exit 0 goes to the debug log, not the transcript.' : focusT < 0.79 ? 'Follow-up questions keep building on the same context. Everything from earlier is still there.' : focusT < 0.87 ? "The subagent works in its own separate context window. None of its file reads touch yours. Only the final summary comes back." : focusT < 0.88 ? 'Bang commands run in your shell and prefix the output to your next message. Useful for grounding Claude in command results without it running them.' : focusT < 0.90 ? 'User-only skills stay out of context entirely until you invoke them. The skill index at startup only lists skills Claude can call on its own.' : '/compact summarizes the conversation to free space while keeping key information. In a real session, run it when context starts affecting performance or before a long new task.';
  const terminalView = isCompacted ? 'A "Conversation compacted" message. The summarization happens silently.' : focusT < STARTUP_END ? 'The input box, waiting for your first message. Everything above loads silently before you type anything.' : focusT < 0.28 ? 'Your prompt. Claude hasn\'t started working yet.' : focusT < 0.52 ? 'Your prompt and "Reading files...". Rules show as one-line "Loaded" notices, not their content.' : focusT < 0.72 ? "Claude's response and file diffs. Hooks fire silently. Tool output like npm test shows as a brief summary, not the full content." : focusT < 0.79 ? 'Your follow-up prompt.' : focusT < 0.86 ? "A brief notice that a subagent is working, then its result. You don't see the subagent's individual file reads." : focusT < 0.90 ? "Claude's response, your git status output, and the commit-push skill running." : 'Your full conversation. /compact is available to run.';
  const mono = 'var(--font-mono, ui-monospace, SFMono-Regular, Menlo, monospace)';
  const renderWithCode = s => s.split('`').map((part, i) => i % 2 === 1 ? <code key={i} style={{
    fontFamily: mono,
    fontSize: '0.92em',
    background: 'var(--cw-track)',
    padding: '1px 4px',
    borderRadius: 3
  }}>{part}</code> : part);
  if (!mounted) return null;
  return <>
    <div className="cw-mobile-fallback">
      This interactive timeline works best on a larger screen. See <a href="#what-the-timeline-shows" style={{
    color: '#D97757'
  }}>the written breakdown below</a> for the same concepts.
    </div>
    <div className="cw-root" ref={rootRef} onClickCapture={() => setHasInteracted(true)} style={isFullscreen ? {
    height: '100vh',
    borderRadius: 0,
    display: 'flex',
    flexDirection: 'column'
  } : {}}>
      <style>{`
        .cw-root {
          --cw-bg: #FAFAF8;
          --cw-text: #1A1918;
          --cw-text-2: #3D3C38;
          --cw-text-3: #5E5D59;
          --cw-text-dim: #6E6C64;
          --cw-text-faint: #8A8880;
          --cw-surface: rgba(0,0,0,0.025);
          --cw-surface-2: rgba(0,0,0,0.04);
          --cw-border: rgba(0,0,0,0.08);
          --cw-track: rgba(0,0,0,0.04);
          --cw-hover: rgba(0,0,0,0.04);
          --cw-rail: rgba(0,0,0,0.08);
          --cw-scrollbar: rgba(0,0,0,0.22);
          background: var(--cw-bg);
          border-radius: 12px;
          overflow: hidden;
          font-family: var(--font-sans, -apple-system, BlinkMacSystemFont, sans-serif);
          color: var(--cw-text);
          border: 1px solid var(--cw-border);
        }
        .dark .cw-root {
          --cw-bg: #111110;
          --cw-text: #E8E6DC;
          --cw-text-2: #B8B6AE;
          --cw-text-3: #9C9A92;
          --cw-text-dim: #8A8880;
          --cw-text-faint: #6E6C64;
          --cw-surface: rgba(255,255,255,0.02);
          --cw-surface-2: rgba(255,255,255,0.015);
          --cw-border: rgba(255,255,255,0.06);
          --cw-track: rgba(255,255,255,0.03);
          --cw-hover: rgba(255,255,255,0.04);
          --cw-rail: rgba(255,255,255,0.04);
          --cw-scrollbar: rgba(255,255,255,0.18);
        }
        .cw-scroll::-webkit-scrollbar { width: 6px; }
        .cw-scroll::-webkit-scrollbar-track { background: transparent; }
        .cw-scroll::-webkit-scrollbar-thumb { background: var(--cw-scrollbar); border-radius: 3px; }
        @keyframes cw-blink { 50% { opacity: 0; } }
        @keyframes cw-fadein { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }
        .cw-compacted-row { animation: cw-fadein 0.3s ease-out backwards; }
        .cw-mobile-fallback { display: none; padding: 14px 16px; border-radius: 8px; font-size: 14px; border: 1px solid rgba(0,0,0,0.1); background: rgba(0,0,0,0.03); }
        .dark .cw-mobile-fallback { border-color: rgba(255,255,255,0.15); background: rgba(255,255,255,0.04); }
        @media (max-width: 700px) {
          .cw-root { display: none !important; }
          .cw-mobile-fallback { display: block; }
        }
      `}</style>

      {}
      <div style={{
    padding: '16px 20px 12px',
    display: 'flex',
    alignItems: 'flex-end',
    gap: 24
  }}>
        <div style={{
    flex: 1,
    minWidth: 0
  }}>
          <div style={{
    fontSize: 18,
    fontWeight: 600,
    letterSpacing: -0.3,
    lineHeight: 1
  }}>
            Explore the context window
          </div>
          <div style={{
    fontSize: 14,
    color: 'var(--cw-text-dim)',
    marginTop: 4
  }}>
            A simulated session showing what enters context and what it costs
          </div>
        </div>
        <div style={{
    textAlign: 'right',
    flexShrink: 0
  }}>
          <div style={{
    fontFamily: mono,
    fontSize: 20,
    fontWeight: 600,
    color: barColor,
    letterSpacing: -0.5,
    lineHeight: 1
  }}>
            ~{fmt(totalTokens)}<span style={{
    fontSize: 15,
    fontWeight: 500,
    marginLeft: 4
  }}>tokens</span>
          </div>
          <div style={{
    fontFamily: mono,
    fontSize: 13,
    color: 'var(--cw-text-dim)',
    marginTop: 2
  }} title="Token counts are illustrative. Actual values vary with your CLAUDE.md size, MCP servers, and file lengths.">
            / {fmt(MAX)} · illustrative
          </div>
        </div>
      </div>

      {}
      <div style={{
    padding: '0 20px'
  }}>
        <div style={{
    height: 4,
    borderRadius: 2,
    background: 'var(--cw-track)',
    overflow: 'hidden',
    marginBottom: 6
  }}>
          <div style={{
    width: pct + '%',
    height: '100%',
    background: barColor,
    transition: 'width 0.6s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s'
  }} />
        </div>
        <div style={{
    height: 28,
    borderRadius: 5,
    background: 'var(--cw-track)',
    border: '1px solid var(--cw-border)',
    overflow: 'hidden',
    display: 'flex'
  }}>
          {blocks.map((b, i) => {
    const w = Math.max(b.tokens / MAX * 100, 0.15);
    const isHov = b.visIdx === activeIdx;
    const catMatch = hovCat && b.color === hovCat;
    const dimmed = hovCat ? !catMatch : activeIdx !== null && !isHov;
    return <div key={b.id} onMouseEnter={() => setHovIdx(b.visIdx)} onMouseLeave={() => setHovIdx(null)} onClick={() => setSelIdx(selIdx === b.visIdx ? null : b.visIdx)} style={{
      width: w + '%',
      height: '100%',
      background: b.color,
      opacity: isHov || catMatch ? 1 : dimmed ? 0.25 : 0.65,
      borderRight: i < blocks.length - 1 ? '0.5px solid var(--cw-border)' : 'none',
      transition: 'opacity 0.15s',
      cursor: 'pointer'
    }} />;
  })}
        </div>
        <div style={{
    display: 'flex',
    gap: 12,
    marginTop: 6,
    flexWrap: 'wrap',
    justifyContent: 'space-between'
  }}>
          <div style={{
    display: 'flex',
    gap: 12,
    flexWrap: 'wrap'
  }}>
            {LEGEND.map(x => {
    const active = hovCat === x.c;
    return <div key={x.l} onMouseEnter={() => setHovCat(x.c)} onMouseLeave={() => setHovCat(null)} style={{
      display: 'flex',
      alignItems: 'center',
      gap: 4,
      padding: '2px 6px',
      borderRadius: 4,
      cursor: 'pointer',
      background: active ? 'var(--cw-hover)' : 'transparent',
      transition: 'background 0.1s'
    }}>
                  <div style={{
      width: 6,
      height: 6,
      borderRadius: 1.5,
      background: x.c,
      opacity: active ? 1 : 0.7
    }} />
                  <span style={{
      fontSize: 12,
      color: active ? 'var(--cw-text)' : 'var(--cw-text-dim)'
    }}>{x.l}</span>
                </div>;
  })}
          </div>
          <div style={{
    display: 'flex',
    gap: 6,
    alignItems: 'center',
    fontSize: 12,
    color: 'var(--cw-text-dim)'
  }}>
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#558A42" strokeWidth="2.5">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" />
            </svg>
            <span>= appears in your terminal</span>
          </div>
        </div>
      </div>

      {}
      <div style={{
    display: 'flex',
    padding: '14px 20px 0',
    gap: 16,
    height: isFullscreen ? 'calc(100vh - 240px)' : 420
  }}>

        {}
        <div ref={scrollRef} className="cw-scroll" style={{
    flex: 1,
    minWidth: 0,
    overflowY: 'auto',
    paddingRight: 8,
    scrollBehavior: 'smooth'
  }}>
          {visible.length === 0 && !playing && <div style={{
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 16
  }}>
              <div style={{
    fontFamily: mono,
    fontSize: 16,
    color: 'var(--cw-text-dim)',
    display: 'flex',
    alignItems: 'center',
    gap: 8
  }}>
                <span style={{
    color: 'var(--cw-text-faint)'
  }}>$</span>
                <span>claude</span>
                <span style={{
    display: 'inline-block',
    width: 8,
    height: 16,
    background: 'var(--cw-text-dim)',
    opacity: 0.5,
    animation: 'cw-blink 1s step-end infinite'
  }} />
              </div>
              <button onClick={() => setPlaying(true)} style={{
    padding: '10px 20px',
    borderRadius: 8,
    border: '1px solid rgba(217,119,87,0.3)',
    background: 'rgba(217,119,87,0.08)',
    color: '#D97757',
    fontSize: 15,
    fontWeight: 600,
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    gap: 8
  }}>
                <span>▶</span>
                <span>Start session</span>
              </button>
              <div style={{
    fontSize: 13,
    color: 'var(--cw-text-faint)',
    maxWidth: 280,
    textAlign: 'center',
    lineHeight: 1.5
  }}>
                Watch what loads into context, from the moment you run <code style={{
    fontFamily: mono
  }}>claude</code> through a full conversation.
              </div>
            </div>}
          {isCompacted && <div style={{
    marginBottom: 10,
    padding: '10px 12px',
    borderRadius: 6,
    background: 'rgba(217,119,87,0.05)',
    border: '1px solid rgba(217,119,87,0.15)'
  }}>
              <div style={{
    fontSize: 13,
    fontWeight: 600,
    color: '#D97757',
    marginBottom: 3
  }}>
                After /compact
              </div>
              <div style={{
    fontSize: 13,
    color: 'var(--cw-text-3)',
    lineHeight: 1.5,
    fontFamily: mono
  }}>
                {fmt(preCompactTotal)} → {fmt(totalTokens)} tokens · freed {fmt(preCompactTotal - totalTokens)}
              </div>
              <div style={{
    fontSize: 13,
    color: 'var(--cw-text-dim)',
    lineHeight: 1.5,
    marginTop: 4
  }}>
                This is what's left in context: startup content, which lives outside the message history and reloads after compaction, plus a structured summary of the entire conversation. Skill descriptions don't reload.
              </div>
            </div>}
          {time > 0 && visible.length > 0 && <div style={{
    fontSize: 12,
    fontWeight: 700,
    color: 'var(--cw-text-faint)',
    textTransform: 'uppercase',
    letterSpacing: 0.6,
    marginBottom: 6,
    paddingLeft: 28
  }}>
              {isCompacted ? 'Reloaded after compact' : 'Before you type anything'}
            </div>}

          {time > 0 && visible.map((evt, i) => {
    const meta = KIND_META[evt.kind];
    const isHov = hovIdx === i;
    const prevKind = i > 0 ? visible[i - 1].kind : null;
    const isSub = evt.kind === 'sub';
    const enteringSubagent = isSub && prevKind !== 'sub';
    const leavingSubagent = prevKind === 'sub' && !isSub;
    let showPhase = null;
    if (evt.kind === 'user' && prevKind !== 'user') showPhase = 'You'; else if (evt.kind === 'claude' && prevKind === 'user') showPhase = 'Claude works'; else if (evt.label === 'Conversation summary') showPhase = 'Summarized by /compact';
    const isNewRow = isCompacted && !(evt.kind === 'auto' && evt.t < STARTUP_END);
    return <div key={evt.label + evt.t} className={isNewRow ? 'cw-compacted-row' : ''} style={isNewRow ? {
      animationDelay: `${i * 60}ms`
    } : {}}>
                {showPhase && <div style={{
      fontSize: 12,
      fontWeight: 700,
      color: 'var(--cw-text-faint)',
      textTransform: 'uppercase',
      letterSpacing: 0.6,
      marginTop: 14,
      marginBottom: 6,
      paddingLeft: 28
    }}>
                    {showPhase}
                  </div>}
                {enteringSubagent && <div style={{
      marginLeft: 28,
      marginTop: 6,
      marginBottom: 2,
      paddingLeft: 10,
      borderLeft: '2px solid rgba(155,123,196,0.4)',
      fontSize: 12,
      fontWeight: 600,
      color: '#9B7BC4',
      textTransform: 'uppercase',
      letterSpacing: 0.5
    }}>
                    Subagent's separate context window
                  </div>}
                {leavingSubagent && <div style={{
      marginLeft: 28,
      marginBottom: 6,
      paddingLeft: 10,
      paddingBottom: 6,
      borderLeft: '2px solid rgba(155,123,196,0.4)',
      fontSize: 12,
      color: 'var(--cw-text-dim)',
      fontFamily: mono
    }}>
                    ↓ {fmt(subTotal)} tokens stayed in subagent's context · only the summary returns
                  </div>}
                <div onMouseEnter={() => setHovIdx(i)} onMouseLeave={() => setHovIdx(null)} onClick={() => setSelIdx(selIdx === i ? null : i)} style={{
      display: 'flex',
      alignItems: 'flex-start',
      borderRadius: 6,
      cursor: 'pointer',
      background: selIdx === i || isHov ? 'var(--cw-hover)' : 'transparent',
      outline: selIdx === i ? '1px solid rgba(217,119,87,0.4)' : 'none',
      opacity: hovCat && evt.color !== hovCat ? 0.35 : 1,
      transition: 'background 0.1s, opacity 0.15s',
      marginLeft: isSub ? 28 : 0,
      paddingLeft: isSub ? 10 : 0,
      borderLeft: isSub ? '2px solid rgba(155,123,196,0.4)' : 'none'
    }}>
                  <div style={{
      width: 28,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      paddingTop: 8,
      flexShrink: 0
    }}>
                    <div style={{
      width: evt.kind === 'user' || evt.kind === 'compact' ? 10 : 7,
      height: evt.kind === 'user' || evt.kind === 'compact' ? 10 : 7,
      borderRadius: '50%',
      background: evt.color,
      opacity: isHov ? 1 : 0.6,
      transition: 'opacity 0.15s',
      boxShadow: isHov ? `0 0 8px ${evt.color}40` : 'none'
    }} />
                    {i < visible.length - 1 && <div style={{
      width: 1.5,
      flex: 1,
      background: 'var(--cw-rail)',
      marginTop: 2,
      minHeight: 6
    }} />}
                  </div>
                  <div style={{
      flex: 1,
      minWidth: 0,
      padding: '5px 10px 5px 4px',
      display: 'flex',
      alignItems: 'center',
      gap: 8
    }}>
                    <span style={{
      fontSize: 12,
      fontWeight: 600,
      padding: '1px 5px',
      borderRadius: 3,
      background: meta.badgeBg,
      color: meta.badgeColor,
      flexShrink: 0,
      fontFamily: mono
    }}>
                      {meta.badge}
                    </span>
                    <span style={{
      fontSize: 15,
      fontFamily: mono,
      color: isHov ? 'var(--cw-text)' : evt.kind === 'user' ? '#558A42' : evt.kind === 'auto' ? 'var(--cw-text-dim)' : 'var(--cw-text-2)',
      flex: 1,
      minWidth: 0,
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap',
      fontWeight: evt.kind === 'user' ? 550 : 400
    }}>
                      {evt.label}
                    </span>
                    {evt.tokens > 0 && <span style={{
      fontSize: 12,
      fontFamily: mono,
      color: 'var(--cw-text-faint)',
      flexShrink: 0
    }}>
                        +{fmt(evt.tokens)}
                      </span>}
                    {evt.subTokens > 0 && <span style={{
      fontSize: 12,
      fontFamily: mono,
      color: '#9B7BC4',
      flexShrink: 0,
      opacity: 0.6
    }}>
                        +{fmt(evt.subTokens)}
                      </span>}
                    {evt.tokens > 0 && <div style={{
      width: 50,
      height: 5,
      borderRadius: 2,
      background: 'var(--cw-track)',
      flexShrink: 0,
      overflow: 'hidden'
    }}>
                        <div style={{
      width: Math.min(evt.tokens / 5000 * 100, 100) + '%',
      height: '100%',
      background: evt.color,
      opacity: isHov ? 0.8 : 0.4,
      transition: 'opacity 0.15s'
    }} />
                      </div>}
                    <span style={{
      width: 14,
      flexShrink: 0,
      display: 'flex',
      justifyContent: 'center'
    }} title={VIS_META[evt.vis].label}>
                      {evt.vis !== 'hidden' && <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke={evt.vis === 'full' ? '#558A42' : 'currentColor'} style={{
      color: 'var(--cw-text-faint)',
      opacity: evt.vis === 'full' ? 1 : 0.5
    }} strokeWidth="2">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" />
                        </svg>}
                    </span>
                  </div>
                </div>
              </div>;
  })}

          {activeGate && (activeGate.kind === 'prompt' || activeGate.kind === 'bang' || activeGate.kind === 'slash') && <div style={{
    paddingLeft: 28,
    marginTop: 12,
    paddingRight: 8
  }}>
              <div style={{
    fontSize: 11,
    fontWeight: 600,
    color: '#6BA656',
    fontFamily: mono,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: 4,
    paddingLeft: 2
  }}>
                You type in your terminal
              </div>
              <div style={{
    display: 'flex',
    alignItems: 'flex-start',
    gap: 8,
    padding: '10px 12px',
    borderRadius: 6,
    background: 'rgba(85,138,66,0.06)',
    border: '1px solid rgba(85,138,66,0.2)'
  }}>
                <span style={{
    color: '#558A42',
    fontSize: 15,
    fontFamily: mono,
    flexShrink: 0
  }}>❯</span>
                <span style={{
    fontSize: 15,
    fontFamily: mono,
    color: 'var(--cw-text-2)',
    flex: 1,
    lineHeight: 1.5
  }}>
                  {activeGate.text}
                  <span style={{
    display: 'inline-block',
    width: 7,
    height: 13,
    marginLeft: 2,
    background: '#558A42',
    opacity: 0.5,
    verticalAlign: 'middle',
    animation: 'cw-blink 1s step-end infinite'
  }} />
                </span>
                <button onClick={sendPrompt} style={{
    padding: '5px 12px',
    borderRadius: 5,
    border: 'none',
    background: '#558A42',
    color: '#fff',
    fontSize: 13,
    fontWeight: 600,
    cursor: 'pointer',
    flexShrink: 0
  }}>
                  {activeGate.kind === 'prompt' ? 'Send ↵' : 'Run ↵'}
                </button>
              </div>
            </div>}
          {activeGate && activeGate.kind === 'compact' && <div style={{
    paddingLeft: 28,
    marginTop: 12,
    paddingRight: 8
  }}>
              <div style={{
    padding: '12px 14px',
    borderRadius: 6,
    background: 'rgba(217,119,87,0.06)',
    border: '1px solid rgba(217,119,87,0.25)'
  }}>
                <div style={{
    fontSize: 13,
    color: 'var(--cw-text-3)',
    marginBottom: 8,
    lineHeight: 1.5
  }}>
                  Context is at <span style={{
    fontFamily: mono,
    fontWeight: 600,
    color: barColor
  }}>{fmt(totalTokens)} tokens</span>.
                  Run <code style={{
    fontFamily: mono,
    background: 'var(--cw-track)',
    padding: '1px 4px',
    borderRadius: 3
  }}>/compact</code> to
                  summarize older exchanges and free space for more work.
                </div>
                <div style={{
    display: 'flex',
    alignItems: 'center',
    gap: 8
  }}>
                  <span style={{
    color: '#D97757',
    fontSize: 15,
    fontFamily: mono
  }}>❯</span>
                  <span style={{
    fontSize: 15,
    fontFamily: mono,
    color: 'var(--cw-text-2)',
    flex: 1
  }}>
                    {activeGate.text}
                  </span>
                  <button onClick={sendPrompt} style={{
    padding: '5px 12px',
    borderRadius: 5,
    border: 'none',
    background: '#D97757',
    color: '#fff',
    fontSize: 13,
    fontWeight: 600,
    cursor: 'pointer',
    flexShrink: 0
  }}>
                    Run ↵
                  </button>
                </div>
              </div>
            </div>}
        </div>

        {}
        <div style={{
    width: 300,
    flexShrink: 0,
    display: 'flex',
    flexDirection: 'column'
  }}>
          <div ref={detailRef} className="cw-scroll" style={{
    padding: '14px 16px',
    borderRadius: 10,
    background: 'var(--cw-surface)',
    border: '1px solid var(--cw-border)',
    flex: 1,
    minHeight: 0,
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
    gap: 10
  }}>
            {hovEvent ? <div>
                <div style={{
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    marginBottom: 8
  }}>
                  <div style={{
    width: 10,
    height: 10,
    borderRadius: 3,
    background: hovEvent.color,
    opacity: 0.8
  }} />
                  <span style={{
    fontSize: 16,
    fontWeight: 600
  }}>{hovEvent.label}</span>
                </div>
                <div style={{
    display: 'flex',
    width: 'fit-content',
    padding: '3px 8px',
    borderRadius: 4,
    marginBottom: 8,
    background: KIND_META[hovEvent.kind].badgeBg
  }}>
                  <span style={{
    fontSize: 12,
    fontWeight: 600,
    color: KIND_META[hovEvent.kind].badgeColor
  }}>
                    {KIND_META[hovEvent.kind].detail}
                  </span>
                </div>
                {hovEvent.tokens > 0 && <div style={{
    fontSize: 14,
    fontFamily: mono,
    color: 'var(--cw-text-dim)',
    marginBottom: 6
  }}>
                    {fmt(hovEvent.tokens)} tokens
                  </div>}
                {hovEvent.subTokens > 0 && <div style={{
    fontSize: 14,
    fontFamily: mono,
    color: '#9B7BC4',
    marginBottom: 6
  }}>
                    {fmt(hovEvent.subTokens)} tokens in the subagent's context
                  </div>}
                <p style={{
    fontSize: 15,
    color: 'var(--cw-text-3)',
    lineHeight: 1.55,
    margin: 0
  }}>
                  {renderWithCode(hovEvent.desc)}
                </p>
                <div style={{
    marginTop: 10,
    padding: '8px 10px',
    borderRadius: 6,
    background: hovEvent.vis === 'full' ? 'rgba(85,138,66,0.08)' : 'var(--cw-surface-2)',
    border: '1px solid ' + (hovEvent.vis === 'full' ? 'rgba(85,138,66,0.2)' : 'var(--cw-border)')
  }}>
                  <div style={{
    display: 'flex',
    alignItems: 'center',
    gap: 6,
    marginBottom: 3
  }}>
                    <span style={{
    fontSize: 13,
    color: hovEvent.vis === 'full' ? '#558A42' : 'var(--cw-text-dim)'
  }}>
                      {hovEvent.vis === 'full' ? '●' : hovEvent.vis === 'brief' ? '◐' : '○'}
                    </span>
                    <span style={{
    fontSize: 12,
    fontWeight: 600,
    color: 'var(--cw-text-2)'
  }}>
                      {VIS_META[hovEvent.vis].label}
                    </span>
                  </div>
                  <div style={{
    fontSize: 13,
    color: 'var(--cw-text-dim)',
    lineHeight: 1.4
  }}>
                    {VIS_META[hovEvent.vis].sub}
                  </div>
                </div>
                {hovEvent.tip && <div style={{
    marginTop: 10,
    padding: '8px 10px',
    borderRadius: 6,
    background: 'rgba(85,138,66,0.06)',
    border: '1px solid rgba(85,138,66,0.15)'
  }}>
                    <div style={{
    fontSize: 12,
    fontWeight: 600,
    color: '#558A42',
    marginBottom: 3,
    display: 'flex',
    alignItems: 'center',
    gap: 4
  }}>
                      <span>💡</span> Save context
                    </div>
                    <div style={{
    fontSize: 13,
    color: 'var(--cw-text-3)',
    lineHeight: 1.5
  }}>
                      {renderWithCode(hovEvent.tip)}
                    </div>
                  </div>}
                {hovEvent.link && <a href={hovEvent.link} style={{
    display: 'inline-block',
    marginTop: 10,
    fontSize: 13,
    color: '#D97757',
    textDecoration: 'none',
    borderBottom: '1px solid rgba(217,119,87,0.3)'
  }}>
                    Learn more →
                  </a>}
              </div> : <div style={{
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    textAlign: 'center',
    gap: 4,
    padding: '12px 0 4px'
  }}>
                <div style={{
    fontSize: 22,
    opacity: 0.2
  }}>👁</div>
                <div style={{
    fontSize: 14,
    fontWeight: 500,
    color: 'var(--cw-text-dim)'
  }}>Hover or click any event</div>
                <div style={{
    fontSize: 12,
    color: 'var(--cw-text-faint)',
    lineHeight: 1.4,
    maxWidth: 200
  }}>
                  Hover to preview. Click to pin so you can scroll.
                </div>
              </div>}

            <div style={{
    padding: '10px 12px',
    borderRadius: 8,
    background: 'rgba(217,119,87,0.05)',
    border: '1px solid rgba(217,119,87,0.12)'
  }}>
              <div style={{
    fontSize: 11,
    fontWeight: 700,
    color: '#D97757',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: 3
  }}>
                Key takeaway
              </div>
              <div style={{
    fontSize: 13,
    color: 'var(--cw-text-3)',
    lineHeight: 1.5
  }}>
                {takeaway}
              </div>
            </div>

            <div style={{
    padding: '10px 12px',
    borderRadius: 8,
    background: 'var(--cw-surface-2)',
    border: '1px solid var(--cw-border)'
  }}>
              <div style={{
    fontSize: 11,
    fontWeight: 700,
    color: 'var(--cw-text-dim)',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: 3
  }}>
                In your terminal you see
              </div>
              <div style={{
    fontSize: 13,
    color: 'var(--cw-text-3)',
    lineHeight: 1.5
  }}>
                {terminalView}
              </div>
            </div>
          </div>
        </div>
      </div>

      {}
      <div style={{
    padding: '10px 20px 14px',
    display: 'flex',
    alignItems: 'center',
    gap: 10
  }}>
        <button aria-label={time >= 1 ? 'Restart' : activeGate ? 'Continue' : playing ? 'Pause' : 'Play'} onClick={() => {
    if (time >= 1) {
      setTime(0);
      setGatesPassed(0);
      setSelIdx(null);
      setHovIdx(null);
      setPlaying(true);
    } else if (activeGate) sendPrompt(); else setPlaying(!playing);
  }} style={{
    width: 30,
    height: 30,
    borderRadius: 6,
    border: 'none',
    background: 'rgba(217,119,87,0.1)',
    color: '#D97757',
    cursor: 'pointer',
    fontSize: 15,
    fontWeight: 700,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>
          {time >= 1 ? '↺' : playing ? '⏸' : '▶'}
        </button>
        <div style={{
    flex: 1,
    height: 3,
    borderRadius: 2,
    background: 'var(--cw-track)',
    overflow: 'hidden'
  }}>
          <div style={{
    width: time * 100 + '%',
    height: '100%',
    background: '#D97757',
    transition: 'width 0.1s linear'
  }} />
        </div>
        <span style={{
    fontSize: 12,
    fontFamily: mono,
    color: 'var(--cw-text-faint)',
    minWidth: 30
  }}>
          {Math.round(time * 100)}%
        </span>
        <button onClick={toggleFullscreen} aria-label={isFullscreen ? 'Exit fullscreen' : 'Enter fullscreen'} title={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'} style={{
    width: 28,
    height: 28,
    borderRadius: 6,
    border: '1px solid var(--cw-border)',
    background: 'var(--cw-surface)',
    color: 'var(--cw-text-dim)',
    cursor: 'pointer',
    fontSize: 15,
    flexShrink: 0,
    marginLeft: 4,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>
          {isFullscreen ? '⤡' : '⛶'}
        </button>
      </div>
    </div>
    </>;
};

Claude Code's context window holds everything Claude knows about your session: your instructions, the files it reads, its own responses, and content that never appears in your terminal. The timeline below walks through what loads and when. See [the written breakdown](#what-the-timeline-shows) for the same content as a list.

<ContextWindow />

## What the timeline shows

The session walks through a realistic flow with representative token counts:

* **Before you type anything**: CLAUDE.md, auto memory, MCP tool names, and skill descriptions all load into context. Your own setup may add more here, like an [output style](/en/output-styles) or text from [`--append-system-prompt`](/en/cli-reference), which both go into the system prompt the same way.
* **As Claude works**: each file read adds to context, [path-scoped rules](/en/memory#path-specific-rules) load automatically alongside matching files, and a [PostToolUse hook](/en/hooks-guide) fires after each edit.
* **The follow-up prompt**: a [subagent](/en/sub-agents) handles the research in its own separate context window, so the large file reads stay out of yours. Only the summary and a small metadata trailer come back.
* **At the end**: `/compact` replaces the conversation with a structured summary. Most startup content reloads automatically; the table below shows what happens to each mechanism.

## What survives compaction

When a long session compacts, Claude Code summarizes the conversation history to fit the context window. What happens to your instructions depends on how they were loaded:

| Mechanism                                 | After compaction                                                                            |
| :---------------------------------------- | :------------------------------------------------------------------------------------------ |
| System prompt and output style            | Unchanged; not part of message history                                                      |
| Project-root CLAUDE.md and unscoped rules | Re-injected from disk                                                                       |
| Auto memory                               | Re-injected from disk                                                                       |
| Rules with `paths:` frontmatter           | Lost until a matching file is read again                                                    |
| Nested CLAUDE.md in subdirectories        | Lost until a file in that subdirectory is read again                                        |
| Invoked skill bodies                      | Re-injected, capped at 5,000 tokens per skill and 25,000 tokens total; oldest dropped first |
| Hooks                                     | Not applicable; hooks run as code, not context                                              |

Path-scoped rules and nested CLAUDE.md files load into message history when their trigger file is read, so compaction summarizes them away with everything else. They reload the next time Claude reads a matching file. If a rule must persist across compaction, drop the `paths:` frontmatter or move it to the project-root CLAUDE.md.

Skill bodies are re-injected after compaction, but large skills are truncated to fit the per-skill cap, and the oldest invoked skills are dropped once the total budget is exceeded. Truncation keeps the start of the file, so put the most important instructions near the top of `SKILL.md`.

## Check your own session

The visualization uses representative numbers. To see your actual context usage at any point, run `/context` for a live breakdown by category with optimization suggestions. Run `/memory` to check which CLAUDE.md and auto memory files loaded at startup.

## Related resources

For deeper coverage of the features shown in the timeline, see these pages:

* [Extend Claude Code](/en/features-overview): when to use CLAUDE.md vs skills vs rules vs hooks vs MCP
* [Store instructions and memories](/en/memory): CLAUDE.md hierarchy and auto memory
* [Subagents](/en/sub-agents): delegate research to a separate context window
* [Best practices](/en/best-practices): managing context as your primary constraint
* [Reduce token usage](/en/costs#reduce-token-usage): strategies for keeping context usage low


---

# 擴展 Claude Code

> 了解何時使用 CLAUDE.md、Skills、subagents、hooks、MCP 和 plugins。

Claude Code 結合了一個能夠推理您程式碼的模型與[內建工具](/zh-TW/how-claude-code-works#tools)，用於檔案操作、搜尋、執行和網路存取。內建工具涵蓋了大多數編碼任務。本指南涵蓋擴展層：您添加的功能，用於自訂 Claude 的知識、將其連接到外部服務，以及自動化工作流程。

<Note>
  有關核心代理迴圈如何運作的資訊，請參閱[Claude Code 如何運作](/zh-TW/how-claude-code-works)。
</Note>

**初次使用 Claude Code？** 從[CLAUDE.md](/zh-TW/memory)開始了解專案約定，然後根據特定觸發器添加其他擴展。

## 概述

擴展插入代理迴圈的不同部分：

* **[CLAUDE.md](/zh-TW/memory)** 添加 Claude 在每個會話中看到的持久上下文
* **[Skills](/zh-TW/skills)** 添加可重複使用的知識和可調用的工作流程
* **[MCP](/zh-TW/mcp)** 將 Claude 連接到外部服務和工具
* **[Subagents](/zh-TW/sub-agents)** 在隔離的上下文中運行自己的迴圈，返回摘要
* **[Agent teams](/zh-TW/agent-teams)** 協調多個獨立會話，具有共享任務和點對點訊息傳遞
* **[Hooks](/zh-TW/hooks-guide)** 在生命週期事件上觸發，可以運行指令碼、HTTP 請求、提示或 subagent
* **[Plugins](/zh-TW/plugins)** 和 **[marketplaces](/zh-TW/plugin-marketplaces)** 打包和分發這些功能

[Skills](/zh-TW/skills)是最靈活的擴展。Skill 是一個包含知識、工作流程或指令的 markdown 檔案。您可以使用像 `/deploy` 這樣的命令調用 skills，或者 Claude 可以在相關時自動載入它們。Skills 可以在您目前的對話中運行，或通過 subagents 在隔離的上下文中運行。

## 將功能與您的目標相匹配

功能範圍從 Claude 在每個會話中看到的始終開啟的上下文，到您或 Claude 可以調用的按需功能，再到在特定事件上運行的背景自動化。下表顯示了可用的功能以及何時使用每一個。

| 功能                                    | 它的作用                           | 何時使用                  | 範例                                        |
| ------------------------------------- | ------------------------------ | --------------------- | ----------------------------------------- |
| **CLAUDE.md**                         | 每次對話載入的持久上下文                   | 專案約定、「始終執行 X」規則       | 「使用 pnpm，而不是 npm。在提交前運行測試。」               |
| **Skill**                             | Claude 可以使用的指令、知識和工作流程         | 可重複使用的內容、參考文件、可重複的任務  | `/deploy` 運行您的部署檢查清單；包含端點模式的 API 文件 skill |
| **Subagent**                          | 返回摘要結果的隔離執行上下文                 | 上下文隔離、並行任務、專門的工作者     | 讀取許多檔案但僅返回關鍵發現的研究任務                       |
| **[Agent teams](/zh-TW/agent-teams)** | 協調多個獨立的 Claude Code 會話         | 並行研究、新功能開發、使用競爭假設進行除錯 | 生成審查者以同時檢查安全性、效能和測試                       |
| **MCP**                               | 連接到外部服務                        | 外部資料或操作               | 查詢您的資料庫、發佈到 Slack、控制瀏覽器                   |
| **Hook**                              | 由事件觸發的指令碼、HTTP 請求、提示或 subagent | 必須在每個匹配事件上運行的自動化      | 在每次檔案編輯後運行 ESLint                         |

**[Plugins](/zh-TW/plugins)** 是打包層。Plugin 將 skills、hooks、subagents 和 MCP servers 捆綁到單個可安裝單元中。Plugin skills 是命名空間的（如 `/my-plugin:review`），因此多個 plugins 可以共存。當您想在多個儲存庫中重複使用相同的設置或通過 **[marketplace](/zh-TW/plugin-marketplaces)** 分發給他人時，使用 plugins。

### 隨著時間推移構建您的設置

您不需要預先配置所有內容。每個功能都有一個可識別的觸發器，大多數團隊大致按以下順序添加它們：

| 觸發器                          | 添加                                   |
| :--------------------------- | :----------------------------------- |
| Claude 兩次出錯的約定或命令            | 將其添加到 [CLAUDE.md](/zh-TW/memory)     |
| 您一直在輸入相同的提示來啟動任務             | 將其保存為使用者可調用的 [skill](/zh-TW/skills)  |
| 您第三次將相同的劇本或多步驟程序粘貼到聊天中       | 將其捕獲為 [skill](/zh-TW/skills)         |
| 您一直在從 Claude 無法看到的瀏覽器選項卡複製資料 | 將該系統連接為 [MCP server](/zh-TW/mcp)     |
| 一個附帶任務用您不會再次參考的輸出淹沒您的對話      | 通過 [subagent](/zh-TW/sub-agents) 路由它 |
| 您希望每次都發生某事而無需詢問              | 編寫 [hook](/zh-TW/hooks-guide)        |
| 第二個儲存庫需要相同的設置                | 將其打包為 [plugin](/zh-TW/plugins)       |

相同的觸發器告訴您何時更新您已經擁有的內容。重複的錯誤或反覆出現的審查評論是 CLAUDE.md 編輯，而不是聊天中的一次性更正。您一直手動調整的工作流程是需要另一次修訂的 skill。

### 比較相似的功能

某些功能可能看起來相似。以下是如何區分它們。

<Tabs>
  <Tab title="Skill vs Subagent">
    Skills 和 subagents 解決不同的問題：

    * **Skills** 是可重複使用的內容，您可以將其載入任何上下文
    * **Subagents** 是與您的主要對話分開運行的隔離工作者

    | 方面                                   | Skill            | Subagent              |
    | ------------------------------------ | ---------------- | --------------------- |
    | **它是什麼**                             | 可重複使用的指令、知識或工作流程 | 具有自己上下文的隔離工作者         |
    | **主要優勢**                             | 在上下文之間共享內容       | 上下文隔離。工作單獨進行，僅返回摘要    |
    | **[上下文視窗](/zh-TW/context-window)影響** | 添加到您的主視窗         | 使用具有自己輸入和輸出令牌的單獨視窗    |
    | **最適合**                              | 參考資料、可調用的工作流程    | 讀取許多檔案的任務、並行工作、專門的工作者 |

    **Skills 可以是參考或操作。** 參考 skills 提供 Claude 在整個會話中使用的知識（如您的 API 風格指南）。操作 skills 告訴 Claude 執行特定操作（如運行您的部署工作流程的 `/deploy`）。

    **當您需要上下文隔離或您的上下文視窗變滿時，使用 subagent**。Subagent 可能讀取數十個檔案或運行廣泛的搜尋，但您的主要對話僅接收摘要。由於 subagent 工作不消耗您的主要上下文，當您不需要中間工作保持可見時，這也很有用。自訂 subagents 可以有自己的指令，並可以預載 skills。

    **它們可以結合。** Subagent 可以預載特定 skills（`skills:` 欄位）。Skill 可以使用 `context: fork` 在隔離的上下文中運行。有關詳細資訊，請參閱 [Skills](/zh-TW/skills)。
  </Tab>

  <Tab title="CLAUDE.md vs Skill">
    兩者都存儲指令，但它們的載入方式和用途不同。

    | 方面           | CLAUDE.md       | Skill           |
    | ------------ | --------------- | --------------- |
    | **載入**       | 每個會話，自動         | 按需              |
    | **可以包含檔案**   | 是，使用 `@path` 匯入 | 是，使用 `@path` 匯入 |
    | **可以觸發工作流程** | 否               | 是，使用 `/<name>`  |
    | **最適合**      | 「始終執行 X」規則      | 參考資料、可調用的工作流程   |

    **如果 Claude 應該始終知道它，請將其放在 CLAUDE.md 中**：編碼約定、構建命令、專案結構、「永遠不要執行 X」規則。

    **如果它是 Claude 有時需要的參考資料（API 文件、風格指南）或您使用 `/<name>` 觸發的工作流程（部署、審查、發佈），請將其放在 skill 中**。

    **經驗法則：** 保持 CLAUDE.md 在 200 行以下。如果它在增長，將參考內容移動到 skills 或拆分為 [`.claude/rules/`](/zh-TW/memory#organize-rules-with-clauderules) 檔案。
  </Tab>

  <Tab title="CLAUDE.md vs Rules vs Skills">
    所有三者都存儲指令，但它們的載入方式不同：

    | 方面      | CLAUDE.md | `.claude/rules/` | Skill         |
    | ------- | --------- | ---------------- | ------------- |
    | **載入**  | 每個會話      | 每個會話，或在打開匹配檔案時   | 按需，在調用或相關時    |
    | **範圍**  | 整個專案      | 可以限定到檔案路徑        | 特定於任務         |
    | **最適合** | 核心約定和構建命令 | 特定於語言或目錄的指南      | 參考資料、可重複的工作流程 |

    **使用 CLAUDE.md** 用於每個會話需要的指令：構建命令、測試約定、專案架構。

    **使用 rules** 保持 CLAUDE.md 專注。具有 [`paths` frontmatter](/zh-TW/memory#path-specific-rules) 的 rules 僅在 Claude 使用匹配檔案時載入，節省上下文。

    **使用 skills** 用於 Claude 有時只需要的內容，如 API 文件或您使用 `/<name>` 觸發的部署檢查清單。
  </Tab>

  <Tab title="Subagent vs Agent team">
    兩者都並行化工作，但它們在架構上不同：

    * **Subagents** 在您的會話內運行並將結果報告回您的主要上下文
    * **Agent teams** 是相互通訊的獨立 Claude Code 會話

    | 方面       | Subagent          | Agent team            |
    | -------- | ----------------- | --------------------- |
    | **上下文**  | 自己的上下文視窗；結果返回給呼叫者 | 自己的上下文視窗；完全獨立         |
    | **通訊**   | 僅向主代理報告結果         | 隊友直接相互訊息傳遞            |
    | **協調**   | 主代理管理所有工作         | 具有自我協調的共享任務清單         |
    | **最適合**  | 只有結果重要的專注任務       | 需要討論和協作的複雜工作          |
    | **令牌成本** | 較低：結果摘要回主上下文      | 較高：每個隊友是單獨的 Claude 實例 |

    **當您需要快速、專注的工作者時，使用 subagent**：研究問題、驗證聲明、審查檔案。Subagent 執行工作並返回摘要。您的主要對話保持乾淨。

    **當隊友需要共享發現、相互質疑和獨立協調時，使用 agent team**。Agent teams 最適合具有競爭假設的研究、並行程式碼審查，以及每個隊友擁有單獨部分的新功能開發。

    **轉換點：** 如果您運行並行 subagents 但遇到上下文限制，或者您的 subagents 需要相互通訊，agent teams 是自然的下一步。

    <Note>
      Agent teams 是實驗性的，預設情況下被禁用。有關設置和目前限制，請參閱 [agent teams](/zh-TW/agent-teams)。
    </Note>
  </Tab>

  <Tab title="MCP vs Skill">
    MCP 將 Claude 連接到外部服務。Skills 擴展 Claude 的知識，包括如何有效地使用這些服務。

    | 方面       | MCP                  | Skill                     |
    | -------- | -------------------- | ------------------------- |
    | **它是什麼** | 連接到外部服務的協議           | 知識、工作流程和參考資料              |
    | **提供**   | 工具和資料存取              | 知識、工作流程、參考資料              |
    | **範例**   | Slack 整合、資料庫查詢、瀏覽器控制 | 程式碼審查檢查清單、部署工作流程、API 風格指南 |

    這些解決不同的問題，並且可以很好地協同工作：

    **MCP** 給予 Claude 與外部系統互動的能力。沒有 MCP，Claude 無法查詢您的資料庫或發佈到 Slack。

    **Skills** 給予 Claude 關於如何有效使用這些工具的知識，以及您可以使用 `/<name>` 觸發的工作流程。Skill 可能包括您的團隊資料庫架構和查詢模式，或具有您的團隊訊息格式規則的 `/post-to-slack` 工作流程。

    範例：MCP 伺服器將 Claude 連接到您的資料庫。Skill 教導 Claude 您的資料模型、常見查詢模式，以及用於不同任務的表格。
  </Tab>

  <Tab title="Hook vs Skill">
    Hook 在生命週期事件上觸發；skill 被載入上下文供 Claude 應用。

    | 方面        | Hook                                                                 | Skill                              |
    | --------- | -------------------------------------------------------------------- | ---------------------------------- |
    | **運行**    | 殼層命令、HTTP 請求、LLM 提示或 subagent                                        | Claude 讀取並遵循的指令                    |
    | **由以下觸發** | [生命週期事件](/zh-TW/hooks#hook-events)，例如 `PostToolUse` 或 `SessionStart` | 您輸入 `/<name>`，或 Claude 將描述與您的任務相匹配 |
    | **確定性**   | 始終在其事件上觸發；觸發器是有保證的                                                   | Claude 解釋指令；結果可能會有所不同              |
    | **上下文成本** | 零，除非 hook 返回輸出                                                       | 描述在每個會話載入；使用時完整內容載入                |
    | **最適合**   | 每次都以相同方式發生且不需要 Claude 思考的操作                                          | 需要推理的工作流程、參考資料、多步驟任務               |

    **當操作必須每次都以相同方式發生且不需要 Claude 思考時，使用 hook**。例如：保存時格式化、拒絕 `rm -rf /`、在會話結束時發佈 Slack 訊息。

    **當 Claude 應該決定如何應用步驟或內容是知識而不是指令碼時，使用 skill**。例如：`/release` 檢查清單、您的 API 風格指南、除錯劇本。

    **將護欄放在 hooks 中。** CLAUDE.md 或 skill 中的「永遠不要編輯 `.env`」之類的指令是請求，而不是保證。阻止編輯的 `PreToolUse` hook 是強制執行。如果規則必須每次都成立，將其作為 hook 而不是提示指令。

    **Hook 輸出進入上下文。** 運行您的 linter 的 `PostToolUse` hook 將結果作為 Claude 讀取的文本反饋；`/fix-lint` skill 告訴 Claude 如何解決它們。
  </Tab>
</Tabs>

### 了解功能如何分層

功能可以在多個級別定義：使用者範圍、每個專案、通過 plugins，或通過受管理的策略。您也可以在子目錄中嵌套 CLAUDE.md 檔案，或在 monorepo 的特定套件中放置 skills。當相同的功能存在於多個級別時，以下是它們的分層方式：

* **CLAUDE.md 檔案** 是累加的：所有級別同時對 Claude 的上下文貢獻內容。來自您的工作目錄及以上的檔案在啟動時載入；子目錄在您在其中工作時載入。當指令衝突時，Claude 使用判斷來協調它們，更具體的指令通常優先。請參閱 [CLAUDE.md 檔案如何載入](/zh-TW/memory#how-claudemd-files-load)。
* **Skills 和 subagents** 按名稱覆蓋：當相同名稱存在於多個級別時，一個定義根據優先級獲勝（skills 為受管理 > 使用者 > 專案；subagents 為受管理 > CLI 標誌 > 專案 > 使用者 > plugin）。Plugin skills 是[命名空間](/zh-TW/plugins#add-skills-to-your-plugin)的，以避免衝突。請參閱 [skill 發現](/zh-TW/skills#where-skills-live) 和 [subagent 範圍](/zh-TW/sub-agents#choose-the-subagent-scope)。
* **MCP 伺服器** 按名稱覆蓋：本地 > 專案 > 使用者。請參閱 [MCP 範圍](/zh-TW/mcp#scope-hierarchy-and-precedence)。
* **Hooks** 合併：所有註冊的 hooks 為其匹配事件觸發，無論來源如何。請參閱 [hooks](/zh-TW/hooks-guide)。

### 結合功能

每個擴展解決不同的問題：CLAUDE.md 處理始終開啟的上下文，skills 處理按需知識和工作流程，MCP 處理外部連接，subagents 處理隔離，hooks 處理自動化。真實的設置根據您的工作流程結合它們。

例如，您可能使用 CLAUDE.md 用於專案約定、skill 用於您的部署工作流程、MCP 用於連接到您的資料庫，以及 hook 用於在每次編輯後運行 linting。每個功能處理它最擅長的事情。

| 模式                     | 它如何運作                                  | 範例                                             |
| ---------------------- | -------------------------------------- | ---------------------------------------------- |
| **Skill + MCP**        | MCP 提供連接；skill 教導 Claude 如何很好地使用它      | MCP 連接到您的資料庫，skill 記錄您的架構和查詢模式                 |
| **Skill + Subagent**   | Skill 生成 subagents 進行並行工作              | `/audit` skill 啟動在隔離上下文中工作的安全性、效能和風格 subagents |
| **CLAUDE.md + Skills** | CLAUDE.md 保持始終開啟的規則；skills 保持按需載入的參考資料 | CLAUDE.md 說「遵循我們的 API 約定」，skill 包含完整的 API 風格指南 |
| **Hook + MCP**         | Hook 通過 MCP 觸發外部操作                     | 編輯後 hook 在 Claude 修改關鍵檔案時發送 Slack 通知           |

## 了解上下文成本

您添加的每個功能都消耗 Claude 的一些上下文。太多可能會填滿您的上下文視窗，但它也可能添加噪聲，使 Claude 效率降低；skills 可能無法正確觸發，或 Claude 可能會失去對您的約定的追蹤。了解這些權衡有助於您構建有效的設置。有關這些功能如何在運行會話中結合的互動式視圖，請參閱[探索上下文視窗](/zh-TW/context-window)。

### 按功能的上下文成本

每個功能都有不同的載入策略和上下文成本：

| 功能            | 何時載入       | 什麼載入               | 上下文成本             |
| ------------- | ---------- | ------------------ | ----------------- |
| **CLAUDE.md** | 會話開始       | 完整內容               | 每個請求              |
| **Skills**    | 會話開始 + 使用時 | 啟動時的描述，使用時的完整內容    | 低（每個請求的描述）\*      |
| **MCP 伺服器**   | 會話開始       | 工具名稱；完整架構按需        | 低，直到使用工具          |
| **Subagents** | 生成時        | 具有指定 skills 的新鮮上下文 | 與主會話隔離            |
| **Hooks**     | 觸發時        | 無（外部運行）            | 零，除非 hook 返回額外上下文 |

\*預設情況下，skill 描述在會話開始時載入，以便 Claude 決定何時使用它們。在 skill 的 frontmatter 中設置 `disable-model-invocation: true` 以將其完全隱藏在 Claude 中，直到您手動調用它。這將 skills 的上下文成本降低到零，您只需自己觸發這些 skills。對於您未編寫的 skill，在設置中設置 [`skillOverrides`](/zh-TW/skills#override-skill-visibility-from-settings) 以執行相同操作，而無需編輯其檔案。

### 了解功能如何載入

每個功能在您的會話中的不同點載入。下面的選項卡說明每個功能何時載入以及什麼進入上下文。

<img src="https://mintcdn.com/claude-code/6yTCYq1p37ZB8-CQ/images/context-loading.svg?fit=max&auto=format&n=6yTCYq1p37ZB8-CQ&q=85&s=5a58ce953a35a2412892015e2ad6cb67" alt="上下文載入：CLAUDE.md 在會話開始時載入並保留在每個請求中。MCP 工具名稱在啟動時載入，完整架構延遲到使用。Skills 在啟動時載入描述，在調用時載入完整內容。Subagents 獲得隔離的上下文。Hooks 外部運行。" width="720" height="410" data-path="images/context-loading.svg" />

<Tabs>
  <Tab title="CLAUDE.md">
    **何時：** 會話開始

    **什麼載入：** 所有 CLAUDE.md 檔案的完整內容（受管理、使用者和專案級別）。

    **繼承：** Claude 從您的工作目錄讀取 CLAUDE.md 檔案直到根目錄，並在訪問這些檔案時在子目錄中發現嵌套的檔案。有關詳細資訊，請參閱 [CLAUDE.md 檔案如何載入](/zh-TW/memory#how-claudemd-files-load)。

    <Tip>保持 CLAUDE.md 在 200 行以下。將參考資料移動到 skills，它們按需載入。</Tip>
  </Tab>

  <Tab title="Skills">
    Skills 是 Claude 工具包中的額外功能。它們可以是參考資料（如 API 風格指南）或可調用的工作流程，您可以使用 `/<name>` 觸發（如 `/deploy`）。Claude Code 附帶[捆綁的 skills](/zh-TW/commands)，如 `/simplify`、`/batch` 和 `/debug`，開箱即用。您也可以創建自己的。Claude 在適當時使用 skills，或者您可以直接調用一個。

    **何時：** 取決於 skill 的配置。預設情況下，描述在會話開始時載入，完整內容在使用時載入。對於僅使用者 skills（`disable-model-invocation: true`），在您調用它們之前不會載入任何內容。

    **什麼載入：** 對於模型可調用的 skills，Claude 在每個請求中看到名稱和描述。當您使用 `/<name>` 調用 skill 或 Claude 自動載入它時，完整內容載入到您的對話中。

    **Claude 如何選擇 skills：** Claude 將您的任務與 skill 描述相匹配，以決定哪些相關。如果描述模糊或重疊，Claude 可能載入錯誤的 skill 或錯過會有幫助的。要告訴 Claude 使用特定 skill，請使用 `/<name>` 調用它。具有 `disable-model-invocation: true` 的 Skills 對 Claude 不可見，直到您調用它們。

    **上下文成本：** 低，直到使用。僅使用者 skills 在調用前成本為零。

    **在 subagents 中：** Skills 在 subagents 中的工作方式不同。不是按需載入，skills 列表中列出的 skills 在啟動時完全預載入其上下文。Subagents 仍然可以通過 Skill 工具發現和調用未列出的專案、使用者和 plugin skills。

    <Tip>對具有副作用的 skills 使用 `disable-model-invocation: true`。這節省上下文並確保只有您觸發它們。</Tip>
  </Tab>

  <Tab title="MCP 伺服器">
    **何時：** 會話開始。

    **什麼載入：** 來自連接伺服器的工具名稱。完整 JSON 架構保持延遲，直到 Claude 需要特定工具。

    **上下文成本：** [工具搜尋](/zh-TW/mcp#scale-with-mcp-tool-search)預設啟用，因此閒置 MCP 工具消耗最少上下文。

    **可靠性注意：** MCP 連接可能在會話中途無聲地失敗。如果伺服器斷開連接，其工具會無警告地消失。Claude 可能嘗試使用不再存在的工具。如果您注意到 Claude 無法使用它之前可以存取的 MCP 工具，請使用 `/mcp` 檢查連接。

    <Tip>運行 `/mcp` 以查看每個伺服器的令牌成本。斷開您未主動使用的伺服器。</Tip>
  </Tab>

  <Tab title="Subagents">
    **何時：** 按需，當您或 Claude 為任務生成一個時。

    **什麼載入：** 新鮮、隔離的上下文，包含：

    * 系統提示（與父級共享以提高快取效率）
    * 代理 `skills:` 欄位中列出的 skills 的完整內容
    * CLAUDE.md 和 git 狀態（從父級繼承）
    * 主代理在提示中傳遞的任何上下文

    **上下文成本：** 與主會話隔離。Subagents 不繼承您的對話歷史或調用的 skills。

    <Tip>對不需要您完整對話上下文的工作使用 subagents。它們的隔離防止膨脹您的主會話。</Tip>
  </Tab>

  <Tab title="Hooks">
    **何時：** 觸發時。Hooks 在特定生命週期事件（如工具執行、會話邊界、提示提交、權限請求和壓縮）時觸發。有關完整清單，請參閱 [Hooks](/zh-TW/hooks)。

    **什麼載入：** 預設情況下無。Hooks 在主對話外執行。

    **上下文成本：** 零，除非 hook 返回添加為訊息到您的對話的輸出。

    <Tip>Hooks 非常適合不需要影響 Claude 上下文的副作用（linting、logging）。</Tip>
  </Tab>
</Tabs>

## 了解更多

每個功能都有自己的指南，包含設置指令、範例和配置選項。

<CardGroup cols={2}>
  <Card title="CLAUDE.md" icon="file-lines" href="/zh-TW/memory">
    存儲專案上下文、約定和指令
  </Card>

  <Card title="Skills" icon="brain" href="/zh-TW/skills">
    給予 Claude 領域專業知識和可重複使用的工作流程
  </Card>

  <Card title="Subagents" icon="users" href="/zh-TW/sub-agents">
    將工作卸載到隔離的上下文
  </Card>

  <Card title="Agent teams" icon="network" href="/zh-TW/agent-teams">
    協調多個並行工作的會話
  </Card>

  <Card title="MCP" icon="plug" href="/zh-TW/mcp">
    將 Claude 連接到外部服務
  </Card>

  <Card title="Hooks" icon="bolt" href="/zh-TW/hooks-guide">
    使用 hooks 自動化工作流程
  </Card>

  <Card title="Plugins" icon="puzzle-piece" href="/zh-TW/plugins">
    捆綁和共享功能集
  </Card>

  <Card title="Marketplaces" icon="store" href="/zh-TW/plugin-marketplaces">
    託管和分發 plugin 集合
  </Card>
</CardGroup>


---

