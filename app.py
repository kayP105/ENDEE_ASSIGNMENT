import os
import streamlit as st
from backend.ingest import ingest_file
from backend.semantic_search import semantic_search
from backend.rag import generate_answer
import streamlit as st
from backend.endee_client import get_index

if "index_initialized" not in st.session_state:
    get_index()
    st.session_state.index_initialized = True

UPLOAD_DIR = "data/sample_docs"

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["txt", "pdf"]
)

if uploaded_file:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    ingest_file(file_path)
    st.success(f"Document '{uploaded_file.name}' ingested successfully")



query = st.text_input("Ask a question")

mode = st.radio("Mode", ["Semantic Search", "RAG"])

if st.button("Run"):
    if mode == "Semantic Search":
        results = semantic_search(query)

        st.subheader("Retrieved Context")
        for r in results:
            meta = r["meta"]
            st.markdown(f"""
**Confidence:** {r["confidence"]}% 
**Source:** `{meta['source']}`  
**Page:** {meta['page']}

{meta['text']}
---
""")

    elif mode == "RAG":
        with st.spinner("Generating answer using local LLM..."):
            results = semantic_search(query,top_k=3)
            answer = generate_answer(query, results)
        
        avg_confidence = round(
            sum(r["confidence"] for r in results) / len(results), 2
        )
        st.subheader("Answer")
        st.progress(avg_confidence / 100)
        st.write(answer)

        st.subheader("Sources")
        for r in results:
            meta = r["meta"]
            st.markdown(
                f"- `{meta['source']}`, page {meta['page']}"
            )
