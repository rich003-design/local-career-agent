"""
Streamlit UI for the Local Career Agent.
"""

import streamlit as st

from agent import run_agent


WELCOME_MESSAGE = (
    "Hello! I am your local Career Agent. "
    "I can calculate experience, analyze skill gaps, "
    "create learning plans, and manage local notes."
)


def initialize_session() -> None:
    """
    Initialize conversation history.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    WELCOME_MESSAGE
                ),
            }
        ]

    if "last_trace" not in (
        st.session_state
    ):
        st.session_state.last_trace = []


def reset_conversation() -> None:
    """
    Clear the current conversation.
    """

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE,
        }
    ]

    st.session_state.last_trace = []


st.set_page_config(
    page_title="Local Career Agent",
    page_icon="🤖",
    layout="centered",
)


initialize_session()


st.title(
    "🤖 Local Career Agent"
)

st.caption(
    "An Ollama-powered tool-calling AI agent."
)


with st.sidebar:
    st.header(
        "Agent capabilities"
    )

    st.write(
        """
        The agent can:

        - Calculate professional experience
        - Compare skill gaps
        - Create learning plans
        - Save local notes
        - Read previously saved notes
        - Use multiple tools for one request
        """
    )

    if st.button(
        "Clear conversation",
        use_container_width=True,
    ):
        reset_conversation()
        st.rerun()

    if st.session_state.last_trace:
        st.divider()

        with st.expander(
            "Last agent execution trace"
        ):
            st.json(
                st.session_state.last_trace
            )


for message in (
    st.session_state.messages
):
    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )


user_prompt = st.chat_input(
    "Ask the agent to perform a task..."
)


if user_prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    with st.chat_message(
        "user"
    ):
        st.markdown(
            user_prompt
        )

    history = (
        st.session_state.messages[
            :-1
        ]
    )

    with st.chat_message(
        "assistant"
    ):
        try:
            with st.status(
                "Agent is working...",
                expanded=False,
            ) as status:

                result = run_agent(
                    user_message=(
                        user_prompt
                    ),
                    conversation_history=(
                        history
                    ),
                )

                status.update(
                    label=(
                        "Agent task completed."
                    ),
                    state="complete",
                )

            answer = result[
                "answer"
            ]

            st.markdown(
                answer
            )

            st.session_state.last_trace = (
                result["trace"]
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as error:
            st.error(
                "The agent could not "
                "complete the request."
            )

            st.caption(
                f"Error type: "
                f"{type(error).__name__}"
            )

            # During development:
            # st.exception(error)
