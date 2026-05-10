# Claude Code Planning Mode：先想清楚再動手，開多個 Agent 加速開發

Claude Code 預設是「你說我做」——你打一句話，它馬上開始改程式碼。這對簡單任務很方便，但碰到複雜功能時，這種方式很容易讓它改了一堆你不想動的地方。Planning Mode 和多 Agent 平行執行，是解決這個問題的兩個關鍵工具。

---

## 什麼是 Planning Mode？

Planning Mode 是 Claude Code 的一個特殊模式：進入之後，Claude Code **只能讀、不能寫**。它可以：

- 讀取程式碼、查文件、搜尋資料
- 分析問題、設計方案
- 產出一份實作規格文件

但它**不能**：編輯檔案、執行指令、`git commit`、安裝套件。

說白了，就是強迫 Claude Code 先「想清楚」，把計畫寫出來給你 review，你點頭之後才能動手。

這個流程和資深工程師的工作方式很像：

```
需求說明 → 技術設計文件 → Review → 核准 → 實作
```

### 怎麼進入 Planning Mode？

```bash
# 先開啟 Claude Code
claude

# 輸入指令進入 Planning Mode
/plan
```

進入後，畫面底部會出現 `plan mode on` 的提示。此時輸入你的需求，Claude Code 會開始分析並產出規格，而不會直接改任何東西。

---

## 為什麼要用 Planning Mode？

| 情境 | 不用 Planning Mode | 用 Planning Mode |
|------|--------------------|-----------------|
| Claude 改了你沒預期的檔案 | 常發生 | 因為先 review 規格，幾乎不會 |
| 需求理解有誤才發現 | 改完才知道 | 看規格時就能發現 |
| 複雜功能的副作用 | 難預測 | 規格中可以明確列出影響範圍 |
| 規格文件 | 沒有 | 自動產出，可存檔 |

**最大的好處**是：一份清楚的規格文件可以把 Claude Code 的「幻覺空間」縮到最小。它知道自己要做什麼、不做什麼，改錯的機率大幅下降。

---

## 實際操作：用 Planning Mode 設計認證系統

假設你要新增一個使用者登入功能。

**第一步：進入 Planning Mode 並描述需求**

```
/plan

幫我設計一個使用者認證系統。需求如下：
- Email + 密碼登入
- JWT token 管理（access token 15分鐘、refresh token 7天）
- 密碼用 bcrypt 加密
- 登入失敗 5 次後鎖定帳號 15 分鐘
- 技術棧：Node.js + Express + PostgreSQL
```

**第二步：Claude Code 產出規格（你只要看，不會有程式碼被改）**

Claude Code 會分析現有程式碼架構，然後產出類似這樣的規格：

```markdown
# 認證系統實作規格

## 影響範圍
- 新增：src/auth/ 目錄（AuthService、TokenService、AuthController）
- 修改：src/routes/index.ts（新增 /auth 路由）
- 修改：src/middleware/auth.ts（更新 JWT 驗證邏輯）
- 資料庫：新增 users 表、login_attempts 表

## API 端點
- POST /auth/login
- POST /auth/refresh
- POST /auth/logout

## 安全考量
- bcrypt rounds: 12
- Token 儲存：access token 放 memory，refresh token 放 httpOnly cookie
- 失敗鎖定：Redis 計數，避免 DB 壓力
```

**第三步：Review 並調整**

你看完規格後，可以直接對話修改：

```
Redis 這個環境沒有，改用 PostgreSQL 記錄登入失敗次數
```

Claude Code 會更新規格，直到你滿意為止。

**第四步：把規格存起來（強烈建議）**

```
把這份規格存成 .claude/auth-spec.md
```

規格存下來有兩個好處：
1. 之後叫 Claude Code 實作時，直接 `@.claude/auth-spec.md` 引用，方向不會跑掉
2. 下次要改功能時，有文件可以對照

**第五步：離開 Planning Mode，開始實作**

