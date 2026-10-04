<p align="center">
  <img src="docs/assets/winai_oe_banner.svg" alt="WinAI-OE Banner" width="100%">
</p>

# Enterprise Autonomous AI Employee & Company Operator (WinAI-OE)

> **An open-source, enterprise-grade, zero-implicit-trust autonomous execution runtime.**  
> *Engineered to transform high-level business goals into verified outcomes across desktop software, authenticated browsers, local filesystems, and enterprise APIs with minimal human supervision.*

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
  <a href="#"><img src="https://img.shields.io/badge/tests-412%20passed%20%7C%20100%25-brightgreen.svg" alt="Tests"></a>
  <a href="#"><img src="https://img.shields.io/badge/platform-Windows%2010%20%2F%2011%20x64-blue.svg" alt="Platform"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/security-Windows%20DPAPI%20%2B%20Zero--Trust-red.svg" alt="Security"></a>
  <a href="#"><img src="https://img.shields.io/badge/execution-Desktop%20%2B%20Browser%20%2B%20OS-purple.svg" alt="Execution"></a>
</p>

---

## Executive Summary

Enterprise work is fragmented across legacy desktop applications, web-based SaaS tools, local documents, and internal APIs. Knowledge workers spend hours manually moving data between tools, following rigid procedural checklists, and verifying results. Furthermore, natural language requests frequently leave operational procedures and context unstated.

Standard conversational AI assistants generate text suggestions, but cannot reliably execute or verify end-to-end work. 

**WinAI-OE (Windows AI Operating Environment)** is an autonomous **AI Employee and Company Operator**. It interprets business objectives, queries persistent organizational memory, operates computer tools (browser, desktop apps, files, terminals), recovers from obstacles, verifies verifiable evidence of completion, and requests cryptographic human approval only when executing high-impact actions.

---

## The Autonomous Execution Loop

WinAI-OE operates on a closed-loop autonomous execution cycle:

```
+-------------------------------------------------------------------------------------------------------+
|                                    THE AUTONOMOUS OPERATOR LOOP                                       |
|                                                                                                       |
|   [GOAL] ──> [UNDERSTAND] ──> [PLAN] ──> [EXECUTE] ──> [OBSERVE] ──> [ADAPT] ──> [VERIFY] ──> [COMPLETE]|
+-------------------------------------------------------------------------------------------------------+
```

1. **Goal:** The operator receives an open-ended natural language business objective via Web Console, WinUI 3 desktop shell, or REST/WebSocket IPC.
2. **Understand:** Resolves company context using the 4-tier memory architecture (Working RAM, Persistent Episodic SQLite WAL, Semantic Vector Store, and Project Context). Determines permitted tools, policies, and target environments.
3. **Plan:** Deconstructs goals into an executable Directed Acyclic Graph (DAG) using `task_planner.py`, guided by the ultra-low-latency pre-cognitive JEV advisory layer (70–500ms).
4. **Execute:** Directly interacts with the operating environment via:
   - **Desktop Applications:** Native UI Automation (`UIAutomationCore`), Win32 process management, and 119 discovered Windows apps.
   - **Web Browsers:** Authenticated remote debugging session against user Chrome/Edge profiles (zero cookie theft, zero headless bot traps).
   - **Filesystems:** Canonicalized scoped file operations with automatic atomic pre-write backups (`.winai/backups/`).
   - **Internal APIs & Scripts:** Scrubbed subprocess sandboxes with strict execution timeouts.
5. **Observe:** Inspects execution outcomes through real-time telemetry: DOM mutations, stdout/stderr exit codes, process statuses, and OpenCV 4.12 computer vision (with automatic 125% Windows DPI scaling compensation).
6. **Adapt:** When tool calls or environmental states diverge from expectations, the **Mistake-Learning Database** (`error_memory.py`) captures error signatures, determines root causes, and retrieves verified corrections to synthesize dynamic recovery paths without repeating failures.
7. **Verify:** Assesses observable proof of completion: test pass rates, DOM elements, file content hashes, or visual UI states before declaring completion.
8. **Complete:** Returns structured operational evidence and audit transcripts, serialized into tamper-evident SHA-256 hash-chained logs.

---

## Evaluation Benchmark & Core Competencies

