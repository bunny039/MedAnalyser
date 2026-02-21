"""
Medical Report Analyzer - Streamlit Frontend
Main application file for the Streamlit web interface
"""

import streamlit as st
import requests
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000/api"

# Page configuration
st.set_page_config(
    page_title="Medical Report Analyzer",
    page_icon="🏥",
    layout="wide"
)


def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    """Main application"""
    st.title("🏥 Medical Report Analyzer")
    st.markdown("AI-powered medical report analysis with RAG")
    
    # Check API connection
    if not check_api_health():
        st.warning("⚠️ API is not running. Please start the backend server.")
        st.code("uvicorn backend.app.main:app --reload", language="bash")
        return
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Upload", "Chat", "Query", "Summary"])
    
    if page == "Upload":
        show_upload_page()
    elif page == "Chat":
        show_chat_page()
    elif page == "Query":
        show_query_page()
    elif page == "Summary":
        show_summary_page()


def show_upload_page():
    """Upload medical documents"""
    st.header("📤 Upload Medical Reports")
    
    uploaded_file = st.file_uploader(
        "Choose a medical report file",
        type=['pdf', 'docx', 'txt', 'jpg', 'jpeg', 'png']
    )
    
    if uploaded_file is not None:
        st.write(f"**File:** {uploaded_file.name}")
        st.write(f"**Size:** {uploaded_file.size} bytes")
        
        if st.button("Upload Document"):
            with st.spinner("Uploading..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    response = requests.post(f"{API_BASE_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ Document uploaded successfully!")
                        st.json(result)
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


def show_chat_page():
    """Conversational interface"""
    st.header("💬 Chat with Medical Reports")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about your medical reports..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/chat",
                        json={"message": prompt}
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.markdown(result.get("response", "No response"))
                        st.session_state.messages.append(
                            {"role": "assistant", "content": result.get("response", "No response")}
                        )
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")


def show_query_page():
    """Query the medical reports"""
    st.header("🔍 Query Medical Reports")
    
    query = st.text_input("Enter your question about the medical reports:")
    
    if st.button("Search"):
        if query:
            with st.spinner("Searching..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/query",
                        json={"question": query}
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Found relevant information:")
                        st.markdown(result.get("answer", "No answer"))
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a question")


def show_summary_page():
    """Generate medical summary"""
    st.header("📋 Medical Report Summary")
    
    if st.button("Generate Summary"):
        with st.spinner("Generating summary..."):
            try:
                response = requests.post(f"{API_BASE_URL}/summary/generate")
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Summary generated:")
                    st.markdown(result.get("summary", "No summary"))
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
