import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

def load_pdf(path: str) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def load_txt(path: str) -> str:
    """Extract text from a plain text file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def ingest(file_path: str):
    """Process a file and store embeddings in FAISS."""

    # Step 1 — Load the file
    print("Loading file...")
    if file_path.endswith(".pdf"):
        text = load_pdf(file_path)
    else:
        text = load_txt(file_path)

    # Step 2 — Split into chunks
    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # each chunk = 1000 characters
        chunk_overlap=200     # 200 character overlap between chunks
                              # so context isn't lost at boundaries
    )
    chunks = splitter.split_text(text)
    print(f"Created {len(chunks)} chunks")

    # Step 3 — Create embeddings and store in FAISS
    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(chunks, embeddings)

    # Step 4 — Save to disk
    vector_store.save_local("faiss_index")
    print("Done! Vector store saved to faiss_index/")

if __name__ == "__main__":
    # Change this to your actual notes file
    ingest("notes.pdf")