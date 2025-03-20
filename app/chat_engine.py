from langchain_openai import ChatOpenAI
from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate

class ChatEngine:
    def __init__(self):
        self.chat_model = ChatOpenAI()
        self.system_message = """You are a helpful assistant that answers questions based on the provided context.
        You should ONLY answer questions when context is provided. If no context is provided, respond with:
        "I cannot answer this question without context. Please provide relevant context first."
        """
        
        # Initialize conversation history with system message
        self.conversation_history = [SystemMessage(content=self.system_message)]
        
        # Define the prompt template using a simple string format
        self.prompt = ChatPromptTemplate.from_template(
            "Answer the following question based on the provided context.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}"
        )
        
    def send_message(self, user_message, context=""):
        """Send a message to the chat engine and get a response"""
        # Format the messages using the prompt template
        messages = self.prompt.format_messages(
            context=context,
            question=user_message
        )
        
        # Add the current message to the conversation history
        self.conversation_history.append(HumanMessage(content=user_message))
        
        # Get the response from the model
        response = self.chat_model.invoke(messages)
        
        # Add the response to conversation history
        self.conversation_history.append(AIMessage(content=response.content))
        
        return response.content
        
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = [SystemMessage(content=self.system_message)]
        return "Conversation history has been reset."