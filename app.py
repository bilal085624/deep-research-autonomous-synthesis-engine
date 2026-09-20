import streamlit as st
from langchain_core.messages import HumanMessage
from graph import research_graph
from dotenv import load_dotenv

load_dotenv()

# Configure the viewport and custom typography
st.set_page_config(page_title="AI Research Engine", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Noto Sans', sans-serif;
}
.stButton>button {
    width: 100%;
    border-radius: 5px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("Deep Research Autonomous Synthesis Engine")

# Thread configuration ensures the checkpointer tracks this specific user session
config = {"configurable": {"thread_id": "session_1"}}

query = st.text_input("Enter your research topic:", placeholder="e.g., Latest generative AI benchmarks")

if st.button("Run Engine") and query:
    initial_state = {"messages": [HumanMessage(content=query)]}
    
    # UI Elements for real-time updates
    status_box = st.info("Initializing connection...")
    report_placeholder = st.empty()
    
    # Stream the graph execution directly to the UI
    for event in research_graph.stream(initial_state, config=config):
        for node_name, node_update in event.items():
            
            if node_name == "synthesize":
                status_box.success("✅ Synthesis Complete")
                report_placeholder.markdown(node_update["final_report"])
            else:
                messages = node_update.get("messages", [])
                if messages:
                    latest = messages[-1]
                    if getattr(latest, "tool_calls", None):
                        status_box.warning(f"🛠️ Executing Search: {latest.tool_calls[0]['args']}")
                    elif latest.type == "tool":
                        status_box.info("📄 Processing Web Context...")
                    else:
                        status_box.info("🧠 Reasoning Model Engaged...")