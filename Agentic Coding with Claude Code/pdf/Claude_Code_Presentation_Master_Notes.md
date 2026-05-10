# Comprehensive Training Notes: Agentic Coding with Claude Code

These notes are designed to provide extensive material for a 60-80 slide presentation. This document covers foundational concepts, essential commands, extensibility via MCP, GitHub automation, multi-agent workflows, skills, and deep agents.

---

## Part 1: Foundations and Workflows (Chapters 1-5)

### Chapter 1: Context Engineering

#### 1. The Foundation of Agentic Coding
*   **Definition of Context Engineering:** The deliberate practice of curating, structuring, and managing the information provided to an LLM (like Claude) to maximize its performance and accuracy.
*   **Why Context Matters:** LLMs lack persistent memory of your entire local environment. The quality of Claude Code's output is directly proportional to the relevance and clarity of the context it receives.
*   **The Goldilocks Rule of Context:**
    *   *Too Little Context:* Leads to hallucinations, generalized answers, and incorrect assumptions about your codebase.
    *   *Too Much Context:* Increases token costs, slows down processing, and can cause the model to lose focus (the "needle in a haystack" problem).
    *   *Just Right:* Providing exactly the files, functions, and architectural rules needed for the specific task.

#### 2. How Claude Code Handles Context
*   **Automatic Discovery:** Claude Code features an advanced Context Engine that automatically scans the workspace, reads project structures, and identifies relevant files based on the user's prompt.
*   **Semantic Search:** It utilizes vector-based or semantic search techniques to find related code snippets even if exact keyword matches are missing.
*   **Context Window Management:** Claude Code continuously manages the active context window, dropping older or less relevant information to stay within token limits while preserving critical task information.

#### 3. Best Practices for Developers
*   **Explicit Referencing:** When asking Claude Code to perform a task, explicitly mention the core files involved (e.g., "Update the authentication logic in `src/auth.js` and `src/middleware.js`").
*   **System Prompting via Files:** Use project-level instructions (like `GEMINI.md` or `.claudecode` files) to establish baseline context (coding standards, architectural patterns) that applies to all interactions.
*   **Iterative Context Refinement:** Start with a broad task and narrow down the context as the agent explores the codebase. If the agent makes a wrong assumption, correct it by pointing to the correct file.


#### Hands-on Lab: Context Engineering & Explicit Referencing

**Objective:** Observe the "Goldilocks Rule of Context" by comparing a vague request to a prompt with explicit file referencing.

**Setup:** 
Continue in the `claude-demo-lab1` directory. Create a new utility file:
```bash
echo "module.exports = { calculateSum: (a, b) => Number(a) + Number(b) };" > utils.js
```

**The Prompt/Command:**
*Attempt 1 (The Vague Approach):*
Prompt: *"Add a route to calculate things."*
*(Notice how Claude asks clarifying questions or guesses poorly).*

*Attempt 2 (The Engineered Context Approach):*
Prompt: *"Read `utils.js`. Add a new GET route `/add` in `index.js` that takes query parameters `a` and `b`, uses the `calculateSum` function from `utils.js` to add them, and returns the result as JSON."*

**Expected Outcome:**
- Claude will immediately read `utils.js` to understand the imported function.
- It will correctly modify `index.js` to require `utils.js` and implement the precise `req.query` parsing needed, proving that explicit file references lead to zero-shot success.

---

### Chapter 2: The Gist of Claude Code

#### 1. What is Claude Code?
*   **Agentic CLI Assistant:** Claude Code is an advanced, terminal-based AI coding assistant developed by Anthropic. Unlike standard chat interfaces, it operates autonomously within your local file system.
*   **The "Agentic" Shift:** It doesn't just suggest code; it *executes* tasks. It reads files, writes code, runs tests, and navigates directories, acting as a collaborative pair programmer.
*   **Target Audience:** Designed for software engineers, devops professionals, and technical leads who want to integrate AI deeply into their existing terminal-centric workflows.

#### 2. Core Philosophy
*   **Staying in the Flow:** By living in the terminal, Claude Code eliminates the need to context-switch between an IDE, a browser-based LLM, and the command line.
*   **Security and Privacy:** Operates with strict adherence to local file system permissions. It only modifies what it has been granted access to.
*   **Transparency:** Every action Claude Code takes (reading a file, running a command) is visible to the user, ensuring the developer maintains ultimate control.

