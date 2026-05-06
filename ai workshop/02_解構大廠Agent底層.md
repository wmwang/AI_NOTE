# 第二堂：解構大廠 Agent 底層 — 從 30 行 Python 到 Claude Code

> **核心命題**：AI Agent 不是魔術。Agency 來自模型（訓練），程式碼只是「harness」（鞍具）——讓模型感知和行動的環境。我們用 6 個漸進步驟，從 30 行 Python 開始，一步步打造出 Claude Code 的核心架構。

---

## 📋 本堂摘要

| 項目 | 內容 |
|------|------|
| 🎯 主題 | 從零打造 Agent Loop，漸進加入 Tool Dispatch / TodoWrite / Subagent / Skill / Context 管理 |
| 🎬 Demo | 逐步執行 s01→s06 Python Agent，觀察每一步帶來的行為變化 |
| ⚡ Quick Win | 執行 s01 Agent Loop，用自然語言讓它完成一個任務 |
| 📝 作業 | 用 Agent 找出維運腳本的錯誤根因，觀察底層 Agentic Loop 的迭代過程 |

---

## 📖 核心洞察與來源宣告

> 本堂主要參考 [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) 的漸進式教學設計。
>
> 該 repo 的核心理念：
> - **Agency comes from the model (training), not from code.**
> - **The code is the "harness" — the environment that lets the model perceive and act.**
> - 每一步只加一個機制，Agent Loop 本身永遠不變。
>
> Claude Code 本身是閉源產品（TypeScript），但其核心架構模式是通用的 Agent 設計原則，我們用 Python 復刻來理解。

---

## 一、概念講授：6 步漸進打造 Agent（40 mins）

### 學習路線圖

```
Phase 1: The Loop (循環)              Phase 2: Planning & Knowledge (規劃與知識)
┌───────────────────────────┐         ┌─────────────────────────────────────────┐
│ s01 Agent Loop (30行)      │         │ s03 TodoWrite — 讓 Agent 不偏航        │
│     ↓ +Tool Dispatch       │  ──→    │ s04 Subagent  — 上下文隔離             │
│ s02 Tool Use (4工具)        │         │ s05 Skills    — 按需載入知識           │
│                            │         │ s06 Context   — 三層壓縮管理           │
└───────────────────────────┘         └─────────────────────────────────────────┘

    每一步只加一個機制，Agent Loop 本身永遠不變。
```

---

### Step 1 (s01)：Agent Loop — 30 行 Python 就是一個 Agent

> *"One loop & Bash is all you need"* — 一個工具 + 一個循環 = 一個 Agent。

**問題**：LLM 能推理程式碼，但碰不到真實世界——不能讀檔案、跑測試、看報錯。沒有循環，每次工具呼叫你都得手動把結果貼回去。**你自己就是那個循環**。

**架構圖**：

```
+--------+      +-------+      +---------+
|  User  | ---> |  LLM  | ---> |  Tool   |
| prompt |      |       |      | execute |
+--------+      +---+---+      +----+----+
                    ^                |
                    |   tool_result  |
                    +----------------+
                    (loop until stop_reason != "tool_use")
```

**完整程式碼（不到 30 行）**：

```python
def agent_loop(query):
    messages = [{"role": "user", "content": query}]
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return  # AI 不再呼叫工具 → 任務完成

        results = []
        for block in response.content:
            if block.type == "tool_use":
                output = run_bash(block.input["command"])
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
        messages.append({"role": "user", "content": results})
```

💡 **這就是整個 Agent**。後面 5 個步驟都在這個循環上疊加機制——**循環本身始終不變**。

---

### Step 2 (s02)：Tool Use — 加工具不用改循環

> *"加一個工具，只加一個 handler"* — 循環不用動，新工具註冊進 dispatch map 就行。

**問題**：只有 `bash` 時，所有操作都走 shell。專用工具（`read_file`、`write_file`）可以在工具層面做路徑沙箱。

**關鍵設計：Dispatch Map**

```python
# 路徑沙箱 — 防止逃逸工作目錄
def safe_path(p: str) -> Path:
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path

# 每個工具有自己的 handler
TOOL_HANDLERS = {
    "bash":       lambda **kw: run_bash(kw["command"]),
    "read_file":  lambda **kw: run_read(kw["path"], kw.get("limit")),
    "write_file": lambda **kw: run_write(kw["path"], kw["content"]),
    "edit_file":  lambda **kw: run_edit(kw["path"], kw["old_text"], kw["new_text"]),
}

# 循環中按名稱查找 handler — 循環體與 s01 完全一致
handler = TOOL_HANDLERS.get(block.name)
output = handler(**block.input) if handler else f"Unknown tool: {block.name}"
```

**加工具 = 加 handler + 加 schema。循環永遠不變。**

| 元件 | s01 | s02 |
|------|-----|-----|
| Tools | 1（僅 bash） | 4（bash, read, write, edit） |
| Dispatch | 硬編碼 | `TOOL_HANDLERS` 字典 |
| 路徑安全 | 無 | `safe_path()` 沙箱 |
| **Agent Loop** | **不變** | **不變** |

