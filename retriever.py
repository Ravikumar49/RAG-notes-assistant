import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

def load_retriever():
    """Load the FAISS vector store from disk."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True  # required by LangChain for local files
    )
    return vector_store.as_retriever(search_kwargs={"k": 3})
    # k=3 means return the 3 most relevant chunks

def retrieve(query: str) -> str:
    """Search the vector store for relevant chunks."""
    retriever = load_retriever()
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found in your notes."

    # Combine all retrieved chunks into one string
    result = ""
    for i, doc in enumerate(docs):
        result += f"--- Chunk {i+1} ---\n{doc.page_content}\n\n"

    return result

# Test it
if __name__ == "__main__":
    query = "What is the main topic of these notes?"
    print(f"Query: {query}\n")
    print(retrieve(query))