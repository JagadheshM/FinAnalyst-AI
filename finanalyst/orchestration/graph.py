from langgraph.graph import StateGraph, END
from .state import WorkflowState

# Import Agent Nodes
from ..agents.news_collector import news_collector_node
from ..agents.news_impact import news_impact_node
from ..agents.sector_analysts import (
    technology_analyst_node,
    banking_analyst_node,
    energy_analyst_node,
    automobile_analyst_node,
    merge_stocks_node
)
from ..agents.market_data import market_data_node
from ..agents.stock_analysis import stock_analysis_node
from ..agents.summary_agent import summary_agent_node

def build_workflow() -> StateGraph:
    """Builds and compiles the FinAnalyst AI LangGraph workflow."""
    print("Building LangGraph Workflow...")
    
    # Initialize the graph with our state schema
    workflow = StateGraph(WorkflowState)
    
    # Add all nodes
    workflow.add_node("news_collector", news_collector_node)
    workflow.add_node("news_impact", news_impact_node)
    
    # Parallel Sector Analysts
    workflow.add_node("tech_analyst", technology_analyst_node)
    workflow.add_node("banking_analyst", banking_analyst_node)
    workflow.add_node("energy_analyst", energy_analyst_node)
    workflow.add_node("auto_analyst", automobile_analyst_node)
    
    workflow.add_node("merge_stocks", merge_stocks_node)
    workflow.add_node("market_data", market_data_node)
    workflow.add_node("stock_analysis", stock_analysis_node)
    workflow.add_node("summary_agent", summary_agent_node)
    
    # Define Edges
    workflow.set_entry_point("news_collector")
    workflow.add_edge("news_collector", "news_impact")
    
    # From Impact, fan out to Sector Analysts in parallel
    workflow.add_edge("news_impact", "tech_analyst")
    workflow.add_edge("news_impact", "banking_analyst")
    workflow.add_edge("news_impact", "energy_analyst")
    workflow.add_edge("news_impact", "auto_analyst")
    
    # From Sector Analysts, fan in to Merge Stocks
    workflow.add_edge("tech_analyst", "merge_stocks")
    workflow.add_edge("banking_analyst", "merge_stocks")
    workflow.add_edge("energy_analyst", "merge_stocks")
    workflow.add_edge("auto_analyst", "merge_stocks")
    
    # Continue pipeline
    workflow.add_edge("merge_stocks", "market_data")
    workflow.add_edge("market_data", "stock_analysis")
    workflow.add_edge("stock_analysis", "summary_agent")
    
    # End node
    workflow.add_edge("summary_agent", END)
    
    # Compile the graph
    app = workflow.compile()
    return app

# Expose a compiled instance
app = build_workflow()

async def run_pipeline():
    """Runs the FinAnalyst AI workflow and returns the final state."""
    
    initial_state = {
        "news_articles": [],
        "impactful_news": [],
        "sector_analysis": {},
        "stocks_identified": [],
        "market_data": {},
        "stock_analysis": {},
        "final_report": ""
    }

    final_state = None

    async for step in app.astream(initial_state):
        final_state = step

    return final_state
