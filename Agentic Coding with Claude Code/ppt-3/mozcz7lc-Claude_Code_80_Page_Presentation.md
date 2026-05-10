# Expanded Presentation Outline: Agentic Coding with Claude Code (Part 1)

## Chapter 1: Context Engineering

### Slide 1.1: The Paradigm Shift: From Prompting to Context Engineering
- **Detailed Bullet Points**:
  - Transitioning from zero-shot or few-shot prompts to structural context management.
  - Context engineering focuses on establishing durable environments rather than transient requests.
  - Recognizing context as code: treating configuration, readmes, and system prompts as versioned artifacts.
  - Shifting developer focus from "how to write the code" to "how to define the environment for the agent".
  - Warning: Overloading context leads to attention dilution; precision is key to maintaining model performance.
- **Code Snippet / CLI Command**:
  ```markdown
  # Bad Context
  Fix the bug in the login function.

  # Good Context (Context Engineering)
  Project: E-commerce API (Node.js/Express)
  Constraint: Use explicit type guards for user session objects.
  Task: Resolve null pointer exception in `src/auth/login.ts` at line 42.
  ```
- **Speaker Notes**:
  Welcome to Chapter 1. We are fundamentally shifting our mindset from "prompt engineering" to "context engineering". Prompting is what you do for a single, isolated query. Context engineering is what you do when you are building an environment for an autonomous agent to live and work in over an extended period. We are no longer just asking a model a question; we are providing it with a workspace, a set of rules, architectural guidelines, and continuous state. The main architectural warning here is context bloat. If you feed the agent everything, it loses focus. We must architect our context to be lean, relevant, and highly structured, treating these instructions as first-class citizens in our version control system.

### Slide 1.2: System-Level Context vs. Ephemeral Context
- **Detailed Bullet Points**:
  - Delineating long-lived project constraints (System) from immediate task requirements (Ephemeral).
  - System-level context governs overarching architecture, code style, and testing frameworks.
  - Ephemeral context includes active error logs, current file diffs, and temporary user directives.
  - Architectural Warning: Blurring these lines causes agents to hyper-fixate on global rules instead of local fixes, or vice versa.
  - Edge Case: Dealing with contradicting contexts where an ephemeral instruction violates a system-level constraint.
- **Code Snippet / CLI Command**:
  ```json
  // System Context (project.json)
  { "style": "functional", "test_framework": "jest", "strict_types": true }
  
  // Ephemeral Context (Current Turn)
  "Fix the failing test in UserLogin.test.ts due to a missing mock."
  ```
- **Speaker Notes**:
  It is critical to distinguish between what the agent needs to know forever, and what it needs to know right now. System-level context is your project's constitution—it defines the architectural patterns, the formatting rules, and the immutable constraints. Ephemeral context is the current weather—it's the stack trace, the immediate bug report, the current open files. If you mix these up, the agent gets confused. An edge case to watch out for is when a developer gives an ephemeral prompt that contradicts a system rule—for instance, asking the agent to use a 'quick hack' when the system context demands strict type safety. You must design your context hierarchies to handle these overrides predictably.

### Slide 1.3: Creating and Curating `CLAUDE.md`
- **Detailed Bullet Points**:
  - The `CLAUDE.md` file acts as the primary anchor for Claude Code's system-level context.
  - Best practices for structuring: Build instructions, Lint commands, Test commands, and specific coding conventions.
  - Ensuring deterministic agent behavior by providing explicit terminal commands rather than vague English descriptions.
  - Advanced tactic: Using directory-specific `CLAUDE.md` files for monorepos or microservices to scope context tightly.
  - Warning: Keep the file concise. Exceeding 200-300 lines can dilute the importance of critical constraints.
- **Code Snippet / CLI Command**:
  ```markdown
  # CLAUDE.md
  ## Build Commands
  - UI: `cd frontend && npm run build`
  - API: `cd backend && cargo build --release`
  
  ## Code Style
  - Use early returns to avoid deep nesting.
  - Prefer immutable data structures.
  ```
- **Speaker Notes**:
  The `CLAUDE.md` file is where you codify your project's DNA. It's the first thing Claude Code reads to orient itself. To get the best results, do not just list rules; list the exact commands the agent needs to run to validate its work. Instead of saying "run the tests," write "npm run test:unit". This gives the agent a deterministic way to verify its actions. An advanced tactic for large monorepos is to place a `CLAUDE.md` in each subdirectory, allowing the agent to switch context dynamically depending on whether it's working on the frontend in React or the backend in Rust. Just remember to keep these files punchy.

### Slide 1.4: Dynamic Context Management and RAG
- **Detailed Bullet Points**:
  - Overcoming static context limitations with Retrieval-Augmented Generation (RAG).
  - How Claude Code automatically indexes the workspace to fetch relevant symbols, definitions, and references.
  - Advanced tactic: Guiding the agent’s retrieval focus using targeted search queries instead of loading entire files.
  - Handling large codebases: Strategies to prevent the agent from getting lost in irrelevant abstractions.
  - Edge Case: Shadowed variables or identically named classes across different modules confusing the retrieval mechanism.
- **Code Snippet / CLI Command**:
  ```bash
  # Guiding Claude Code to specific context
  claude "Search for the implementation of 'AuthService' and update the token expiration logic, ignoring the mock files."
  ```
- **Speaker Notes**:
  While `CLAUDE.md` is static, modern codebases are massive and dynamic. Claude Code relies heavily on search and retrieval—similar to RAG—to pull in the context it needs on the fly. However, it's not magic. You must learn to guide the agent. If you have an `AuthService` in your core library and a mock `AuthService` in your tests, the agent might pull the wrong one. You mitigate this by being explicit in your ephemeral context, telling it exactly which paths to search or which patterns to ignore. By mastering dynamic context, you enable the agent to navigate codebases that are far larger than its context window.

### Slide 1.5: The Impact of Context Window Limits
- **Detailed Bullet Points**:
  - Understanding the hard limits of token windows and the cost of maximizing them.
  - "Lost in the middle" phenomenon: Why putting crucial instructions at the beginning or end of context matters.
  - Advanced tactic: Context summarization. Instructing the agent to summarize findings before proceeding to the next step.
  - Warning: Unbounded loops where the agent repeatedly reads large files, rapidly exhausting the token budget.
  - Edge Case: Working with minified files or massive JSON datasets that consume disproportionate tokens.
- **Code Snippet / CLI Command**:
  ```bash
  # Example of an instruction to mitigate context bloat
  claude "Read the 5000-line legacy controller, but ONLY output a 3-bullet summary of the routing logic before attempting any edits."
  ```
- **Speaker Notes**:
  Every token has a cost, both in terms of compute latency and potential cognitive degradation for the model. Even with massive context windows, models suffer from the 'lost in the middle' phenomenon, where they forget details buried in the center of a long prompt. As developers, we must treat the context window as a constrained resource. If you point Claude Code at a 10,000-line log file, you will blow your budget and confuse the agent. Instead, use advanced tactics like asking the agent to summarize large files first, or using grep tools to slice out only the relevant lines.

### Slide 1.6: Ephemeral State and Turn History
- **Detailed Bullet Points**:
  - Analyzing how Claude Code maintains state across multiple conversational turns.
  - The compounding effect of errors: How early mistakes in a conversation pollute subsequent context.
  - Tactical reset: Knowing when to clear the conversation history (`/clear`) to establish a clean state.
  - Tracking tool output: Understanding that every tool execution (like bash commands) appends to the context.
  - Architectural Warning: Leaving noisy background processes running that flood the context with verbose logs.
- **Code Snippet / CLI Command**:
  ```bash
  # Good practice: Run tests quietly to save context
  npm test -- --silent
  
  # Bad practice: Verbose logging that fills the context window
  npm test -- --verbose
  ```
- **Speaker Notes**:
  Every command, every output, and every mistake Claude Code makes becomes part of the turn history. This is a double-edged sword. It provides continuity, but it also creates a compounding effect for errors. If the agent goes down a wrong path for three turns, its context is now polluted with bad assumptions. You must monitor this state. A crucial tactic is forcing the agent to use silent or quiet flags on CLI commands. If a test runner spits out 2,000 lines of verbose logs, that entire log is injected into the context, pushing out valuable system instructions. Learn when to use `/clear` to start fresh.

### Slide 1.7: Overcoming Context Fragmentation
- **Detailed Bullet Points**:
  - Context fragmentation occurs when related logic is scattered across dozens of small files.
  - Symptoms: The agent makes incomplete changes, fixing the interface but missing the implementation or tests.
  - Advanced tactic: Asking the agent to map dependencies explicitly before making any code modifications.
  - Mitigating fragmentation with cohesive module design and clear naming conventions.
  - Edge Case: Circular dependencies that cause the agent to endlessly jump between files.
- **Code Snippet / CLI Command**:
  ```bash
  claude "Before modifying 'UserService', identify all files that import it and list the required cascading changes."
  ```
- **Speaker Notes**:
  Modern architectures like microservices or highly modular React applications are great for humans but can cause severe context fragmentation for AI agents. When logic is spread across twenty files, the agent might successfully update a class signature but completely miss updating the corresponding unit tests or downstream consumers. To combat this, we enforce a planning phase. You must instruct the agent to explicitly map out the dependencies and acknowledge the blast radius of a change before it touches a single line of code.

### Slide 1.8: Security and Context Isolation
- **Detailed Bullet Points**:
  - Ensuring sensitive environment variables, API keys, and credentials are kept out of the agent's context.
  - Utilizing `.geminiignore` or `.gitignore` equivalents to blind the agent to specific directories.
  - Architectural Warning: The risk of the agent inadvertently logging or committing secrets found in unencrypted files.
  - Best Practices: Passing credentials via secure environment variable injection rather than hardcoding in configuration files.
  - Edge Case: The agent needing access to a staging database but lacking the secure context to connect.
- **Code Snippet / CLI Command**:
  ```bash
  # .claudeignore
  .env
  .env.*
  secrets.json
  **/*.pem
  ```
- **Speaker Notes**:
  Our final point on context engineering is security. An autonomous agent will read whatever it can access to solve a problem. If you leave a `.env` file containing production database credentials un-ignored, the agent will read it, incorporate it into its context window, and potentially expose it in a log output or commit message. You must treat the agent's environment with zero-trust principles. Use ignore files aggressively. Ensure that any tasks requiring authentication rely on secure, pre-configured environment variables managed by the host system, keeping the raw secrets out of the LLM's text context entirely.

## Chapter 2: The Gist of Claude Code

### Slide 2.1: The Architecture of an Autonomous Agent
- **Detailed Bullet Points**:
  - Defining the difference between a conversational copilot and an autonomous agent.
  - The integration of LLM reasoning with direct filesystem access, terminal execution, and API integration.
  - The continuous feedback loop: Action -> Observation -> Reaction.
  - Advanced tactic: Leveraging the agent's ability to autonomously self-correct based on compiler or linter errors.
  - Edge Case: Infinite loops caused by deterministic failing tests that the agent cannot conceptually resolve.
- **Code Snippet / CLI Command**:
  ```text
  User: "Fix the type errors in the project."
  Agent: [Runs `tsc`] -> [Observes Error in file X] -> [Edits file X] -> [Runs `tsc`] -> [Success]
  ```
- **Speaker Notes**:
  Chapter 2 delves into the core of what makes Claude Code different. We are moving past the Copilot era—where the AI just suggests code for you to accept—into the Agent era. Claude Code is an autonomous entity. It is wired directly into your terminal and filesystem. It doesn't just write code; it runs the compiler, reads the stack trace, and modifies the code again until it works. This Action-Observation loop is its superpower. However, the biggest risk is infinite looping. If a test fails for a reason outside the codebase—say, network latency—the agent might stubbornly rewrite the code forever trying to fix it. We have to design for these edge cases.

### Slide 2.2: The Core Loop: Plan, Act, Validate
- **Detailed Bullet Points**:
  - Breaking down the agent workflow into three distinct phases to ensure stability and correctness.
  - Plan phase: Gathering context, searching files, and proposing an architectural approach.
  - Act phase: Executing specific, targeted file replacements or shell commands.
  - Validate phase: Running test suites and linters to verify the change didn't introduce regressions.
  - Architectural Warning: Skipping the validation phase is the primary cause of compounded codebase corruption.
- **Code Snippet / CLI Command**:
  ```bash
  # Forcing the validation loop
  claude "Refactor the payment gateway. You MUST run 'npm run test:payments' after your changes and ensure it passes before completing the task."
  ```
- **Speaker Notes**:
  To get reliable results from Claude Code, you must enforce the Plan, Act, Validate loop. When humans code, we often blur these steps. For an AI agent, blurring them is disastrous. If the agent just acts without validating, it might break three other modules silently. You must instruct the agent to prove its work. The validate phase is non-negotiable. If you ask it to refactor a component, you must also demand that it runs the specific test suite for that component. Validation is the only path to finality and the only way to prevent silent corruption of your codebase.

### Slide 2.3: Tool Use and Environment Interaction
- **Detailed Bullet Points**:
  - Exploring the specific tools Claude Code uses: `read_file`, `write_file`, `replace`, `run_command`.
  - The `replace` tool: Demanding exact literal string matching to ensure surgical precision during refactoring.
  - The `run_command` tool: Executing bash commands with proper escaping and environment isolation.
  - Advanced tactic: Using AST-based tools or specialized linters via the shell rather than relying solely on regex replacements.
  - Warning: Command injection risks and the importance of escaping user inputs when the agent runs shell scripts.
