# Windows AI Operating Environment (WinAI-OE)

> **A secure, context-aware, vendor-agnostic autonomous desktop execution environment for Microsoft Windows.**

Unlike conventional chatbots or unconstrained desktop automation scripts, **WinAI-OE** enforces a **zero-implicit-trust architecture**: AI models propose actions, while an independent host-side security engine validates, sandboxes, authorizes, and verifies every operation against deterministic policies and hardware-backed credential storage.

---

## 1. System Architecture Overview

```
+-------------------------------------------------------------------------+
|                       Presentation & Client Shell                       |
|   - Interactive Terminal Workspace (chat_cli.py)                        |
|   - Native Windows App SDK Shell (src/client/WinAI.Client - .NET 8)     |
+------------------------------------+------------------------------------+
                                     | Loopback IPC (127.0.0.1:8765)
+------------------------------------v------------------------------------+
|                   AI Orchestration & Intelligence Core                  |
|  - Intelligent Model Router (Complexity, Latency, Cost, Privacy)       |
|  - Token & Cost Optimizer (Exact & Semantic Caching, Prefix Alignment) |
|  - Dynamic Agent Factory (12 Specialized Domain Roles)                 |
|  - Autonomous Project Builder (Full-Stack & Data Science Pipelines)    |
+-------------------+----------------+-------------------+----------------+
                    |                |                   |
                    v                v                   v
+-----------------------+  +------------------+  +------------------------+
|   Context Layer Brain |  |  Security Core   |  |   Windows Integration  |
| - Task & Proj Context |  | - Policy Matrix  |  | - Authenticated Chrome |
| - 4-Tier Memory Store |  | - CSPRNG Nonces  |  | - Scoped File Service  |
| - Mistake Learning DB |  | - Active Shield  |  | - OpenCV Computer Vision
| - Provenance Tiers    |  | - Audit Logger   |  | - Sandboxed Subprocess |
+-----------------------+  +------------------+  +------------------------+
            |                        |                       |
            +------------------------+-----------------------+
                                     |
+------------------------------------v------------------------------------+
|                         Hardware & Storage                              |
|  - Windows DPAPI Hardware Key Vault (CryptProtectData)                  |
|  - SQLite Write-Ahead Logging (WAL) Persistent Databases                |
|  - SHA-256 Tamper-Evident Hash-Chained Audit Logs (JSONL)               |
+-------------------------------------------------------------------------+
```

---

## 2. What the System Currently Achieves

### 🌐 A. Live Web & Authenticated Browser Operations
* **Primary Profile Integration:** Connects directly to the user's primary, authenticated Google Chrome profile (`Default` / `vakitirahul@gmail.com`) without stealing cookies or spawning blank guest sessions.
* **Computer Vision Feed Reading:** Focuses live social platforms (e.g., X / Twitter) and uses multimodal vision (`gemini-3.1-flash-lite`) to extract posts, authors, and images without being blocked by dynamic DOM rendering.
* **Autonomous SaaS Workflow Construction:** Connects to live cloud instances (e.g. `https://ravoz.app.n8n.cloud`), automatically creates new workflows, wires multi-node execution pipelines (`Manual Trigger` ➔ `Edit Fields` ➔ `IF` ➔ `Output`), triggers executions, verifies branch results, and saves workflows.
* **Live Recruiter & Job Intelligence:** Scrapes and filters hiring posts from LinkedIn, Internshala, and job portals for AI/ML/Python roles (e.g., within the past 24 hours) and extracts direct recruiter contact emails (`oxastra7@gmail.com`, `shubham@jobblow.in`).
* **Automated Email Dispatch Preparation:** Generates personalized cold emails and cover letters incorporating the user's live portfolio (`rahulvakiti.space`), research publications, and attaches local resumes (`Rahul_vak_resume.pdf`).

### 💻 B. Local Windows Application Control & Computer Vision
* **System Application Discovery:** Scans the Windows Registry (HKLM & HKCU 32/64-bit), Start Menu, and System PATH to catalog all installed software (**119 applications discovered**, 33 developer & AI tools).
* **Controlled App Management:** Securely launches and tracks approved binaries (`chrome.exe`, `notepad.exe`, `Code.exe`, `mspaint.exe`, Antigravity IDE) while preventing background process leaks.
* **Dynamic Computer Vision (`OpenCV 4.12`):**
  * Auto-detects display DPI scaling (`125%` scaling compensation).
  * Uses real-time contour thresholding to identify application canvas boundaries without hard-coded coordinates.
  * **HumanCursorController:** Implements smooth cubic-eased (`3t² - 2t³`) mouse travel so the user can visually observe cursor movements in real time.
* **Creative Canvas Illustration:** Autonomously operates Microsoft Paint to design and hand-draw multi-layered vector illustrations (aerodynamic rocket, crimson nose cone, dual riveted portholes, swept delta fins, and fiery exhaust plumes).