#### 3. Key Capabilities
*   **Codebase Comprehension:** Can understand massive, multi-repository projects by autonomously navigating the directory structure.
*   **Refactoring and Bug Fixing:** Capable of executing complex, multi-file refactoring operations and diagnosing obscure bugs by tracing logic across modules.
*   **Test Generation:** Automatically writes comprehensive unit and integration tests based on the existing code logic.

---

### Chapter 3: Getting Started with Claude Code - A Tour of Essential Commands

#### 1. Installation and Initialization
*   **Prerequisites:** Node.js/npm or a standalone binary installation (depending on platform). Requires an active Anthropic API key.
*   **Initial Setup:** Running `claude init` or simply `claude` in a directory to begin a session.

#### 2. The Command Palette (Slash Commands)
Claude Code uses intuitive slash commands for session management and specialized tasks.
*   **`/help`:** The primary discovery tool. Lists all available commands, capabilities, and system features.
*   **`/compact`:** A critical command for context management. It compresses the current conversation history, summarizing past interactions to free up tokens and reduce API costs while maintaining the overarching task context.
*   **`/clear`:** Completely wipes the current session history, starting with a fresh context window. Ideal when switching to a completely unrelated task.
*   **`/cost`:** Provides real-time metrics on token usage and estimated API costs for the current session, enabling cost-conscious development.
*   **`/bug`:** A built-in mechanism to report issues directly to the development team or log local anomalies.

#### 3. Interacting with the Agent
*   **Natural Language Prompts:** The primary interface. (e.g., "Find the memory leak in the worker process and fix it.")
*   **Command Execution:** Claude Code can run shell commands using built-in tools. For example, it will run `npm test` to verify its own changes.
*   **Approval Workflows:** For destructive actions (deleting files, running complex shell scripts), Claude Code prompts the user for confirmation, ensuring safety.


#### Hands-on Lab: Basic Commands and Session Management

**Objective:** Learn how to initialize a session, interact with Claude Code, and manage context and costs using built-in slash commands.

**Setup:** 
Create a new dummy directory and initialize a basic Node.js project. Open your terminal and run:
```bash
mkdir claude-demo-lab1 && cd claude-demo-lab1
npm init -y
touch index.js
```

**The Prompt/Command:**
1. Start your Claude Code session by typing: `claude`
2. Enter the prompt: *"Write a simple Express server in `index.js` with a single `/ping` route that returns 'pong'. If express is not installed, please install it."*
3. Once Claude finishes, run the slash command: `/cost`
4. Run the slash command: `/compact`

**Expected Outcome:**
- Claude Code will autonomously execute `npm install express`.
- It will write the Express boilerplate to `index.js` and show you the diff.
- The `/cost` command will output your current token usage and estimated API cost for the session.
- The `/compact` command will summarize your conversation history, compressing it to free up token space while maintaining context.

---

### Chapter 4: Extending Claude Code with MCP Servers and Plugins

#### 1. Understanding Model Context Protocol (MCP)
*   **What is MCP?** An open standard that allows AI models to securely connect to local and remote data sources, external tools, and enterprise systems.
*   **The Architecture:**
    *   *MCP Client:* Claude Code acts as the client.
    *   *MCP Server:* A lightweight bridge connected to a specific resource (e.g., a database, an API).
    *   *The Protocol:* Standardized JSON-RPC messages defining how tools and resources are exposed.
*   **Why Extensibility Matters:** It breaks the LLM out of its isolated shell, allowing it to interact with live databases, read Jira tickets, or query cloud infrastructure directly from the terminal.

#### 2. Connecting and Configuring Plugins
*   **Configuration File:** MCP servers are typically configured in a `.claudecode` or `mcp.json` configuration file within the project or globally.
*   **Example Configuration:**
    ```json
    {
      "mcpServers": {
        "postgres-db": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@localhost/db"]
        }
      }
    }
    ```
*   **Discoverability:** Once configured, Claude Code automatically discovers the new tools provided by the MCP server and integrates them into its planning phase.

