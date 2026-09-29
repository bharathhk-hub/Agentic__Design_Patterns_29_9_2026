# Agentic Design Patterns

A small LangGraph application that routes arithmetic questions to a calculator tool and sends general questions to an LLM fallback. A Streamlit chat interface provides the user-facing app.

## Workflow

1. `reasoning_agent` classifies the request as arithmetic or general and extracts a math expression when appropriate.
2. Arithmetic requests go to `math_agent`, which evaluates only a restricted set of arithmetic operations.
3. Other requests go to `fallback_agent`, which answers with the configured chat model.

Both paths return a response to the same chat interface. The calculator does not use Python `eval` and rejects calls, names, attributes, and other non-arithmetic syntax.

## Requirements

- Python 3.10 or newer
- An OpenAI API key

## Setup

From the repository root, create and activate a virtual environment, then install the dependencies:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the repository root and add your key:

```text
OPENAI_API_KEY=your-api-key
```

Keep `.env` private; it is ignored by Git.

## Run

Start the Streamlit app from the repository root:

```powershell
streamlit run app.py
```

Try an arithmetic question such as `What is the square of the average of 10 and 5?`, or a general question such as `Define AI.` The interface shows the expression and evaluated result for arithmetic requests.

## Tests

Run the dependency-free calculator and routing tests with:

```powershell
python -m unittest discover -s tests -v
```

## Project layout

```text
app.py                       Streamlit chat interface
config/llm.py                Chat model configuration
patterns/tool_using/graph.py LangGraph workflow and routing
patterns/tool_using/nodes.py Intent planner, math agent, and fallback agent
patterns/tool_using/state.py Shared graph state and route selection
tools/calculator.py          Restricted arithmetic evaluator
tests/                       Unit tests
```