- **Code Snippet / CLI Command**:
  ```javascript
  // Agent Tool Call Example
  {
    "tool": "replace",
    "file": "src/utils.js",
    "old_string": "const maxItems = 10;",
    "new_string": "const maxItems = process.env.MAX_ITEMS || 10;"
  }
  ```
- **Speaker Notes**:
  Claude Code interacts with your system through a strictly defined set of tools. It doesn't magically edit files; it uses a `replace` tool that requires exact string matching. This is designed for safety—it prevents the AI from accidentally deleting half your file because of a hallucinated line number. Similarly, its ability to run terminal commands is powerful but requires oversight. You should encourage the agent to leverage existing ecosystem tools like `eslint --fix` or `cargo fmt` rather than trying to manually format code using text replacement. It’s faster, safer, and less error-prone.

### Slide 2.4: Agentic Reasoning vs. Rule-Based Execution
- **Detailed Bullet Points**:
  - The distinction between traditional CI/CD pipelines (rule-based) and Claude Code (agentic reasoning).
  - How Claude Code handles ambiguity: Making probabilistic decisions based on contextual clues.
  - The role of the "Chain of Thought": Forcing the agent to write out its reasoning before acting.
  - Edge Case: The agent misinterpreting a convention because of outdated comments or dead code.
  - Tactic: Asking the agent to explicitly state its assumptions before initiating large changes.
- **Code Snippet / CLI Command**:
  ```bash
  claude "Before you begin, list out your understanding of our database migration strategy based on the current files."
  ```
- **Speaker Notes**:
  Unlike a CI/CD pipeline which breaks the moment a script fails, Claude Code uses agentic reasoning to overcome obstacles. If a package manager fails due to a network error, Claude Code can recognize the error, wait, and retry, or try an alternative registry. However, this probabilistic reasoning means it can also make the wrong logical leaps. If your codebase has outdated comments, the agent will read them and might make a fundamentally flawed architectural decision. Therefore, we must mandate transparency. Always ask the agent to output its Chain of Thought and state its assumptions explicitly before it begins heavy execution.

### Slide 2.5: Safe Autonomy: Boundaries and Approvals
- **Detailed Bullet Points**:
  - Designing safety nets to prevent the agent from performing destructive actions (e.g., dropping databases).
  - The concept of "Human in the Loop" (HITL) for high-risk commands and git operations.
  - Configuring Claude Code policies to automatically reject or require confirmation for specific commands.
  - Architectural Warning: Giving the agent overly permissive sudo access or raw database credentials.
  - Best Practice: Isolating the agent in a containerized environment or a dedicated branch.
- **Code Snippet / CLI Command**:
  ```bash
  # Policy Configuration (Pseudo-code)
  ALLOW: npm test, git status, cat, ls
  REQUIRE_APPROVAL: git push, npm publish, dropdb, rm -rf
  ```
- **Speaker Notes**:
  Autonomy is powerful, but unrestricted autonomy is dangerous. We must establish safe boundaries for Claude Code. The primary mechanism is the Human in the Loop, or HITL, protocol. While the agent can autonomously read files and run local tests, actions that modify external state—like pushing code to production, dropping a database, or publishing a package—must require explicit human approval. As engineers, you should configure the agent's environment so that it simply cannot perform catastrophic actions, even if hallucinated. Always run agent workflows in isolated branches or containerized dev environments.

### Slide 2.6: Collaboration Models: Pair Programming vs. Delegation
- **Detailed Bullet Points**:
  - Differentiating between synchronous pairing and asynchronous task delegation.
  - Pair Programming Mode: Fast feedback loops, step-by-step guidance, and interactive problem-solving.
  - Delegation Mode: Fire-and-forget tasks, bulk refactoring, and extensive research operations.
  - Advanced tactic: Using sub-agents to handle specific delegated tasks (e.g., "send the code to a specialized refactoring agent").
  - Warning: Delegating poorly scoped tasks leads to unpredictable and massive code alterations.
- **Code Snippet / CLI Command**:
  ```bash
  # Pair Programming
  claude "Let's write the CSS for the new button. I'll guide you on the exact colors."
  
  # Delegation
  claude "Update all React class components in the 'legacy' folder to functional components with Hooks. Run the test suite after each file."
  ```
- **Speaker Notes**:
  How you interact with Claude Code dictates its effectiveness. In "Pair Programming" mode, you are side-by-side. You give small, micro-instructions, and correct the agent immediately. It's highly interactive. In "Delegation" mode, you hand off a massive, tedious task—like migrating 50 files to a new framework—and walk away. The danger in delegation is poor scoping. If you just say "make the app faster," you will return to find a completely unrecognizable codebase. Delegation requires rigorous, exhaustive context and strict validation rules. We must match the collaboration model to the complexity of the task.

### Slide 2.7: Handling Ambiguity and Incomplete Requirements
- **Detailed Bullet Points**:
  - Strategies for when the agent encounters vague tasks or missing dependencies.
  - Proactive querying: How Claude Code can (and should) ask the user clarifying questions.
  - Using Plan Mode to force the agent to outline the missing requirements before execution.
  - Edge Case: The agent making silent, incorrect assumptions to fill gaps in requirements.
  - Mitigation: Establishing a system rule that "When in doubt, ask; do not guess."
- **Code Snippet / CLI Command**:
  ```markdown
  # In CLAUDE.md
  If a feature request lacks explicit error-handling requirements, you MUST stop and ask the user for clarification using the `ask_user` tool before proceeding.
  ```
- **Speaker Notes**:
  Ambiguity is the enemy of automation. When a human developer hits an ambiguous requirement, they ask a product manager. When an AI hits ambiguity, its default behavior is often to guess and hallucinate a path forward to please the user. We have to train the agent out of this habit. By using system-level instructions in `CLAUDE.md`, we can force the agent to halt and use the `ask_user` tool when it encounters missing data. If the database schema isn't defined, the agent shouldn't invent one; it should ask. Enforcing Plan Mode for complex tasks is a great way to catch ambiguity before code is written.

### Slide 2.8: The Lifecycle of a Claude Code Session
- **Detailed Bullet Points**:
  - Understanding the initialization, execution, and termination phases of a session.
  - How context accumulates and performance degrades over a long, continuous session.
  - Best Practice: Embracing short-lived, task-specific sessions over week-long sprawling conversations.
  - Commit boundaries: Using Git commits to snapshot progress and provide natural breakpoints for the agent.
  - Warning: Retaining stale context from solved problems that confuses the agent on new tasks.
- **Code Snippet / CLI Command**:
  ```bash
  # Ideal workflow
  claude "Implement login feature"
  git commit -am "feat: add login"
  # Exit and start a NEW session
  claude "Now build the logout feature"
  ```
- **Speaker Notes**:
  A Claude Code session should not be a never-ending chat log. Just like human memory, the agent's context window gets cluttered with the ghosts of past tasks. If you spend an hour fixing a tricky CSS bug, and then ask the agent to design a database schema in the same session, the agent's attention is still polluted by CSS context. The best practice is to treat sessions as ephemeral. Open a session, accomplish a specific, scoped task, commit the code, and then terminate the session. Starting fresh ensures maximum context availability and razor-sharp focus for the next task.

## Chapter 3: Getting Started with Claude Code - Essential Commands

### Slide 3.1: Installation and Security Sandboxing
- **Detailed Bullet Points**:
  - Prerequisites for running Claude Code securely: Node.js environments and API key management.
  - Global vs. Local installation paradigms and managing tool versions.
  - Advanced tactic: Running Claude Code within isolated Docker containers or ephemeral DevContainers.
  - Architectural Warning: Ensuring the CLI operates with the principle of least privilege on the host machine.
  - Edge Case: Conflicting system dependencies when the agent attempts to install missing packages globally.
- **Code Snippet / CLI Command**:
  ```bash
  # Secure initialization using environment variables, avoiding hardcoded keys
  export ANTHROPIC_API_KEY="sk-..."
  npm install -g @anthropic-ai/claude-code
  claude --version
  ```
- **Speaker Notes**:
  Before we use the tool, we have to secure it. Claude Code is a powerful application that executes arbitrary commands on your machine. You should avoid running it with root privileges. The most professional way to deploy it is within an isolated environment, like a DevContainer or a Docker image, ensuring that even if the agent hallucinates a destructive command, the host machine remains untouched. Furthermore, strict management of your API keys via environment variables, rather than configuration files, is paramount to prevent accidental commits of sensitive data.

### Slide 3.2: Basic Invocation and The Interactive REPL
- **Detailed Bullet Points**:
  - Navigating the primary Read-Eval-Print Loop (REPL) interface of Claude Code.
  - Synchronous querying vs. issuing actionable commands.
  - Using natural language to interact with the filesystem (e.g., "What files changed recently?").
  - Advanced tactic: Pipelining standard output from other CLI tools directly into Claude Code.
  - Warning: Mistaking the REPL for a standard bash prompt and issuing naked system commands.
- **Code Snippet / CLI Command**:
  ```bash
  # Passing context directly via stdin
  git diff | claude "Review these changes for security vulnerabilities before I commit."
  ```
- **Speaker Notes**:
  The interactive REPL is your primary interface. It looks like a terminal prompt, but it's fundamentally different. You aren't typing bash commands directly; you are conversing with an intelligence that *can* type bash commands. A highly effective workflow is to pipe the output of standard Unix tools directly into Claude. By doing `git diff | claude`, you bypass the need for the agent to figure out what changed, instantly providing it with the exact context required to perform a code review. This hybrid approach of traditional CLI pipelines and AI reasoning is incredibly potent.

### Slide 3.3: Managing Context State: `/clear` and `/compact`
- **Detailed Bullet Points**:
  - The absolute necessity of the `/clear` command to reset the conversational context window.
  - Recognizing the symptoms of context degradation: repeated loops, ignoring new instructions, sluggish responses.
  - Using `/compact` (if available) to summarize previous turns and retain critical data while freeing tokens.
  - Advanced tactic: Establishing a workflow habit of clearing the context after every successful `git commit`.
  - Edge Case: Clearing the context and accidentally losing the overarching system constraints for the session.
- **Code Snippet / CLI Command**:
  ```text
  > /clear
  Context cleared. Ready for a new task.
  ```
- **Speaker Notes**:
  As we discussed in the context engineering chapter, the context window fills up. When Claude Code starts ignoring your instructions or repeating the same failed fix, its context is saturated. Your primary weapon against this is the `/clear` command. You must build muscle memory to use this command frequently. Treat `/clear` like washing your hands between surgical procedures. Finish a task, verify the code, commit it, and immediately run `/clear`. This guarantees the agent tackles the next problem with maximum cognitive bandwidth and no preconceived biases from the last issue.

### Slide 3.4: Deep Dives with the `/bug` and Feedback Commands
- **Detailed Bullet Points**:
  - Utilizing built-in feedback loops to report anomalies or poor agent behavior.
  - How diagnostic commands capture system state, logs, and trace data for debugging the agent itself.
  - Advanced tactic: Using the feedback loop to refine internal custom prompts or `CLAUDE.md` configurations.
  - Warning: Relying on the tool to fix itself without human intervention in infinite failure states.
  - The distinction between a bug in your code and a bug in the agent's logic.
- **Code Snippet / CLI Command**:
  ```text
  > /bug The agent is repeatedly failing to recognize the locally installed Python environment.
  ```
- **Speaker Notes**:
  Claude Code is an evolving tool. Sometimes, the issue isn't your code; it's the agent's internal logic or tool execution failing. The `/bug` command is crucial here. It doesn't just send a text message; it captures the diagnostic state, the tool call history, and the environmental context. As an engineer, you must distinguish between the agent failing to write good code and the agent failing to operate its tools correctly. Providing rich, detailed feedback via these commands helps improve the core model, but locally, it signals that you may need to step in and manually execute a command to unblock the agent.

### Slide 3.5: Navigating the File System and Searching
- **Detailed Bullet Points**:
  - How Claude Code utilizes advanced `grep` and `glob` searches to navigate massive repositories.
  - Bypassing manual directory traversal by giving semantic search instructions.
  - Advanced tactic: Instructing the agent to search *by regex* or *by AST pattern* to find specific implementations.
  - Edge Case: The agent getting overwhelmed by `node_modules` or `.git` directories if ignore files are misconfigured.
  - Warning: Broad searches returning thousands of matches, paralyzing the context window.
- **Code Snippet / CLI Command**:
  ```bash
  claude "Find all instances of 'localStorage.getItem' in the 'src' directory, ignoring test files, and convert them to use the new 'SecureStore' utility."
  ```
- **Speaker Notes**:
  One of the most powerful features of Claude Code is its ability to index and search your project autonomously. You do not need to tell it which file to open. However, because it uses real tools like `grep` under the hood, you must apply the same hygiene you would on the command line. If you don't have your `.gitignore` set up correctly, the agent might try to search through gigabytes of compiled binaries or `node_modules`, crashing the session or wasting tokens. Always explicitly scope the search in your prompt, telling it exactly which directories to include or exclude to guarantee precision.

