# Spec Kit 使用手册

> Spec Kit 是一个开源工具包，帮助您通过规格驱动开发（Spec-Driven Development，简称 SDD）更快地构建高质量软件。

---

## 目录

- [快速开始](#快速开始)
- [核心命令](#核心命令)
- [完整工作流程](#完整工作流程)
- [进阶功能](#进阶功能)
- [扩展与预设](#扩展与预设)
- [常见问题](#常见问题)
- [最佳实践](#最佳实践)

---

## 快速开始

### 1. 安装 Specify CLI

**重要提示**：Spec Kit 的官方包仅通过 GitHub 发布。请使用以下方法安装：

#### 持久化安装（推荐）

使用 `uv`（推荐的 Python 包管理器）或 `pipx`：

```bash
# 使用 uv（推荐）
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 或使用 pipx
pipx install git+https://github.com/github/spec-kit.git
```

安装后验证版本：

```bash
specify version
```

#### 一次性使用

无需安装，直接运行：

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

### 2. 初始化项目

```bash
# 创建新项目
specify init my-awesome-project

# 或在现有项目中初始化
specify init . --integration copilot
```

### 3. 建立项目原则

在 AI 编程助手中运行：

```
/speckit.constitution 创建关注代码质量、测试标准、用户体验一致性和性能要求的原则
```

### 4. 创建规格说明

```
/speckit.specify 构建一个照片相册管理应用，支持按日期分组相册，通过拖拽重新排序
```

### 5. 制定实施计划

```
/speckit.plan 使用 Vite、原生 HTML/CSS/JavaScript，图片不上传，元数据存储在本地 SQLite 数据库中
```

### 6. 生成任务列表

```
/speckit.tasks
```

### 7. 执行实施

```
/speckit.implement
```

---

## 核心命令

### `/speckit.constitution` - 建立项目原则

创建或更新项目的治理原则和开发指南，这些原则将指导所有后续开发工作。

**用法示例**：

```
/speckit.constitution 创建以下原则：
- 优先使用简单直接的解决方案
- 必须先写测试再写实现（TDD）
- 所有 API 必须有明确的契约
- 禁止过度抽象
```

**输出文件**：`.specify/memory/constitution.md`

### `/speckit.specify` - 创建功能规格

将您的功能描述转换为结构化的规格文档。这是 SDD 工作流程的起点。

**用法示例**：

```
/speckit.specify 构建一个团队任务管理平台 Taskify。它应该允许用户创建项目、添加团队成员、分配任务，以及以看板样式在不同状态之间移动任务。
```

**自动执行**：
1. 扫描现有规格以确定下一个功能编号
2. 根据描述创建语义化的分支名称
3. 生成 `specs/[分支名]/spec.md` 规格文件
4. 创建完整的目录结构

**输出文件**：
```
specs/[###-feature-name]/
└── spec.md
```

### `/speckit.plan` - 制定实施计划

基于功能规格创建详细的技术实施计划。

**用法示例**：

```
/speckit.plan 使用 .NET Aspire 和 PostgreSQL 作为数据库，前端使用 Blazor Server 支持拖拽看板和实时更新，创建 REST API 包括项目、任务和通知接口
```

**输出文件**：
```
specs/[###-feature-name]/
├── plan.md              # 实施计划
├── research.md          # 技术调研
├── data-model.md        # 数据模型
├── quickstart.md        # 快速验证指南
└── contracts/           # API 契约
```

### `/speckit.tasks` - 生成任务列表

将实施计划分解为可执行的具体任务。

**用法**：
```
/speckit.tasks
```

**输出文件**：
```
specs/[###-feature-name]/
└── tasks.md             # 任务分解列表
```

**任务特点**：
- 按用户故事组织
- 标记可并行执行的任务 `[P]`
- 指定文件路径
- 包含 TDD 结构

### `/speckit.implement` - 执行实施

按照任务列表执行所有任务，构建功能。

**用法**：
```
/speckit.implement
```

**执行流程**：
1. 验证所有前置条件
2. 解析任务列表
3. 按正确顺序执行任务
4. 遵循 TDD 方法
5. 提供进度更新

---

## 完整工作流程

### 阶段 0：准备

1. **安装工具**
   ```bash
   uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
   specify check
   ```

2. **初始化项目**
   ```bash
   specify init my-project --integration claude
   ```

3. **启动 AI 编程助手**
   在项目目录中启动您的 AI 编程助手（如 Claude Code、GitHub Copilot 等）

### 阶段 1：建立原则

使用 `/speckit.constitution` 建立项目的核心原则：

```
/speckit.constitution 创建关注以下方面的原则：
- 代码质量：清晰、简洁、可维护
- 测试：先写测试（TDD），使用真实环境而非 mock
- 简单性：避免过度设计，最多使用 3 个项目
- 用户体验：保持一致性
- 性能：满足特定性能要求
```

### 阶段 2：定义功能规格

使用 `/speckit.specify` 创建功能规格：

**关键要点**：
- ✅ 聚焦于 **什么**（what）和 **为什么**（why）
- ❌ 避免技术细节（how）

**规格模板结构**：

```markdown
# Feature Specification: [功能名称]

## User Scenarios & Testing

### User Story 1 - [标题] (Priority: P1)
[用户旅程描述]

**Acceptance Scenarios**:
1. Given [初始状态], When [操作], Then [期望结果]

## Requirements

### Functional Requirements
- FR-001: 系统 MUST [具体能力]
- FR-002: 用户 MUST 能够 [关键交互]

## Success Criteria
- SC-001: [可衡量指标]
```

### 阶段 3：澄清需求（可选但推荐）

使用 `/speckit.clarify` 进行结构化澄清：

```
/speckit.clarify
```

这将通过系统性问答确保规格没有歧义。

### 阶段 4：制定技术计划

使用 `/speckit.plan` 创建技术实施计划：

**计划应包含**：
- 技术栈选择
- 项目结构
- 数据模型
- API 契约
- 实施阶段
- 合规性检查（基于 constitution）

### 阶段 5：生成任务

使用 `/speckit.tasks` 分解任务：

**任务列表特点**：
- 按依赖关系排序
- 标记可并行任务
- 指定具体文件路径
- 包含测试要求

### 阶段 6：执行实施

使用 `/speckit.implement` 执行实施：

**执行过程**：
1. 遵循 TDD：先写测试，再写实现
2. 按任务顺序执行
3. 处理并行任务
4. 验证每个用户故事

### 阶段 7：验证与交付

1. 运行测试套件
2. 验证用户场景
3. 创建 Pull Request
4. 合并到主分支

---

## 进阶功能

### `/speckit.clarify` - 需求澄清

在创建计划前进行结构化需求澄清，减少下游返工。

```
/speckit.clarify
```

### `/speckit.analyze` - 一致性分析

分析规格、计划和任务之间的一致性和覆盖范围。

```
/speckit.analyze
```

### `/speckit.checklist` - 质量清单

生成自定义质量清单来验证需求的完整性、清晰度和一致性。

```
/speckit.checklist
```

### `/speckit.taskstoissues` - 转换为 GitHub Issues

将生成的任务列表转换为 GitHub Issues 进行跟踪和执行。

```
/speckit.taskstoissues
```

---

## 扩展与预设

### 社区扩展

扩展为 Spec Kit 添加新功能，如：
- 与外部工具集成（Jira、Azure DevOps、Confluence）
- 代码审查和质量门
- 安全审查
- 项目健康检查
- 成本追踪

**安装扩展**：

```bash
# 搜索扩展
specify extension search

# 安装扩展
specify extension add <extension-name>
```

### 社区预设

预设自定义 Spec Kit 的行为，如：
- 强制合规导向的规格格式
- 使用领域特定术语
- 应用组织标准
- 本地化到不同语言

**安装预设**：

```bash
# 搜索预设
specify preset search

# 安装预设
specify preset add <preset-name>
```

### 项目本地覆盖

在 `.specify/templates/overrides/` 中创建模板覆盖，为单个项目进行一次性调整。

---

## 常见问题

### Q1: 我应该在何时使用 `/speckit.clarify`？

A: 建议在 `/speckit.specify` 之后、`/speckit.plan` 之前使用。这样可以减少因需求不明确导致的下游返工。

### Q2: 如何在现有项目中引入 Spec Kit？

A: 使用 `specify init . --integration <agent>` 在现有项目中初始化。对于遗留系统，可以使用 Brownfield 扩展帮助增量采用。

### Q3: AI 代理会生成过度设计的方案吗？

A: 可能会。Constitution 中的简单性和反抽象条款通过"前实施门控"机制防止过度设计。如果发现过度设计，可以要求 AI 解释理由。

### Q4: 如何回滚或修改已生成的计划？

A: 所有文档都是纯文本文件，可以直接编辑。修改后重新运行 `/speckit.tasks` 来更新任务列表。

### Q5: Spec Kit 支持哪些 AI 编程助手？

A: Spec Kit 支持 30+ 种 AI 编程助手，包括：
- Claude Code
- GitHub Copilot
- Cursor
- Windsurf
- Gemini CLI
- Codex CLI
- 等等

运行 `specify integration list` 查看完整列表。

### Q6: 如何更新 Spec Kit？

A: 使用以下命令：

```bash
# 使用 uv
uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git@vX.Y.Z

# 使用 pipx
pipx install --force git+https://github.com/github/spec-kit.git@vX.Y.Z
```

---

## 最佳实践

### 1. 从小开始

- 第一个功能保持简单，熟悉工作流程
- 优先级清晰：P1 功能必须能独立测试和交付

### 2. 保持规格简洁

- ✅ 描述用户需要什么
- ❌ 不要指定技术实现细节
- 使用 `[NEEDS CLARIFICATION]` 标记不明确的地方

### 3. 遵循 TDD

- Constitution 要求：不写测试就不能写实现
- 测试必须在实现之前通过评审

### 4. 验证门控

- 执行前验证 Constitution 检查
- 检查 Review & Acceptance 清单
- 确保没有 `[NEEDS CLARIFICATION]` 标记

### 5. 版本控制

- 每个功能在独立分支上开发
- 规格、计划、任务都是版本化文档
- 使用 PR 来合并并跟踪变更

### 6. 迭代改进

- 规格不是一次性完成的
- 根据实现反馈持续完善
- 生产问题应回馈到规格中

### 7. 利用并行能力

- 标记可并行的任务 `[P]`
- 在适当的工作流中并行执行

---

## 学习资源

- [完整的 SDD 方法论](./spec-driven.md)
- [CLI 参考文档](https://github.github.io/spec-kit/reference/overview.html)
- [社区扩展目录](https://speckit-community.github.io/extensions/)
- [视频教程](https://www.youtube.com/watch?v=a9eR1xsfvHg)

---

## 获取支持

- [GitHub Issues](https://github.com/github/spec-kit/issues) - 报告问题或提问
- [文档站点](https://github.github.io/spec-kit/) - 查看详细文档
- [社区讨论](https://github.com/github/spec-kit/discussions) - 参与社区讨论

---

*本手册基于 Spec Kit v0.8.9+ 编写*
