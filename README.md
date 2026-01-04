# Boeing Internal Documentation RAG Application

A Streamlit-based web application that leverages Large Language Models (LLMs) to help Boeing employees search and retrieve information from internal documentation. This tool significantly reduces document search times by approximately 80%.

<img width="1440" height="900" alt="image" src="https://github.com/user-attachments/assets/a8e501f1-07b7-46ea-b331-2aa83a7409a0" />
<img width="1440" height="900" alt="image" src="https://github.com/user-attachments/assets/31acec9b-d5a9-43c1-969a-8f6374f2914c" />
<img width="1440" height="900" alt="image" src="https://github.com/user-attachments/assets/6ec9ed7f-970b-4878-8109-b12ac3e4add1" />



## Overview

This application provides an intuitive chat interface where employees can ask natural language questions about Boeing's internal documentation. The system uses Retrieval-Augmented Generation (RAG) to find relevant documents and generate accurate, contextual responses with proper source citations.

## Features

- **Natural Language Search**: Ask questions in plain English instead of using complex search queries
- **Chat Interface**: Conversational UI that maintains chat history within a session
- **Advanced Filtering**: Optional filters to narrow results by:
  - Department (General, Documentation, Engineering, Public Relations)
  - Date Range (Last 7 days, Last 2 weeks, Last month, Last quarter, Last year, etc.)
- **Source Citations**: Each response includes links to source documents from Google Drive or the VectorStore
- **Responsive Layout**: Wide layout design for comfortable reading and interaction

## Tech Stack

- **Frontend**: Streamlit
- **Backend API**: Vext API (payload.vextapp.com)
- **Language**: Python 3.x

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Vraj1234/Boeing-Internal-Documentation-Dynamic-RAG-Application.git
   cd Boeing-Internal-Documentation-Dynamic-RAG-Application
   ```

2. Install dependencies:
   ```bash
   pip install streamlit requests
   ```

3. Configure your API key by creating a `.streamlit/secrets.toml` file:
   ```toml
   [api]
   key = "your-api-key-here"
   ```

4. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

## Usage

1. Launch the application in your browser (typically at `http://localhost:8501`)
2. Type your question in the chat input at the bottom of the page
3. Optionally, enable "Advanced filter" to specify department and date range
4. Press Enter to submit your query
5. View the AI-generated response along with source citations

## Configuration

The application connects to a Vext API endpoint for RAG processing. The API payload includes:
- `payload`: The user's question
- `env`: Environment setting (defaults to "dev")
- `custom_variables`: Optional filters for Department and Date

## File Structure

```
Boeing-Internal-Documentation-Dynamic-RAG-Application/
├── streamlit_app.py    # Main application file
├── image.png           # Application screenshot/image
└── README.md           # This file
```

## API Response Handling

The application processes API responses to:
- Extract the generated text answer
- Parse and deduplicate source citations
- Identify source types (Google Drive, VectorStore, Other)
- Format sources for display with appropriate prefixes

## Contributing

For questions or contributions, please contact the repository maintainer.
