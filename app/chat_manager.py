from document_processor import DocumentProcessor
from chat_engine import ChatEngine
from langchain.schema.messages import HumanMessage, AIMessage

class ChatManager:
    """
    Manages the chat session, document processing, and conversation history.
    Acts as the main interface between the application and the chat functionality.
    """
    
    def __init__(self):
        """
        Initialize a new chat session with empty state.
        Sets up document processor and chat engine without any loaded documents.
        """
        self.processor = DocumentProcessor()  # Handles document processing
        self.vectorstore = None  # Stores document embeddings when loaded
        self.chat_engine = ChatEngine()  # Handles conversation with AI
        self.chat_history = []  # Stores conversation as LangChain messages
        
    def _update_chat_engine(self):
        """
        Updates the chat engine with the current vector store.
        Called after document uploads to enable document-aware conversations.
        """
        self.chat_engine = ChatEngine(self.vectorstore)
        
    def upload_document(self, file_path):
        """
        Process and load a new document for context-aware conversations.
        
        Args:
            file_path: Path to the document to process
            
        Returns:
            Dictionary containing the status of the upload
        """
        # Process document and get its vector store
        self.processor.process_file(file_path)
        self.vectorstore = self.processor.get_vectorstore()
        
        # Update chat engine to use new document context
        self._update_chat_engine()
        return {"status": "Document processed successfully."}
        
    def send_message(self, user_message):
        """
        Send a message to the AI and get its response.
        
        Args:
            user_message: The user's question or message
            
        Returns:
            AI generated response as a string
        """
        # Get AI response using current context and history
        ai_response = self.chat_engine.generate_response(user_message, self.chat_history)
        
        # Add the exchange to chat history as LangChain messages
        self.chat_history.extend([
            HumanMessage(content=user_message),
            AIMessage(content=ai_response)
        ])
        return ai_response
        
    def reset_session(self):
        """
        Reset the chat session to its initial state.
        Clears loaded documents, conversation history, and reinitializes components.
        
        Returns:
            Dictionary containing the status of the reset
        """
        self.vectorstore = None
        self.chat_engine = ChatEngine()
        self.processor = DocumentProcessor()
        self.chat_history = []
        return {"status": "Chat session has been reset."}