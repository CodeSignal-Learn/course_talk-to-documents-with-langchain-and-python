from langchain_openai import ChatOpenAI
from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage

class ChatEngine:
    def __init__(self):
        self.chat_model = ChatOpenAI()
        self.conversation_history = []
        self.system_message = "You are a helpful assistant that answers questions based on the provided context."
        
    def send_message(self, user_message, context=""):
        """Send a message to the chat engine and get a response"""
        # Create messages list with system message and conversation history
        messages = [SystemMessage(content=self.system_message)]
        messages.extend(self.conversation_history)
        
        # Create the current message with context if available
        if context:
            formatted_message = f"""Answer based on this context:
            
            {context}
            
            Question: {user_message}"""
            current_message = HumanMessage(content=formatted_message)
        else:
            current_message = HumanMessage(content=user_message)
        
        # Add the current message to the messages list
        messages.append(current_message)
        
        # Get the response from the model
        response = self.chat_model.invoke(messages)
        
        # Add the exchange to conversation history
        self.conversation_history.append(HumanMessage(content=user_message))
        self.conversation_history.append(AIMessage(content=response.content))
        
        return response.content
        
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
        return "Conversation history has been reset."