#### 3. Practical Use Cases for MCP
*   **Database Interactions:** Querying a local PostgreSQL or SQLite database to understand data schema before writing ORM models.
*   **Documentation Systems:** Connecting to Confluence or Notion MCP servers to retrieve company-specific API specifications.
*   **Custom Internal Tools:** Wrapping proprietary company CLI tools in an MCP server so Claude Code can utilize internal deployment pipelines.

---

### Chapter 5: Automating Your Development Workflow with Claude Code and GitHub

#### 1. The Synergy of Agentic Coding and Version Control
*   **Beyond Local Edits:** Claude Code is not just for writing code; it excels at managing the lifecycle of that code through Git.
*   **Contextual Commits:** Because Claude Code understands the *intent* behind the changes it just made, it can generate highly accurate, descriptive, and formatted commit messages automatically.

#### 2. Core Git Workflows with Claude Code
*   **Branch Management:** Instruct Claude to "Create a new branch for the authentication feature based on the latest main."
*   **Staging and Committing:** Claude can review the `git diff`, stage relevant files, and craft a commit message.
    *   *Example Prompt:* "Review my unstaged changes, group them logically, and create separate commits for the UI updates and the backend logic."
*   **Resolving Merge Conflicts:** Claude Code can read conflict markers, analyze both incoming and current changes, and intelligently resolve the conflict based on project logic.

#### 3. GitHub Integration
*   **Pull Request Generation:** Claude Code can generate comprehensive PR descriptions, summarizing the technical changes, the business logic altered, and testing steps.
*   **Automated Issue Resolution:** You can point Claude Code directly to a GitHub issue:
    *   *Example Prompt:* "Read GitHub issue #402, investigate the reported bug in the user profile service, fix the code, run tests, and open a PR closing the issue."
*   **Code Review Assistance:** Use Claude Code as a pre-reviewer. Ask it to "Review the latest commit on this branch for security vulnerabilities and style violations before I push."


#### Hands-on Lab: Automating Git and GitHub Workflows

**Objective:** Use Claude Code to understand code changes, write semantic commit messages, and execute version control operations.

**Setup:** 
Initialize a git repository in your project directory and stage your current work.
```bash
git init
git add index.js package.json package-lock.json utils.js
```

**The Prompt/Command:**
Prompt: *"Review my staged changes. Create a single, descriptive commit message following the Conventional Commits format (e.g., feat: ...). After showing me the message, go ahead and execute the commit."*

**Expected Outcome:**
- Claude will run a background shell command like `git diff --staged` or `git status`.
- It will analyze the diffs and generate a precise commit message (e.g., `feat: setup express server with ping and calculate endpoints`).
- It will use the `git commit -m` command to successfully commit your staged files.

---

## Part 2: Advanced Capabilities (Chapters 6-11)

### Chapter 6: Claude Code Planning and Multi-agent Workflows

#### Key Concepts
*   **Strategic Planning Phase:** Emphasizes the critical shift from reactive coding to proactive, deliberate planning. Claude Code can act as a system architect, drafting structural blueprints before writing a single line of code.
*   **Multi-agent Architecture:** The paradigm of utilizing multiple, specialized agent instances to tackle different components of a complex system concurrently, reducing cognitive load on any single agent.
*   **Context Segregation:** Keeping different tasks in separate agent contexts to prevent token overflow, hallucination, and context dilution.
*   **The Orchestrator-Worker Pattern:** The primary Claude Code instance acts as the "orchestrator," breaking down the overarching goal and delegating specific, isolated implementations to "worker" subagents.

#### Important Commands & Workflows
*   **The Planning Workflow:**
    1.  **Discovery:** Command Claude to explore the codebase and ingest the requirements.
    2.  **Drafting the Plan:** Prompt Claude to generate a step-by-step execution plan.
    3.  **Review & Refine:** The human user reviews the plan, enforces constraints, and approves.
    4.  **Execution:** Claude systematically executes the plan, crossing off tasks sequentially.
*   **Persistent Memory Tracking:** Utilizing tracking files (like `PLAN.md` or `TODO.md`) so the agent has a source of truth to refer back to across long sessions.

