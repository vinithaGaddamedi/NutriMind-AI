# Repository Structure Audit & Migration Plan

This document details the audit of the current repository structure of the **NutriMind AI** framework and outlines the safe, incremental migration sequence to transition it into an enterprise-grade Quality Engineering (QE) architecture.

---

## 1. Directory and Component Analysis

| Current Path | Purpose | Owner / Responsibility | Duplicate Functionality | Proposed Destination | Risk of Moving | Dependencies & Imports | Recommended Action |
|---|---|---|---|---|---|---|---|
| `agents/` | 5-Tier AI Agent framework (orchestration, shift_left, automation, intelligence) | AI QA Orchestration Engine | None | `agents/` (Retain root, restructure contents) | Low | Imported widely by unit tests and `demo_e2e_lifecycle.py` | **KEEP** and align interior subdirectories |
| `agents/gateway/` | Centralized AI gateway logic | AI API Infrastructure | None | `agents/providers/` or `agents/infrastructure/` | Medium | Imported by all agents via `from agents.gateway.ai_gateway import AIGateway` | **MOVE** contents to `agents/providers/` and update references |
| `agents/self_healing/` | Dynamic locator healer | Self-healing automation utility | Duplicates `agents/automation/healer_agent.py` and `automation/utils/self_healing_service.py` | `agents/automation/` (Merge with healer agent) | Low | Imported by `test_enterprise_framework.py` | **MERGE** `healer.py` logic into `agents/automation/healer_agent.py` or keep helper as `agents/automation/healer.py` |
| `agents/schemas/` | Pydantic data schemas for all agents | Agent Input/Output Protocols | None | `agents/infrastructure/` | Medium | Imported by almost all agents and schemas | **MOVE** to `agents/infrastructure/schemas/` |
| `automation/` | Classic QA automation framework | QA Team / SDET | None | `automation/` (Retain root, restructure contents) | Low | Shared conftest, pytest configurations | **RESTRUCTURE** interior subdirectories |
| `automation/ui_tests/` | Playwright E2E UI tests | UI QA Automation | None | `automation/tests/ui/` | High | Imports page objects and steps | **MOVE** test files to `automation/tests/ui/` |
| `automation/ui_tests/pages/` | Page Object Models for UI | UI QA Automation | Duplicates `automation/pages/chat_page.py` | `automation/pages/` | High | Imported by step definitions and UI tests | **MERGE** all page objects into `automation/pages/` |
| `automation/ui_tests/step_defs/` | BDD step definitions for UI | UI QA Automation | None | `automation/tests/ui/step_defs/` | High | Imported by pytest-bdd runners | **MOVE** to `automation/tests/ui/step_defs/` |
| `automation/ui_tests/features/` | Gherkin feature files for UI | QA Product Analyst | None | `automation/tests/ui/features/` | Low | Loaded by pytest-bdd | **MOVE** to `automation/tests/ui/features/` |
| `automation/api_tests/` | Backend REST API tests | API QA Automation | None | `automation/tests/api/` | High | Imports API clients | **MOVE** tests/features/steps to `automation/tests/api/` |
| `automation/api_tests/clients/` | HTTP client wrappers for API | API QA Automation | None | `automation/utils/` (or `automation/tests/api/clients/`) | Medium | Imported by API and integration tests | **MOVE** `api_client.py` to `automation/utils/` |
| `automation/integration_tests/` | Meal planner integration tests | Integration QA | None | `automation/tests/integration/` | Medium | Imports SUT services and API clients | **MOVE** to `automation/tests/integration/` |
| `automation/mobile_tests/` | Appium/Mobile UI test stubs | Mobile QA | None | `automation/tests/mobile/` | Low | Isolated stubs | **MOVE** to `automation/tests/mobile/` |
| `automation/tests/` | Existing agent/AI/gate tests | Framework / AI QA | None | `automation/tests/` (Refactored) | Low | Imported widely | **ALIGN** with target subdirectories |
| `automation/test_data/` | CSV/JSON mock test inputs | QA Team | Duplicates root `test_data/` | `test_data/` (Root-level) | Medium | Imported by page objects and data loaders | **MOVE** static test files to root `test_data/` |
| `automation/agent/` | Legacy/Temporary Phase 1 Agent stubs | Historical / Redundant | Duplicates new orchestrated agents | Archive / Delete | None | Not imported by any active test suite | **REMOVE** or archive `automation/agent/` |
| `ai_testing/` | AI evaluation and regression suites | AI Safety & Quality | None | `ai_testing/` | Low | DeepEval libraries | **KEEP** and align interior subdirectories |
| `mcp/` | Model Context Protocol modules | MCP Infrastructure | None | `mcp/` (Retain root, restructure contents) | Low | Used by orchestration and agents | **RESTRUCTURE** into `server/` and `tools/` |
| `application/` | System Under Test (SUT) application code | Dev Team | None | `application/` | Low | None | **KEEP** (backend, web-app, mobile-app) |

---

## 2. Target Corporate Architecture

The final directory tree will cleanly isolate development code, classic automation, AI testing, and agent frameworks:

```text
NutriMind-AI/
├── .agents/                      # Agent skills and governance rules
├── .github/                      # CI/CD pipeline definitions
├── agents/                       # AI Agent Framework
│   ├── orchestration/            # Execution flows (orchestrator.py, etc.)
│   ├── shift_left/               # Jira, requirement, risk agents
│   ├── automation/               # Planner, generator, validator, healer agents
│   ├── intelligence/             # Analytics, coverage, failure analysis agents
│   ├── infrastructure/           # Schemas, common agent utilities
│   └── providers/                # AI gateway, Gemini provider
│
├── automation/                   # Classic QA Automation Framework
│   ├── tests/                    # Executable test suites
│   │   ├── ui/                   # Playwright UI tests, BDD steps, features
│   │   ├── api/                  # REST API tests, BDD steps, features
│   │   ├── integration/          # Core end-to-end integration tests
│   │   └── mobile/               # Appium mobile test scripts
│   ├── pages/                    # Unified Page Object Models (POM)
│   ├── fixtures/                 # Shared pytest fixtures
│   ├── utils/                    # Reporting, API client wrappers, utilities
│   ├── assertions/               # Custom test verification matchers
│   └── config/                   # QA environments and gate threshold settings
│
├── ai_testing/                   # AI/LLM Quality and Semantic Evaluation
│   ├── deepeval/                 # DeepEval test cases and pipelines
│   ├── golden_datasets/          # Version-controlled golden datasets
│   ├── validators/               # Deterministic business rule validators
│   ├── security/                 # Prompt injection and security suites
│   └── prompts/                  # Versioned prompt templates
│
├── mcp/                          # Model Context Protocol Infrastructure
│   ├── server/                   # MCP Server core logic
│   ├── tools/                    # Playwright browser tools for agents
│   └── config/                   # MCP server and client configurations
│
├── application/                  # SUT (System Under Test)
│   ├── backend/                  # FastAPI Application
│   ├── web-app/                  # React Frontend
│   └── mobile-app/               # Mobile React Native (Stub)
│
├── test_data/                    # Project-level static test data (CSV, JSON)
├── scripts/                      # Helper scripts (run_demo.sh)
├── docs/                         # Quality engineering documentation
│   ├── architecture/
│   ├── testing/
│   ├── automation/
│   ├── governance/
│   └── interview/
│
├── pytest.ini                    # Root-level Pytest configurations
├── requirements.txt              # Top-level Python dependencies
└── README.md                     # Executive summary and showcase guide
```

---

## 3. Safe Step-by-Step Migration Plan

To avoid breaking any imports or running into test failures, we will apply the changes incrementally and validate with `pytest` after each step.

### Step 1: Fix Existing Backend & Chatbot Schema Regressions
* **Issue**: The chatbot backend imports `ChatMessage` from `application/backend/schemas/chat.py`, but it doesn't exist. Also `chat_service` is not instantiated or exported.
* **Resolution**: Already applied (ChatMessage added, ai_chat_service.py updated with `generate_chat_response` and instantiated `chat_service`).
* **Verification**: Ensure backend imports resolve.

### Step 2: Restructure the MCP Directory
* Create directories `mcp/server/` and `mcp/tools/`.
* Move `mcp/mcp_server.py` to `mcp/server/mcp_server.py`.
* Move `mcp/mcp_playwright_agent.py` to `mcp/tools/mcp_playwright_agent.py`.
* Create `mcp/server/__init__.py` and `mcp/tools/__init__.py`.
* Run global import update for `mcp.mcp_server` and `mcp.mcp_playwright_agent` (e.g. in `agents/orchestration/orchestrator.py` and `automation/tests/agents/test_mcp_agent.py`).

### Step 3: Restructure the Agents Directory
* Create `agents/infrastructure/` and `agents/infrastructure/schemas/`.
* Move `agents/schemas/*.py` to `agents/infrastructure/schemas/`.
* Move `agents/gateway/ai_gateway.py` to `agents/providers/ai_gateway.py` (since gateway is provider infrastructure).
* Remove empty `agents/gateway/` directory.
* Merge `agents/self_healing/healer.py` helper into `agents/automation/healer_agent.py` or move to `agents/automation/healer.py`. Remove `agents/self_healing/`.
* Run global import update for all schema and gateway references.

### Step 4: Restructure the Automation Directory
* Create the target test folders: `automation/tests/ui/`, `automation/tests/api/`, `automation/tests/integration/`, `automation/tests/mobile/`, `automation/tests/ai/`.
* **UI**: Move `automation/ui_tests/tests/*` to `automation/tests/ui/`, `automation/ui_tests/step_defs/` and `automation/ui_tests/features/` into `automation/tests/ui/`.
* **API**: Move `automation/api_tests/tests/*` to `automation/tests/api/`, `automation/api_tests/step_defs/` and `automation/api_tests/features/` into `automation/tests/api/`.
* **Integration**: Move `automation/integration_tests/*` to `automation/tests/integration/`.
* **Mobile**: Move `automation/mobile_tests/*` to `automation/tests/mobile/`.
* **AI**: Move existing AI tests from `automation/tests/ai/` into `automation/tests/ai/` (keeping them aligned).
* **Pages**: Move page objects from `automation/ui_tests/pages/*` to `automation/pages/`.
* **Clients**: Move `automation/api_tests/clients/api_client.py` to `automation/utils/api_client.py`.
* **Clean up**: Remove directories `ui_tests`, `api_tests`, `integration_tests`, `mobile_tests` once empty.
* **Remove Legacy**: Remove redundant `automation/agent/` stubs.

### Step 5: Update Imports and Run Tests
* Run a python script to search and replace import references across the entire codebase to match the new structure.
* Specifically fix imports in:
  - All test files under `automation/tests/`
  - Integration tests pointing to Dev backend services (`services.*` -> `application.backend.services.*`)
  - Page object references and step definitions
* Run `pytest` to confirm all 100+ tests collect and execute successfully.