| Evaluation Dimension | Challenge Standard | How WinAI-OE Executes It |
| :--- | :--- | :--- |
| **1. Autonomy** | Complete meaningful multi-step workflows without step-by-step handholding | Interprets goals, determines required tools, generates plans, and autonomously navigates browser/desktop applications to finish the task. |
| **2. Real Execution** | Perform actual work rather than merely explaining what should be done | Controls real GUI applications (Chrome, Notepad, Calc, n8n, Paint) using UI Automation, Windows Win32 API, and human-like cursor paths. |
| **3. Reliability & Recovery** | Recover gracefully from errors, plan failures, and changed states | Implements an active Mistake-Learning Database (`error_memory.py`), multi-provider circuit breakers, and Git task-branch rollbacks. |
| **4. Verification** | Validate whether requested outcomes were actually achieved | Evaluates concrete proof-of-work: 412 automated tests, file hash validation, visual UI state verification, and observable DOM checks. |
| **5. Generalization** | Reusable tool and connector abstractions across varied tasks | 12 specialized agent roles instantiated dynamically through a unified `AgentFactory`, universal model adapters (Gemini, GPT-4o, Claude, Ollama). |
| **6. Engineering Quality** | Architectural rigor, memory safety, and security | Zero Implicit Trust: host-side deterministic security engine, Windows DPAPI hardware-backed encryption, 412 hermetic automated tests. |
| **7. Product Thinking** | Focus on business objectives with minimal human friction | Integrated on-screen approval overlay widget, token cost accounting ($ USD / ₹ INR), and human-in-the-loop approvals for sensitive actions. |
| **8. Technical Understanding** | First-principles systems engineering | Decoupled LLMs as untrusted advisory components with out-of-band host validation, ensuring security against prompt injection. |

---

## System Architecture

```
+-----------------------------------------------------------------------------------------------+
|                                  USER PRESENTATION SHELLS                                     |
|   - Real-Time Web Control Center (http://127.0.0.1:8765/dashboard - SSE Streaming)             |
|   - Native Windows App SDK Shell (src/client/WinAI.Client - .NET 8 / C# / WinUI 3)            |
|   - Interactive CLI Terminal Workspace (chat_cli.py)                                          |
+-----------------------------------------------+-----------------------------------------------+
                                                |
                                                v Loopback IPC (REST / WebSockets on 127.0.0.1:8765)
+-----------------------------------------------------------------------------------------------+
|                               FAST ADVISORY DECISION LAYER (JEV)                             |
|  - Ultra-low latency classification & routing (70-500ms System One heuristic advisor)        |
|  - Advisory Only: Zero authorization authority; mandatory fallback on failure/timeout        |
+-----------------------------------------------+-----------------------------------------------+
                                                |
                                                v
+-----------------------------------------------------------------------------------------------+
|                             AI ORCHESTRATION & INTELLIGENCE CORE                              |
|  - Intelligent Model Router: Evaluates complexity, latency, budget, and privacy constraints    |
|  - Token & Cost Optimizer: SHA-256 prompt deduplication, semantic caching, prefix alignment   |
|  - 12-Role Agent Factory: Planner, Coordinator, Coder, Reviewer, SecurityAuditor, QA, etc.    |
|  - Autonomous Project Builder: Scaffolding, git task isolation, self-healing test loop         |
+-----------------------+-------------------------------+-------------------------------+-------+
                        |                               |                               |
                        v                               v                               v
+-------------------------------+  +----------------------------+  +----------------------------+
|      CONTEXT LAYER BRAIN      |  |   HOST-SIDE SECURITY CORE  |  |    WINDOWS OS INTEGRATION  |
| - Working Memory (RAM scratch)|  | - Policy Matrix (ALLOW/    |  | - Authenticated Chrome     |
| - Persistent Episodic (SQLite)|  |   DENY/REQUIRE_APPROVAL)   |  |   Profile (Default/Session)|
| - Semantic Vector Engine      |  | - CSPRNG 256-Bit Nonces    |  | - Scoped File Service with |
| - Project Workspace Context   |  | - Dynamic Defense Guard    |  |   Atomic Pre-Write Backups |
| - Mistake-Learning Database   |  | - Privilege Guard Sandbox  |  | - Sandboxed Subprocess with|
| - Strict Quality Provenance   |  | - Anomaly Burst Monitor    |  |   Scrubbed Environment     |
|   (VERIFIED_FACT vs ASSUME)   |  | - SHA-256 Chained Audit Log|  | - OpenCV 4.12 Vision (DPI) |
+-------------------------------+  +----------------------------+  +----------------------------+
                        |                               |                               |
                        +-------------------------------+-------------------------------+
                                                        |
                                                        v
+-----------------------------------------------------------------------------------------------+
|                                  HARDWARE & PERSISTENCE LAYER                                 |
|  - Windows DPAPI Hardware Credential Vault (CryptProtectData / CryptUnprotectData)            |
|  - High-Concurrency SQLite Write-Ahead Logging (WAL) Engines                                  |
|  - Tamper-Evident SHA-256 Hash-Chained JSONL Audit Log (Local Disk)                          |
+-----------------------------------------------------------------------------------------------+
```

