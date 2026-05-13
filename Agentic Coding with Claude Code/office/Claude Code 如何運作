> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

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
