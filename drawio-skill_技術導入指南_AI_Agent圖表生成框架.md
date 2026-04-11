---
title: drawio-skill 技術導入指南：讓 AI Agent 直接產出 Production-Ready 架構圖
tags:
  - drawio
  - diagram
  - ai-coding
  - agent-skill
  - architecture
  - visualization
aliases:
  - drawio-skill Guide
  - AI 圖表生成技術指南
date: 2026-04-12
---

# drawio-skill 技術導入指南：讓 AI Agent 直接產出 Production-Ready 架構圖

> 架構討論到一半，手動開 draw.io 排版是流程斷點。drawio-skill 讓 AI agent 從自然語言直接生成 `.drawio` XML 並 export 為 PNG/SVG/PDF——圖表成為對話的副產物，而非額外工序。

---

## 問題背景：AI 輔助開發中的視覺化斷層

AI coding agent 擅長產出程式碼與文字，但在系統設計討論中，**視覺化仍然是手動工序**。典型的問題場景：

- Agent 用文字描述了一套微服務架構，但工程師仍需手動開 draw.io 畫圖才能與團隊溝通
- 設計 review 需要架構圖，但圖與 code 分屬不同工具鏈，同步成本高
- ER diagram、sequence diagram 等在需求釐清階段極有價值，但「畫一張圖」的摩擦力導致它們經常被省略

問題本質是：**AI agent 的輸出管道缺少結構化圖表生成能力。** 文字描述與視覺化之間存在一個 manual gap，而這個 gap 恰好可以被 draw.io 的 XML 格式 + CLI export 能力填補。

> [!important] drawio-skill 的工程定位
> 不是圖表編輯器的替代品，而是 AI agent 的 **視覺化輸出通道**——將自然語言描述轉換為結構化的 `.drawio` XML，透過 CLI 自動 export，並以 vision capability 進行 self-check。

---

## 架構概覽

### 技術棧

```
Natural Language → AI Agent (with SKILL.md) → .drawio XML → draw.io CLI → PNG/SVG/PDF/JPG
                                                   ↑                           ↓
                                              Self-check ←── Vision Read ──← Export
```

drawio-skill 由一份 `SKILL.md` 驅動，定義了 agent 在圖表生成場景下的完整行為規範：XML 結構、shape/edge 語法、layout 規則、色彩系統、export pipeline、self-check loop。

### 核心組件

| 組件 | 角色 |
|------|------|
| `SKILL.md` | Skill 定義文件（唯一必要檔案） |
| draw.io Desktop CLI | XML → 圖檔 export 引擎 |
| Vision capability | Export 後的 self-check（偵測重疊、裁切、斷線等） |
| Browser fallback | CLI 不可用時，生成 diagrams.net URL（client-side，無資料上傳） |

### 跨平台相容性

| 平台 | 安裝路徑 | 整合方式 |
|------|----------|----------|
| **Claude Code** | `~/.claude/skills/drawio-skill/` | 原生 SKILL.md |
| **OpenClaw** | `~/.openclaw/skills/drawio-skill/` | `metadata.openclaw` namespace |
| **Hermes Agent** | `~/.hermes/skills/design/drawio-skill/` | `metadata.hermes` + tags |
| **OpenAI Codex** | `~/.agents/skills/drawio-skill/` | `agents/openai.yaml` sidecar |
| **SkillsMP** | CLI 安裝 | GitHub topics 索引 |

---

## 安裝

### 前置需求：draw.io Desktop

drawio-skill 依賴 draw.io desktop 的 CLI export 功能，需先安裝桌面應用。

**macOS（推薦 Homebrew）**：

```bash
brew install --cask drawio
```

**Windows**：

