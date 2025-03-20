import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import uvicorn
from rag_chatbot import RAGChatbot

app = FastAPI(title="RAG Chatbot API")

# Initialize the RAG chatbot
chatbot = RAGChatbot()

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str

@app.post("/upload", response_model=dict)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            # Write the uploaded file content to the temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Process the document
            result = chatbot.upload_document(temp_file_path)
            return {"status": "success", "message": result}
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """Send a message to the chatbot and get a response"""
    try:
        response = chatbot.send_message(request.message)
        return MessageResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.post("/reset/chat", response_model=dict)
async def reset_chat():
    """Reset the conversation history"""
    try:
        result = chatbot.reset_conversation()
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting chat: {str(e)}")

@app.post("/reset/documents", response_model=dict)
async def reset_documents():
    """Reset the document knowledge"""
    try:
        result = chatbot.reset_documents()
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting documents: {str(e)}")

@app.post("/reset/all", response_model=dict)
async def reset_all():
    """Reset both conversation history and document knowledge"""
    try:
        result = chatbot.reset_all()
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting all: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)