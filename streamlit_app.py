import streamlit as st
import requests
import uuid

st.title("Document QA System")
session_id = st.session_state.get("session_id", str(uuid.uuid4()))
st.session_state["session_id"] = session_id

if "doc_id" not in st.session_state:
    st.session_state.doc_id = ""

uploaded = st.file_uploader("Upload the document")
if uploaded:
    response = requests.post("http://localhost:8000/upload", files={"file": uploaded})
    st.session_state.doc_id = response.json()["document_id"]
    st.success(f"Uploaded as ID: {st.session_state.doc_id}")

query = st.text_input("Ask a question")
if query and st.session_state.doc_id:
    data = {"session_id": session_id, "question": query, "document_id": st.session_state.doc_id}
    response = requests.post("http://localhost:8000/query", data=data)
    res = response.json()
    st.write("**Answer:**", res["answer"])
    st.write("**Context:**", res["context"])