從 [draw.io desktop releases](https://github.com/jgraph/drawio-desktop/releases) 下載安裝。驗證：

```bash
"C:\Program Files\draw.io\draw.io.exe" --version
```

**Linux**：

下載 `.deb` / `.rpm`。Headless 環境需搭配 `xvfb`：

```bash
xvfb-run -a drawio --version
```

### Skill 安裝

以 Claude Code 為例，將 `SKILL.md` 置於 `~/.claude/skills/drawio-skill/` 即可。其他平台依對應路徑放置。

### 驗證

啟動新 session，要求 agent 繪製任意架構圖。若 agent 自動進入 dependency check → clarification → XML generation 流程，表示 skill 已正確載入。

---

## 七步工作流

drawio-skill 定義了結構化的七步 pipeline：

### Step 1：Dependency Check

Agent 確認 `draw.io --version` 可執行，並記錄平台資訊以選擇正確的 CLI 路徑。

### Step 2：Clarification

若使用者描述不完整，agent 提出 1-3 個聚焦問題：

- 圖表類型（ERD / UML / Sequence / Architecture / Flowchart / ML）
- 輸出格式（預設 PNG）
- 範圍界定（元件數量、技術棧）

### Step 3：Planning

規劃 shape 清單、relationship mapping、layout 方向（LR / TB）、tier/layer 分組。

### Step 4：XML Generation

根據規劃結果生成 `.drawio` XML，遵循 skill 定義的結構規範（詳見下節）。

### Step 5：Draft Export & Self-Check

Export PNG 後，以 vision capability 讀取圖檔，自動偵測並修復最多 6 類問題：

| 問題 | 修復策略 |
|------|----------|
| Shape 重疊 | 間距拉開 ≥200px |
| Label 被裁切 | 擴大 shape 尺寸 |
| 連線缺失 | 驗證 source/target ID 對應 |
| Shape 超出畫布 | 移至正座標範圍 |
| Edge 穿過 shape | 添加 waypoint 或增加間距 |
| Edge 堆疊 | 分散 entry/exit point |

Self-check 最多執行 **2 輪**。若仍有問題，直接呈現供使用者判斷。

### Step 6：Review Loop

顯示圖檔，收集使用者 feedback。執行定向修改（單一元素調整），每輪 re-export。

**規則**：
- 保留先前迭代的 layout 調整
- 覆寫同一 `.png`（不產生 v1、v2、v3）
- 5 輪後建議使用者在 draw.io desktop 中手動微調

### Step 7：Final Export

Export 至所有指定格式。回報 `.drawio` 原始檔與 export 檔的路徑。

---

## 技術規格：draw.io XML 結構

### 文件骨架

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="drawio" version="26.0.0">
  <diagram name="Page-1">
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- user shapes 從 id="2" 開始 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

> [!warning] 必要約束
> - `id="0"` 與 `id="1"` 為 required root cells，缺少任一將導致 render 失敗
> - User shape 的 id 從 `2` 開始，遞增分配
> - 所有 text 使用 `html=1`
> - 特殊字元必須 escape：`&amp;` `&lt;` `&gt;` `&quot;`
> - 換行使用 `&#xa;`（非 `\n`）
> - XML comment 中禁止 `--`（違反 XML spec）

### Shape 類型

| Style keyword | 視覺效果 | 典型用途 |
|---------------|----------|----------|
| `rounded=0` | 直角矩形 | 一般 process |
| `rounded=1` | 圓角矩形 | Services、modules |
| `ellipse;` | 橢圓 / 圓形 | Start/End、database icon |
| `rhombus;` | 菱形 | Decision point |
| `shape=cylinder3;` | 圓柱體 | Database |
| `swimlane;startSize=30;` | 帶標題欄的容器 | Tier、group、table |

### 容器與巢狀

架構圖的分層結構使用 parent-child containment（非視覺重疊）：

| 容器類型 | Style | 適用場景 |
|----------|-------|----------|
| **Group** | `group;pointerEvents=0;` | 無邊框、不接受連線的純分組 |
| **Swimlane** | `swimlane;startSize=30;` | 需要標題欄或容器層級連線 |
| **Custom container** | `container=1;pointerEvents=0;` | 任意 shape 作為容器但不接受連線 |

Child shape 的座標為 **相對於 parent 的偏移量**，非全域座標。

### Edge（連線）

每條 edge **必須** 包含 `<mxGeometry relative="1" as="geometry" />` 子元素，self-closing edge 不會 render：

```xml
<mxCell id="10" value="HTTP/REST"
  style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;
         jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;
         entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
  edge="1" parent="1" source="2" target="4">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

**Entry/Exit point 座標系**：

| 位置 | X | Y |
|------|---|---|
| Top center | 0.5 | 0 |
| Right center | 1 | 0.5 |
| Bottom center | 0.5 | 1 |
| Left center | 0 | 0.5 |
| Top-left | 0.25 | 0 |
| Top-right | 0.75 | 0 |

單一 shape 有 N 條連線時，需均勻分散 entry/exit point，避免堆疊。

**動畫連線**：style 中加入 `flowAnimation=1;` 可顯示沿箭頭方向的動態圓點，適用於 data flow 視覺化。

### 七色語義系統

| 色彩 | fillColor | strokeColor | 語義 |
|------|-----------|-------------|------|
| Blue | `#dae8fc` | `#6c8ebf` | Services、clients |
| Green | `#d5e8d4` | `#82b366` | Database、success |
| Yellow | `#fff2cc` | `#d6b656` | Queue、decision |
| Orange | `#ffe6cc` | `#d79b00` | Gateway、API |
| Red | `#f8cecc` | `#b85450` | Error、alert |
| Grey | `#f5f5f5` | `#666666` | External、neutral |
| Purple | `#e1d5e7` | `#9673a6` | Security、auth |

色彩一致性使圖表具備即時可讀性——不需要圖例，color coding 本身即傳達角色語義。

### Layout 規則

**間距依複雜度自動 scale**：

| 複雜度 | Node 數 | 水平間距 | 垂直間距 |
|--------|---------|----------|----------|
| Simple | ≤5 | 200px | 150px |
| Medium | 6-10 | 280px | 200px |
| Complex | >10 | 350px | 250px |

**關鍵規範**：
- 所有座標 snap 至 10px 倍數（grid alignment）
- Shape 行/列之間保留 ~80px routing corridor
- Hub node（如 API Gateway、Message Bus）置於中心位置
- Star topology 採用 hub-center 策略
- 垂直直線連接時，pin entry/exit point 為 `exitX=0.5;exitY=1` / `entryX=0.5;entryY=0`

---

## 支援的圖表類型 Preset

### Architecture Diagram

以 swimlane 劃分 tier（Client → API → Service → Data）。Services 為 tier 對應色彩的圓角矩形，database 為 green cylinder，queue/bus 為 yellow 置於 service row 中央，gateway 為 orange。

### ERD（Entity-Relationship）

Table 以 swimlane container 表示，column 作為 child row。PK/FK 標注於 label。Relationship 使用 ER notation edge（`endArrow=ERmandOne;`）。相關 table 垂直排列，間距 300px。

### UML Class Diagram

Class 以 swimlane 分三區：title / attributes / methods。支援 inheritance（`endArrow=block;endFill=0;`）、composition（filled diamond）、aggregation（hollow diamond）、implementation（dashed）。Interface 置於 implementation 上方，間距 250px。

### Sequence Diagram

Lifeline 使用 `shape=umlLifeline;container=1;`，垂直 dashed line 表示時間軸。Sync message（`endArrow=block;`）、async（`endArrow=open;dashed=1;`）、return（grey dashed）。Activation box 於 lifeline 上。Lifeline 間距 200px，時間由上而下。

### ML / Deep Learning Model

Layer 以類型色彩區分：Input/Output=green、Conv/Pooling=blue、Attention/Transformer=purple、RNN/LSTM/GRU=yellow、FC/Linear=orange、Loss/Activation=red。Skip connection 以 dashed curved arrow 表示。Label 包含 tensor shape annotation `(B, C, H, W)`。TB layout，layer 間距 150px。

### Flowchart

Start/End=green oval、Process=blue rectangle、Decision=yellow diamond、I/O=orange parallelogram、Subprocess=purple double-border。Decision 分支標注 Yes/No。TB layout，decision 向 LR 分支後 merge 回中心線。

---

## Export 指令參考

```bash
# PNG（含嵌入 XML，macOS Homebrew）
draw.io -x -f png -e -s 2 -o output.drawio.png input.drawio

# macOS 完整路徑
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -e -s 2 -o output.drawio.png input.drawio

# Windows
"C:\Program Files\draw.io\draw.io.exe" -x -f png -e -s 2 -o output.drawio.png input.drawio

# Linux headless
xvfb-run -a draw.io -x -f png -e -s 2 -o output.drawio.png input.drawio

# SVG / PDF
draw.io -x -f svg -o output.svg input.drawio
draw.io -x -f pdf -o output.pdf input.drawio
```

| Flag | 功能 |
|------|------|
| `-x` | Export mode（必要） |
| `-f` | 格式：png / svg / pdf / jpg |
| `-e` | 將 XML 嵌入 export 檔（PNG/SVG/PDF） |
| `-s` | Scale factor：1 / 2 / 3（PNG 建議 2） |
| `-o` | 輸出路徑 |
| `-t` | 透明背景（僅 PNG） |
| `--page-index N` | Export 指定頁面 |

> [!note] `-e` flag 的工程意義
> 以 `-e`（`--embed-diagram`）export 的 PNG 內嵌完整 `.drawio` XML。這意味著一份 PNG 檔即可用 draw.io desktop 直接開啟編輯——不需要額外保留 `.drawio` 原始檔。對於需要在 Markdown/Wiki 中嵌入圖片、同時保留可編輯性的場景，這是最佳實踐。

### Fallback Chain

| 情境 | 降級策略 |
|------|----------|
| CLI 不可用 + Python 可用 | 生成 diagrams.net URL（client-side compression，無資料上傳） |
| CLI 不可用 + Python 不可用 | 交付 `.drawio` XML，指導手動開啟 |
| Vision 不可用 | 跳過 self-check，直接呈現 PNG |
| Linux export 失敗 | 以 `xvfb-run -a` 重試；仍失敗則交付 XML |

---

## 觸發條件

### 顯式觸發

使用者提及以下關鍵詞時自動啟用：diagram、flowchart、visualize、architecture、UML、ER diagram。

### 主動觸發

Agent 在以下情境中應 **主動提議** 生成圖表：

- 解釋包含 3+ 元件的系統架構
- 描述多步驟流程或 state machine
- 比較不同架構方案

### 不觸發

簡單的清單/表格即可表達的內容，或快速 Q&A session 中不啟用。

---

## 常見問題與對策

| 問題 | 根因 | 對策 |
|------|------|------|
| Export 輸出空白 | macOS CLI 路徑未找到 | 使用完整路徑 `/Applications/draw.io.app/Contents/MacOS/draw.io` |
| Linux export 失敗 | 無 display server | `xvfb-run -a` 前綴 |
| Shape 不 render | 缺少 root cells | 確保 `id="0"` 與 `id="1"` 存在 |
| Edge 不顯示 | Self-closing `<mxCell />` | 展開為 `<mxCell ...><mxGeometry relative="1" as="geometry" /></mxCell>` |
| 連線斷裂 | source/target ID 不匹配 | 驗證 edge 的 source/target 對應 shape id |
| Arrowhead 重疊 bend | 最後一段 edge 過短 | 確保 final segment ≥20px |
| Label 含特殊字元 | 未 escape | 使用 `&amp;` `&lt;` `&gt;` `&quot;` |

---

## 與 Superpowers / OpenSpec 的協作

drawio-skill 可嵌入 Superpowers 的 brainstorming phase 或 OpenSpec 的 propose phase：

| 工作流階段 | drawio-skill 的角色 |
|-----------|-------------------|
| **Brainstorming** | Agent 在提出設計方案時自動生成架構圖，使設計 review 可視化 |
| **OpenSpec Propose** | `design.md` 中嵌入自動生成的架構圖，supplement 文字描述 |
| **Code Review** | Reviewer 可要求 agent 生成 before/after 架構對比圖 |
| **Documentation** | 功能完成後自動生成 architecture diagram 嵌入文件 |

這使得圖表不再是獨立的手動產出物，而是 **開發流程中自動生成的附屬 artifact**。

---

## 導入建議

1. **先裝 draw.io desktop**——skill 的核心價值依賴 CLI export；無 CLI 時降級為純 XML 交付，效益大幅降低
2. **使用 `-e` flag export PNG**——內嵌 XML 的 PNG 同時具備「可嵌入文件」與「可再編輯」兩項特性，是最佳 export 策略
3. **信任 self-check loop**——前 2 輪自動修復可處理大部分 layout 問題；5 輪 review 後建議切換至 desktop 手動微調
4. **建立團隊色彩約定**——七色語義系統是 skill 的預設值，團隊可依需求自訂 color mapping 並寫入 SKILL.md
5. **搭配 vision-capable model**——self-check 需要模型具備圖像理解能力；無 vision 時仍可運作但失去自動修復能力

> [!abstract] 適用場景判斷
> drawio-skill 的最大效益出現在 **設計討論頻繁、需要快速視覺化溝通** 的場景——架構設計、系統拆分、技術方案比較、onboarding 文件。對於純 coding task 或不涉及系統結構的工作，無需啟用。

---

## 小結

drawio-skill 填補的是 AI agent 輸出管道中的 **視覺化缺口**。它不替代 draw.io desktop 的手動編輯能力，而是將 「自然語言 → 結構化圖表」的轉換自動化——透過嚴格的 XML 結構規範、complexity-scaled layout 規則、self-check loop，使 agent 產出的圖表達到可直接用於技術文件與設計 review 的品質。

一份 `SKILL.md`、一個 draw.io desktop、零額外基礎設施。圖表成為對話的副產物，而非額外工序。

```bash
brew install --cask drawio
```