#### Code Examples & Best Practices
*   **Best Practice:** Always start a complex feature with a well-structured PRD (Product Requirements Document). Provide this document to the agent explicitly.
*   **Best Practice:** Force Claude to write out the plan to the file system. If the context window resets or the session drops, the plan remains intact.
*   **Example Prompt:** *"Read `specs/feature-x.md`. Generate a step-by-step technical plan and save it to `PLAN.md`. Break the work down into atomic, testable steps. Do not begin writing application code until I approve the plan."*

---

### Chapter 7: Working with Claude Code Subagents

#### Key Concepts
*   **Subagent Definition:** Ephemeral, highly-focused AI instances spawned by the main orchestrator agent to handle singular tasks.
*   **Delegation & Isolation:** Offloading isolated tasks (e.g., writing unit tests for a specific utility file, or refactoring a single React component) to subagents.
*   **Context Economy:** The primary benefit of subagents is that they only receive the context required for their specific task. This saves tokens, reduces processing cost, and dramatically improves accuracy.

#### Important Commands & Workflows
*   **Spawning Subagents:** Using programmatic instructions or natural language directives to instruct the main agent to delegate.
*   **The Subagent Workflow Loop:**
    1.  **Identification:** The main agent identifies a task that is independent and isolatable.
    2.  **Prompt Engineering (Automated):** The main agent crafts a precise prompt for the subagent, restricting its file access to only what is necessary.
    3.  **Execution:** The subagent completes the task autonomously.
    4.  **Integration:** The subagent returns a diff or a summary, which the main agent then integrates into the broader project scope.

#### Code Examples & Best Practices
*   **Best Practice:** Keep subagent scopes microscopically small and perfectly defined. Ambiguous instructions to a subagent lead to cascading errors.
*   **Best Practice:** Ideal use cases for subagents include repetitive, parallelizable tasks.
*   **Example Prompt:** *"Spawn a subagent to go through the `/utils` directory and add JSDoc comments to every exported function. Ensure the subagent only modifies the comments and does not alter the business logic."*


#### Hands-on Lab: Delegating to Subagents

**Objective:** Delegate a highly scoped, repetitive task to a worker subagent to preserve main context tokens.

**Setup:** 
Create a new directory with undocumented code.
```bash
mkdir math-lib
echo "export const sub = (a, b) => a - b;" > math-lib/sub.js
echo "export const mul = (a, b) => a * b;" > math-lib/mul.js
```

**The Prompt/Command:**
Prompt: *"Spawn a subagent to analyze the `math-lib` directory. Instruct it to add detailed JSDoc comments to every exported function explaining the parameters and return type. It must not modify any business logic."*

**Expected Outcome:**
- The main Claude orchestrator will formulate a prompt and spin up a subagent process.
- The subagent will independently read `sub.js` and `mul.js`.
- It will write correct `/** ... */` annotations to the files.
- The main agent will report back that the subagent successfully completed the task, keeping your main context window unpolluted by the individual file reads.

---

### Chapter 8: Creating and Customizing Output Styles

#### Key Concepts
*   **Output Styling:** Giving the user control over how Claude Code formats its responses, structures code blocks, and authors commit messages.
*   **Persona & Tone Customization:** Adapting Claude's communication style (e.g., ultra-concise for senior devs, verbose and mentor-like for juniors) to fit the user's or team's preferences.
*   **Code Standardization:** Forcing the agent to strictly adhere to the project's specific linting rules, architectural patterns, and style guides.

#### Important Commands & Workflows
*   **Configuration Files:** Utilizing project-specific configuration files (typically `CLAUDE.md` or `.claudecode`) to set global rules.
*   **System Prompt Overrides:** Injecting custom instructions that run before every interaction.
*   **Iterative Feedback:** Correcting Claude's style during a session to train its output formatting in real-time.

#### Code Examples & Best Practices
*   **Best Practice:** Maintain a comprehensive `CLAUDE.md` at the root of the repository. This acts as the persistent "brain" for project standards.
*   **Example `CLAUDE.md` Configuration:**
    ```markdown
    # Project Guidelines
    - Language: TypeScript 5.x
    - Framework: React 18 (Strict Mode)
    - Style: Tailwind CSS for all styling. No external CSS files.
    - Types: Never use `any`. Always define explicit interfaces.
    - Tone: Be extremely concise. Do not explain the code unless asked. Output only the modified code.
    ```


