"""
Local tool-calling Career Agent powered by Ollama.
"""

import json
from typing import Any

from ollama import (
    ChatResponse,
    Client,
)

from config import (
    MAX_AGENT_STEPS,
    OLLAMA_HOST,
    OLLAMA_MODEL,
)

from tools import (
    calculate_experience,
    create_learning_plan,
    read_notes,
    save_note,
    skills_gap,
)


SYSTEM_PROMPT = """
You are Career Agent, a practical AI career assistant.

You are an agent, not only a chatbot.

You have access to tools that can:

- calculate professional experience;
- compare current and target skills;
- create learning plans;
- save notes locally;
- read previously saved notes.

Agent rules:

1. Use tools whenever they can provide a more reliable result.
2. Do not claim that a tool was used unless you actually called it.
3. You may call multiple tools before answering.
4. Use the result of one tool when deciding whether another tool is needed.
5. Do not invent tool results.
6. Ask a clarifying question if critical information is missing.
7. Give a clear final answer after tool work is complete.
8. Do not expose internal implementation details.
9. Only save a note when the user explicitly asks for information to be saved.
10. Never modify arbitrary files. You may only use the provided note-storage tool.
"""


AVAILABLE_TOOLS = {
    "calculate_experience": (
        calculate_experience
    ),
    "skills_gap": skills_gap,
    "create_learning_plan": (
        create_learning_plan
    ),
    "save_note": save_note,
    "read_notes": read_notes,
}


TOOL_FUNCTIONS = list(
    AVAILABLE_TOOLS.values()
)


client = Client(
    host=OLLAMA_HOST
)


def serialize_tool_result(
    result: Any,
) -> str:
    """
    Convert tool output into text that can be sent back to the model.
    """

    if isinstance(
        result,
        (
            dict,
            list,
        ),
    ):
        return json.dumps(
            result,
            ensure_ascii=False,
        )

    return str(result)


def execute_tool_call(
    tool_call,
) -> dict[str, str]:
    """
    Execute one tool requested by the language model.
    """

    tool_name = (
        tool_call.function.name
    )

    arguments = (
        tool_call.function.arguments
    )

    function_to_call = (
        AVAILABLE_TOOLS.get(
            tool_name
        )
    )

    if function_to_call is None:
        return {
            "role": "tool",
            "tool_name": tool_name,
            "content": (
                f"Tool '{tool_name}' "
                "is not available."
            ),
        }

    try:
        result = function_to_call(
            **arguments
        )

        content = (
            serialize_tool_result(
                result
            )
        )

    except Exception as error:
        content = json.dumps(
            {
                "error": (
                    type(error).__name__
                ),
                "message": str(error),
            }
        )

    return {
        "role": "tool",
        "tool_name": tool_name,
        "content": content,
    }


def run_agent(
    user_message: str,
    conversation_history: list[
        dict[str, str]
    ]
    | None = None,
) -> dict[str, Any]:
    """
    Run the multi-step agent loop.

    The model may:
    - answer directly;
    - call one tool;
    - call several tools;
    - use one tool result to decide on another tool.

    Returns:
        Final response and execution trace.
    """

    messages: list[Any] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    if conversation_history:
        for message in (
            conversation_history[-10:]
        ):
            if message["role"] in {
                "user",
                "assistant",
            }:
                messages.append(
                    {
                        "role": (
                            message["role"]
                        ),
                        "content": (
                            message["content"]
                        ),
                    }
                )

    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    trace: list[dict[str, Any]] = []

    for step_number in range(
        1,
        MAX_AGENT_STEPS + 1,
    ):
        response: ChatResponse = (
            client.chat(
                model=OLLAMA_MODEL,
                messages=messages,
                tools=TOOL_FUNCTIONS,
                stream=False,
            )
        )

        assistant_message = (
            response.message
        )

        messages.append(
            assistant_message
        )

        tool_calls = (
            assistant_message.tool_calls
            or []
        )

        trace.append(
            {
                "step": step_number,
                "tool_calls": [
                    call.function.name
                    for call in tool_calls
                ],
            }
        )

        if not tool_calls:
            final_answer = (
                assistant_message.content
                or (
                    "The agent completed "
                    "without producing a "
                    "text response."
                )
            )

            return {
                "answer": final_answer,
                "trace": trace,
            }

        for tool_call in tool_calls:
            tool_result_message = (
                execute_tool_call(
                    tool_call
                )
            )

            trace.append(
                {
                    "step": step_number,
                    "tool": (
                        tool_call
                        .function
                        .name
                    ),
                    "arguments": (
                        tool_call
                        .function
                        .arguments
                    ),
                    "result": (
                        tool_result_message[
                            "content"
                        ]
                    ),
                }
            )

            messages.append(
                tool_result_message
            )

    return {
        "answer": (
            "The agent reached its maximum "
            "number of tool steps without "
            "finishing the task."
        ),
        "trace": trace,
    }


if __name__ == "__main__":
    print(
        "Local Career Agent"
    )
    print(
        "Type 'exit' to stop."
    )

    history = []

    while True:
        user_input = input(
            "\nYou: "
        ).strip()

        if user_input.lower() in {
            "exit",
            "quit",
        }:
            break

        result = run_agent(
            user_message=user_input,
            conversation_history=history,
        )

        print(
            "\nAgent:",
            result["answer"],
        )

        history.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": result["answer"],
            }
        )
