# Model Context Protocol (MCP) Strategy

The **Model Context Protocol (MCP)** is the bridge that allows our AI agents to step out of their text-only sandbox and physically interact with the NutriMind application.

## Why MCP is Used
Historically, LLMs generated code that a human had to copy-paste and execute. MCP provides standard client/server architecture that exposes localized tooling directly to the LLM. 
For example, our `AutomationAgent` uses an MCP tool to trigger Playwright to execute a UI click on `button#submit`. This allows the agent to visually and functionally interact with the application state in real-time.

## Security Boundary
MCP provides a critical security sandbox. The LLM does not have raw `bash` access to our servers. It is strictly limited to the specific tools exposed via the MCP server (e.g., `click_element`, `read_dom`, `submit_api_payload`). This prevents malicious prompt injections from tricking the AI into executing destructive system commands.
