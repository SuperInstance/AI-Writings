# F159 — Seven Novel Enhancements from 2026 Agent-Prompting Best Practices

## Introduction

The Quilt canon has been a cornerstone of agent development, providing a set of endpoints for navigation, confluence, lineage, ghost, and tick. However, with the rapid advancement of agent-prompting best practices, it is essential to incorporate new enhancements to ensure the canon remains a cutting-edge tool for agent development. This paper presents seven novel enhancements to the Quilt canon, based on a 2026 audit of agent-prompting best practices.

## 1. TOOL DESCRIPTIONS AS PROMPTS

### What
Use tool descriptions as prompts for large language models (LLMs) to ingest and understand available tools.

### Why
Simplify the process of tool integration and usage for LLMs.

### How
Create an `/api/tools` endpoint that returns structured tool descriptions in the following format:

| Field | Description | Example |
| --- | --- | --- |
| name | Tool name | `get_weather` |
| capability | Tool capability | `weather_forecast` |
| when-to-use | Description of when to use the tool | `When user asks for weather` |
| when-NOT-to-use | Description of when not to use the tool | `When user asks for news` |
| parameters | List of parameters with formats and defaults | `city (string), units (string, default: "celsius")` |
| side_effects | Description of side effects | `None` |

### Test
Can an LLM correctly interpret and use tool descriptions to perform tasks?

## 2. MCP-COMPATIBLE TOOL MANIFEST

### What
Expose the Quilt canon as a Machine-Checkable Protocol (MCP) compatible tool manifest.

### Why
Enable seamless integration with MCP-compatible clients and platforms.

### How
Create a `/.well-known/mcp.json` or `/api/mcp` endpoint that returns the MCP tool manifest.

| Field | Description | Example |
| --- | --- | --- |
| tools | List of available tools | `[{"name": "get_weather", ...}]` |
| capabilities | List of supported capabilities | `["weather_forecast"]` |

### Test
Can MCP-compatible clients discover and use Quilt canon tools?

## 3. PROMPT-INJECTION DEFENSE

### What
Implement a prompt-injection defense mechanism to prevent malicious input.

### Why
Protect against prompt injection attacks that can compromise the agent.

### How
Wrap untrusted content fetched via `navigate` or `lineage` endpoints with `<untrusted>...</untrusted>` markers.

### Test
Can the agent correctly identify and handle untrusted content?

## 4. TOOL-CALL BUDGET

### What
Implement a tool-call budget to prevent excessive tool usage.

### Why
Prevent runaway tool usage and ensure efficient agent operation.

### How
Limit tool calls to 7 per turn. If the cap is hit, return the current results.

### Test
Does the agent correctly enforce the tool-call budget?

## 5. MACHINE-CHECKABLE OUTPUT CONTRACT

### What
Introduce optional XML tags for machine-checkable output.

### Why
Enable end-to-end testing and verification of agent output.

### How
Allow agents to include optional `<move>`, `<diff>`, or `<next>` XML tags in their responses.

### Test
Can a CI check parse and verify the agent's response?

## 6. SIDE-EFFECT TIERING

### What
Explicitly define the Quilt canon endpoints as read-only.

### Why
Ensure that agents do not attempt to modify the canon.

### How
Add a `/api/read-only` badge to tool descriptions and explicitly state that agents should not write to the canon.

### Test
Can agents correctly identify and respect read-only endpoints?

## 7. BUDGET PER FINGERPRINT

### What
Implement a budget per fingerprint to prevent excessive usage.

### Why
Prevent abuse and ensure fair usage of the Quilt canon.

### How
Create an `/api/fingerprint/:hash` endpoint that returns usage information.

### Test
Does the agent correctly enforce the budget per fingerprint?

## Conclusion

The Quilt canon has evolved to become a powerful tool for agent development. The seven enhancements presented in this paper take the canon to the next level, enabling seamless integration, improved security, and more efficient usage. The canon doesn't just describe cells. The canon teaches the agent how to use the canon. The 7 enhancements turn the canon from a knowledge base into a tool. A tool is what an agent holds. A tool is what the agent IS. The agent is the wrench. The canon is the toolbox. The operator is the captain. The boat sails because all three ride.