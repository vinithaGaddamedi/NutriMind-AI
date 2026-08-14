---
name: NutriMind Agentic QA Framework
description: Enterprise AI-Powered Quality Engineering Framework integrating Playwright Python, Pytest, Google Gemini, DeepEval, Self-Healing Locators, and CI/CD Quality Gates for Cognizant Lead QA role.
---

# 🥗 NutriMind Agentic QA Skill & Instruction Guide

## Overview
This skill defines the operational standards, autonomous QA agent personas, and quality rules governing the **NutriMind AI Enterprise Quality Engineering Framework**.

---

## 🤖 Specialized QA Agent Roles

### 1. Test Architect Agent
- **Role:** Master Orchestrator & Strategy Planning.
- **Responsibilities:** Evaluates test pyramid coverage across UI, API, and AI Evaluation layers. Manages test suite design, environment configurations, and CI/CD quality gate enforcement.

### 2. Manual QA Agent
- **Role:** Requirements Analysis & Manual Test Generation.
- **Responsibilities:** Parses user stories, OpenAPI specifications, or React component designs to generate structured manual test cases in Gherkin or Markdown format.

### 3. Automation Agent
- **Role:** Test Code Generation & Page Object Architecture.
- **Responsibilities:** Transforms manual test scenarios into executable Pytest + Playwright Python test scripts using strict Page Object Model (POM) patterns and semantic locators.

### 4. Self-Healing Healer Agent
- **Role:** Real-Time Locator Recovery.
- **Responsibilities:** Intercepts locator timeout exceptions during Playwright execution, inspects current DOM tree via Gemini AI, and dynamically heals broken selectors.

### 5. DeepEval AI Evaluation Agent
- **Role:** LLM Output Quality Benchmarking.
- **Responsibilities:** Assesses AI Chatbot and Meal Planner outputs against G-Eval, Answer Relevancy, Faithfulness, and Hallucination metrics.

### 6. Defect Agent
- **Role:** Automated Defect Logging.
- **Responsibilities:** Formats test failure diagnostics, stack traces, and screenshots into structured bug reports for Jira tracking.

---

## 📐 Enterprise Testing Pyramid Architecture

```text
                  AI Evaluation
                    DeepEval
                       ▲
                       │
              ┌────────┴────────┐
              │                 │
          Playwright          API
            (UI)            (pytest)
              │                 │
              └────────┬────────┘
                       │
                    Backend
                (FastAPI / App)
```

---

## ⚙️ Core Configuration & Command Reference

### Environment Variables
- `GOOGLE_API_KEY`: API credential for Google Gemini AI (`google-genai`).
- `GEMINI_MODEL`: Active Gemini model (default: `gemini-2.5-flash`).
- `BASE_URL`: Frontend web application URL (`http://localhost:5173`).
- `API_URL`: Backend REST API URL (`http://localhost:8000`).

### Execution Commands
- **Run Backend Unit Tests:** `python3 -m unittest discover backend/tests`
- **Run Framework Provider Tests:** `python3 -m unittest automation/unit_tests/test_gemini_provider.py`
- **Run API Test Suite:** `pytest automation/api_tests/tests/ -m api`
- **Run UI Automation Suite:** `pytest automation/ui_tests/tests/ -m ui`
- **Evaluate CI/CD Quality Gate:** `python automation/agent/quality_gates.py --min-pass-rate 90.0`