---

### Step 3 (s03)：TodoWrite — 沒有計畫的 Agent 走哪算哪

> *"先列步驟再動手，完成率翻倍"* — 規劃不替模型畫航線，只讓它不偏航。

**問題**：多步任務中，模型會丟失進度——重複做過的事、跳步、跑偏。一個 10 步重構可能做完 1-3 步就開始即興發揮。

**關鍵設計：TodoManager + Nag Reminder**

```python
class TodoManager:
    def update(self, items: list) -> str:
        in_progress_count = sum(1 for i in items if i.get("status") == "in_progress")
        if in_progress_count > 1:
            raise ValueError("Only one task can be in_progress")  # 強制順序聚焦
        self.items = validated
        return self.render()

# Nag：連續 3 輪不更新 todo 就提醒
if rounds_since_todo >= 3:
    messages[-1]["content"].insert(0, {
        "type": "text", "text": "<reminder>Update your todos.</reminder>"
    })
```

**設計巧思**：「同時只能有一個 in_progress」強制順序聚焦。Nag reminder 製造問責壓力。

這就是 Claude Code 內建 `TodoWrite` 工具的設計原型！

---

### Step 4 (s04)：Subagent — 乾淨的上下文，乾淨的結果

> *"大任務拆小，每個小任務用乾淨的上下文"* — Subagent 用獨立 messages[]，不污染主對話。

**問題**：「這個專案用什麼測試框架？」可能要讀 5 個檔案，但父 Agent 只需要一個詞：「pytest」。

**架構**：

```
Parent agent                     Subagent
+------------------+             +------------------+
| messages=[...]   |             | messages=[]      | ← 全新
| tool: task       | ----------> | while tool_use:  |
|   result="pytest"| <---------- | return last text |
+------------------+             +------------------+
 Parent context clean    Subagent context discarded
```

```python
def run_subagent(prompt: str) -> str:
    sub_messages = [{"role": "user", "content": prompt}]
    for _ in range(30):
        # ... 子 Agent 跑自己的循環 ...
    # 整個訊息歷史丟棄，只回傳摘要
    return "".join(b.text for b in response.content if hasattr(b, "text"))
```

> 💡 **Boris Cherny**：*"Separate context windows make results better; one agent can cause bugs and another (same model) can find them."*

---

### Step 5 (s05)：Skills — 用到什麼知識，臨時載入什麼知識

> *"用 tool_result 注入，不塞 system prompt"* — 模型開口要時才給的領域專長。

**兩層載入設計**：

```
Layer 1 — System Prompt（便宜 ~100 tokens/skill）:
│ Skills available:
│   - git: Git workflow helpers
│   - test: Testing best practices

Layer 2 — tool_result（按需 ~2000 tokens）:
│ <skill name="git">
│   Full git workflow instructions...
│ </skill>
```

```python
class SkillLoader:
    def get_descriptions(self) -> str:   # Layer 1：便宜名稱
        return "\n".join(f"  - {n}: {s['meta'].get('description', '')}" ...)

    def get_content(self, name: str) -> str:  # Layer 2：按需完整內容
        return f"<skill name=\"{name}\">\n{self.skills[name]['body']}\n</skill>"
```

**對應到 Claude Code**：這就是 `.claude/skills/` 的漸進式揭露機制。

---

### Step 6 (s06)：Context Compact — 三層壓縮，無限會話

> *"上下文總會滿，要有辦法騰地方"* — 乾淨的記憶，無限的會話。

**三層壓縮（激進程度遞增）**：

```
Layer 1: micro_compact (每輪自動)
  → 舊 tool_result 替換為 "[Previous: used {tool_name}]"

Layer 2: auto_compact (token > 閾值)
  → 保存 transcript 到磁碟
  → LLM 做摘要，替換所有 messages

Layer 3: compact tool (手動觸發)
  → 使用者或模型主動呼叫
  → 同 Layer 2 的摘要機制
```

**對應到 Claude Code**：
- Layer 1 = 自動清理舊 tool_result
- Layer 2 = auto-compact
- Layer 3 = 使用者手動 `/compact`

> 💡 **Thariq**：*"/compact with a hint beats letting autocompact fire — the model is at its least intelligent point when auto-compacting."*

---

### 6 步總覽：從 30 行到完整 Agent

| 步驟 | 機制 | 工具數 | 對應 Claude Code |
|------|------|:---:|-----------------|
| s01 | Agent Loop | 1 (bash) | 核心迴圈 |
| s02 | Tool Dispatch | 4 | Bash/Read/Write/Edit + MCP |
| s03 | TodoWrite | 5 | 內建 TodoWrite 工具 |
| s04 | Subagent | 5+task | `.claude/agents/` 子代理 |
| s05 | Skill Loading | +load_skill | `.claude/skills/` 漸進式揭露 |
| s06 | Context Compact | +compact | `/compact` + 自動壓縮 |

**核心洞察**：每一層都是獨立的正交設計。你可以只用 s01，也可以全部疊加。Claude Code 就是把這 6 層（加上 Hooks、MCP、Settings）全部組合起來的結果。