### Slide 3.6: The `/plan` Command for Complex Architectures
- **Detailed Bullet Points**:
  - Transitioning into "Plan Mode" to enforce a read-only research and design phase.
  - Preventing premature code modifications by requiring a written, step-by-step strategy first.
  - Advanced tactic: Reviewing and amending the agent's generated plan before authorizing the execution phase.
  - Architectural Warning: Skipping Plan Mode for cross-cutting concerns (like API changes) results in fragmented, broken code.
  - Edge Case: The plan relies on a deprecated library version found during the research phase.
- **Code Snippet / CLI Command**:
  ```text
  > /plan Design a migration strategy from SQLite to PostgreSQL for the user authentication module.
  ```
- **Speaker Notes**:
  For trivial bug fixes, standard execution is fine. But when you ask Claude Code to refactor an entire module or implement a complex new feature, you must use the `/plan` command. Plan Mode restricts the agent to read-only tools. It can search, read files, and analyze, but it cannot write code. It is forced to output a comprehensive design document first. This gives you, the human architect, a chance to review its strategy, correct its assumptions, and ensure alignment with the broader system architecture before a single line of code is mutated. It is the most critical command for complex engineering.

### Slide 3.7: Emergency Interventions: The `/stop` Command
- **Detailed Bullet Points**:
  - Taking immediate control when the agent begins executing a destructive or runaway process.
  - How `/stop` interrupts internal processing, tool execution, and the action-observation loop.
  - Advanced tactic: Using `/stop` to inject mid-flight corrections without completely abandoning the current context.
  - Edge Case: Background shell commands spawned by the agent continuing to run even after the agent loop is halted.
  - Best Practice: Combining `/stop` with `git restore` to revert half-baked file modifications.
- **Code Snippet / CLI Command**:
  ```text
  > /stop
  Agent halted. 
  > The approach is wrong. Do not use regex. Use the AST parser instead. Continue.
  ```
- **Speaker Notes**:
  When dealing with autonomous agents, things will occasionally go off the rails. The agent might misunderstand a prompt and start systematically deleting critical configuration files, or it might get stuck in an infinite loop running failing tests. The `/stop` command is your emergency brake. It instantly halts the agent's thought process and tool execution. Crucially, it doesn't kill the session. You can stop the agent, explain why its current trajectory is flawed, give it a new directive, and let it resume. However, always verify if it spawned detached background processes, as those might require manual termination.

### Slide 3.8: Configuration Profiles and Themes
- **Detailed Bullet Points**:
  - Customizing the CLI environment for different workflows, aesthetics, and verbosity levels.
  - Managing multiple profiles for different environments (e.g., `work`, `personal`, `experimental`).
  - Advanced tactic: Tuning the agent's default system prompt via profile configurations to enforce specific personas.
  - Edge Case: Profile configurations silently overriding local `CLAUDE.md` instructions, causing unexpected behavior.
  - Warning: Ensuring API keys and secrets are cleanly separated across profiles to avoid cross-contamination.
- **Code Snippet / CLI Command**:
  ```bash
  claude config set theme "dark"
  claude config set default-profile "work-backend"
  ```
- **Speaker Notes**:
  Finally, Chapter 3 covers customizing your workspace. Claude Code allows you to configure different profiles. This is highly useful if you bounce between different tech stacks or clients. You might have a profile heavily optimized for strict enterprise Java development with high verbosity, and another lightweight profile for a personal Python scripting project. Just be aware of the inheritance hierarchy. You need to understand how global profile settings interact with the local `CLAUDE.md` files. Always ensure your project-specific rules take precedence over global configurations to maintain deterministic builds.

## Chapter 4: Extending Claude Code with MCP Servers and Plugins

### Slide 4.1: Introduction to the Model Context Protocol (MCP)
- **Detailed Bullet Points**:
  - MCP as the standardized bridge between foundation models and external data sources or tools.
  - Overcoming the isolation of LLMs by enabling secure, local, and remote API interactions.
  - The Client-Server architecture: Claude Code as the client, custom tools as the server.
  - Advanced tactic: Standardizing internal company tooling by wrapping them in MCP interfaces for AI consumption.
  - Architectural Warning: The latency overhead introduced by routing agent thought processes through multiple external MCP servers.
- **Code Snippet / CLI Command**:
  ```json
  // MCP Configuration snippet
  "mcpServers": {
    "jira-mcp": {
      "command": "node",
      "args": ["/path/to/jira-mcp-server/index.js"]
    }
  }
  ```
- **Speaker Notes**:
  Chapter 4 introduces the most transformative feature: the Model Context Protocol, or MCP. Out of the box, Claude Code can read files and run bash commands. But what if it needs to query your Jira board, pull metrics from Datadog, or interact with a proprietary internal API? You don't want to give it raw API keys and hope it writes the right `curl` commands. MCP provides a standardized, structural protocol to expose these systems as dedicated, type-safe tools to the agent. It turns Claude Code from a local coding assistant into a fully integrated enterprise developer platform.

### Slide 4.2: Anatomy of an MCP Server
- **Detailed Bullet Points**:
  - The core components of an MCP Server: Resources, Prompts, and Tools.
  - Tools: Executable functions exposed to the agent (e.g., `create_ticket`, `query_db`).
  - Resources: Static or dynamic data exposed to the agent (e.g., live API documentation, database schemas).
  - Advanced tactic: Using JSON Schema to rigidly define tool inputs, forcing the agent to conform to strict types.
  - Edge Case: Handling timeouts and network failures gracefully within the MCP server logic to prevent agent crashes.
- **Code Snippet / CLI Command**:
  ```typescript
  // Exposing a Tool in an MCP Server
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    if (request.params.name === "get_user_data") {
      // Execute internal logic securely
      return { content: [{ type: "text", text: data }] };
    }
  });
  ```
- **Speaker Notes**:
  An MCP server is surprisingly simple. It exposes three main things: Resources, Prompts, and Tools. Tools are the most important for agentic coding. When you build an MCP server, you define a tool using JSON schema. This acts as a rigid contract. Claude Code cannot guess the parameters; it must strictly adhere to your schema. This ensures high reliability. If you create a `query_db` tool, you can enforce that the agent only passes read-only queries, handling the actual execution and security validation inside your server code, far away from the AI's prompt space.

### Slide 4.3: Integrating Custom Internal APIs
- **Detailed Bullet Points**:
  - The necessity of MCP for legacy systems or proprietary protocols that the foundation model hasn't learned.
  - Securely bridging the gap between the local agent environment and internal corporate networks via VPNs/VPCs.
  - Advanced tactic: Creating "Read-Only" MCP servers for documentation and "Read-Write" servers for active state manipulation.
  - Architectural Warning: Exposing highly destructive internal APIs (e.g., infrastructure orchestration) without human-in-the-loop checkpoints.
  - Best Practice: Logging every tool invocation at the MCP server level for compliance and auditability.
- **Code Snippet / CLI Command**:
  ```bash
  claude "Use the internal-docs MCP server to find the pagination format for the legacy SOAP API, then implement the fetch logic."
  ```
- **Speaker Notes**:
  Every enterprise has hidden, undocumented, or proprietary systems. LLMs don't know how they work. Instead of pasting documentation into the context window repeatedly, you wrap your internal systems in an MCP server. This allows Claude Code to dynamically query your internal Swagger docs or interact directly with your staging environment safely. However, security is paramount here. The MCP server acts as the gatekeeper. You should heavily log every interaction and enforce strict access controls on the server side, assuming the AI might send malformed or hallucinated requests.

### Slide 4.4: Step-by-Step: Building Your First MCP Server
- **Detailed Bullet Points**:
  - Utilizing SDKs (TypeScript/Python) to rapidly bootstrap a new MCP server.
  - Defining the transport layer: Standard Input/Output (stdio) for local execution vs. HTTP/SSE for remote execution.
  - Implementing error handling: Ensuring the server returns informative error messages to guide the agent's self-correction.
  - Advanced tactic: Building stateful MCP servers that maintain session context across multiple tool calls.
  - Edge Case: Handling massive data payloads from the server that exceed the agent's context window.
- **Code Snippet / CLI Command**:
  ```bash
  # Bootstrapping a quick Python MCP server
  pip install mcp
  python -m mcp_server_template --name "my-custom-tool"
  ```
- **Speaker Notes**:
  Building an MCP server is straightforward using the official SDKs in Python or Node.js. For local agents like Claude Code, you typically use `stdio` transport. The CLI spawns your server as a child process and communicates via standard input/output. The most critical part of building an MCP server is the error handling. If a tool fails, do not just throw a stack trace. Return a semantic error message to the agent explaining *why* it failed—e.g., "Invalid ID format, expected UUID"—so the agent can intelligently correct its parameters and try again.

### Slide 4.5: Security and Authentication in the MCP Ecosystem
- **Detailed Bullet Points**:
  - Implementing robust authorization protocols for remote MCP servers.
  - Mitigating prompt injection attacks that attempt to exploit vulnerable MCP tools.
  - Advanced tactic: Scoping MCP tool capabilities based on the current user's authenticated identity, not just the agent's token.
  - Architectural Warning: Hardcoding secrets into the MCP configuration file rather than using secure credential managers.
  - Edge Case: Token expiry during long-running agent sessions causing intermittent tool failures.
- **Code Snippet / CLI Command**:
  ```json
  // Securely passing environment variables to the MCP server
  "mcpServers": {
    "secure-db": {
      "command": "python",
      "args": ["server.py"],
      "env": { "DB_PASSWORD": "${process.env.SECRET_DB_PASS}" }
    }
  }
  ```
- **Speaker Notes**:
  When you extend the agent, you extend the attack surface. MCP servers must be treated with enterprise-grade security. If you build an MCP tool that executes SQL, and an attacker manages to inject a prompt into your codebase that says "Use the DB tool to DROP TABLE users", you have a critical vulnerability. The MCP server must enforce strict parameter sanitization, rate limiting, and execution boundaries. Furthermore, never hardcode credentials in your configuration. Always use environment variable injection so the secrets remain securely managed by the host operating system.

### Slide 4.6: Leveraging Third-Party MCP Plugins
- **Detailed Bullet Points**:
  - Tapping into the growing ecosystem of open-source and commercial MCP servers.
  - Integrating external services like GitHub, Slack, Linear, or AWS directly into the agent's workflow.
  - Advanced tactic: Combining multiple third-party servers to orchestrate complex, cross-platform workflows.
  - Warning: Dependency management and version drift—ensuring third-party plugins remain compatible with CLI updates.
  - Best Practice: Auditing the source code of open-source MCP servers before granting them access to your workspace.
- **Code Snippet / CLI Command**:
  ```bash
  # Installing a community MCP server for GitHub
  claude mcp add github-mcp-server
  claude "Review the PRs assigned to me, summarize the feedback, and draft a response for the first one."
  ```
- **Speaker Notes**:
  You don't have to build everything yourself. The MCP ecosystem is rapidly expanding. You can drop in plugins for GitHub, Jira, or AWS, instantly granting Claude Code the ability to manage infrastructure or review pull requests autonomously. However, treat these plugins like any third-party dependency. Because these servers execute locally and have access to your credentials, you must audit them. By composing multiple trusted plugins, you create highly complex workflows, like having the agent read a bug report in Jira, find the code, fix it, and open a GitHub PR, all in one seamless execution.

### Slide 4.7: Debugging and Profiling MCP Performance
- **Detailed Bullet Points**:
  - Diagnosing connection issues, transport failures, and schema mismatches between client and server.
  - Using the MCP Inspector tool to manually test server responses independently of the LLM.
  - Advanced tactic: Profiling the latency of tool execution to ensure it doesn't bottleneck the agent's thought loop.
  - Edge Case: Deadlocks caused when an MCP server requires interactive input that the headless agent cannot provide.
  - Mitigation: Designing all MCP tools to be strictly non-interactive and asynchronous.
- **Code Snippet / CLI Command**:
  ```bash
  # Running the MCP inspector for local debugging
  npx @modelcontextprotocol/inspector node my-server.js
  ```
- **Speaker Notes**:
  Debugging a multi-agent or agent-to-tool system is complex. If Claude Code is failing, you need to know if the model is hallucinating or if your custom MCP server is crashing. The MCP Inspector is your best friend here. It allows you to mock the agent and interact with your tools directly via a web UI. Pay close attention to latency. If your custom tool takes 30 seconds to query a database, the agent is sitting idle, and the user experience degrades. Furthermore, ensure all your tools are headless; if a tool pauses to ask for a password prompt, the automated session will deadlock entirely.

### Slide 4.8: Future-Proofing Architectures with MCP
- **Detailed Bullet Points**:
  - Why the decoupled nature of MCP protects your tooling investments as underlying foundation models evolve.
  - Scaling from local developer environments to centralized, cloud-hosted MCP tool registries.
  - Advanced tactic: Designing stateless tool interfaces that allow any compliant agent framework to utilize them seamlessly.
  - The evolution from monolithic agent scripts to micro-tool architectures.
  - Wrap-up: Integrating Claude Code and MCP as the foundational layer for AI-native engineering teams.
