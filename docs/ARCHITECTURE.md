# SYSTEM ARCHITECTURE SPECIFICATION
## Windows AI Operating Environment (WinAI-OE)
**Document Version:** 1.0.0  
**Phase:** Stage I — Phase 2 (System Architecture)  
**Status:** Approved Specification  

---

## 1. High-Level Architecture Overview

The Windows AI Operating Environment (WinAI-OE) is architected as a modular, decoupled, multi-process desktop platform. The architecture separates presentation, intelligent orchestration, memory persistence, operating system integration, and security enforcement into isolated layers.

```
+-------------------------------------------------------------------------+
|                       WinUI 3 Desktop Application                       |
|               (C# / .NET 8 / Windows App SDK / MVVM)                     |
|  - Chat & Streaming UI           - Task & Agent Workspace               |
|  - Permission & Approval Dialogs - Memory & Audit Inspector             |
|  - DPAPI Credential Vault Helper - Real-Time Event Hub (WebSocket)      |
+------------------------------------+------------------------------------+
                                     |
               IPC Boundary (Loopback REST / WebSocket / TLS)
                                     |
+------------------------------------+------------------------------------+
|                   AI Orchestration Subsystem (Python)                   |
|                      (FastAPI / AsyncIO Task Engine)                    |
|  - Provider Adapter Registry (OpenAI, Anthropic, Gemini, Ollama, Local) |
|  - Capability Negotiator & Context Budget Planner                       |
|  - Agent Registry & Task Decomposition Engine                           |
|  - Tool Dispatch Pipeline                                               |
+-------------------+----------------+-------------------+----------------+
                    |                |                   |
                    v                v                   v
+-----------------------+  +------------------+  +------------------------+
|    Contextual Brain   |  |  Security Core   |  |   Windows Integration  |
|  (Tiered Memory Sys)  |  | (Policy Engine)  |  |    (Controlled Ops)    |
| - Working Memory      |  | - Agent Token Mgr|  | - UI Automation (UIA)  |
| - Episodic Memory     |  | - Policy Matrix  |  | - Sandboxed Subprocess |
| - Semantic (Vectors)  |  | - Human Approvals|  | - Scoped Filesystem    |
| - Project Memory      |  | - Emergency Kill |  | - Process Watcher      |
+-----------------------+  +------------------+  +------------------------+
            |                        |                       |
            +------------------------+-----------------------+
                                     |
+------------------------------------+------------------------------------+
|                         Storage Subsystem                               |
|  - SQLite (WAL Mode) / PostgreSQL Compatible Persistence                |
|  - Embedded Vector Index (sqlite-vec / Chroma / FAISS)                  |
|  - Windows DPAPI Protected Key Vault (AES-256-GCM)                      |
|  - Tamper-Evident SHA-256 Hash-Chained Audit Logs (JSONL)               |
+-------------------------------------------------------------------------+
```

---

## 2. Component Specifications

### 2.1 Native Desktop Application (Client Layer)
* **Framework:** WinUI 3 via Windows App SDK with .NET 8, implementing the Model-View-ViewModel (MVVM) design pattern.
* **Core Responsibilities:**
  * **Shell & Navigation:** Workspaces, Agent Monitors, Memory Explorer, Provider Settings, Audit Log viewer.
  * **Conversational Streaming:** Low-latency markdown/code rendering, real-time token streaming over WebSocket with instant cancellation controls.
  * **Interactive Approval Cards:** Cryptographically bound dialogs presenting exact parameters, security risk tier, target resource paths, and approval choices (Approve Once, Deny, Approve for Session).
  * **Emergency Kill Switch:** Prominent UI hardware/software action that transmits an immediate revocation signal to terminate all active agent processes.
  * **Local Credential Bridge:** Direct access to Windows Data Protection API (DPAPI) and Windows Credential Locker for key generation and secret hydration.

