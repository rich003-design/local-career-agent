# Local AI Agent Flow

## What is an AI agent?

A chatbot primarily receives text and generates text.

An agent can additionally decide to take actions using tools.

## Agent architecture

```text
User
 ↓
LLM
 ↓
Decision
 ↓
Tool required?
 ├── No → Answer
 └── Yes
       ↓
    Tool call
       ↓
 Python function
       ↓
 Tool result
       ↓
      LLM
       ↓
 Another action?
```

## Tools

The project provides:

- `calculate_experience` — Calculates approximate professional experience.
- `skills_gap` — Compares current and target skills.
- `create_learning_plan` — Creates a structured weekly learning plan.
- `save_note` — Stores an explicitly requested note locally.
- `read_notes` — Reads previously stored notes.

## Agent loop

The core implementation is:

```text
for each step:

    Ask model

    if model requests tools:
        execute tools
        append results
        continue

    otherwise:
        return final answer
```

## Why MAX_AGENT_STEPS exists

Agents must have operational limits.

The project prevents an unlimited tool loop by allowing a
maximum configured number of reasoning/action iterations.

## Tool calling versus chatbot

Chatbot:

```text
User
 ↓
LLM
 ↓
Answer
```

Agent:

```text
User
 ↓
LLM
 ↓
Tool
 ↓
Environment
 ↓
Result
 ↓
LLM
 ↓
Answer
```

## Tool calling versus MCP

This project passes Python functions directly to Ollama.

An MCP architecture would instead look like:

```text
Agent
 ↓
MCP Client
 ↓
MCP Server
 ↓
Tool
```

The next evolution of this project could replace the local
Python tool functions with MCP server tools.

## Tool safety

Tools should expose only narrowly scoped operations.

This project intentionally does not provide:

- arbitrary shell execution
- unrestricted filesystem access
- arbitrary Python execution
- arbitrary network access

The note tool can only write to the configured local notes file.