- **Code Snippet / CLI Command**:
  ```yaml
  # Vision: A centralized registry of enterprise tools
  architecture: micro-tools
  protocol: mcp-v1
  compatibility: [claude-code, cursor, custom-agents]
  ```
- **Speaker Notes**:
  We conclude Chapter 4 by looking at the architectural implications. The brilliance of MCP is that it decouples your custom tooling from the LLM itself. If you spend weeks building a robust database-querying tool, you aren't locking yourself into Claude Code alone. Because it's a standard protocol, any future agent or IDE that supports MCP can instantly use your tool. We are moving towards a world of 'micro-tools', where enterprise capabilities are exposed via standardized interfaces, allowing a swarm of different specialized AI agents to interact with your corporate infrastructure safely and efficiently.

# Presentation: Agentic Coding with Claude Code

## Chapter 5: Automating Your Development Workflow with Claude Code and GitHub

### Slide 1: Unlocking Continuous Integration with Claude Code
- **Detailed Bullet Points**:
  - Claude Code seamlessly integrates with GitHub to automate issue resolution, PR generation, and code review processes via GitHub Actions.
  - Setup requires the GitHub CLI (`gh`) to be authenticated locally, linking your terminal workspace with the repository identity.
  - Workflows are defined using YAML configuration files placed inside the `.github/workflows` directory, allowing trigger customization.
  - Two primary automation modes are available: interactive tagging on issues/PRs, and automated code review upon PR creation.
  - **Architectural Warning**: The integration only functions inside an explicitly initialized Git repository connected to a remote GitHub project; running setup elsewhere will result in persistent error states.
- **Code Snippet / CLI Command**:
  ```bash
  # Prerequisite installation and authentication for GitHub CLI
  brew install gh
  gh auth login # Select HTTPS and authenticate via browser
  
  # Initialize Claude GitHub app integration inside project directory
  /install-github-app
  ```
- **Speaker Notes**:
  Welcome to Chapter 5. Integrating Claude Code directly into your GitHub workflow transforms the AI from a local assistant into a persistent, autonomous contributor. This setup leverages GitHub Actions as the serverless compute environment. Before diving into the integration, the GitHub CLI must be fully authenticated locally. We trigger the setup directly from the Claude Code CLI, which scaffolds the necessary YAML files for CI/CD. Remember, attempting this initialization in an unlinked local directory is a common edge case that causes silent failures during the authentication handshake.

### Slide 2: The GitHub Workflow Architecture
- **Detailed Bullet Points**:
  - The GitHub integration commits two primary workflow YAMLs: `claude.yml` for issue triggers and `claude-code-review.yml` for PR approvals.
  - The workflow executes using the `anthropics/claude-code-action@beta` step to spin up the Claude environment within the GitHub Action runner.
  - Compute tokens are consumed remotely; you must configure either a long-lived OAuth token (suitable for moderate subscription use) or a direct API key (for high-frequency enterprise scale).
  - Secrets are securely managed via GitHub Actions Secrets (e.g., `CLAUDE_CODE_OAUTH_TOKEN`), keeping sensitive data out of the repository.
  - **Edge Case**: If the repository lacks adequate Actions permissions, Claude's automated self-review and PR merging processes will stall pending manual admin overrides.
- **Code Snippet / CLI Command**:
  ```yaml
  name: Claude Code
  on:
    issue_comment:
      types: [created]
  jobs:
    claude:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Run Claude Code
          uses: anthropics/claude-code-action@beta
          with:
            claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
  ```
- **Speaker Notes**:
  This slide breaks down the actual architecture of the automation. When you authorize the GitHub app, it creates a Pull Request adding YAML files that dictate how and when Claude acts. The action listens for specific webhook events, like a comment creation. Security is paramount here: your Anthropic API tokens are injected dynamically as secrets. A crucial decision for your team is choosing between an API key or a subscription-based OAuth token—the former scales infinitely but risks billing bloat, while the latter caps your usage to prevent runaway costs.

### Slide 3: Resolving Issues via Tagging
- **Detailed Bullet Points**:
  - Developers can summon the agent to solve bugs directly in GitHub by tagging `@claude` in issue comments.
  - Triggering the agent initiates a real-time Action where Claude generates a dynamic to-do list, performing context discovery before writing code.
  - Claude never works on the `main` branch; it automatically provisions isolated branches following naming conventions like `claude/issue/<issue-number>`.
  - The raw Action logs expose JSON tool calls and MCP inputs, which is invaluable for deep debugging of agent hallucination.
  - **Deep Insight**: The agent's isolation mechanism allows multiple issue resolutions to occur concurrently across different remote branches without merge locks.
- **Code Snippet / CLI Command**:
  ```markdown
  <!-- GitHub Issue Comment Trigger -->
  @claude, can you fix this bug? Please notice that you need to edit the function `ice_breaker` to apply the patch.
  ```
- **Speaker Notes**:
  Imagine reviewing an issue ticket and immediately assigning it to an AI. By simply tagging Claude, a GitHub Action spins up, and Claude begins executing a cognitive loop: planning, searching the repository, and implementing fixes. It is critical to understand that Claude defensively creates its own branch. This architectural choice prevents broken code from ever hitting your production branch directly and inherently supports parallel workstreams. If Claude behaves unexpectedly, the GitHub Action logs output the raw JSON tool payloads, giving engineers complete visibility into the AI's internal decision tree.

### Slide 4: The Perils of Missing Context
- **Detailed Bullet Points**:
  - Without explicit context, Claude Code operates on generalized coding assumptions, which can cause subtle but catastrophic bugs.
  - Example: Renaming `linkedin_username` to `linkedin_url` may improve local readability but breaks strict third-party API JSON payload contracts.
  - Agentic systems cannot implicitly know external system constraints unless they are documented within the project boundary.
  - Blindly merging AI-generated PRs without human review circumvents the safety nets that catch logical contract breakages.
  - **Architectural Warning**: Always validate whether a variable rename or refactor spans across API boundaries or database schemas before approving the agent's PR.
- **Code Snippet / CLI Command**:
  ```python
  # Claude's "helpful" but contract-breaking refactor:
  # External API expects 'linkedin_username', but Claude sends:
  response = requests.post(API_URL, json={
      "linkedin_url": profile_url  # FATAL: 400 Bad Request
  })
  ```
- **Speaker Notes**:
  This slide highlights a critical failure mode in agentic coding. In the text, Claude was asked to improve variable readability and rightfully changed `linkedin_username` to `linkedin_url`. The code was syntactically perfect and passed local linters. However, the variable was part of a payload sent to an external third-party API. The API contract was violated, and the system broke. This teaches us that AI is context-bound; it cannot infer external upstream constraints. This reinforces why human code review on AI pull requests is absolutely mandatory, regardless of how confident the agent's PR description reads.

### Slide 5: Engineering Context with CLAUDE.md
- **Detailed Bullet Points**:
  - The `/init` command generates a `CLAUDE.md` file, establishing shared project memory and persistent architectural guidelines for the AI.
  - `CLAUDE.md` documents tech stacks, coding conventions, external API contracts, and directory structures.
  - Providing this explicit repository context severely reduces hallucination and constrains Claude to safe operational boundaries.
  - During initialization, Claude scans files but requires explicit user whitelisting to read local settings, creating a fine-grained permission model.
  - **Advanced Tactic**: Treat `CLAUDE.md` as versioned infrastructure; commit it to the repository so GitHub Actions and remote Claude instances share the exact same context baseline.
- **Code Snippet / CLI Command**:
  ```bash
  # Generate project context memory
  /init
  
  # Add, commit, and push memory to the remote repository
  git add CLAUDE.md
  git commit -m "chore: add CLAUDE.md for agentic context"
  git push origin main
  ```
- **Speaker Notes**:
  To prevent the exact API contract breakage we just discussed, Claude Code relies on Context Engineering. Running `/init` creates a `CLAUDE.md` file. Think of this as the "System Prompt" customized for your specific repository. It maps out your tech stack, your styling preferences, and crucial external dependencies. By committing this file to your codebase, you ensure that every time the GitHub Action spins up a fresh environment, Claude immediately reads the `CLAUDE.md` file to calibrate itself. It is the single most effective way to align the AI's behavior with your team's engineering standards.

### Slide 6: Automated Code Review via Claude
- **Detailed Bullet Points**:
  - Claude can be configured to automatically review every new PR created by humans or other agents.
  - The review workflow (`claude-code-review.yml`) triggers on the `pull_request` event, fetching the diffs and performing a semantic analysis.
  - Claude produces a structured checklist of review steps, evaluating logic, security vulnerabilities, and adherence to `CLAUDE.md`.
  - The review system is highly configurable and can be chained to run *after* CI linters and test execution.
  - **Deep Insight**: Using Claude to review its *own* generated PRs introduces a secondary verification layer, though it should never fully replace human oversight due to potential confirmation bias.
- **Code Snippet / CLI Command**:
  ```yaml
  # Inside claude-code-review.yml
  on:
    pull_request:
      types: [opened, synchronize]
  # Claude will post its review directly as a PR comment
  ```
- **Speaker Notes**:
  Beyond just writing code, Claude acts as a tireless senior reviewer. By enabling the Claude Code Review workflow, every pull request gets an immediate, deep semantic analysis. Claude checks the code against the rules defined in `CLAUDE.md`, looking for security flaws and logical errors. What's fascinating is that you can integrate this into a pipeline where traditional static analysis and linters run first, and Claude provides the final qualitative review. While Claude reviewing its own AI-generated PRs is a neat trick, beware of confirmation bias—human engineers still hold the final responsibility for production deployments.

### Slide 7: Security and Permission Granularity
- **Detailed Bullet Points**:
  - Running autonomous agents in CI requires strict scoping of permissions to prevent unauthorized codebase mutation or secret exfiltration.
  - By default, GitHub Actions workflows limit tokens to the repository scope, but explicitly restricting `contents: write` to specific branches is recommended.
  - Claude's local settings file maintains a whitelist of approved commands, ensuring it cannot arbitrarily execute destructive bash scripts (e.g., `rm -rf`).
  - API token leaks are mitigated by using GitHub Secrets, but the raw tool-call logs must be monitored to ensure no PII or sensitive data is outputted in PR comments.
  - **Architectural Warning**: Never run Claude Code Actions on untrusted forks without requiring approval, as malicious actors could manipulate the prompt via issue creation to execute arbitrary code.
- **Code Snippet / CLI Command**:
  ```yaml
  # Best practice: Restrict permissions in the workflow file
  permissions:
    contents: write
    pull-requests: write
    issues: write
  ```
- **Speaker Notes**:
  Security cannot be an afterthought when giving an AI write access to your repository. This slide covers the attack vectors and mitigations. Claude respects the permission bounds set by GitHub Actions and your local settings. You must ensure that the `CLAUDE_CODE_OAUTH_TOKEN` is protected and that GitHub workflow permissions are explicitly defined. A significant edge case to watch for is prompt injection via public issues. If a malicious user opens an issue with instructions to output secure environment variables, an improperly sandboxed Claude Action might attempt to execute it. Always require manual approval for workflows running on external forks.

### Slide 8: Scaling the Integration and Edge Cases
- **Detailed Bullet Points**:
  - The integration scales elegantly across monorepos and polyglot codebases when directory-specific `CLAUDE.md` files are maintained.
  - Handling merge conflicts agentically remains a challenge; Claude creates the PR, but humans must resolve upstream conflicts if `main` advances significantly.
  - Token consumption scales linearly with the size of the project context and the frequency of PRs/issues; monitor billing alerts closely.
  - If the agent loops continuously due to failing test pipelines, it will exhaust API limits unless hard timeouts are enforced in the GitHub Action.
  - **Deep Insight**: The true power of this integration is unlocked when combined with subagents or Git Worktrees to handle complex, multi-file refactors asynchronously.
- **Code Snippet / CLI Command**:
  ```bash
  # To avoid infinite loops, set a timeout in the Action
  jobs:
    claude:
      timeout-minutes: 15
  ```
- **Speaker Notes**:
  To wrap up Chapter 5, let's look at operational scaling. When deploying Claude across large repositories, managing token consumption becomes a real financial consideration. An AI attempting to fix a persistently failing test might enter a retry loop, burning tokens rapidly—this is why setting strict `timeout-minutes` in your GitHub Action is mandatory. Furthermore, while Claude creates branches effortlessly, it struggles with complex merge conflicts if the target branch moves too fast. The integration is incredibly powerful, but it requires developers to act as orchestrators, monitoring costs, managing conflicts, and providing explicit boundaries.

---

## Chapter 6: Claude Code Planning and Multi-agent Workflows

### Slide 1: The Transition to Spec-Driven Development
- **Detailed Bullet Points**:
  - Agentic coding fails when complex tasks are handled via ad hoc, exploratory prompting, leading to unpredictable file mutations.
  - Planning Mode (`/plan`) forces Claude into a strictly read-only state, shifting the paradigm to Spec-Driven Development.
  - In this phase, the agent acts as an architect: reading files, searching documentation, and utilizing MCP calls to design a solution without writing execution code.
  - By separating strategy from execution, teams establish a verifiable implementation plan that drastically reduces hallucinations and scope creep.
  - **Deep Insight**: Approving a plan creates a bounded problem space, acting as an anchor that restricts the language model from introducing unnecessary side-effects.
