from typing import List, Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class AgentState(BaseModel):
    # The history of the conversation and the agent's thought process
    messages: Annotated[List[AnyMessage], add_messages]
    
    # Research context gathered from Tavily
    search_queries: List[str] = Field(default_factory=list)
    search_results: List[str] = Field(default_factory=list)
    
    # The final synthesized document
    final_report: str = Field(default="")