---

## Subsystem Deep Dive

### 1. Independent Host-Side Security Core & Policy Sandbox
Located in `src/security/`:
* **Zero Implicit Trust:** The AI model is treated as an **untrusted advisory component**. Every tool call is intercepted by an independent host security engine outside the LLM context.
* **Deterministic Policy Engine (`policy_engine.py`):** Evaluates operations against an explicit permission matrix: `ALLOW`, `DENY`, or `REQUIRE_APPROVAL`.
* **Action Validator (`action_validator.py`):** Enforces strict Pydantic schemas, blocking path traversals (`../`), null-byte injections, shell metacharacter chains (`;`, `&&`, `|`), and UNC hijack paths.
* **Cryptographic Approval Broker (`approval_broker.py`):** Generates single-use 256-bit CSPRNG nonces for high-impact actions. Nonces expire after 300 seconds and cannot be reused or replayed.
* **Tamper-Evident Audit Logger (`audit_logger.py`):** All events, approvals, and tool executions are serialized into an append-only JSONL log where each record includes the SHA-256 hash of the previous line.

### 2. Hardware-Backed Credential Vault (Windows DPAPI)
Located in `src/storage/credential_vault.py`:
* API keys and credentials are encrypted using Microsoft's native **Windows Data Protection API (DPAPI)** (`CryptProtectData`), tied directly to the Windows machine user account and TPM chip.
* Zero plaintext secrets exist on disk or in `.env` files. Secrets are decrypted **in-memory only** during outgoing HTTP request dispatch.

### 3. 4-Tier Memory Super-Brain & Mistake-Learning Database
Located in `src/orchestrator/brain/`:
* **Tier 1: Working Memory (`working_memory.py`):** In-memory ephemeral scratchpad tracking active subtask variables and observations.
* **Tier 2: Episodic Memory (`episodic_memory.py`):** SQLite database in WAL mode recording task histories, outcomes, and preferences across restarts.
* **Tier 3: Semantic Memory (`semantic_memory.py`):** Local vector embeddings enabling cross-session conceptual retrieval.
* **Tier 4: Project Memory (`project_memory.py`):** Indexes workspace directory structure, dependencies, and business rules.
* **Mistake-Learning Database (`error_memory.py`):** Indexes past tool and environment failures with verified solutions. Before creating plans, the agent retrieves relevant past mistakes to guarantee it never repeats the same error.
* **Strict Provenance Filtering:** Information carries verification tags (`VERIFIED_FACT`, `USER_ASSERTED`, `MODEL_HYPOTHESIS`). Hypotheses are prevented from being treated as facts without verified execution outputs.

### 4. Windows OS Integration & Native UI Automation
Located in `src/windows_integration/`:
* **Scoped File Service (`scoped_file_service.py`):** Path canonicalization with `os.path.realpath`, isolation sandboxing, and atomic pre-write backups before every file write.
* **Restricted Subprocess Runner (`process_runner.py`):** Executes Windows subprocesses with scrubbed environments (blocking secret leakage), execution timeouts, and complete process tree termination.
* **System Application Discovery (`app_scanner.py`):** Scans 32/64-bit Windows Registry hives and PATH to discover installed applications (**119 apps indexed**).
* **Computer Vision Engine (`vision_engine.py`):** Powered by `OpenCV 4.12` with real-time **125% Windows Display DPI scaling compensation** to dynamically locate UI buttons and windows without static coordinate files.
* **HumanCursorController (`human_cursor.py`):** Moves the mouse cursor along cubic-eased bezier curves (`3t² - 2t³`) with natural micro-jitters, enabling visual verification of automation without robotic snapping.