- **Code Snippet / CLI Command**:
  ```bash
  # Enter the read-only architectural mode
  /plan
  
  # Prompt: "Create a detailed specification for HookHub..."
  ```
- **Speaker Notes**:
  Welcome to Chapter 6, where we move from basic usage to advanced architectural workflows. If you ask an agent to build a complex system in one prompt, it will inevitably hallucinate or modify files it shouldn't. The solution is Planning Mode. When you type `/plan`, Claude becomes a read-only architect. It searches your codebase, makes tool calls, and drafts a comprehensive specification—but it cannot touch your code. This is spec-driven development. By separating the "thinking" from the "doing," you get the chance to review the blueprint. This eliminates the risk of unintended consequences and significantly increases the success rate of complex tasks.

### Slide 2: Executing the Planning Workflow Lifecycle
- **Detailed Bullet Points**:
  - The workflow follows a strict 4-step sequence: Research/Analysis, Plan Formulation, Human Review, and Execution.
  - During formulation, Claude generates a structured task list defining concepts, technical stack, and required file changes.
  - Refinement is highly iterative; human engineers can provide feedback to the read-only model to tweak UI layouts or data contracts before any code is generated.
  - Only upon explicit human approval does Claude exit planning mode to begin execution.
  - **Edge Case**: If the underlying codebase changes during the prolonged planning phase, the generated specification may become stale, requiring a plan refresh.
- **Code Snippet / CLI Command**:
  ```markdown
  <!-- Iterative Refinement in Planning Mode -->
  User: Remove the carousel layout from the spec and use a grid instead.
  Claude: [Updates the read-only plan document accordingly]
  ```
- **Speaker Notes**:
  The lifecycle in Planning Mode mirrors how senior engineers operate. First, gather context. Second, draft the design document. Third, submit it for review. The beauty of this process is the iterative refinement. In the HookHub example from the text, Claude initially suggested a carousel layout. The user rejected this in favor of a grid. Because Claude hadn't written any React components yet, pivoting cost zero execution tokens. One edge case to watch for: if you spend days in planning mode on a fast-moving repo, the underlying codebase might change, rendering your specification instantly obsolete upon execution.

### Slide 3: Persisting Project Memory
- **Detailed Bullet Points**:
  - A finalized plan is ephemeral unless explicitly exported; it must be saved as a Markdown artifact (e.g., inside a `.claude` or `docs` directory).
  - Persisting the specification converts it into permanent project memory, accessible by future Claude sessions and subagents.
  - The `.md` file becomes the single source of truth, constraining the agent's behavior and serving as shared documentation for human developers.
  - **Advanced Tactic**: Link the persisted specification inside the global `CLAUDE.md` to ensure all parallel agents reference the exact same architectural blueprint.
  - **Architectural Warning**: Do not overwrite architectural specifications automatically; manual versioning of planning files prevents loss of design context.
- **Code Snippet / CLI Command**:
  ```bash
  # After plan refinement, instruct Claude to save the output
  User: Export this specification to docs/hookhub_spec.md
  
  # Reference it in future sessions
  User: Implement the feature exactly as described in docs/hookhub_spec.md
  ```
- **Speaker Notes**:
  A plan is only as good as its permanence. Once you and Claude finalize the specification, you must explicitly instruct it to export the plan to a Markdown file. This transforms a fleeting chat context into permanent project memory. For example, saving it to `docs/hookhub_spec.md`. Why is this vital? Because in a multi-agent workflow, every new agent needs to know the grand design. By persisting the spec and committing it to Git, you create an anchor. Every agent you spin up can be pointed to this document, ensuring they all row in the same direction without hallucinating competing architectures.

### Slide 4: Introduction to Multi-Agent Parallelism
- **Detailed Bullet Points**:
  - Claude Code allows executing multiple autonomous agent instances concurrently within the same project to dramatically reduce delivery time.
  - Think of parallel agents as multiple developers sharing the same GitHub branch, each with full read/write access to the repository.
  - The effectiveness of this strategy hinges entirely on identifying and assigning strictly independent tasks.
  - **Deep Insight**: The developer's role elevates from writing syntax to orchestrating concurrent AI workstreams, monitoring logs, and managing state across terminals.
  - **Architectural Warning**: Shared read/write access on a single branch is inherently fragile; overlapping file access will result in race conditions and corrupted states.
- **Code Snippet / CLI Command**:
  ```bash
  # Terminal 1
  claude -- prompt "Update HookCard.tsx"
  
  # Terminal 2 (Running concurrently)
  claude -- prompt "Redesign Hero.tsx"
  ```
- **Speaker Notes**:
  Now we reach the holy grail: multi-agent parallelism. Imagine spinning up three terminals, each running a separate instance of Claude Code, and assigning them different tasks. This is the equivalent of adding three engineers to your team for an afternoon. In the text's example, one agent updates the `HookCard` component while another simultaneously redesigns the `Hero` section. However, with great power comes great fragility. They are operating on the same branch. The engineer's job is no longer to code, but to act as a project manager, carefully partitioning tasks to ensure these agents don't collide.

### Slide 5: The Independence Constraint
- **Detailed Bullet Points**:
  - Parallel execution requires tasks to be strictly orthogonal; e.g., styling a frontend component while fixing a localized backend utility bug.
  - Sequential tasks (e.g., building a backend API and then consuming it on the frontend) cannot be parallelized without stubbing/mocking, which AI struggles to coordinate dynamically.
  - File-level isolation is mandatory. If two agents attempt to append logic to `App.tsx` simultaneously, file corruption or Git conflicts are inevitable.
  - Code modularity (separating components into single files) is not just a human best practice; it is a structural prerequisite for agentic scaling.
  - **Edge Case**: Shared dependencies (like updating `package.json`) will cause lockfile collisions if two agents install different packages at the same moment.
- **Code Snippet / CLI Command**:
  ```bash
  # DANGER: Overlapping file edits
  Agent 1: "Add user auth to api/routes.ts"
  Agent 2: "Add payment webhook to api/routes.ts"
  # Result: Race condition, overwritten logic, syntax errors.
  ```
- **Speaker Notes**:
  Parallelism will destroy your project if you violate the Independence Constraint. You cannot assign two agents to modify the same file at the same time. If Agent A and Agent B both write to `routes.ts`, whoever saves last overwrites the other, creating corrupted logic. Furthermore, sequential tasks—like building an API and writing the UI that calls it—must be done in order. You must adopt extremely modular codebases. Breaking components into distinct, isolated files isn't just for human readability anymore; it is a strict structural requirement to allow armies of AI agents to work concurrently without stepping on each other's toes.

### Slide 6: Executing the HookHub Parallel Scenario
- **Detailed Bullet Points**:
  - The baseline is established via a specific Git commit (`project/hookhub`), ensuring all agents share identical starting context.
  - Agent 1 is explicitly scoped: `"Modify only src/components/HookCard.tsx. Do not modify other files."`
  - Agent 2 is explicitly scoped: `"Redesign the hero section. Modify only src/components/Hero.tsx. Do not modify HookCard."`
  - Providing explicit negative constraints (`"Do not modify..."`) prevents agents from performing unprompted "cleanup" refactoring that causes conflicts.
  - The successful merge of their simultaneous work demonstrates the viability of multi-agent development for highly modular UI tasks.
- **Code Snippet / CLI Command**:
  ```bash
  # Establishing the clean baseline before launching parallel agents
  git checkout project/hookhub
  git reset --hard <commit-hash>
  npm install && npm run dev
  ```
- **Speaker Notes**:
  Let's walk through the actual HookHub scenario from the text. We start by resetting our branch to a known baseline. Then, we launch our two terminals. The secret sauce here is how the prompts are crafted. We don't just tell Agent 1 what to do; we explicitly tell it what *not* to do. "Modify only HookCard.tsx. Do not modify other files." AI agents love to be helpful; they will spontaneously decide to fix a typo in a neighboring file if they see it. By applying these strict negative constraints, we enforce file-level isolation, guaranteeing that when the agents finish, their code merges flawlessly.

### Slide 7: Moving Beyond Single-Branch Parallelism
- **Detailed Bullet Points**:
  - While single-branch parallel execution is easy to demonstrate, it is not scalable for enterprise-grade applications.
  - The industry-standard approach for agent concurrency involves leveraging Git Worktrees or isolated branches.
  - Git Worktrees allow multiple agents to operate in entirely separate directory instances with independent copies of the codebase, neutralizing race conditions.
  - Changes from worktrees are subsequently compiled into discrete Pull Requests, enforcing a structured merge and review workflow.
  - **Deep Insight**: Transitioning to Worktrees transforms AI agents from "simultaneous local typists" into independent, asynchronous feature developers.
- **Code Snippet / CLI Command**:
  ```bash
  # Creating isolated worktrees for agents
  git worktree add ../feature-hero branch-hero
  git worktree add ../feature-card branch-card
  # Agents run in the respective worktree directories
  ```
- **Speaker Notes**:
  The single-branch technique we just covered is great for simple demos, but it is too fragile for real-world enterprise use. If you want to scale to dozens of agents, you must use Git Worktrees or separate branches. A Git Worktree checks out multiple branches into separate physical directories on your hard drive. This means Agent 1 and Agent 2 have completely isolated filesystems. They can install dependencies, modify overlapping files, and rewrite history without ever colliding. Once they finish, you simply review their separate Pull Requests. This isolates changes and treats AI agents exactly like remote human contributors.

### Slide 8: Anti-patterns in Multi-Agent Orchestration
- **Detailed Bullet Points**:
  - **The "Do Everything" Prompt**: Assigning an entire epic to a single agent leads to token exhaustion, context decay, and cascading failures.
  - **Assuming Interface Contracts**: Letting frontend/backend parallel agents assume API shapes without a shared specification file results in integration nightmares.
  - **Ignoring Action Logs**: Failing to monitor the background tool calls means missing loops where agents fight over test failures.
  - **Lack of Verification Gate**: Allowing agents to commit directly without running local test suites or linters compromises project integrity.
  - **Architectural Warning**: Always ensure that automated linters (`eslint`, `prettier`) run as post-generation hooks, or agents will introduce massive style regressions.
- **Code Snippet / CLI Command**:
  ```bash
  # Validate combined agent outputs before committing
  npm run lint && npm run build && npm run test
  git add . && git commit -m "Merge parallel agent updates safely"
  ```
- **Speaker Notes**:
  To conclude Chapter 6, let's review the anti-patterns that will crash your workflow. First, the "Do Everything" prompt—if a task spans 20 files, break it down; otherwise, the model's context window will decay, and it will forget its objective. Second, never let agents guess contracts; always point them to the `docs/spec.md` you generated in Planning Mode. Finally, never trust the agents blindly. Before you stage and commit their parallel work, you must run your linters and test suites. Orchestrating AI isn't about letting go of the wheel; it's about shifting your oversight from syntax-level debugging to system-level verification.

---

## Chapter 7: Working with Claude Code Subagents

### Slide 1: Introduction to Claude Code Subagents
- **Detailed Bullet Points**:
  - Subagents represent an evolution from manual parallel terminals to programmatically orchestrated, specialized autonomous actors.
  - A subagent is a strictly scoped instance of the language model invoked to solve a granular, highly specific sub-task.
  - The Main Agent acts as the Orchestrator, dynamically spawning subagents, delegating tasks, and synthesizing their outputs.
  - Subagents excel at tasks requiring deep focus and high token consumption, such as log analysis, test generation, or localized refactoring.
  - **Deep Insight**: By offloading work to subagents, the Orchestrator preserves its own context window, keeping the main loop lean and strategic.
- **Code Snippet / CLI Command**:
  ```javascript
  // Conceptual Orchestrator -> Subagent delegation
  const testSubagent = await spawnSubagent({
    role: "QA Engineer",
    task: "Write exhaustive unit tests for HookCard.tsx",
    context: ["src/components/HookCard.tsx"]
  });
  ```
- **Speaker Notes**:
  Welcome to Chapter 7, where we explore the pinnacle of agentic workflows: Subagents. In the previous chapter, we manually opened terminals to run parallel agents. Subagents automate this entirely. Think of the Main Agent as your Staff Engineer. When confronted with a massive task, it doesn't do all the typing itself. Instead, it acts as an Orchestrator, programmatically spinning up a "Subagent" to handle a specific, deep-focus task—like writing a massive test suite. The beauty of this is context preservation. The Orchestrator doesn't pollute its own memory with the thousands of lines of test code; it simply receives a clean summary from the subagent upon completion.

### Slide 2: Defining Subagent Capabilities and Scope
- **Detailed Bullet Points**:
  - Subagents are not generic; they are instantiated with hyper-specific system prompts mapping them to distinct roles (e.g., Codebase Investigator, License Auditor).
  - Scope boundaries are rigidly enforced. A test-writing subagent should only have permissions to read source code and write to the `/tests` directory.
  - They can be provisioned with specialized toolsets or MCP servers that the Main Agent might not need, optimizing tool-call latency.
  - **Architectural Warning**: Giving a subagent broad, unfocused tasks ("Fix the app") negates the pattern's benefits and guarantees hallucination.
  - Subagents terminate immediately after fulfilling their specific directive, returning execution control to the Orchestrator.