#### Hands-on Lab: Customizing Output Styles & Enforcing Rules

**Objective:** Use a project-level configuration file to force Claude Code to adhere to strict stylistic and architectural guidelines.

**Setup:** 
Create a global instruction file that acts as the project's "brain".
```bash
echo "# Project Guidelines
- Response Format: All Express API responses MUST be wrapped in a standard JSON format: { \"success\": boolean, \"data\": object | null, \"error\": string | null }
- Tone: Be extremely concise. Output only the requested changes." > CLAUDE.md
```

**The Prompt/Command:**
Prompt: *"Update the `/ping` route in `index.js` to return the current server timestamp."*

**Expected Outcome:**
- Because of `CLAUDE.md`, Claude will automatically apply your architectural constraints.
- Instead of returning a plain string or raw JSON, it will enforce the wrapper: `{ "success": true, "data": { "timestamp": "2023-10-27T..." }, "error": null }`.
- Claude's conversational text in the terminal will be notably brief.

---

### Chapter 9: Understanding Agent Skills

#### Key Concepts
*   **Agent Skills Definition:** Extensible, programmatic capabilities that allow Claude to perform specialized actions beyond simple text generation (e.g., executing CLI commands, querying a database, interacting with cloud infrastructure).
*   **Model Context Protocol (MCP):** The underlying architecture that bridges the LLM with local and remote tools, giving Claude "hands" to manipulate its environment.
*   **Skill Modularity:** Building reusable skills that can be shared across projects or teams.

#### Important Commands & Workflows
*   **Registering Skills:** Writing scripts or JSON configurations that expose local tools to the Claude Code environment.
*   **Autonomous Invocation:** Once a skill is registered, Claude can autonomously decide to use it when a user's request necessitates it.

#### Code Examples & Best Practices
*   **Best Practice:** Implement strict safety boundaries. Destructive skills (like `DROP TABLE` or `git push --force`) should always require explicit human confirmation.
*   **Best Practice:** Write clear, semantic descriptions for your skills. The LLM relies on the description to understand *when* and *how* to use the tool.
*   **Example Skill Concept:** A "Database Migration" skill.
    *   *Description for Claude:* "Use this skill to generate and apply PostgreSQL migrations using Prisma."
    *   *Workflow:* Claude writes the Prisma schema, invokes the skill to run `prisma migrate dev`, and reads the standard output to verify success.

---

### Chapter 11: Understanding Deep Agents

#### Key Concepts
*   **Deep vs. Shallow Execution:** Shallow agents are for quick Q&A and simple edits. "Deep Agents" are designed for long-running, complex, exploratory tasks (e.g., deep debugging, architectural refactoring, legacy code migration).
*   **Autonomous Codebase Traversal:** Deep agents have the autonomy to navigate massive codebases, read dozens of files, run automated tests, and iterate on errors without waiting for user input.
*   **Resilience & Backtracking:** The hallmark of a deep agent is its ability to recognize when an approach is failing, backtrack to a previous state, and attempt an alternative path.

#### Important Commands & Workflows
*   **The Deep Investigation Workflow:**
    1.  **Goal Definition:** Define a complex, high-level goal (e.g., "Resolve the race condition in the WebSocket handler").
    2.  **Hypothesis Generation:** The agent formulates potential causes.
    3.  **Instrumentation:** The agent writes and deploys temporary logging/instrumentation code to gather data.
    4.  **Analysis:** The agent runs the code (or tests), analyzes the logs, and refines its hypothesis.
    5.  **Resolution:** The agent implements the final fix and runs regression tests to verify.

#### Code Examples & Best Practices
*   **Best Practice:** Establish a "Budget." Give deep agents limits (e.g., maximum number of steps, token limits, or time limits) to prevent runaway execution loops.
*   **Best Practice:** Use a "Scratchpad." Force the agent to document its thought process.
*   **Example Prompt:** *"Act as a deep agent to refactor the payment processing module. You have a budget of 20 steps. Use a file named `scratchpad.md` to document your findings, hypotheses, and intended architecture before making code changes. Run the test suite after every major change. If you hit a roadblock 3 times, pause and ask for my input."*


