import os
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from retriever import retrieve
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# ---- Tool ----
@tool
def search_notes(query: str) -> str:
    """Searches the user's personal notes for relevant information.
    Use this whenever the user asks a question about their notes,
    wants an explanation, or asks to be quizzed on a topic."""
    return retrieve(query)

# ---- LLM ----
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# ---- Agent ----
tools = [search_notes]
agent_executor = create_react_agent(llm, tools)

def ask(question: str) -> str:
    result = agent_executor.invoke({
        "messages": [("human", f"""
        You are a helpful study assistant. The user has uploaded their personal 
        notes. Use the search_notes tool to find relevant information, then 
        answer the question clearly and helpfully.
        
        Always base your answer on the retrieved notes content.
        If the notes don't contain enough information, say so honestly.
        
        Question: {question}
        """)]
    })
    return result["messages"][-1].content

# ---- Test ----
if __name__ == "__main__":
    print(ask("Explain the main concepts in these notes"))