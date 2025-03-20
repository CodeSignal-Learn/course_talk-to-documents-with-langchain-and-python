from document_processor import DocumentProcessor
from chat_engine import ChatEngine

class RAGChatbot:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.chat_engine = ChatEngine()
        
    def upload_document(self, file_path):
        """Upload and process a document"""
        try:
            self.document_processor.process_document(file_path)
            return f"Successfully processed document: {file_path}"
        except ValueError as e:
            return f"Error: {str(e)}"
        
    def send_message(self, message):
        """Send a message to the chatbot and get a response"""
        # Retrieve relevant context from documents
        relevant_docs = self.document_processor.retrieve_relevant_context(message)
        
        # If we have relevant documents, create context
        if relevant_docs:
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
        else:
            context = ""
            
        # Send the message with context to the chat engine
        return self.chat_engine.send_message(message, context)
        
    def reset_conversation(self):
        """Reset the conversation history"""
        return self.chat_engine.reset_conversation()
        
    def reset_documents(self):
        """Reset the document processor"""
        self.document_processor.reset()
        return "Document knowledge has been reset."
        
    def reset_all(self):
        """Reset both conversation and documents"""
        conv_reset = self.reset_conversation()
        doc_reset = self.reset_documents()
        return "Both conversation history and document knowledge have been reset."