- **Code Snippet / CLI Command**:
  ```bash
  # CLI invocation of a specific subagent role
  claude invoke code_investigator --prompt "Map the dependency graph of Hero.tsx"
  ```
- **Speaker Notes**:
  A subagent is defined by its limitations. If you create a subagent to write tests, you restrict its scope so it can only write to the test directory. You give it a specialized system prompt, telling it to adopt the persona of a rigorous QA engineer. You might even give it specialized tools, like a coverage analyzer, that the main orchestrator doesn't need. This specialization reduces the cognitive load on the LLM. It's crucial to remember that subagents are ephemeral. They wake up, complete their highly granular task, hand the result back to the orchestrator, and terminate. Broad prompts kill subagents; extreme specificity makes them shine.

### Slide 3: Inter-Agent Communication Protocols
- **Detailed Bullet Points**:
  - Subagents communicate with the Orchestrator exclusively through structured outputs (often JSON or summarized Markdown) rather than conversational text.
  - The Orchestrator passes necessary context (file paths, goal state) downwards, and the subagent passes empirical results (diffs, test results) upwards.
  - This strict interface prevents the Orchestrator from being overwhelmed by the verbose inner monologues and tool-call logs of the subagent.
  - **Edge Case**: If a subagent encounters a blocker outside its scope, it must fail gracefully and return a diagnostic error to the Orchestrator for reassignment.
  - **Deep Insight**: The protocol relies heavily on deterministic summaries. The subagent compresses hours of exploratory work into a 3-bullet-point executive summary.
- **Code Snippet / CLI Command**:
  ```json
  // Typical Subagent return payload
  {
    "status": "success",
    "files_modified": ["src/tests/Hero.test.tsx"],
    "test_coverage": "98%",
    "summary": "Implemented 12 unit tests. Edge cases covered."
  }
  ```
- **Speaker Notes**:
  How do agents talk to each other? They don't chat. They use strict communication protocols. The Orchestrator passes down an exact payload: "Here is the file path, here is your objective." The subagent goes off, runs maybe 50 tool calls, reads 10 files, writes code, and tests it. But it doesn't send that massive transcript back to the Orchestrator. Instead, it compresses that entire journey into a structured JSON payload or a tight Markdown summary. This is vital for managing context windows. If the subagent fails—say, it realizes it needs database access it doesn't have—it must throw a graceful exception back up the chain, allowing the Orchestrator to pivot.

### Slide 4: Developing Custom Specialized Subagents
- **Detailed Bullet Points**:
  - Teams can develop custom subagents tailored to proprietary internal systems, APIs, or unique domain logic.
  - Creation involves defining a YAML or JSON manifest that dictates the subagent's name, description, system prompt, and allowed tools.
  - Custom subagents can be bound to internal MCP (Model Context Protocol) servers to fetch real-time data from internal databases safely.
  - By wrapping legacy bash scripts or complex CLI tools within a custom subagent, legacy infrastructure becomes accessible to the agentic workflow.
  - **Advanced Tactic**: Create a "Security Auditor" subagent that automatically scans PRs for secret leaks and CVEs using local security binaries before allowing a commit.
- **Code Snippet / CLI Command**:
  ```yaml
  # Example Subagent Manifest
  name: security_auditor
  description: "Scans codebase for vulnerabilities"
  tools:
    - name: run_trivy_scan
      command: "trivy fs ."
  system_prompt: "You are a SecOps auditor. Run trivy and report critical CVEs."
  ```
- **Speaker Notes**:
  While Claude Code comes with built-in subagents, the true power for enterprises lies in building custom ones. Let's say your company has a highly complex, legacy deployment script. You can write a custom subagent manifest that wraps that script, gives it a specific persona, and exposes it to the Orchestrator. You could build a "Security Auditor" subagent that uses internal tools like Trivy to scan code. Because this subagent is specialized, it knows exactly how to read the Trivy logs and summarize the vulnerabilities. This abstracts the complexity away from the Main Agent, creating a clean, modular ecosystem of AI capabilities tailored precisely to your business.

### Slide 5: The Architect-Coder-Tester Pattern
- **Detailed Bullet Points**:
  - The most effective multi-agent pattern delegates the software lifecycle across three distinct roles: Architect, Coder, and Tester.
  - **The Architect** uses Planning Mode to generate the specification (`spec.md`) and orchestrates the workflow.
  - **The Coder Subagent** receives the spec and implements the raw logic, modifying source files autonomously.
  - **The Tester Subagent** receives the diffs and the spec, writing and executing tests, passing failures back to the Coder.
  - **Architectural Warning**: Do not allow the Coder to write its own tests; separating these subagents prevents the AI from writing superficial tests that merely echo flawed logic.
- **Code Snippet / CLI Command**:
  ```bash
  # The Orchestrator automates this pipeline
  1. Architect -> Generates spec.md
  2. invoke coder --context spec.md --target src/
  3. invoke tester --context spec.md --target tests/
  ```
- **Speaker Notes**:
  This slide introduces the golden standard of multi-agent workflows: The Architect-Coder-Tester Pattern. Think of the Main Agent as the Architect. It plans the feature and writes the spec. It then invokes the Coder subagent to write the actual code. Once the Coder finishes, the Architect invokes the Tester subagent. Crucially, the Tester must be a separate subagent. If you ask the same AI that wrote the code to test it, it often writes "happy path" tests that validate its own logical flaws. By instantiating a completely fresh Tester subagent that only reads the spec and the finished code, you introduce an adversarial dynamic that catches edge cases and ensures robust software.

### Slide 6: Token Economics and State Management
- **Detailed Bullet Points**:
  - Subagent invocation is expensive; every new subagent requires processing its system prompt, context payload, and subsequent tool loops.
  - Managing state is critical: passing entire codebases into subagents results in massive token bloat and API rate limiting.
  - The Orchestrator must employ "lazy loading" of context, passing only the exact file paths or diffs the subagent needs to function.
  - Output token caps must be strictly enforced on subagents to prevent runaway generation if the subagent gets caught in a hallucination loop.
  - **Deep Insight**: The most efficient subagent orchestrators use intelligent caching, only re-invoking subagents if the underlying target files have changed since the last run.
- **Code Snippet / CLI Command**:
  ```javascript
  // Good: Passing explicit, minimal context
  invoke_agent("tester", { files: ["src/utils/math.ts"] })
  
  // Bad: Token exhaustion
  invoke_agent("tester", { files: ["src/**/*.ts"] }) // Will crash context window
  ```
- **Speaker Notes**:
  We need to talk about token economics. Multi-agent workflows are computationally expensive. When the Orchestrator spins up a subagent, it consumes API tokens for the prompt, the context, and the tool calls. If your Orchestrator lazily passes the entire repository context to every subagent, you will burn through your budget and hit API rate limits instantly. State management requires surgical precision. Pass only the exact files the subagent needs. Enforce hard timeouts. If a subagent gets confused and enters an infinite loop trying to fix a typo, it will drain your account unless strict token caps are mathematically enforced at the architectural level.

### Slide 7: Sandboxing and Execution Safety
- **Detailed Bullet Points**:
  - Subagents operating autonomously must be strictly sandboxed; malicious prompt injections in issue tickets could theoretically hijack a subagent.
  - Network access for subagents should be zero-trust, utilizing MCP servers to broker data rather than allowing arbitrary `curl` commands.
  - Leverage containerization (e.g., Docker) to run subagent execution environments, ensuring that filesystem mutations are ephemeral and discardable.
  - Implementing an "approval gate" where the Orchestrator pauses to require human validation before merging subagent PRs is the ultimate fail-safe.
  - **Edge Case**: A subagent generating infinite recursive loops of sub-processes will cause local out-of-memory (OOM) crashes unless the shell environment is restricted.
- **Code Snippet / CLI Command**:
  ```bash
  # Running subagent execution within a bounded Docker container
  docker run -v $(pwd):/workspace agent_sandbox claude invoke test_runner
  ```
- **Speaker Notes**:
  Security and sandboxing are critical when delegating autonomy to subagents. Imagine a scenario where a subagent reads a GitHub issue containing a malicious prompt injection instructing it to exfiltrate your `.env` file. To prevent this, subagents must operate in a zero-trust environment. Network access should be heavily restricted, and filesystem writes should ideally happen inside temporary containers or Git Worktrees. Never let a subagent execute arbitrary bash scripts without whitelisting. The ultimate safety net is the Orchestrator's approval gate. The subagents can do all the heavy lifting, but the Main Agent—or a human—must pull the lever to actually merge the code.

### Slide 8: Debugging the Multi-Agent Matrix
- **Detailed Bullet Points**:
  - Debugging multi-agent systems is exponentially harder than debugging single agents due to asynchronous state and inter-agent communication boundaries.
  - Distributed tracing principles must be applied: every subagent must log its invocation ID, prompt payload, tool execution timeline, and raw output.
  - When a subagent fails silently, the Orchestrator might hallucinate a success state; deterministic validation (e.g., parsing actual test output) is mandatory.
  - Log aggregation of MCP calls provides the observability required to understand why a subagent chose a specific, flawed implementation path.
  - **Architectural Warning**: Avoid deep nesting of subagents (subagents spawning subagents). Keep the hierarchy flat (Orchestrator -> Subagents) to maintain debuggability.
- **Code Snippet / CLI Command**:
  ```bash
  # Reviewing aggregated subagent trace logs
  cat .claude/logs/orchestrator_trace.json | jq '.events[] | select(.agent == "coder")'
  ```
- **Speaker Notes**:
  We conclude Chapter 7 with the reality of debugging. When a single agent fails, you read the chat log. When a multi-agent system fails, it's like debugging a distributed microservices architecture. Did the Orchestrator pass the wrong file? Did the Coder hallucinate? Did the Tester write a bad test? To survive, you must apply distributed tracing principles. Log every JSON payload passed between agents. Rely on deterministic validation—make the Orchestrator read the actual XML test reports, not the subagent's summary, to confirm success. And fundamentally, keep your agent hierarchy flat. If you allow subagents to spawn their own subagents, you create an un-debuggable black box of AI behavior. Keep it flat, keep it logged, and keep it deterministic.


# Presentation Outline: Agentic Coding with Claude Code (Expanded Part 3)

## Chapter 8: Creating and Customizing Output Styles

### Slide 1: The Anatomy of Claude Code Output Styles
- **Detailed Bullet Points**:
    - Understanding how Claude Code formats its output is crucial for integration into automated pipelines and CI/CD systems.
    - Default output styles prioritize human readability, utilizing markdown formatting for code blocks, bulleted lists for explanations, and conversational text.
    - Customizing output styles involves creating specific system prompts or configuration flags that enforce strict formatting rules.
    - You can suppress conversational filler (the "chatty" aspect of AI) to receive pure, actionable code or raw data formats.
    - The structural integrity of the output (e.g., ensuring a JSON payload is well-formed without markdown backticks) is a common challenge addressed by custom styles.
- **Code Snippet / CLI Command**:
    ```bash
    claude --style raw-json --prompt "Analyze src/main.js and return cyclomatic complexity"
    ```
- **Speaker Notes**: When we use Claude Code out of the box, it wants to talk to us. It wants to explain what it did, how it did it, and maybe wish us a good day. That's great for an interactive session, but it's a nightmare if you're piping the output into `jq` or another script. Customizing output styles isn't just about aesthetics; it's about programmatic interoperability. By defining strict output styles, we constrain the LLM's natural language generation capabilities and force it to act as a structured data generator.

### Slide 2: Crafting Strict System Prompts for Formatting
- **Detailed Bullet Points**:
    - The most effective way to customize output is through deeply directive system prompts that define the exact output schema.
    - Using XML tags within your prompt to specify desired output sections helps the model understand boundaries and structure.
    - Negative prompting (e.g., "Do NOT include introductory text") is essential for eliminating preamble and postamble.
    - Advanced formatting requests should provide a "few-shot" example within the prompt to set a clear pattern for the model to follow.
    - Be aware of the token overhead: highly constrained output prompts require more input tokens but save on output tokens and parsing logic.
- **Code Snippet / CLI Command**:
    ```xml
    <instruction>
      Provide the result strictly in this format, with no other text:
      <output>
        <status>SUCCESS|FAILURE</status>
        <message>...</message>
      </output>
    </instruction>
    ```
- **Speaker Notes**: Let's talk about the mechanics of forcing an LLM to behave. You can't just ask nicely; you have to build a fence around the output. We use XML tags because models like Claude are heavily trained to recognize and respect XML boundaries. When you use negative prompts, you have to be explicit. Saying "just the code" often fails. Saying "Do not output any markdown formatting, do not output any conversational text, output only the literal code" has a much higher success rate. This slide shows how we build that constraint.

