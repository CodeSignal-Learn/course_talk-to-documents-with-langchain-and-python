from langchain_openai import ChatOpenAI
from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage

class ChatEngine:
    """
    Handles the conversation with the AI model, including document-based (RAG) and general conversations.
    Manages both document retrieval and chat functionality in a unified interface.
    """
    
    def __init__(self, vectorstore=None, k=3):
        """
        Initialize the chat engine with optional document context support.
        
        Args:
            vectorstore: Vector store containing document embeddings for similarity search
            k: Number of relevant document chunks to retrieve for each query
        """
        self.vectorstore = vectorstore  # Store for document embeddings
        self.k = k  # Number of relevant chunks to retrieve
        self.chat_model = ChatOpenAI()  # Language model for generating responses
        self.base_system_prompt = "You are a helpful AI assistant. "  # Default personality
        
    def _get_relevant_context(self, query):
        """
        Retrieve relevant document context for a given query using similarity search.
        
        Args:
            query: User's question to find relevant document chunks for
            
        Returns:
            Formatted string containing relevant context and the original query
        """
        if not self.vectorstore:
            return ""
            
        # Get most relevant document chunks
        context_docs = self.vectorstore.similarity_search(query, k=self.k)
        # Combine all chunks into a single context string
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        # Format context and query together
        return f"Use this context to answer the question:\n{context_text}\n\nQuestion: {query}"

    def generate_response(self, user_message, chat_history=[]):
        """
        Generate an AI response based on the user's message, chat history, and document context if available.
        The response will be informed by:
        1. Previous conversation history
        2. Relevant document context (if documents are loaded)
        3. The current user message
        
        Args:
            user_message: Current user's message or question
            chat_history: List of previous HumanMessage and AIMessage objects
            
        Returns:
            AI generated response as a string
        """
        # Combine system prompt with existing conversation history
        messages = [SystemMessage(content=self.base_system_prompt)] + chat_history
        
        # Prepare the current message with document context if available
        if self.vectorstore:
            # If we have documents loaded, include relevant context
            current_message = self._get_relevant_context(user_message)
        else:
            # If no documents are loaded, use the message as is
            current_message = user_message
            
        messages.append(HumanMessage(content=current_message))
        
        # Get AI response based on all messages
        response = self.chat_model.invoke(messages)
        return response.content