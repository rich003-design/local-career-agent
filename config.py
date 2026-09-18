"""
Configuration for the local AI agent.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent

load_dotenv(
    PROJECT_ROOT / ".env"
)


OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:4b",
)

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)

MAX_AGENT_STEPS = int(
    os.getenv(
        "MAX_AGENT_STEPS",
        "8",
    )
)

NOTES_FILE = PROJECT_ROOT / os.getenv(
    "NOTES_FILE",
    "data/notes.json",
)