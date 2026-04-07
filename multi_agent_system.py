import os
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

# Define the Shared State Schema
class TravelState(TypedDict):
    destination: str          # User input
    duration: int             # User input (number of days)
    budget_range: str         # User input (e.g. "budget", "mid-range", "luxury")
    research_notes: str       # Filled by Researcher Agent
    itinerary: str            # Filled by Itinerary Planner Agent
    budget_breakdown: str     # Filled by Budget Estimator Agent
    final_plan: str           # Filled by Summarizer Agent

# Configure LLM
# Load API keys from .env file (never hardcode secrets in source code!)
from dotenv import load_dotenv
load_dotenv()

# Using llama-3.3-70b-versatile via Groq (free tier, very fast)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

def researcher_agent(state: TravelState) -> dict:
    """
    Agent Role: Researcher Agent
    Responsibility: Gathers destination info, climate, culture, visa, safety tips
    """
    prompt = ChatPromptTemplate.from_template("""
    You are a travel research expert.
    Research the destination: {destination}
    Trip duration: {duration} days
    
    Provide:
    - Best time to visit / current climate
    - Top 5 must-know cultural tips
    - Visa requirements (general)
    - Safety rating and key precautions
    
    Be concise and factual.
    """)
    chain = prompt | llm
    result = chain.invoke({
        "destination": state["destination"],
        "duration": state["duration"]
    })
    
    # Returns partial state update
    return {"research_notes": result.content}

def itinerary_planner_agent(state: TravelState) -> dict:
    """
    Agent Role: Itinerary Planner Agent
    Responsibility: Plans day-by-day activities based on research
    """
    prompt = ChatPromptTemplate.from_template("""
    You are a travel itinerary expert. 
    Using the research notes provided, create a detailed {duration}-day itinerary for {destination}. 
    List morning, afternoon, and evening activities for each day.
    
    Research Notes:
    {research_notes}
    """)
    chain = prompt | llm
    result = chain.invoke({
        "destination": state["destination"],
        "duration": state["duration"],
        "research_notes": state["research_notes"]
    })
    
    # Returns partial state update
    return {"itinerary": result.content}

def budget_estimator_agent(state: TravelState) -> dict:
    """
    Agent Role: Budget Estimator Agent
    Responsibility: Estimates cost breakdown for flights, hotels, food, etc.
    """
    prompt = ChatPromptTemplate.from_template("""
    You are a travel finance expert. 
    Based on the itinerary and a '{budget_range}' budget level, estimate daily costs for: 
    accommodation, food, transport, and activities. 
    Give a total estimated trip cost in USD.
    
    Destination: {destination}
    Duration: {duration} days
    
    Itinerary:
    {itinerary}
    """)
    chain = prompt | llm
    result = chain.invoke({
        "budget_range": state["budget_range"],
        "destination": state["destination"],
        "duration": state["duration"],
        "itinerary": state["itinerary"]
    })
    
    # Returns partial state update
    return {"budget_breakdown": result.content}

def summarizer_agent(state: TravelState) -> dict:
    """
    Agent Role: Summarizer Agent
    Responsibility: Compiles everything into a clean presentation
    """
    prompt = ChatPromptTemplate.from_template("""
    You are a travel consultant. Compile the research notes, itinerary, and budget breakdown 
    into one clean, well-formatted travel plan a tourist can print and carry.
    Use emojis and sections to make it look professional and readable.
    
    Destination: {destination}
    Duration: {duration} days
    Budget Range: {budget_range}
    
    Research Notes:
    {research_notes}
    
    Itinerary:
    {itinerary}
    
    Budget:
    {budget_breakdown}
    """)
    chain = prompt | llm
    result = chain.invoke({
        "destination": state["destination"],
        "duration": state["duration"],
        "budget_range": state["budget_range"],
        "research_notes": state["research_notes"],
        "itinerary": state["itinerary"],
        "budget_breakdown": state["budget_breakdown"]
    })
    
    # Returns partial state update
    return {"final_plan": result.content}

def build_graph():
    """
    Constructs the StateGraph with explicitly named nodes and edges mapping 
    the sequential control flow: Researcher -> Planner -> Budget -> Summarizer -> End
    """
    graph = StateGraph(TravelState)

    # 1. Add nodes
    graph.add_node("researcher",  researcher_agent)
    graph.add_node("planner",     itinerary_planner_agent)
    graph.add_node("budget",      budget_estimator_agent)
    graph.add_node("summarizer",  summarizer_agent)

    # 2. Define edges (sequential flow)
    graph.set_entry_point("researcher")
    graph.add_edge("researcher", "planner")
    graph.add_edge("planner",    "budget")
    graph.add_edge("budget",     "summarizer")
    graph.add_edge("summarizer", END)

    # Compile the graph
    return graph.compile()

def main():
    print("=== 🌍 AI Travel Planner Component Initialization ===\n")
    
    if not os.environ.get("GROQ_API_KEY"):
        print("⚠️  Warning: GROQ_API_KEY environment variable not set.")
        print("Please export GROQ_API_KEY='your-key' before running.")
        return

    destination    = input("Enter your destination (e.g. Paris, Tokyo, Delhi): ")
    duration_input = input("How many days will you travel? (e.g. 5): ")
    budget_range   = input("Budget range — type exactly one of [budget / mid-range / luxury]: ")
    
    try:
        duration = int(duration_input)
    except ValueError:
        print("Invalid duration, defaulting to 3 days.")
        duration = 3

    # Initialize state with user inputs and empty fields
    initial_state: TravelState = {
        "destination":     destination,
        "duration":        duration,
        "budget_range":    budget_range,
        "research_notes":  "",
        "itinerary":       "",
        "budget_breakdown": "",
        "final_plan":      ""
    }

    print("\n⏳ Running agents (Researcher -> Planner -> Budget -> Summarizer)...\n")
    
    # Build and invoke graph
    app = build_graph()
    final_state = app.invoke(initial_state)

    # Display final professional output
    print("=" * 60)
    print("✅ YOUR TRAVEL PLAN")
    print("=" * 60)
    print(final_state["final_plan"])

if __name__ == "__main__":
    main()