### 5. Authenticated Browser Automation & SaaS Integration
Located in `src/windows_integration/browser_service.py`:
* **Primary Profile Connection:** Attaches directly to the user's active Google Chrome/Edge profile via remote debugging. Uses existing authenticated enterprise sessions without stealing cookies or spawning unauthenticated guest windows.
* **SaaS Workflow Automation:** Capable of navigating cloud workflow builders (e.g. n8n cloud), placing nodes, wiring automation graphs, running test triggers, and validating outputs.
* **Multimodal Feed Scraping:** Reads dynamic web timelines via multimodal vision and DOM inspection, bypassing anti-scraping walls and dynamic CSS obfuscations.

### 6. Dynamic 12-Role Agent Factory
Located in `src/orchestrator/planner/`:
* Spawns specialized agents based on task classification:
  1. `PlannerAgent`: Task decomposition and dependency DAG construction.
  2. `CoordinatorAgent`: Multi-agent orchestration and inter-agent synchronization.
  3. `CoderAgent`: Software development and targeted bug fixes.
  4. `ReviewerAgent`: Code quality, style, and regression analysis.
  5. `SecurityAuditorAgent`: AST security analysis and injection screening.
  6. `DevOpsAgent`: Build scripts, environment setup, and CI configurations.
  7. `DataScientistAgent`: Statistical modeling, data transformations, and analysis.
  8. `TechnicalWriterAgent`: Documentation, user guides, and API specs.
  9. `UIUXDesignerAgent`: UI layout, color palettes, and accessibility.
  10. `DatabaseArchitectAgent`: Schema design, migrations, and query tuning.
  11. `ResearcherAgent`: Web synthesis, literature search, and intelligence gathering.
  12. `QAEngineerAgent`: Automated test creation and edge-case validation.
* Governed with hard recursion bounds (`max_depth = 2`, `max_active_agents = 5`).

### 7. Token & Cost Optimization Subsystem
Located in `src/orchestrator/token_optimizer.py`:
* **Exact SHA-256 Prompt Caching:** Identical requests return instant cache hits (**0 tokens consumed**, 0 latency).
* **Semantic Caching:** Local cosine similarity projection (`threshold > 0.95`) satisfies conceptually identical queries without external API roundtrips.
* **Prefix Caching Alignment:** Structures system prompts and tool definitions at the front of the prompt context, activating provider prompt caching (up to **50% discount**).
* **Dual Currency Accounting:** Calculates exact spend and savings in both **USD ($)** and **INR (₹)**.

---

## Real-World Operational Demonstrations

| Operational Capability | How the Autonomous Operator Executes It |
|---|---|
| **Autonomous Invoice & Sync** | Reads natural language requests, locates target invoices/documents in local directories or email, extracts amount/due date, opens target business tools, inputs data, and returns verifiable evidence. |
| **SaaS Workflow Construction** | Navigates to cloud workflow engines (e.g. n8n cloud), drags and connects nodes (`Manual Trigger` ➔ `Code` ➔ `IF Condition` ➔ `Webhook`), executes tests, and verifies output payloads. |
| **Authenticated Web Outreach** | Connects to authenticated Chrome sessions, navigates feeds, extracts verified contact information, drafts contextual personalized communications, and stages drafts with pre-send verification. |
| **Self-Healing Code Building** | Scaffolds complete FastAPI/React projects, generates unit tests, executes `pytest` in sandboxed environments, analyzes failures, fixes errors, and merges on 100% test pass. |
| **Direct Desktop UI Control** | Launches desktop applications (Notepad, Paint, Calculator), identifies UI controls via OpenCV contour analysis, and operates tools using a smooth cubic-eased cursor. |
| **Cryptographic Human Approval** | Triggers an always-on-top floating desktop widget with 256-bit CSPRNG nonces whenever high-impact filesystem or code execution operations are attempted. |

---

## Automated Verification Net (412 Tests)

WinAI-OE maintains a strict, hermetic test suite with **412 automated tests**:

```powershell
python -m pytest tests -q
........................................................................ [ 17%]
........................................................................ [ 34%]
........................................................................ [ 52%]
........................................................................ [ 69%]
........................................................................ [ 87%]
....................................................                     [100%]
============================= 412 passed in 18.06s =============================
```