### 2.2 AI Orchestration Subsystem (FastAPI / AsyncIO)
* **Framework:** Python 3.12, FastAPI, Uvicorn, AsyncIO.
* **Core Responsibilities:**
  * **Provider Abstraction Layer:** Common abstract interface (`BaseModelProvider`) standardizing:
    * `complete(messages, tools, options)`
    * `stream(messages, tools, options)`
    * `get_capabilities()` (context window, tool support, vision support, streaming flag)
    * `health_check()`
  * **Supported Providers:**
    * `AnthropicAdapter` (Claude 3.5 / 3.7 Sonnet, Haiku via official REST API)
    * `OpenAIAdapter` (GPT-4o, o1, o3-mini via official SDK)
    * `GeminiAdapter` (Google Gemini 2.0 Flash / Pro)
    * `OllamaAdapter` / `LocalInferenceAdapter` (Local inference endpoints via OpenAI-compatible endpoints)
  * **Provider Resilience:** Circuit breaker pattern, token-bucket rate limiter, exponential backoff with jitter, unified timeout handlers.
  * **Agent Execution Loop:** ReAct / Tool-calling state machine managing agent thoughts, tool requests, validation results, and execution observations.

### 2.3 Contextual Super Brain (Memory Layer)
* **Architecture:** Multi-tiered memory engine ensuring task continuity across model switches and application lifecycles.
  * **Tier 1: Working Memory:** In-memory, high-fidelity representation of current task state, active sub-goals, recent tool execution results, and working variables.
  * **Tier 2: Episodic Memory:** Structured summaries of completed tasks, user corrections, errors encountered, and outcome evaluations, stored in SQLite.
  * **Tier 3: Semantic Memory:** Vector-indexed facts, long-term user preferences, and reference concepts. Local embedding model (`all-MiniLM-L6-v2` or `bge-small-en-v1.5`) generating 384-dimensional vectors indexed via cosine similarity.
  * **Tier 4: Project Memory:** Scoped specifically to target workspaces/repositories, indexing `.winai/project-context.json`, architectural notes, directory maps, and active dependency definitions.
* **Context Prioritization & Pruner:** Dynamic token budgeting dynamically allocating model context windows (e.g., 60% working context, 20% retrieved memory, 10% system prompt & schemas, 10% output buffer).

### 2.4 Security Core (Policy & Authorization Authority)
* **Architecture:** Completely isolated from generative model prompt spaces. The model is treated strictly as an untrusted actor requesting actions.
* **Core Responsibilities:**
  * **Agent Identity & Session Management:** Unique UUIDs assigned to each agent run, bound to a specific session token with an explicit expiration TTL.
  * **Permission Matrix:** Granular permission scopes:
    * `fs:read`, `fs:write`, `fs:delete` (scoped to specific path prefixes)
    * `proc:exec` (scoped to permitted binaries e.g. `git.exe`, `pytest.exe`)
    * `net:http` (scoped to approved domain whitelist)
    * `uia:inspect`, `uia:action` (scoped to permitted application window titles/PIDs)
  * **Policy Engine:** Deterministic rule engine evaluating tuples: `(AgentID, ToolName, TargetResource, Parameters) -> { ALLOW, DENY, REQUIRE_APPROVAL }`.
  * **Action Validator:**
    * Validates JSON payload against strict Pydantic / JSON Schema.
    * Canonicalizes filesystem paths (`os.path.realpath`) and verifies boundary confinement (jail check).
    * Rejects shell metacharacters and unquoted paths for process execution.
  * **Human Approval Broker:** Generates ephemeral nonces for approval cards. Only a user-initiated UI callback containing the valid nonce can authorize a `REQUIRE_APPROVAL` action.
  * **Emergency Kill Switch:** Terminates registered sub-process trees via Windows `JobObject` / `taskkill`, invalidates session tokens, and drains task queues in < 200ms.

### 2.5 Windows Integration Service (System Interaction)
* **Core Responsibilities:**
  * **Scoped Filesystem Service:** Read, write, list, diff, and patch files strictly within authorized workspace directories. Hard-coded blocks on Windows system directories (`C:\Windows`, `C:\Program Files`, AppData system hives).
  * **Restricted Subprocess Runner:** Spawns commands with:
    * Working directory pinned to workspace root.
    * Environment variables scrubbed of credentials and API keys.
    * Execution timeout enforcement (default 60s).
    * Standard output / error buffer truncation (maximum 50KB or 2000 lines).
    * Child process tree attached to a Windows Job Object configured to terminate children on exit.
  * **Windows UI Automation (UIA):** Interacts with Windows Accessibility APIs (`IUIAutomation`) to inspect element trees, extract control patterns (Invoke, Value, Selection), and interact with permitted application windows without raw coordinate-based mouse clicking.
  * **Application Discovery:** Enumerates running top-level windows and allows users to explicitly check-box which application instances agents may observe or interact with.