### ⚡ C. Token Optimization & Cost Subsystem
* **Exact SHA-256 Response Caching:** Hashes prompt message structures; repeated queries hit the local cache with **0 tokens consumed** and 0 API cost.
* **Semantic Caching:** Uses lightweight local vector projections (`cosine similarity > 0.95`) to answer similar questions from memory.
* **Provider Prefix Caching Alignment:** Formats system prompts and invariant tool schemas at the head of the context to leverage provider-level prompt caching discounts (up to **50% savings**).
* **Per-Task Token Budgets:** Enforces hard token limits with pre-flight evaluation tripwires to prevent runaway agent loops.
* **Real-Time Cost Accounting:** Computes exact expenditures in both **USD** and **INR** across model pricing matrices (`gemini-3.1-flash-lite`, `gpt-4o`, `claude-3-5-sonnet`, `local`).

### 🧠 D. Context Layer Brain & Mistake Learning
* **4-Tier Memory Architecture:**
  1. *Working Memory:* Ephemeral scratchpad tracking active subtasks, variables, and recent observations.
  2. *Episodic Memory:* Persistent SQLite WAL database storing completed task summaries across application restarts.
  3. *Semantic Memory:* Vector-indexed knowledge base with local embeddings and cosine similarity retrieval.
  4. *Project Memory:* Scoped workspace context indexing dependencies, file structures, and architectural rules.
* **Mistake-Learning Memory (`error_memory.py`):** Captures failed actions, error messages, root causes, and verified corrections in SQLite. Uses hybrid lexical + semantic retrieval to inject `[CRITICAL LESSONS FROM PAST MISTAKES]` into future prompts, preventing repeated errors.
* **Memory Quality Tiers:** Strictly distinguishes `VERIFIED_FACT`, `USER_ASSERTED`, `MODEL_HYPOTHESIS`, `UNVERIFIED_ASSUMPTION`, and `FAILED_APPROACH`. Model hypotheses are never promoted to permanent facts without verified tool evidence.

### 🛠️ E. Autonomous Project Building & Self-Healing Code
* **Natural-Language Scaffolding:** Converts high-level prompts into structured, modular project architectures across Software Engineering, Data Science, and Research.
* **Autonomous Coding & Testing Loop (`coding_agent.py`):** Generates code within an isolated directory, executes unit tests, parses failure traces, applies targeted self-healing fixes, and re-tests until **100% pass rate** is achieved.
* **Git Task Branch Isolation (`git_recovery.py`):** Automatically initializes Git repositories, creates isolated feature branches (`task/<task_id>`), stages changes, previews diffs, and supports one-click atomic rollbacks to `main`.
* **Scoped Filesystem Service:** Canonicalizes paths (`os.path.realpath`) to block directory traversal, enforces workspace jail boundaries, and creates automatic pre-write backup snapshots in `.winai/backups/`.

### 🛡️ F. Independent Security & Defense
* **Hardware Credential Vault:** API keys and tokens are encrypted via **Windows DPAPI** (`CryptProtectData`). Secrets are decrypted only in-memory at request dispatch and never exposed to model prompts or logs.
* **Dynamic Defense Shield (`dynamic_defense.py`):** Real-time heuristic scanning intercepting direct jailbreaks (`"ignore previous instructions"`), indirect injections (`[SYSTEM: ...]`), and shell metacharacter escapes (`; rm -rf`, `powershell -enc`).
* **Categorized Permission System:** Categorizes all operations into `READ`, `WRITE`, `EXECUTE`, `EXTERNAL`, and `HIGH_IMPACT`. Sensitive external operations require single-use 256-bit CSPRNG approval nonces.
* **Dynamic Sub-Agent Factory:** Enforces hierarchical containment (`max_depth = 2`, `max_active_agents = 5`) and least-privilege tool inheritance to prevent unauthorized agent replication.
* **Tamper-Evident Audit Logging:** Cryptographically chains all operational and security events using SHA-256 hashes in an append-only JSONL log.

---

## 3. Supported Model Providers

| Provider | Adapter | Supported Models | Integration Type |
|---|---|---|---|
| **Google Gemini** | `GeminiAdapter` | `gemini-3.1-flash-lite` (Default), `gemini-1.5-flash`, `gemini-2.0-flash` | Official REST / Streaming |
| **OpenAI** | `OpenAIAdapter` | `gpt-4o`, `gpt-4o-mini`, `o1`, `o3-mini` | Official REST / Streaming |
| **Anthropic** | `AnthropicAdapter` | `claude-3-5-sonnet`, `claude-3-haiku` | Official Messages API |
| **Local Inference** | `LocalModelAdapter` | Ollama, LM Studio, vLLM (`llama3.2`, `mistral`, etc.) | Local Loopback (Zero Egress) |
| **Deterministic Mock** | `MockProvider` | `mock-gpt-4o` | Offline Test Net & CI/CD |

