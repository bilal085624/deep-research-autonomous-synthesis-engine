import os
from dotenv import load_dotenv

# Load environment variables before initializing API clients
load_dotenv()

from langchain_tavily import TavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from state import AgentState

# 1. Initialize the Search Tool
search_tool = TavilySearch(max_results=3)
tools = [search_tool]

# 2. Initialize the Base Gemini LLM
base_llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash", 
    temperature=0
)

# 3. Bind the tools FIRST, then attach the retry logic
llm_with_tools = base_llm.bind_tools(tools).with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)

# Create a tool-free version with retry logic for the synthesis node
llm = base_llm.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)

# 4. Define the Agent Node Function
def call_model(state: AgentState):
    messages = state.messages if hasattr(state, "messages") else state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 5. Initialize the Tool Execution Node
tool_node = ToolNode(tools=tools)

# 6. Define the Routing Logic (Conditional Edge)
def should_continue(state: AgentState) -> str:
    messages = state.messages if hasattr(state, "messages") else state["messages"]
    last_message = messages[-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"
    
    return "synthesize"

# 7. Define the Synthesis Node
def synthesize_report(state: AgentState):
    messages = state.messages if hasattr(state, "messages") else state["messages"]
    
    # 1. Keeping your original, rigorous technical prompt
    synthesis_prompt = HumanMessage(
        content="Synthesize all the gathered research above into an executive, "
                "well-cited technical summary. Highlight verified facts, key takeaways, "
                "and any data contradictions."
    )
    
    final_response = llm.invoke(messages + [synthesis_prompt])
    
    # 2. Extracting clean text to hide the raw API dictionary and cryptographic signatures
    content = final_response.content
    if isinstance(content, list):
        # Join all text blocks and ignore metadata/signatures
        clean_text = "".join(part.get("text", "") for part in content if isinstance(part, dict) and "text" in part)
    else:
        clean_text = str(content)
        
    return {
        "messages": [final_response],
        "final_report": clean_text
    }