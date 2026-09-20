import os
from dotenv import load_dotenv

# 1. Must run before internal project imports that read os.environ
load_dotenv()

from langchain_core.messages import HumanMessage
from graph import research_graph

def run_research_engine(query: str):
    print(f"\n🚀 Starting Deep Research Engine")
    print(f"Topic: {query}\n")
    
    initial_state = {
        "messages": [HumanMessage(content=query)]
    }
    
    # 2. Stream the graph execution
    for event in research_graph.stream(initial_state):
        for node_name, node_update in event.items():
            print(f"--- [Node Executed: {node_name.upper()}] ---")
            
            # If the synthesize node ran, print the final report
            if node_name == "synthesize":
                print("\n✅ FINAL REPORT GENERATED:\n")
                print(node_update["final_report"])
                print("\n-----------------------------------\n")
            else:
                # For intermediate nodes, safely extract the latest message
                messages = node_update.get("messages", [])
                if not messages:
                    continue
                    
                latest_message = messages[-1]
                
                # Check if it's a tool call request
                if getattr(latest_message, "tool_calls", None):
                    print(f"🛠️  Agent triggered search for: {latest_message.tool_calls[0]['args']}\n")
                # Check if it's a tool execution result
                elif latest_message.type == "tool":
                    print(f"📄 Search completed. Feeding web data back into context...\n")
                else:
                    print(f"🧠 Agent reasoning...\n")

if __name__ == "__main__":
    # Test our engine with a complex technical question
    test_query = "What are the primary differences between LangChain and LangGraph in AI agent development?"
    run_research_engine(test_query)