#### Hands-on Lab: Planning and Deep Agent Execution

**Objective:** Experience Claude's strategic planning phase and let it execute a multi-step task autonomously.

**Setup:** 
Create a feature specification document in your directory:
```bash
echo "# Feature Request: Rate Limiting
Add rate limiting to the Express server in index.js.
Requirements:
1. Max 5 requests per minute per IP.
2. Return a 429 status code with a custom error message if exceeded.
3. Use a lightweight in-memory store." > feature-x.md
```

**The Prompt/Command:**
Prompt: *"Act as a deep agent to implement the feature described in `feature-x.md`. Before writing any application code, draft a step-by-step technical plan and save it to a new file called `PLAN.md`. Wait for my approval before executing the plan."*

**Expected Outcome:**
- Claude will read `feature-x.md`.
- It will generate a markdown file (`PLAN.md`) outlining the steps (e.g., Step 1: Install `express-rate-limit`, Step 2: Configure middleware, Step 3: Apply to routes).
- It will pause and ask you: *"Do you approve this plan?"*
- Upon replying "Yes", Claude will methodically work through the steps, updating code and installing packages.

---

### Suggested Slide Distribution (60-80 Pages Total)
*   **Introduction & Context Engineering (Chapter 1):** 10-12 Slides (Why Agentic coding? Context principles)
*   **The Gist of Claude Code (Chapter 2):** 8-10 Slides (What it is, philosophy, capabilities)
*   **Essential Commands & Tour (Chapter 3):** 10-12 Slides (Initialization, `/commands`, interactions)
*   **Extending with MCP (Chapter 4):** 8-10 Slides (Architecture, Plugins, Use Cases)
*   **Git & GitHub Automation (Chapter 5):** 8-10 Slides (Workflows, PRs, Issues)
*   **Planning & Multi-agent Workflows (Chapter 6):** 8-10 Slides (Strategy, Orchestration)
*   **Subagents & Deep Agents (Chapters 7 & 11):** 8-12 Slides (Delegation, Deep execution loops)
*   **Output Styles & Agent Skills (Chapters 8 & 9):** 5-8 Slides (Customization, Extending capabilities)

---

# Appendix: Hands-on Labs & Practical Examples

These exercises are designed to accompany the presentation. Presenters can use these as live demos, or attendees can follow these step-by-step labs in their terminal to experience Claude Code's capabilities firsthand.

## Lab 1: Basic Commands and Session Management (Chapter 3)

**Objective:** Learn how to initialize a session, interact with Claude Code, and manage context and costs using built-in slash commands.

**Setup:** 
Create a new dummy directory and initialize a basic Node.js project. Open your terminal and run:
```bash
mkdir claude-demo-lab1 && cd claude-demo-lab1
npm init -y
touch index.js
```

**The Prompt/Command:**
1. Start your Claude Code session by typing: `claude`
2. Enter the prompt: *"Write a simple Express server in `index.js` with a single `/ping` route that returns 'pong'. If express is not installed, please install it."*
3. Once Claude finishes, run the slash command: `/cost`
4. Run the slash command: `/compact`

**Expected Outcome:**
- Claude Code will autonomously execute `npm install express`.
- It will write the Express boilerplate to `index.js` and show you the diff.
- The `/cost` command will output your current token usage and estimated API cost for the session.
- The `/compact` command will summarize your conversation history, compressing it to free up token space while maintaining context.

## Lab 2: Context Engineering & Explicit Referencing (Chapter 1)

**Objective:** Observe the "Goldilocks Rule of Context" by comparing a vague request to a prompt with explicit file referencing.

**Setup:** 
Continue in the `claude-demo-lab1` directory. Create a new utility file:
```bash
echo "module.exports = { calculateSum: (a, b) => Number(a) + Number(b) };" > utils.js
```

**The Prompt/Command:**
*Attempt 1 (The Vague Approach):*
Prompt: *"Add a route to calculate things."*
*(Notice how Claude asks clarifying questions or guesses poorly).*

*Attempt 2 (The Engineered Context Approach):*
Prompt: *"Read `utils.js`. Add a new GET route `/add` in `index.js` that takes query parameters `a` and `b`, uses the `calculateSum` function from `utils.js` to add them, and returns the result as JSON."*

