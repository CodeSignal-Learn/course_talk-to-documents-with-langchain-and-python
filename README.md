# Talk to Documents with LangChain and Python

A powerful document chat application that allows you to have natural conversations with your documents using RAG (Retrieval Augmented Generation) and LangChain. Provides a REST API built with Flask.

## Features

- 📄 Support for PDF and TXT documents
- 💬 Natural conversation with documents
- 🧠 Smart context retrieval using vector similarity
- 🔄 Maintains conversation history
- 🤖 Works with or without document context
- 📎 Multiple document support
- 🌐 REST API interface

## How it Works

The application uses three main components:

1. **DocumentProcessor**: Handles document ingestion and processing
   - Loads PDF and TXT files
   - Splits documents into manageable chunks
   - Creates vector embeddings using OpenAI
   - Stores embeddings in a FAISS vector store

2. **ChatEngine**: Manages the conversation with the AI
   - Retrieves relevant document context for each question
   - Maintains conversation history
   - Generates contextual responses using OpenAI

3. **ChatManager**: Orchestrates the entire process
   - Manages document uploads
   - Handles chat sessions
   - Maintains conversation state

## Requirements

- Python 3.8+
- OpenAI API key

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/CodeSignal-Learn/course_talk-to-documents-with-langchain-and-python
   cd course_talk-to-documents-with-langchain-and-python
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

4. Start the server:
   ```bash
   cd app
   python main.py
   ```
   The Flask server will start on port 3000 (http://localhost:3000)

## API Endpoints

### Upload Document
```http
POST /upload
Content-Type: multipart/form-data

file: <document_file>
```
Upload a PDF or TXT file for processing.

**Response**:
```json
{
    "message": "File 'document.pdf' uploaded and processed successfully.",
    "result": {
        "status": "Document processed successfully."
    }
}
```

### Send Message
```http
POST /message
Content-Type: application/json

{
    "message": "What is the main topic of the document?"
}
```
Send a message to chat with the uploaded documents.

**Response**:
```json
{
    "response": "Based on the document content, the main topic is..."
}
```

### Reset Session
```http
POST /reset
```
Reset the chat session, clearing conversation history and loaded documents.

**Response**:
```json
{
    "message": "Chat session has been reset.",
    "result": {
        "status": "Chat session has been reset."
    }
}
```

## Error Responses
The API may return the following error responses:

```json
{
    "error": "No file part in request"
}
```
```json
{
    "error": "No file selected"
}
```
```json
{
    "error": "No message provided"
}
```