* **Unit Tests (`tests/unit/`):** Configuration schemas, DPAPI vault encryption, provider adapters, 4-tier memory, error reflection, and agent factories.
* **Integration Tests (`tests/integration/`):** FastAPI REST/WebSocket endpoints, scoped filesystem rollback, subprocess environment scrubbing, and browser session locking.
* **Security & Adversarial Tests (`tests/security/`):** Path traversal, null-byte injection, schema tampering, approval nonce replay/forgery, prompt injection defense, and privilege escalation blocking.

---

## Quick-Start & Operational Guide

### Prerequisites
* Windows 10 or Windows 11 (64-bit)
* Python 3.11 or 3.12
* Google Chrome or Microsoft Edge

### Installation
```powershell
# 1. Clone the repository
git clone https://github.com/vakrahul/WinOS-AI.git
cd WinOS-AI

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install core dependencies
pip install -r requirements.txt
```

### 1. Run the Automated Verification Suite
```powershell
python -m pytest tests -q
```

### 2. Store API Credentials in Windows DPAPI Vault
```powershell
# Encrypt API keys securely using Windows DPAPI (zero plaintext on disk):
python -c "from src.storage.credential_vault import CredentialVault; v = CredentialVault(); v.store_credential('gemini', 'YOUR_API_KEY'); print('Encrypted key stored successfully via DPAPI.')"
```

### 3. Launch the Orchestrator & Live Web Control Center
```powershell
python run_vertical_slice.py
```
Open your browser to: **`http://127.0.0.1:8765/dashboard`** or **`http://127.0.0.1:8765/`** to access the live Control Center, JEV controls, and interactive planning console.

### 4. Launch the Interactive Terminal Workspace
```powershell
python chat_cli.py
```

### 5. Launch the Always-On-Top Approval Overlay Widget
```powershell
python approval_button.py
```

---

## Repository Structure

```
D:\Interveiewsass\
├── docs/                                 # Architectural Specifications, PRDs & Audits
│   ├── PRD.md                            # Product Requirements Document
│   ├── ARCHITECTURE.md                   # Core Architecture Specification
│   ├── THREAT_MODEL.md                   # STRIDE & OWASP Threat Analysis
│   ├── TRUST_BOUNDARIES.md               # Trust Boundary Map & Isolation Zones
│   └── jev/                              # JEV Fast Advisory Decision Layer Documentation
├── src/
│   ├── client/                           # Native Windows Desktop Frontend (C# / .NET 8 / WinUI 3)
│   ├── orchestrator/                     # Core Intelligence & Orchestration Service
│   │   ├── main.py                       # FastAPI Application, Endpoints & SSE Streaming
│   │   ├── dashboard.html                # Live Web Control Center, Planner & Task Console
│   │   ├── intelligent_router.py         # Dynamic Model Routing Engine
│   │   ├── token_optimizer.py            # Exact & Semantic Caching, Cost Accounting
│   │   ├── brain/                        # 4-Tier Memory & Mistake-Learning Engine
│   │   │   ├── working_memory.py         # Ephemeral RAM Scratchpad
│   │   │   ├── episodic_memory.py        # Persistent SQLite WAL Storage
│   │   │   ├── semantic_memory.py        # Local Vector Similarity Store
│   │   │   ├── project_memory.py         # Workspace Context & Dependencies
│   │   │   └── error_memory.py           # Mistake-Learning Database
│   │   ├── planner/                      # Autonomous Planning & Agent Hierarchy
│   │   │   ├── task_planner.py           # DAG Task Decomposition
│   │   │   ├── agent_factory.py          # Dynamic Agent Instantiation
│   │   │   └── coding_agent.py           # Self-Healing Code & Test Execution Loop
│   │   └── jev/                          # Fast Advisory Decision Layer
│   ├── providers/                        # Vendor-Agnostic LLM Adapters (Gemini, OpenAI, Claude, Local)
│   ├── security/                         # Independent Host-Side Security Core
│   │   ├── policy_engine.py              # ALLOW/DENY/REQUIRE_APPROVAL Matrix
│   │   ├── action_validator.py           # Schema, Injection & Traversal Validator
│   │   ├── approval_broker.py            # CSPRNG 256-Bit Nonce Broker & Tracker
│   │   ├── dynamic_defense.py            # Prompt Injection & Jailbreak Defense Shield
│   │   └── audit_logger.py               # Tamper-Evident SHA-256 Chained JSONL Logger
│   ├── storage/                          # Persistence & Recovery Engines
│   │   ├── credential_vault.py           # Windows DPAPI Hardware Credential Vault
│   │   ├── sqlite_storage.py             # High-Concurrency WAL SQLite Engine
│   │   └── git_recovery.py               # Automated Git Task Branching & Rollback
│   └── windows_integration/              # Windows Native Automation Subsystems
│       ├── scoped_file_service.py        # Sandboxed Filesystem with Pre-Write Backups
│       ├── process_runner.py             # Sanitized Subprocess Runner with Timeouts
│       ├── app_scanner.py                # 119-App Registry & PATH Scanner
│       ├── browser_service.py            # Authenticated Chrome Remote Debugging
│       ├── vision_engine.py              # OpenCV 4.12 Vision with 125% DPI Compensation
│       └── human_cursor.py               # Cubic-Eased Realistic Mouse Travel
├── tests/                                # Automated Test Net (412 Tests / 100% Pass)
└── archive/                              # Archived Experimental Workflows & Test Media
```

