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

        self.agent_prompts = {
            "analyzer": "As an analytical agent, break down the question into key components:",
            "critic": "As a critical thinker, identify potential issues or considerations:",
            "synthesizer": "Based on the analysis and critique, provide a comprehensive response:"
        }
        
        # Initialize conversation history
        self.conversation_history = []

        self.reasoning_enabled = False  # Default state
        
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
                model="openai/gpt-3.5-turbo-instruct",
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


    def multi_agent_response(self, user_input):
        responses = []
        
        # Simulate multiple agents analyzing the problem
        for role, prompt in self.agent_prompts.items():
            full_prompt = f"{prompt}\n{user_input}"
            self.add_message("user", full_prompt)
            
            completion = self.client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=self.conversation_history[-1:],  # Only use the latest prompt
            )
            responses.append(completion.choices[0].message.content)
            
        # Combine all insights into final response
        final_prompt = f"""Based on these analyses:
        Analysis: {responses[0]}
        Critique: {responses[1]}
        
        Please provide a final, well-reasoned response."""
        
        self.add_message("user", final_prompt)
        final_completion = self.client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=self.conversation_history
        )
        return final_completion.choices[0].message.content

    def toggle_reasoning(self):
        """Toggle reasoning mode on/off"""
        self.reasoning_enabled = not self.reasoning_enabled
        return self.reasoning_enabled
        
    def process_input(self, user_input):
        """Process input based on reasoning mode"""
        if self.reasoning_enabled:
            return self.multi_agent_response(user_input)
        else:
            return self.get_response(user_input)