### 2.6 Storage Subsystem
* **Structured Data:** SQLite database with Write-Ahead Logging (WAL) enabled, enforcing foreign keys and ACID transactions. Schema managed via SQLAlchemy. Compatible with PostgreSQL for multi-user scenarios.
* **Vector Index:** Embedded vector store (`sqlite-vec` / Chroma / FAISS) for semantic search.
* **Encrypted Key Vault:** Uses Windows Data Protection API (`CryptProtectData` / `CryptUnprotectData`) to encrypt provider API keys with user login keys. Stored ciphertext is unreadable by other user accounts on the machine.
* **Tamper-Evident Audit Log:** Append-only JSON Lines file where each entry contains a SHA-256 hash of the previous log entry, creating an immutable log chain.

---

## 3. Communication Protocols & Data Contracts

### 3.1 IPC Architecture
* **Endpoint:** Loopback interface only (`127.0.0.1:8765`), bound to a randomly generated session authentication token passed at startup.
* **REST API:** Administrative configuration, provider health, memory management, workspace CRUD.
* **WebSocket API (`/ws/v1/stream`):** Full-duplex messaging for:
  * Prompt submission from UI.
  * Real-time token streaming to UI.
  * Agent state transitions (`PLANNING`, `EXECUTING_TOOL`, `AWAITING_APPROVAL`, `COMPLETED`, `FAILED`).
  * Interactive approval push notifications and user responses.
  * Instant task cancellation commands.

### 3.2 Canonical Message Schemas

#### Tool Action Proposal (From Agent to Security Core)
```json
{
  "task_id": "tsk_01j7b9...",
  "agent_id": "agt_coder_01",
  "tool_name": "fs_write_file",
  "parameters": {
    "file_path": "D:/Interveiewsass/src/main.py",
    "content": "print('hello')",
    "mode": "overwrite"
  },
  "timestamp": "2026-09-20T16:50:00Z"
}
```

#### Policy Evaluation Decision (From Security Core to Orchestrator)
```json
{
  "decision": "REQUIRE_APPROVAL",
  "approval_request_id": "appr_98234...",
  "risk_tier": "HIGH",
  "reason": "File modification target is outside transient scratch directory",
  "target_resource": "D:/Interveiewsass/src/main.py",
  "parameters": {
    "file_path": "D:/Interveiewsass/src/main.py",
    "content_preview": "print('hello')"
  }
}
```

#### Approval Response (From WinUI Client to Security Core)
```json
{
  "approval_request_id": "appr_98234...",
  "user_decision": "APPROVED",
  "granted_scope": "ONCE",
  "signature": "ui_nonce_a9f82c..."
}
```

---

## 4. Verification Against Non-Negotiable Design Principles

1. **Provider Independence:** Universal `BaseModelProvider` interface guarantees any provider can be added without modifying orchestration logic.
2. **User Ownership:** All credentials stored in user's Windows DPAPI; memory and files stored locally in user workspace.
3. **Independent Security Enforcement:** Policy engine runs out-of-process in host code; models have zero access to policy evaluation code.
4. **Least Privilege:** Default permissions set to read-only in workspace root; write/exec operations require explicit authorization.
5. **Explicit Authorization:** Human approval cards bound to action nonces; model cannot simulate user approval.
6. **Transparent Operation:** Real-time WebSocket streaming of agent states, tool proposals, and parameters.
7. **Fail Safely:** Policy engine denies by default if validation fails or parameters are malformed.
8. **Persistent but Controlled Memory:** Tiered memory with user inspect/delete/export APIs.
9. **Reversible Development:** File modifications generate diffs and backups; child processes contained in Job Objects.
10. **No False Security Guarantees:** Clear boundary documentation; acknowledges user-mode Windows limitations.
