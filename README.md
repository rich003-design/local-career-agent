# Local Career Agent

A fully local AI agent built with Python, Streamlit, Ollama,
and native tool calling.

## Features

- Local LLM using Ollama
- Multi-step tool calling
- Professional experience calculation
- Skills-gap analysis
- Learning-plan generation
- Local note storage
- Conversation history
- Agent execution trace
- Streamlit interface

## Architecture

```text
User
 ↓
Streamlit
 ↓
Agent loop
 ↓
Ollama
 ↓
Tool decision
 ↓
Python tool
 ↓
Tool result
 ↓
Ollama
 ↓
Final response
```

## Requirements

- Python 3.10+
- Ollama
- qwen3:4b

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Ollama setup

```bash
ollama pull qwen3:4b
```

Verify:

```bash
ollama list
```

## Environment configuration

```bash
cp .env.example .env
```

## Run CLI agent

```bash
python3 agent.py
```

## Run Streamlit agent

```bash
python3 -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Example request

```text
I started my career in 2015.

My current skills are Java, Docker and Git.

I want Python, Docker, Kubernetes, MLflow and Terraform.

Calculate my experience, identify the missing skills,
create an eight-week learning plan and save it.
```

## Run tests

```bash
python3 -m pytest tests/test_tools.py -v
```

## Security

The agent does not expose:

- shell execution
- arbitrary file access
- arbitrary Python execution

The note tool is restricted to the configured local notes file.
