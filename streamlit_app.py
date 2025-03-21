import streamlit as st
import requests
import json

API_KEY = st.secrets["api"]["key"]


# Configure page
st.set_page_config(layout="wide")

# Store chat history and states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "filters_toggle" not in st.session_state:
    st.session_state.filters_toggle = False

# Dynamic title positioning
if not st.session_state.messages:
    st.title("BOEING RAG APPLICATION")
    st.markdown("<div style='height: 50vh'></div>", unsafe_allow_html=True)  # Vertical centering
else:
    st.title("BOEING RAG APPLICATION")

# Display chat history
for message in st.session_state.messages:
    role, content = message
    with st.chat_message(role):
        st.markdown(content)

# Bottom container for input and filters
input_container = st.container()
with input_container:
    col1, col2 = st.columns([6, 1])
    
    with col1:
        # Chat input with enter submission
        user_input = st.chat_input("Ask a question:", key="input")
    
    # Modify the toggle section in your code:
    with col2:
        # Use a unique key and session state binding
        filters_enabled = st.toggle(
            "Advanced filter",
            value=st.session_state.get("filters_toggle", False),
            key="unique_filter_toggle_key",  # Add this line
            on_change=lambda: st.session_state.update(filters_toggle=not st.session_state.filters_toggle)
        )


# Show advanced filters when toggled
if st.session_state.filters_toggle:
    with st.expander("FILTER OPTIONS", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            department = st.selectbox(
                "Department",
                options=["General", "Documentation", "Engineering", "Public relations"],
                index=0,
                key="department"
            )
        with cols[1]:
            date_range = st.selectbox(
                "Date",
                options=["All time history", "Last 7 days", "Last 2 weeks", "Last month", 
                        "Last quarter", "Last year", "Before a year"],
                index=0,
                key="date_range"
            )
else:
    # Reset to defaults when filters are closed
    st.session_state.department = "General"
    st.session_state.date_range = "All time history"


# API handling
API_URL = "https://payload.vextapp.com/hook/WDEO5O6S2U/catch/hello"


if user_input:
    # Store filter state before resetting
    st.session_state.last_filter_enabled = st.session_state.filters_toggle
    st.session_state.messages.append(("user", user_input))
    st.session_state.filters_toggle = False
    st.rerun()

# Process after rerun when message exists
if st.session_state.messages and st.session_state.messages[-1][0] == "user":
    last_user_message = st.session_state.messages[-1][1]
    
    # Prepare API payload
    payload = {
        "payload": last_user_message,
        "env": "dev",
        "custom_variables": {
            "Date": "",
            "Department": ""
        }
    }

    if st.session_state.get("last_filter_enabled", False):
        payload["custom_variables"].update({
            "Date": st.session_state.date_range,
            "Department": st.session_state.department
        })
    
    # Call API
    headers = {
        "Content-Type": "application/json",
        "Apikey": f"Api-Key {API_KEY}"
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    
    # Process response
    if response.status_code == 200:
        try:
            response_data = response.json()
            response_text = response_data.get("text", "No response received.")
            
            # Process citations
            if "citation" in response_data:
                sources = []
                seen_files = set()
                
                # Use source_deduplicate for unique files
                for source in response_data["citation"].get("source_deduplicate", []):
                    source_url = source.get("source_url", "")
                    source_name = source.get("source_name", "Unnamed Source")
                    
                    # Skip metadata files and duplicates
                    if source_name.lower() == "metadata" or source_name.lower() in seen_files:
                        continue
                    seen_files.add(source_name.lower())
                    
                    # Format source prefix
                    if "drive.google.com" in source_url or "docs.google.com" in source_url:
                        source_prefix = "Google-Drive"
                    elif "googleapis.com" in source_url:
                        source_prefix = "VectorStore"
                    else:
                        source_prefix = "Other"
                    
                    sources.append(f"{source_prefix}/{source_name}")
                
                # Add new lines between sources
                if sources:
                    response_text += "\n\n" + "\n\n".join([f"Source: {s}" for s in sources])


                    
        except json.JSONDecodeError:
            response_text = response.text
    else:
        response_text = f"Error: API request failed ({response.status_code})"
    
    # Append bot response
    st.session_state.messages.append(("assistant", response_text))
    st.rerun()