### Slide 3: Structured Data Outputs (JSON and YAML)
- **Detailed Bullet Points**:
    - Forcing Claude Code to output valid JSON or YAML enables direct ingestion by other tools in your developer ecosystem.
    - A critical edge case is the model injecting markdown code block syntax (e.g., \`\`\`json) around the payload, which breaks naive JSON parsers.
    - Mitigate parsing errors by instructing the model to escape quotes correctly and avoid trailing commas.
    - YAML is sometimes preferred over JSON for LLM output because it is more forgiving of formatting nuances and string escaping issues.
    - Always validate the output programmatically before passing it to the next step in your workflow.
- **Code Snippet / CLI Command**:
    ```bash
    claude "List all dependencies in package.json with vulnerabilities. Output ONLY valid JSON." | jq '.vulnerabilities[]'
    ```
- **Speaker Notes**: JSON is the lingua franca of modern APIs, but LLMs are text generators, not JSON serializers. Getting consistent JSON out of an LLM requires defensive prompting. The biggest headache you'll run into is the model wrapping your perfect JSON in markdown code blocks. You have to explicitly tell it not to do that, or you have to build a wrapper script that strips the markdown before parsing. Interestingly, YAML can often be a safer bet because it doesn't fail catastrophically if a quote is misplaced.

### Slide 4: Customizing Verbosity and Detail Levels
- **Detailed Bullet Points**:
    - Controlling verbosity is essential for managing context window limits and reducing token costs.
    - "High verbosity" styles are useful for deep-dive explanations, architectural reviews, and generating comprehensive documentation.
    - "Low verbosity" or "Terse" styles are ideal for simple bug fixes, fast iterations, and terminal-based workflows where screen real estate is premium.
    - You can dynamically adjust verbosity by passing context-specific flags or by switching configuration profiles.
    - Warning: Too low verbosity can lead to the model skipping crucial context or failing to explain complex, non-obvious code changes.
- **Code Snippet / CLI Command**:
    ```bash
    # Setting verbosity in configuration
    claude config set verbosity low
    claude "Fix the off-by-one error in loop.py"
    ```
- **Speaker Notes**: Verbosity is a dial, not a switch. You want high verbosity when you're asking Claude to explain a legacy codebase you just inherited. You want low verbosity when you're iterating on a CSS fix and you just want the updated class. But there's a danger here: if you set the verbosity too low on a complex task, the model might produce "clever" code without any comments explaining why it took that approach. Finding the right balance for the specific task at hand is key to a smooth workflow.

### Slide 5: Defining Project-Specific Style Guides
- **Detailed Bullet Points**:
    - Claude Code can adhere to your team's specific coding standards (e.g., Airbnb JavaScript Style Guide, PEP 8).
    - Implementing a custom style guide involves referencing standard conventions or providing custom rules in a `GEMINI.md` or `.claude.md` file.
    - Style guides should dictate not just formatting (indentation, quotes) but also architectural preferences (e.g., "prefer functional composition over inheritance").
    - Ensure your custom style instructions include rules for documentation (e.g., JSDoc formats, inline comment density).
    - When onboarding a new project, running Claude Code with a specific style profile ensures immediate consistency.
- **Code Snippet / CLI Command**:
    ```markdown
    <!-- In project knowledge file -->
    ## Coding Style
    - Use 2 spaces for indentation.
    - Prefer React Functional Components with Hooks.
    - Always add JSDoc comments to exported functions.
    ```
- **Speaker Notes**: You don't want Claude writing code that looks like it belongs in a different repository. The real power comes when you codify your team's unwritten rules. Put your style guide in a configuration file that Claude reads on startup. This isn't just about spaces vs. tabs; it's about architectural patterns. If your team hates nested ternaries, tell Claude. If you require strict typing, mandate it. This transforms Claude from a generic coding assistant into a member of your specific engineering team.

### Slide 6: Template-Driven Output Generation
- **Detailed Bullet Points**:
    - For repetitive tasks (e.g., generating boilerplate, scaffolding tests), you can use template-driven output styles.
    - Provide Claude Code with a "fill-in-the-blanks" template and instruct it to populate the variables based on the context.
    - Templates ensure absolute consistency across generated files and drastically reduce the prompt engineering required for each task.
    - Advanced templating can include conditional logic instructions (e.g., "If the function is async, include the Async suffix in the template").
    - Be mindful that complex templates might confuse the model if the structural constraints contradict its training data.
- **Code Snippet / CLI Command**:
    ```text
    Prompt: Use the following template to generate the test file.
    Template:
    import { {FunctionName} } from './{FileName}';
    describe('{FunctionName}', () => {
      it('should {ExpectedBehavior}', () => {
        // Implementation
      });
    });
    ```
- **Speaker Notes**: When you need to scaffold 50 API endpoints, you don't want Claude getting creative. You want a factory line. By feeding Claude a strict template and asking it to merely populate the specific variables, you guarantee uniformity. This is particularly powerful for test generation or creating standard boilerplate like Redux actions or CRUD controllers. The trick is to make the template clear enough that the model doesn't try to "fix" your formatting.

### Slide 7: Managing Diff and Patch Output Styles
- **Detailed Bullet Points**:
    - When modifying existing files, the output style can dictate how changes are presented: full file replacements or unified diffs.
    - Unified diffs (`.patch` format) are highly efficient for large files as they minimize token usage and output generation time.
    - However, models can struggle with generating perfectly applying diffs if the context window lacks the exact surrounding lines.
    - A safer, hybrid approach is requesting a search-and-replace format (e.g., "Find this exact block, replace with this block").
    - Using tools like `patch` or `git apply` to automatically ingest Claude Code's diff output requires strict validation to prevent corrupted files.
- **Code Snippet / CLI Command**:
    ```bash
    claude "Add null checking to processData. Output a unified diff." > fix.patch
    git apply fix.patch
    ```
- **Speaker Notes**: How does Claude actually change a file? It can spit out the entire new file, which is safe but incredibly slow and expensive for large files. Or, it can output a diff. Generating diffs is the holy grail of efficiency, but it's fragile. If Claude gets the context lines wrong by even one character, the patch fails. We often see a "search-and-replace" output style as the sweet spot: it's more robust than a strict unified diff, but far more efficient than rewriting a 2000-line file.

### Slide 8: Error Fallbacks and Graceful Degradation
- **Detailed Bullet Points**:
    - When enforcing complex output styles, models will occasionally fail to adhere to the constraints (e.g., breaking JSON format).
    - Robust integrations require fallback mechanisms: if parsing fails, prompt the model again with the specific parse error.
    - "Graceful degradation" involves accepting a partially formatted output and using heuristic scripts (like regex) to extract the needed data.
    - Implement a retry loop with an escalating "strictness" prompt when the initial output style is violated.
    - Logging style violations helps identify edge cases in your prompts and refine your structural constraints over time.
- **Code Snippet / CLI Command**:
    ```python
    try:
        data = json.loads(claude_output)
    except json.JSONDecodeError as e:
        retry_prompt = f"Your previous output failed JSON parsing: {e}. Output pure JSON."
        # Call Claude again
    ```
- **Speaker Notes**: You must assume the LLM will eventually break your format. It's probabilistic; it's inevitable. If you're building automated pipelines around Claude Code, your parsing logic needs error handling. Don't just crash. Catch the JSON error, and feed that error back to Claude. Say, "You gave me an unescaped quote on line 4, try again." This self-correcting loop is essential for building resilient agentic systems. If you don't build in fallbacks, your automation will be brittle.

---

## Chapter 9: Understanding Agent Skills

### Slide 1: Introduction to Agent Skills
- **Detailed Bullet Points**:
    - Agent skills are modular, specialized capabilities that extend Claude Code beyond its base knowledge and default tools.
    - They represent a paradigm shift from monolithic agents to highly specialized, tool-equipped experts.
    - Skills can encapsulate domain-specific knowledge, complex API integrations, or proprietary internal workflows.
    - By loading specific skills, you focus the agent's context and capabilities, reducing hallucinations and improving task success rates.
    - Skills are defined declaratively, often using structured formats (JSON/YAML) alongside executable code.
- **Code Snippet / CLI Command**:
    ```bash
    # Activating a specific skill for a session
    claude --use-skill aws-deployment-expert
    ```
- **Speaker Notes**: Think of Agent Skills as giving Claude a utility belt. Instead of having one massive agent that knows a little bit about everything, you load specific skills for the task at hand. If you're deploying to AWS, you load the AWS deployment skill. This gives the agent access to specific tools, specific API documentation, and specific contextual rules that it wouldn't have otherwise. It narrows the focus, which drastically reduces the chance of the model getting confused or hallucinating incorrect commands.

### Slide 2: The Architecture of a Skill
- **Detailed Bullet Points**:
    - A typical skill consists of three core components: a manifest (metadata), instructions (system prompts), and tools (executable actions).
    - The **Manifest** defines the skill's name, description, and triggers, allowing the orchestrator to know when to invoke it.
    - **Instructions** provide the specialized persona and constraints. They tell the agent *how* to behave when the skill is active.
    - **Tools** are the actual functions the skill can execute (e.g., reading a database, hitting an API endpoint).
    - Skills must be designed with clear boundaries to prevent overlapping capabilities and conflicting instructions.
- **Code Snippet / CLI Command**:
    ```yaml
    name: "Database Query Skill"
    description: "Executes read-only queries against the staging database."
    tools:
      - name: "execute_sql"
        path: "./tools/exec_sql.sh"
    ```
- **Speaker Notes**: How is a skill actually built? It's not magic. It's a structured package. The manifest is the interface; it's how Claude knows the skill exists. The instructions are the brain, giving Claude the context it needs to use the skill effectively. And the tools are the hands. The most critical architectural decision here is boundary management. If you have two skills that both think they are responsible for file system manipulation, they will conflict. Keep skills scoped and focused.

### Slide 3: Defining Tool Inputs and Schemas
- **Detailed Bullet Points**:
    - Tools within a skill must have rigorously defined input schemas, typically using JSON Schema syntax.
    - Schemas dictate exactly what parameters the LLM must provide when invoking the tool, including types, required fields, and descriptions.
    - Rich descriptions within the schema are crucial; they act as prompt instructions for the LLM on how to populate the parameters.
    - The orchestrator validates the LLM's output against the schema *before* executing the tool, preventing malformed requests.
    - Complex tools might require nested objects or arrays, which demand highly descriptive schema definitions to ensure accuracy.
- **Code Snippet / CLI Command**:
    ```json
    "parameters": {
      "type": "object",
      "properties": {
        "query": { "type": "string", "description": "The SQL query to execute." }
      },
      "required": ["query"]
    }
    ```
- **Speaker Notes**: When Claude decides to use a tool, it generates a JSON object. How does it know what to put in that object? The schema. The schema is the contract between the LLM and the executable code. A common mistake is writing schemas with poor descriptions. The description field isn't just documentation for you; it's the primary instruction for the model. If a parameter is named "flag", the model might not know what to do. If the description says "Set to true to force override," the model understands perfectly.

### Slide 4: Skill Execution and State Management
- **Detailed Bullet Points**:
    - When a skill executes a tool, the output (stdout/stderr) is returned to the agent's context window.
    - Managing state across multiple skill executions is challenging; skills are generally stateless, relying on the orchestrator's history.
    - Large tool outputs must be truncated or paginated to avoid blowing out the context window.
    - Agents must be programmed to handle asynchronous tool executions, polling for results or waiting for callbacks.
    - "Tool failure" is a valid state; agents must be equipped to read error messages and attempt self-correction.
- **Code Snippet / CLI Command**:
    ```text
    > Tool execution failed: stderr: "Connection refused"
    Claude: "The database connection failed. I will try to read the local cache instead using the cache-reader skill."
    ```
- **Speaker Notes**: Execution is where things get messy. Claude calls a tool, the tool runs, and the output comes back. But what if the output is a 10-megabyte log file? It will destroy the context window. Good skill design involves wrapping tools to ensure they return concise, actionable summaries rather than raw firehoses of data. Furthermore, skills should fail gracefully. When an API call fails, the tool should return the specific error so Claude can decide whether to retry, fix the parameters, or pivot to a new strategy.

### Slide 5: Composing Workflows with Multiple Skills
- **Detailed Bullet Points**:
    - Complex tasks require the sequential or parallel invocation of multiple different skills.
    - The "Orchestrator Pattern" involves a primary agent that decides *which* skill to invoke based on the current step in the plan.
    - Data passed between skills must be explicitly managed; output from a 'Search Skill' might be the input for an 'Analysis Skill'.
    - Designing a robust routing mechanism is essential to ensure the agent doesn't get stuck in loops, repeatedly calling the wrong skill.
    - Dependency management between skills requires clear instructions (e.g., "Do not use the Deployment Skill until the Testing Skill returns success").
- **Code Snippet / CLI Command**:
    ```javascript
    // Conceptual workflow
    const data = await agent.run(SearchSkill, query);
    const summary = await agent.run(SummarySkill, data);
    await agent.run(ReportSkill, summary);
    ```
- **Speaker Notes**: Real-world tasks are rarely solved by one tool. You need a workflow. Think of an automated PR reviewer: it needs a Git skill to pull the code, a Linter skill to check style, and an Analysis skill to review logic. The challenge is choreography. The agent needs to know the dependency graph of these skills. It has to know that it can't analyze the code until it pulls the code. Providing the agent with a clear "Standard Operating Procedure" in its system prompt helps it string these skills together effectively.

### Slide 6: Security and Sandboxing for Skills
- **Detailed Bullet Points**:
    - Agent skills, especially those executing shell commands or database queries, present significant security risks (prompt injection leading to RCE).
    - Implementing the Principle of Least Privilege is mandatory; a skill should only have access to the exact resources it needs.
    - Run highly privileged tools inside secure sandboxes (e.g., Docker containers, restricted VMs) to contain potential breaches.
    - Implement "Human-in-the-Loop" (HITL) authorization for destructive actions (e.g., `DROP TABLE`, `git push --force`).
    - Audit logging of all skill invocations, inputs, and outputs is necessary for compliance and post-mortem analysis.
- **Code Snippet / CLI Command**:
    ```bash
    # Tool configuration requiring approval
    name: "Deploy to Production"
    requires_approval: true
    sandbox: "docker-prod-env"
    ```
- **Speaker Notes**: This is the most critical slide in the deck. When you give an AI the ability to run code on your machine, you are opening a massive attack vector. If a malicious user can inject a prompt into a log file that Claude is reading, they could trick Claude into executing a harmful shell command. You must sandbox your skills. If a skill doesn't need network access, disable it. If a skill is about to modify production state, pause execution and ask a human for a thumbs-up. Security cannot be an afterthought here.

### Slide 7: Testing and Debugging Agent Skills
- **Detailed Bullet Points**:
    - Traditional unit testing is insufficient for skills due to the non-deterministic nature of LLMs.
    - "Evaluation Frameworks" (Evals) are required to test skills against a suite of prompts, measuring accuracy and adherence to instructions.
    - Debugging a failing skill requires tracing the exact prompt sent to the LLM, the raw tool call generated, and the tool's output.
    - Mocking external services is essential for reliable skill testing without hitting live APIs.
    - "Agentic loops" (where the agent repeatedly calls a tool with bad arguments) are a common failure mode requiring careful schema adjustments.
- **Code Snippet / CLI Command**:
    ```bash
    # Running an evaluation suite against a skill
    claude-eval run tests/skill_evals.yaml --skill git-manager
    ```
- **Speaker Notes**: How do you test something that gives a slightly different answer every time? You can't just assert equals. You have to use Evals. You run the skill against a hundred different scenarios and measure the success rate. When a skill fails, debugging is like forensics. You have to look at the exact trace: what did the prompt say, what JSON did the model build, what did the script return? Usually, failures are due to ambiguous tool descriptions in the schema, not the underlying script itself.

### Slide 8: Building a Custom Skill: Step-by-Step
- **Detailed Bullet Points**:
    - Identify a repetitive, well-defined task that currently requires manual intervention.
    - Draft the tool script (e.g., a Python script) that performs the atomic action securely.
    - Define the JSON schema for the tool, ensuring parameter descriptions are clear instructions for the LLM.
    - Write the skill's system instructions, establishing its persona, constraints, and standard operating procedures.
    - Integrate, test via Evals, and iterate based on how the LLM actually utilizes the tool in practice.
- **Code Snippet / CLI Command**:
    ```yaml
    # The final integration step: registering the skill
    skills:
      - name: "LogAnalyzer"
        entrypoint: "node ./skills/logAnalyzer.js"
    ```
- **Speaker Notes**: Let's bring it all together. Building a skill is an iterative process. You don't start with the AI; you start with the script. Write a rock-solid bash or Python script first. Then, you write the schema. The schema is the bridge. Then you write the instructions. And finally, you watch the agent try to use it. You'll likely find that the agent misinterprets your schema at first. That's fine. You tweak the descriptions, tighten the constraints, and try again until the skill operates flawlessly.

---

## Chapter 11: Understanding Deep Agents

### Slide 1: What Are Deep Agents?
- **Detailed Bullet Points**:
    - Deep Agents represent a structural evolution from single-prompt interactions to autonomous, multi-step problem-solving entities.
    - They are characterized by their ability to maintain context over long horizons and execute complex plans iteratively.
    - Unlike standard conversational agents, Deep Agents utilize specific cognitive architectures (like ReAct or Plan-and-Solve).
    - They actively interact with their environment, observing the results of their actions and adjusting their strategies accordingly.
    - Deep Agents blur the line between a coding assistant and an autonomous software engineer.
- **Code Snippet / CLI Command**:
    ```text
    Agent Status:
    [x] Planning Phase Complete
    [ ] Executing Step 1: Analyze DB Schema
    [ ] Step 2: Generate Migrations
    ```
- **Speaker Notes**: We are moving beyond "autocomplete on steroids." A deep agent isn't just answering a question; it's taking on a project. It plans, it executes, it verifies. This is the difference between asking for a code snippet and asking an agent to "Migrate this application from PostgreSQL to MongoDB." A deep agent will break that massive task down, look at the files, write the migrations, test them, and fix the errors it encounters along the way. It's a continuous, stateful loop of autonomous action.

### Slide 2: Cognitive Architectures: ReAct and Beyond
- **Detailed Bullet Points**:
    - The ReAct (Reasoning and Acting) framework is foundational for Deep Agents, forcing the model to explicitly state its thoughts before acting.
    - The cycle typically follows: Observation -> Thought -> Action -> Observation.
    - Explicit reasoning allows the agent to break down complex tasks and prevents impulsive, incorrect tool usage.
    - Advanced architectures introduce dedicated "Planning" phases before execution begins, creating a roadmap.
    - "Reflection" nodes allow the agent to evaluate its own progress and recognize when it has gone down a rabbit hole.
- **Code Snippet / CLI Command**:
    ```text
    Thought: I need to find the authentication middleware.
    Action: grep_search("verifyToken")
    Observation: Found in src/auth.js.
    Thought: Now I will review the file to see how tokens are validated.
    ```
- **Speaker Notes**: The ReAct pattern is what makes deep agents reliable. If an LLM just spits out actions, it often hallucinates. By forcing the LLM to write down its "Thought" before its "Action", we drastically improve its logical consistency. It's like asking a junior developer to explain their plan before they start typing. It slows them down, but it prevents massive mistakes. Newer architectures are adding Reflection—teaching the agent to stop, look at the mess it just made, and say, "Wait, this approach isn't working, let's revert and try something else."

### Slide 3: Managing Infinite Loops and Context Exhaustion
- **Detailed Bullet Points**:
    - The two greatest failure modes for Deep Agents are getting stuck in repetitive loops and exhausting the context window limit.
    - Loops occur when an action repeatedly yields the same error, and the agent lacks the reasoning capability to try a novel approach.
    - Context exhaustion happens when tool outputs (e.g., massive log dumps) fill the token limit, causing the agent to "forget" its original instructions.
    - Mitigations include hard step limits (e.g., `max_iterations=10`), loop detection heuristics, and aggressive context summarization.
    - The agent must be explicitly prompted to summarize its findings periodically and flush raw logs from its working memory.
- **Code Snippet / CLI Command**:
    ```python
    if current_step > MAX_STEPS:
        return "Agent halted: Maximum iterations reached."
    if detect_repetition(action_history):
        force_agent_reflection()
    ```
- **Speaker Notes**: If you run a deep agent unsupervised, you will eventually burn through a massive API bill while the agent loops infinitely. It will run a command, get an error, run the exact same command, get the same error, a thousand times. You have to build in circuit breakers. You need loop detection. And you have to manage memory. If the agent reads a 10,000-line file, its brain is full. It will forget what it was trying to do. You have to implement techniques where the agent reads a file, summarizes it, and then discards the raw text to save context.

### Slide 4: Sub-Agent Delegation
- **Detailed Bullet Points**:
    - To manage complexity, primary orchestrator agents delegate specific tasks to specialized sub-agents.
    - This hierarchical structure keeps the main agent's context clean and focused on high-level strategy.
    - Sub-agents are spun up with a specific prompt, execute their task, return a summary, and terminate.
    - Examples include delegating deep codebase research to an 'Investigator' agent while the main agent handles file modification.
    - Delegation prevents the "jack of all trades, master of none" problem, allowing specialized prompts for different phases of development.
- **Code Snippet / CLI Command**:
    ```javascript
    // Orchestrator delegates task
    const researchSummary = await invokeSubAgent('codebase_investigator', {
      query: "Map out all dependencies for the User model."
    });
    ```
- **Speaker Notes**: Delegation is the secret to scaling AI workflows. If the main agent tries to do everything—read the files, write the code, run the tests—its context window gets polluted and it loses its mind. Instead, the main agent acts like a Tech Lead. It says, "Hey Investigator Agent, go map out the database schema and give me a one-paragraph summary." The Investigator uses all the context it needs, but only returns the summary. This keeps the Tech Lead agent lean, focused, and strategic.

### Slide 5: State Persistence and Memory Management
- **Detailed Bullet Points**:
    - Deep Agents require mechanisms to remember decisions across long sessions and even between restarts.
    - Short-term memory is maintained in the current conversational context window.
    - Long-term memory is often implemented by writing to external storage, such as vector databases or local markdown files (e.g., `MEMORY.md`).
    - Explicit memory management allows the agent to update project facts (e.g., "The team prefers React Hooks") persistently.
    - Routing facts to the correct memory tier (Global vs. Project-specific) is crucial for maintaining an organized knowledge base.
- **Code Snippet / CLI Command**:
    ```bash
    # Agent updates project memory
    claude "Note that we are using Tailwind CSS for this project in MEMORY.md"
    ```
- **Speaker Notes**: If your agent forgets the architecture decisions you made yesterday, it's not a true colleague. Deep agents solve this by externalizing their memory. Instead of relying purely on the LLM's context window—which resets every session—the agent is given tools to read and write to files. In Claude Code, this often takes the form of markdown files like `GEMINI.md` or `MEMORY.md`. The agent reads these files on startup to load its long-term memory, ensuring it respects the established conventions of the project across days and weeks of work.

### Slide 6: Navigating Ambiguity and Edge Cases
- **Detailed Bullet Points**:
    - Deep Agents must handle ambiguous user requests without locking up or making dangerous assumptions.
    - The best deep agents are proactive: when faced with ambiguity, they use research tools (`grep`, `find`) to map the codebase before acting.
    - If empirical research fails to resolve the ambiguity, the agent must pause and use an `ask_user` tool to request clarification.
    - Handling edge cases requires defensive prompting, instructing the agent to verify assumptions (e.g., "Check if the file exists before writing to it").
    - The ability to gracefully backtrack from a failed hypothesis is a hallmark of a robust deep agent architecture.
- **Code Snippet / CLI Command**:
    ```text
    Thought: The user asked to "update the login logic", but there are three auth files.
    Action: ask_user("Which authentication module should I modify: JWT, OAuth, or SAML?")
    ```
- **Speaker Notes**: Humans are terrible at giving instructions. We say "Fix the bug," but we don't say where the bug is. A fragile agent guesses, changes random files, and breaks the build. A deep agent investigates. It looks for the bug. But crucially, if it can't figure it out, it stops and asks. The `ask_user` tool is an essential safety valve. Furthermore, deep agents must be comfortable being wrong. They will form a hypothesis, test it, realize it's wrong, and they must be able to roll back their changes and try a new path without human intervention.

### Slide 7: Designing Effective Deep Workflows
- **Detailed Bullet Points**:
    - A successful deep workflow follows a strict lifecycle: Research -> Strategy -> Execution -> Validation.
    - **Research:** Systematically map the codebase to understand the blast radius of the change.
    - **Strategy:** Draft a plan. For complex changes, enter a formal "Plan Mode" to design the architecture before writing code.
    - **Execution:** Implement surgical, atomic changes rather than massive, multi-file rewrites in a single step.
    - **Validation:** This is mandatory. The agent must run tests, linters, or build scripts to empirically prove the change was successful.
- **Code Snippet / CLI Command**:
    ```text
    // The execution cycle
    Action: run_shell_command("npm run test")
    Observation: 1 failed, 45 passed.
    Thought: The test failed because of an import error. I will fix the path.
    ```
- **Speaker Notes**: You don't just point a deep agent at a codebase and say "Go." You enforce a workflow. Research, Strategy, Execution, Validation. The validation phase is where the magic happens. A deep agent isn't done when it writes the code; it's done when the tests pass. If the tests fail, it enters a self-correction loop. This requires giving the agent access to your build tools and test runners. If you don't enforce this rigorous lifecycle, the agent will leave a trail of half-finished, untested code.

### Slide 8: Cost Optimization and Rate Limiting
- **Detailed Bullet Points**:
    - Deep Agents consume massive amounts of tokens due to their iterative loops and extensive context usage.
    - Optimization requires limiting tool output size (e.g., capping `grep` results) and preferring narrow, scoped searches.
    - Parallel tool execution significantly speeds up the agent but can quickly hit API rate limits (Requests Per Minute/Tokens Per Minute).
    - Implementing exponential backoff and retry logic in the orchestrator is necessary to handle API throttling gracefully.
    - Monitor context window growth; aggressive summarization or dropping old conversational turns is vital for long-running tasks.
- **Code Snippet / CLI Command**:
    ```python
    # Example of defensive tool constraints
    grep_search(pattern="TODO", max_matches_per_file=5, total_max_matches=50)
    ```
- **Speaker Notes**: Finally, we have to talk about the bill. Deep agents are expensive. Every time the agent thinks, reads a file, or runs a command, it's sending the entire history back to the API. If your agent is stuck in a loop reading a 10MB log file, you will burn through credits instantly. You have to optimize. You give the agent strict instructions to limit search results. You use sub-agents to keep the main context clean. And you have to implement rate limit handling, because an aggressive agent will easily overwhelm your API quotas if you aren't careful.


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
