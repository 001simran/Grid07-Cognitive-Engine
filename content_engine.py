import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from agent_state import ContentState

load_dotenv()

# Initialize Gemini 1.5 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

@tool
def mock_searxng_search(query: str) -> str:
    """Mock search tool for recent news headlines."""
    query = query.lower()
    if "crypto" in query or "bitcoin" in query:
        return "Bitcoin hits new all-time high. Ethereum scaling adoption peaks."
    elif "ai" in query:
        return "OpenAI previewing GPT-5. Global AI regulation talks intensify."
    elif "market" in query:
        return "Fed signals potential rate cuts. Tech stocks rally."
    return "Global tech trends continue to evolve."

# --- Graph Nodes ---

def node_decide_search(state: ContentState):
    """LLM decides on a topic and search query based on persona."""
    persona = state["persona"]
    prompt = f"Persona: {persona}\n\nDecide on a trending topic and a search query. Return JSON: {{'topic': '...', 'search_query': '...'}}"
    
    response = llm.invoke([SystemMessage(content="You are a social media bot."), HumanMessage(content=prompt)])
    content = response.content
    
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    
    data = json.loads(content.strip())
    return {"topic": data["topic"], "search_query": data["search_query"]}

def node_web_search(state: ContentState):
    """Executes the search tool."""
    results = mock_searxng_search.invoke(state["search_query"])
    return {"search_results": results}

def node_draft_post(state: ContentState):
    """Generates the final 280-char opinionated post."""
    prompt = f"Persona: {state['persona']}\nTopic: {state['topic']}\nContext: {state['search_results']}\n\nDraft a 280-char post. Return JSON: {{'bot_id': '{state['bot_id']}', 'topic': '{state['topic']}', 'post_content': '...'}}"
    
    response = llm.invoke([SystemMessage(content="Professional content creator."), HumanMessage(content=prompt)])
    content = response.content
    
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    
    data = json.loads(content.strip())
    return {"post_content": data["post_content"], "json_output": data}

# --- Workflow Definition ---

builder = StateGraph(ContentState)

builder.add_node("decide_search", node_decide_search)
builder.add_node("web_search", node_web_search)
builder.add_node("draft_post", node_draft_post)

builder.set_entry_point("decide_search")
builder.add_edge("decide_search", "web_search")
builder.add_edge("web_search", "draft_post")
builder.add_edge("draft_post", END)

content_app = builder.compile()
