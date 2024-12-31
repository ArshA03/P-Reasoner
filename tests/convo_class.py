# chatbot.py
from openai import OpenAI
from dotenv import load_dotenv
import os

class Chatbot:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv("env/.env")
        
        # Initialize OpenAI client
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("API_KEY"),
        )
        
        # Initialize conversation history
        self.conversation_history = []
        
    def add_message(self, role, content):
        """Add a message to the conversation history"""
        self.conversation_history.append({"role": role, "content": content})
        
    def get_response(self, user_input):
        """Get a response from the chatbot"""
        # Add user input to conversation history
        self.add_message("user", user_input)
        
        try:
            # Get completion from OpenAI
            completion = self.client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=self.conversation_history
            )
            
            # Get the assistant's response
            assistant_response = completion.choices[0].message.content
            
            # Add assistant's response to conversation history
            self.add_message("assistant", assistant_response)
            
            return assistant_response
            
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []


# test_chatbot.py
def test_chatbot():

    # Create chatbot instance
    bot = Chatbot()
    
    # Test simple conversation
    print("Test 1: Simple question and answer")
    response1 = bot.get_response("What is the meaning of life?")
    print(f"Bot: {response1}\n")
    
    # Test context awareness
    print("Test 2: Follow-up question")
    response2 = bot.get_response("Can you elaborate on that?")
    print(f"Bot: {response2}\n")
    
    # Test conversation history
    print("Test 3: Conversation history")
    print("History:", bot.conversation_history)
    print()
    
    # Test clearing history
    print("Test 4: Clearing history")
    bot.clear_history()
    print("History after clearing:", bot.conversation_history)
    print()
    
    # Test new conversation after clearing
    print("Test 5: New conversation after clearing")
    response3 = bot.get_response("Hello, who are you?")
    print(f"Bot: {response3}")

if __name__ == "__main__":
    test_chatbot()
