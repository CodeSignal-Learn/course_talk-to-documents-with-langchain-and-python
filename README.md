# Talk to Documents with LangChain and Python

A powerful REST API chat application that allows you to have natural conversations with your documents using RAG (Retrieval Augmented Generation) and LangChain.

## How it Works

The application uses three main components:

1. **DocumentProcessor**: Handles document ingestion and processing
   - Loads PDF, TXT, and other unstructured files using appropriate loaders
   - Splits documents into chunks with configurable size and overlap
   - Creates vector embeddings using OpenAI's embedding model
   - Stores and manages embeddings in a FAISS vector store for efficient similarity search

2. **ChatEngine**: Manages the conversation with the AI
   - Uses OpenAI's chat model for generating responses
   - Maintains conversation history with system, human, and AI messages
   - Formats messages with context when available
   - Provides conversation reset functionality

3. **RAGChatbot**: Orchestrates the entire process
   - Coordinates between DocumentProcessor and ChatEngine
   - Handles document uploads and processing
   - Manages chat sessions and message flow
   - Provides independent control over chat and document states
   - Implements the core RAG (Retrieval Augmented Generation) logic

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
   The server will start on port 3000 (http://localhost:3000)

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
    "status": "success",
    "message": "Document processed successfully"
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

### Reset Chat
```http
POST /reset/chat
```
Reset only the conversation history while keeping the document knowledge.

**Response**:
```json
{
    "status": "success",
    "message": "Conversation history has been reset."
}
```

### Reset Documents
```http
POST /reset/documents
```
Reset only the document knowledge while keeping the conversation history.

**Response**:
```json
{
    "status": "success",
    "message": "Document knowledge has been reset."
}
```

### Reset All
```http
POST /reset/all
```
Reset both conversation history and document knowledge.

**Response**:
```json
{
    "status": "success",
    "message": "Both conversation history and document knowledge have been reset."
}
```