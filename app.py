import streamlit as st

from patterns.tool_using.graph import build_graph


st.set_page_config(page_title="Agentic Assistant", page_icon="A", layout="centered")
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 92% 2%, rgba(214, 231, 219, 0.7), transparent 34%),
            #f7f8f4;
        color: #203537;
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 860px; padding-top: 3rem; padding-bottom: 2rem; }
    h1 { color: #17484a; font-family: Georgia, serif; font-weight: 600; }
    [data-testid="stChatMessage"] {
        border: 1px solid #dce5df;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.82);
    }
    [data-testid="stChatInput"] { border-color: #9fb9ac; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Agentic Assistant")
st.caption("Arithmetic, explanations, and general questions")


@st.cache_resource
def get_workflow():
    return build_graph()


if "messages" not in st.session_state:
    st.session_state.messages = []


def render_message(message):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("intent") == "math":
            with st.expander("Calculation details"):
                st.code(message.get("expression", ""), language="python")
                if message.get("result"):
                    st.write(f"Result: {message['result']}")
        if message.get("error"):
            with st.expander("Technical details"):
                st.code(message["error"])


for message in st.session_state.messages:
    render_message(message)

question = st.chat_input("Ask a question")
if question:
    user_message = {"role": "user", "content": question}
    st.session_state.messages.append(user_message)
    render_message(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = get_workflow().invoke({"question": question})
                assistant_message = {
                    "role": "assistant",
                    "content": result.get("response", "I couldn't produce an answer."),
                    "intent": result.get("intent"),
                    "expression": result.get("expression"),
                    "result": result.get("result"),
                }
            except Exception as error:
                assistant_message = {
                    "role": "assistant",
                    "content": "I couldn't complete that request. Check the API key and connection, then try again.",
                    "error": str(error),
                }

        st.markdown(assistant_message["content"])
        if assistant_message.get("intent") == "math":
            with st.expander("Calculation details"):
                st.code(assistant_message.get("expression", ""), language="python")
                if assistant_message.get("result"):
                    st.write(f"Result: {assistant_message['result']}")
        if assistant_message.get("error"):
            with st.expander("Technical details"):
                st.code(assistant_message["error"])
        st.session_state.messages.append(assistant_message)