按 `Shift + Tab` 或輸入 `/plan` 再按一次，離開 Planning Mode，然後：

```
根據 @.claude/auth-spec.md 的規格，開始實作認證系統
```

---

## 多個 Claude Code Agent 同時工作

Planning Mode 解決了「想清楚再動手」的問題，多 Agent 平行執行則解決另一個問題：**速度**。

### 核心概念

你可以同時開多個 terminal，每個 terminal 跑一個獨立的 Claude Code instance，讓它們各自處理不同的任務，互不干擾。

這就像讓兩個工程師同時工作：

- A 工程師負責修登入 bug
- B 工程師負責改按鈕樣式

只要他們改的不是同一個檔案，就不會有衝突。

### 什麼任務適合平行執行？

| 適合平行 | 不適合平行 |
|---------|-----------|
| 修復兩個不相關的 bug | 前後端同時開發（前端需要後端 API） |
| 建立不同的 UI 頁面 | 同一個功能的不同層（controller + service） |
| 獨立的 React 元件 | 有共享狀態的模組 |
| 不同語言的文件翻譯 | 會互相修改同一個設定檔 |

**判斷標準**：如果兩個任務最後會改到**同一個檔案**，就不適合平行。

### 實際示範：同時修兩個 Bug

假設你有兩個待修的 issue：

- Issue #42：`src/auth/login.ts` 登入時沒有正確清空 session
- Issue #57：`src/ui/Button.tsx` 在深色模式下顏色不對

這兩個完全獨立，非常適合平行。

```bash
# Terminal 1
claude
# 輸入：
修復 src/auth/login.ts 的 session 清空問題。
登入成功後，舊的 session data 沒有被清除，請找到問題並修復。
只修改 src/auth/ 目錄下的檔案。
```

```bash
# Terminal 2（同時開第二個 terminal）
claude
# 輸入：
修復 src/ui/Button.tsx 在深色模式下的顏色問題。
dark mode 時按鈕文字顏色使用了 text-gray-900，看不清楚，
應該改成 text-gray-100。只修改 Button.tsx。
```

兩個 terminal 同時執行，互不影響。結束後：

```bash
# 分別 review 兩個 terminal 的修改
git diff src/auth/login.ts
git diff src/ui/Button.tsx

# 確認無誤後 commit
git add src/auth/login.ts src/ui/Button.tsx
git commit -m "fix: clear session on login (#42), fix button dark mode (#57)"
```

### 重要注意事項

> **最佳實務：用不同的 git branch**
>
> 上面的示範為了簡單，讓兩個 agent 在同一個 branch 工作。但在正式開發環境，建議：
> - Agent 1 在 `fix/auth-session` branch
> - Agent 2 在 `fix/button-darkmode` branch
>
> 這樣萬一有衝突，處理起來更安全，也符合團隊的 PR 流程。

---

## 本篇重點整理

| 功能 | 指令 | 主要用途 |
|------|------|---------|
| 進入 Planning Mode | `/plan` | 複雜功能先產規格，再實作 |
| 離開 Planning Mode | `Shift + Tab` 或再按 `/plan` | 核准規格後執行 |
| 多 Agent 平行 | 開多個 terminal 各跑 `claude` | 同時處理多個獨立任務 |

**何時用 Planning Mode：**
- 功能複雜、影響範圍廣
- 不確定 Claude 會改哪些地方
- 需要讓團隊 review 方向再實作

**何時用多 Agent：**
- 有多個互相獨立的任務
- 想加速開發，縮短等待時間
- 任務可以明確限定修改範圍

**下一步：**
1. 下次遇到複雜需求，試試在描述前先加 `/plan`，看它產出的規格你滿不滿意
2. 打開兩個 terminal，各跑一個 Claude Code，試試平行處理兩件不同的事
3. 養成把規格存成 `.claude/*.md` 的習慣，讓後續的 Claude Code 執行更精準
