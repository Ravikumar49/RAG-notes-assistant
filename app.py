import streamlit as st
from ingest import ingest
from agent import ask
import os

st.set_page_config(
    page_title="RAG Notes Assistant",
    page_icon="📚",
    layout="centered"
)

st.title("📚 RAG Notes Assistant")
st.caption("Upload your notes and ask anything about them!")

# ---- File Upload ----
uploaded_file = st.file_uploader("Upload your notes (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    # Save uploaded file temporarily
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Only ingest if not already done
    if "ingested" not in st.session_state or st.session_state.ingested != uploaded_file.name:
        with st.spinner("Reading and indexing your notes..."):
            ingest(file_path)
            st.session_state.ingested = uploaded_file.name
        st.success("Notes indexed! You can now ask questions.")

    # ---- Question Input ----
    st.markdown("---")
    question = st.text_input("Ask a question about your notes",
                placeholder="e.g. Explain the main concepts")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Ask!", use_container_width=True):
            if question:
                with st.spinner("Thinking..."):
                    answer = ask(question)
                st.markdown("### Answer")
                if isinstance(answer, list):
                    st.markdown(answer[0]["text"])
                else:
                    st.markdown(answer)

    with col2:
        if st.button("Quiz Me!", use_container_width=True):
            with st.spinner("Generating quiz questions..."):
                answer = ask("Generate 3 quiz questions based on these notes with answers")
            st.markdown("### Quiz")
            if isinstance(answer, list):
                st.markdown(answer[0]["text"])