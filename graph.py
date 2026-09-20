from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from state import AgentState
from nodes import call_model, tool_node, should_continue, synthesize_report

# 1. Initialize Graph
builder = StateGraph(AgentState)

# 2. Register Nodes
builder.add_node("agent", call_model)
builder.add_node("tools", tool_node)
builder.add_node("synthesize", synthesize_report)

# 3. Define Edges
builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "synthesize": "synthesize"
    }
)
builder.add_edge("tools", "agent")
builder.add_edge("synthesize", END)

# 4. Phase 3: Compile with Memory Checkpointing
memory = MemorySaver()
research_graph = builder.compile(checkpointer=memory)