**Expected Outcome:**
- Claude will immediately read `utils.js` to understand the imported function.
- It will correctly modify `index.js` to require `utils.js` and implement the precise `req.query` parsing needed, proving that explicit file references lead to zero-shot success.

## Lab 3: Automating Git and GitHub Workflows (Chapter 5)

**Objective:** Use Claude Code to understand code changes, write semantic commit messages, and execute version control operations.

**Setup:** 
Initialize a git repository in your project directory and stage your current work.
```bash
git init
git add index.js package.json package-lock.json utils.js
```

**The Prompt/Command:**
Prompt: *"Review my staged changes. Create a single, descriptive commit message following the Conventional Commits format (e.g., feat: ...). After showing me the message, go ahead and execute the commit."*

**Expected Outcome:**
- Claude will run a background shell command like `git diff --staged` or `git status`.
- It will analyze the diffs and generate a precise commit message (e.g., `feat: setup express server with ping and calculate endpoints`).
- It will use the `git commit -m` command to successfully commit your staged files.

## Lab 4: Planning and Deep Agent Execution (Chapters 6 & 11)

**Objective:** Experience Claude's strategic planning phase and let it execute a multi-step task autonomously.

**Setup:** 
Create a feature specification document in your directory:
```bash
echo "# Feature Request: Rate Limiting
Add rate limiting to the Express server in index.js.
Requirements:
1. Max 5 requests per minute per IP.
2. Return a 429 status code with a custom error message if exceeded.
3. Use a lightweight in-memory store." > feature-x.md
```

**The Prompt/Command:**
Prompt: *"Act as a deep agent to implement the feature described in `feature-x.md`. Before writing any application code, draft a step-by-step technical plan and save it to a new file called `PLAN.md`. Wait for my approval before executing the plan."*

**Expected Outcome:**
- Claude will read `feature-x.md`.
- It will generate a markdown file (`PLAN.md`) outlining the steps (e.g., Step 1: Install `express-rate-limit`, Step 2: Configure middleware, Step 3: Apply to routes).
- It will pause and ask you: *"Do you approve this plan?"*
- Upon replying "Yes", Claude will methodically work through the steps, updating code and installing packages.

## Lab 5: Customizing Output Styles & Enforcing Rules (Chapter 8)

**Objective:** Use a project-level configuration file to force Claude Code to adhere to strict stylistic and architectural guidelines.

**Setup:** 
Create a global instruction file that acts as the project's "brain".
```bash
echo "# Project Guidelines
- Response Format: All Express API responses MUST be wrapped in a standard JSON format: { \"success\": boolean, \"data\": object | null, \"error\": string | null }
- Tone: Be extremely concise. Output only the requested changes." > CLAUDE.md
```

**The Prompt/Command:**
Prompt: *"Update the `/ping` route in `index.js` to return the current server timestamp."*

**Expected Outcome:**
- Because of `CLAUDE.md`, Claude will automatically apply your architectural constraints.
- Instead of returning a plain string or raw JSON, it will enforce the wrapper: `{ "success": true, "data": { "timestamp": "2023-10-27T..." }, "error": null }`.
- Claude's conversational text in the terminal will be notably brief.

## Lab 6: Delegating to Subagents (Chapter 7)

**Objective:** Delegate a highly scoped, repetitive task to a worker subagent to preserve main context tokens.

**Setup:** 
Create a new directory with undocumented code.
```bash
mkdir math-lib
echo "export const sub = (a, b) => a - b;" > math-lib/sub.js
echo "export const mul = (a, b) => a * b;" > math-lib/mul.js
```

**The Prompt/Command:**
Prompt: *"Spawn a subagent to analyze the `math-lib` directory. Instruct it to add detailed JSDoc comments to every exported function explaining the parameters and return type. It must not modify any business logic."*

**Expected Outcome:**
- The main Claude orchestrator will formulate a prompt and spin up a subagent process.
- The subagent will independently read `sub.js` and `mul.js`.
- It will write correct `/** ... */` annotations to the files.
- The main agent will report back that the subagent successfully completed the task, keeping your main context window unpolluted by the individual file reads.
