from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from backend.tools.appointment_tools import check_slot_availability, book_appointment

# -----------------------
# Agent State
# -----------------------

class AgentState(TypedDict):
    conversation_history: List[Dict[str, str]]
    last_response: str


# -----------------------
# Initialize Groq LLM
# -----------------------

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7
)


# -----------------------
# Agent Node
# -----------------------

def agent_node(state: AgentState) -> AgentState:

    messages = []

    for msg in state["conversation_history"]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    response = llm.invoke(messages)

    state["last_response"] = response.content

    state["conversation_history"].append({
        "role": "assistant",
        "content": response.content
    })

    return state


# -----------------------
# Graph
# -----------------------

def create_agent_graph():

    workflow = StateGraph(AgentState)

    workflow.add_node("agent", agent_node)

    workflow.set_entry_point("agent")

    workflow.add_edge("agent", END)

    return workflow.compile()