import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

FASTAPI_URL = f"http://{os.getenv('FASTAPI_HOST', '127.0.0.1')}:{os.getenv('FASTAPI_PORT', '8000')}"

st.set_page_config(
    page_title="Llama Document Extraction",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Llama Document Extraction")
st.markdown("Upload a document (PDF or CSV) and extract data using Llama3:8b")

with st.sidebar:
    st.header("⚙️ Configuration")

    try:
        health_response = requests.get(f"{FASTAPI_URL}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            st.success(f" Connected to API")
            st.info(f"Model: {health_data.get('model', 'N/A')}")
        else:
            st.error(" API not responding")
    except Exception as e:
        st.error(f" Cannot connect to API")
        st.caption(f"Make sure the backend is running at {FASTAPI_URL}")

    st.divider()
    st.markdown("""
    ### How to use:
    1. Upload a PDF or CSV file
    2. Enter your extraction query (optional)
    3. Click 'Extract Data'
    4. View the results
    """)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "csv"],
        help="Upload a PDF or CSV file for data extraction"
    )

    if uploaded_file:
        st.success(f"File uploaded: {uploaded_file.name}")
        st.caption(f"File size: {uploaded_file.size / 1024:.2f} KB")

with col2:
    st.subheader("Extraction Query")
    query = st.text_area(
        "What do you want to extract?",
        placeholder="e.g., Extract all names, dates, and amounts from this document",
        help="Describe what information you want to extract. Leave empty for general summarization.",
        height=100
    )

    st.caption(" Be specific about what data you need")

st.divider()

if st.button(" Extract Data", type="primary", use_container_width=True):
    if not uploaded_file:
        st.error("Please upload a file first!")
    else:
        with st.spinner("Processing document with Llama3:8b..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {"query": query} if query else {}

                response = requests.post(
                    f"{FASTAPI_URL}/extract",
                    files=files,
                    data=data,
                    timeout=120
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success(" Extraction complete!")

                    st.subheader(" Extraction Results")
                    st.markdown(result["extraction"])

                    with st.expander(" Document Preview"):
                        st.text(result.get("document_preview", "No preview available"))

                    with st.expander("ℹ Request Details"):
                        st.json({
                            "filename": result.get("filename"),
                            "file_type": result.get("file_type"),
                            "query": result.get("query")
                        })
                else:
                    error_data = response.json()
                    st.error(f"Error: {error_data.get('error', 'Unknown error')}")

            except requests.exceptions.Timeout:
                st.error("Request timed out. The document might be too large or complex.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.divider()

with st.expander(" Example Use Cases"):
    st.markdown("""
    ### CSV Files:
    - Extract specific columns or rows
    - Summarize statistical data
    - Find patterns or anomalies
    - Convert data into natural language

    ### PDF Files:
    - Extract contact information
    - Summarize document content
    - Find specific clauses or terms
    - Extract tables and structured data
    """)