---

## 二、Demo 實演（10 mins）

### 準備工作

```bash
git clone https://github.com/shareAI-lab/learn-claude-code.git
cd learn-claude-code
export ANTHROPIC_API_KEY="your-key-here"
```

### Demo 1：s01 → s02 對比

```bash
# s01: 只有一個 bash 工具
python agents/s01_agent_loop.py
> Create a file called hello.py that prints Hello, World!
# 觀察：AI 用 echo "..." > hello.py

# s02: 有 read/write/edit 工具
python agents/s02_tool_use.py
> Create a file called hello.py that prints Hello, World!
# 觀察：AI 用 write_file 工具，路徑有沙箱保護
```

### Demo 2：s03 規劃能力

```bash
python agents/s03_todo_write.py
> Refactor hello.py: add type hints, docstrings, and a main guard
# 觀察：AI 先建 todo list，逐步完成，3 輪沒更新會被提醒
```

### Demo 3：s04 Subagent 上下文隔離

```bash
python agents/s04_subagent.py
> Use a subtask to find what testing framework this project uses
# 觀察：子 Agent 讀了多個檔案，但父 Agent 只收到一句摘要
```

---

## 三、Quick Win：課堂 10 分鐘動手（10 mins）

### 任務：執行 s01 Agent Loop，親身體驗 Agent 迭代

```bash
# Step 1：克隆 repo（2 min）
git clone https://github.com/shareAI-lab/learn-claude-code.git
cd learn-claude-code
export ANTHROPIC_API_KEY="your-key-here"

# Step 2：執行 s01（3 min）
python agents/s01_agent_loop.py
> Create a file called test.txt with the content "Hello from Agent"
# 觀察 Agent 的迭代：思考 → bash → 結果 → 完成

# Step 3：升級到 s03 對比（3 min）
python agents/s03_todo_write.py
> Create a Python package with __init__.py, utils.py with a hello() function, and tests/test_utils.py
# 觀察：AI 會建 todo list，逐步完成每個子任務

# Step 4：記錄觀察（2 min）
# - s01 迭代了幾次？每次做了什麼？
# - s03 的 todo list 幫了什麼忙？
# - 如果沒有 todo，AI 會漏掉什麼？
```

---

## 四、回家作業

### 作業：挑選一段維運腳本，用 Agent 找出錯誤根因

**目標**：觀察 Agentic Loop 的迭代過程，理解 AI 如何透過 Error Recovery 修復問題。

#### 步驟

1. **準備報錯腳本**：

```bash
cat > broken-script.sh << 'SCRIPT'
#!/bin/bash
# 故意寫錯的維運腳本
echo "Starting deployment to $DEPLOY_ENV"
kubctl get pods -n production
cat /etc/myapp/config.yaml
if [ "$STATUS" = "running" then
  echo "OK"
fi
SCRIPT
```

2. **用 learn-claude-code 的 Agent 分析**：

```bash
python agents/s02_tool_use.py
> Read broken-script.sh, find all errors, and explain the root cause of each.
```

3. **記錄觀察**：

```markdown
## Agentic Loop 觀察報告

### 腳本名稱：___
### 錯誤清單
| # | 錯誤描述 | 根因 | Agent 發現的順序 |
|---|---------|------|-----------------|
| 1 | | | |
| 2 | | | |

### 迭代紀錄
| Iteration | Agent 做了什麼 | 結果 |
|-----------|--------------|------|
| 1 | | |
| 2 | | |

### 心得
- Agent 的 Error Recovery 策略是什麼？
- 對應到我們學的 6 步中的哪一層？
```

#### 評分標準

| 項目 | 比重 |
|------|:---:|
| 腳本選擇的真實性 | 20% |
| 錯誤分析的完整度 | 30% |
| 迭代紀錄的詳細度 | 30% |
| 觀察心得的深度 | 20% |

---

## 五、關鍵 Takeaway

> 💡 **記住這句話**：Agent 的能力上限，取決於你給它的工具定義和錯誤訊息品質。
>
> - **好的 Loop** → Agent 能持續工作直到完成
> - **好的 Dispatch Map** → 加工具不用改循環
> - **好的 TodoManager** → Agent 不會偏航
> - **好的 Subagent** → 上下文保持乾淨
> - **好的 Skill 設計** → 知識按需載入，不浪費 token
> - **好的 Context 管理** → 無限會話，不會「變笨」

### 延伸閱讀

- [learn-claude-code 完整 12 步教程](https://github.com/shareAI-lab/learn-claude-code/tree/main/docs/zh) — 本堂主要參考來源
- [Anthropic Tool Use 官方文件](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Anthropic Agentic Patterns](https://docs.anthropic.com/en/docs/build-with-claude/agentic-patterns)
- [Claude Code Best Practices](https://github.com/shanraisshan/claude-code-best-practice)

---

*上一堂：[企業級 AI 基礎建設](01_企業級AI基礎建設.md) | 下一堂：[專屬 SRE 兵器庫](03_專屬SRE兵器庫.md)*