---

## 4. Test Suite & Verification Net

The system maintains an automated test net of **407 tests with a 100% pass rate**:

```powershell
python -m pytest tests
============================= 407 passed =============================
```

* **Unit Tests (44):** Configuration, logging, DPAPI vault, multi-provider contracts, brain memory tiers, error reflection, token optimization, and specialized agent registries.
* **Integration Tests (26):** FastAPI orchestrator endpoints, WebSocket streaming, scoped file rollback, subprocess runner env-scrubbing, project builder lifecycle, and browser session locking.
* **Security & Adversarial Tests (12):** Directory traversal attempts, null-byte injections, schema tampering, approval nonce forgery/replay, prompt-injection taint tracking, privilege escalation blocking, and emergency kill-switch responsiveness.
* **JEV Decision-Layer Tests:** Abstraction, routing, agent/model advisors, security gateway, context packing, usage tracking, UI service, benchmarks, and validation gaps — all additive alongside the baseline.

---

## 4b. JEV Decision Layer (TypeSafe AI Jev Integration)

Jev is a fast, non-generative **System One decision model** used here strictly as an
**advisory classifier** (task routing, agent/model/tool selection, guardrails,
context pruning). It never generates content, never authorizes actions, and never
bypasses the security policy engine.

* **Code:** `src/orchestrator/jev/` (abstraction, mock adapter, router, agent/model
  advisors, security gateway, context packer, usage tracker, service, benchmarks).
* **Docs:** `docs/jev/` (audit, abstraction, routing, agents, model routing, security,
  context, usage, UI, plus Stage-12 architecture/configuration/testing/benchmarks/
  troubleshooting guides).
* **Status:** Provider abstraction + mock adapter verified; live TypeSafe AI API is
  early-access, so production traffic uses the clearly labelled `mock-jev` simulator
  until verified credentials are configured. Disable anytime via the dashboard JEV
  card or `POST /api/v1/jev/config {"enabled": false}` — the application runs
  identically without it.

---

## 5. Quick-Start & Operational Commands

### 1. Run Complete Automated Test Suite
```powershell
python -m pytest tests
```

### 2. Store an AI Provider API Key (Encrypted via Windows DPAPI)
```powershell
python -c "from src.storage.credential_vault import CredentialVault; v = CredentialVault(); v.store_credential('gemini', 'YOUR_API_KEY'); print('Key encrypted successfully.')"
```

### 3. Launch the Interactive Terminal Workspace
```powershell
python chat_cli.py
```

### 4. Start the Background AI Orchestrator Service
```powershell
python run_vertical_slice.py
```

### 5. Run Live Verified Tasks
```powershell
# Read live logged-in X feed from active Chrome window:
python read_active_chrome_x.py

# Execute autonomous n8n workflow construction in Chrome:
python populate_n8n_live.py

# Hand-draw natural rocket artwork in Microsoft Paint:
python render_natural_paint_experience.py
```

---

## 6. Repository Layout

```
D:\Interveiewsass\
├── docs/                             # Architectural Specifications, PRD & Security Audits
│   ├── PRD.md                        # Product Requirements Document
│   ├── ARCHITECTURE.md               # System Architecture Specification
│   ├── THREAT_MODEL.md               # STRIDE & OWASP Threat Model
│   ├── TRUST_BOUNDARIES.md           # Trust Zones & Gateways
│   ├── CODING_STANDARDS.md           # Engineering Standards
│   ├── PHASE_100_MILESTONE.md        # Master Milestone Delivery Report
│   └── AUTONOMOUS_AGENT_ARCHITECTURE_AUDIT.md # Comprehensive Agent Architecture Audit
├── src/
│   ├── client/                       # Native WinUI 3 Desktop Frontend (C# / .NET 8)
│   ├── orchestrator/                 # Python FastAPI Orchestrator, Brain & Planner
│   │   ├── brain/                    # 4-Tier Memory, Context Engine & Error Reflection
│   │   ├── planner/                  # Autonomous Planner, Coordinator & 12 Agent Roles
│   │   ├── token_optimizer.py        # Token Tracking, Caching & Cost Accounting
│   │   ├── intelligent_router.py     # Complexity & Privacy Model Router
│   │   └── project_builder.py        # Autonomous Multi-Stage Project Builder
│   ├── providers/                    # Modular Model Adapters (Gemini, OpenAI, Claude, Local)
│   ├── security/                     # Independent Policy Engine, Defense Shield & Approval Broker
│   ├── storage/                      # DPAPI Key Vault, SQLite WAL Engines & Git Recovery
│   └── windows_integration/          # Scoped Filesystem, Process Runner, Vision & Browser
└── tests/
    ├── unit/                         # Fast isolated component unit tests
    ├── integration/                  # Cross-boundary API, WebSocket & tool tests
    └── security/                     # Penetration, traversal & prompt injection tests
```