---

## Technical Decisions & Rationale

1. **Host-Side Security Supervisor vs. In-Prompt Guardrails:**  
   LLM prompt guardrails fail reliably against prompt injection, jailbreaks, and indirect injection from untrusted web pages. WinAI-OE implements an out-of-band host-side security engine. The model is treated as an untrusted advisory client; every filesystem write, subprocess execution, and network request must pass deterministic Pydantic schema validation and host policy checks.

2. **Windows DPAPI vs. `.env` Plaintext Files:**  
   Enterprise production environments cannot tolerate plaintext API keys or credentials stored on disk. WinAI-OE binds secrets to the Windows user account and hardware TPM via Windows DPAPI (`CryptProtectData`), decrypting credentials exclusively in volatile RAM during active HTTP requests.

3. **Closed-Loop Verification vs. Text Assumption:**  
   Standard assistants declare success when the language model outputs a conversational conclusion. WinAI-OE enforces closed-loop verification: operations require observable evidence (test execution pass codes, file content hash matching, or visual UI element confirmation) before resolving a task.

4. **Mistake-Learning Reflection Engine vs. Memory Dumps:**  
   When an autonomous agent hits an error, dumping conversational history often leads the model to repeat the same failed pattern. WinAI-OE logs failure signatures, identified root causes, and verified corrections in an SQLite database. These lessons are dynamically injected into future planning prompts to prevent recurring mistakes.

---

## Known Limitations & Future Roadmap

### Current Limitations
1. **Windows-Native OS Specialization:** Core system features leverage native Windows APIs (Windows DPAPI, Win32 EnumWindows, UI Automation, Registry). Cross-platform execution (Linux/macOS) is currently supported in headless/mock mode.
2. **Canvas-Heavy Web Applications:** Web tools that draw entirely onto HTML5 `<canvas>` elements without standard DOM accessibility trees require visual computer vision heuristics, which can be sensitive to dynamic viewport changes.
3. **Unlocked Desktop Session:** Full GUI automation (OpenCV screen capture and cursor movement) requires an active, unlocked Windows desktop session.

### What We Would Build Next
1. **Cross-Platform Enterprise Agent Daemon:** Decouple the core execution runtime into containerized Linux and macOS worker nodes managed via a centralized control plane.
2. **"Demonstrate & Learn" Workflow Synthesizer:** An observation mode where a human operator performs a manual enterprise task once; the system records UI states and generates an executable, parameter-driven DAG with auto-generated verification criteria.
3. **Enterprise SaaS Connector Library:** Out-of-the-box native connectors for Jira, Salesforce, ServiceNow, SAP, and Slack, reducing reliance on browser UI clicks when official APIs are accessible.
4. **Active Learning from Human Approval Nonces:** Utilize approved vs. denied actions in the cryptographic audit log to fine-tune local models on company-specific authorization boundaries.

---

## License & Community

WinAI-OE is open-source under the [MIT License](LICENSE) © 2026 Rahul Vakiti (`vakrahul`) and contributors.
