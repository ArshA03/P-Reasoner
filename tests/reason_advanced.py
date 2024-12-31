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
        
    def analyze_input(self, user_input):
        """Analyze the input to determine the appropriate reasoning approach"""
        analysis_prompt = f"""Analyze this input and help me determine:
        1. Is this a question or a conversational statement?
        2. What is the complexity level (simple/medium/complex)?
        3. What type of reasoning steps would be most appropriate?
        4. List the suggested reasoning steps in order.

        Format your response as JSON:
        {{
            "is_question": true/false,
            "complexity": "simple/medium/complex",
            "reasoning_type": "logical/analytical/creative/etc",
            "steps": ["step1", "step2", ...]
        }}

        Input: "{user_input}" """
        
        self.add_message("user", analysis_prompt)
        completion = self.client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=self.conversation_history[-1:]
        )
        
        import json
        try:
            return json.loads(completion.choices[0].message.content)
        except:
            return None

    def execute_reasoning_step(self, step_prompt, context=""):
        """Execute a single reasoning step"""
        full_prompt = f"""Step Context: {context}

        Task: {step_prompt}

        Provide a clear and concise response that directly addresses this step."""
        
        self.add_message("user", full_prompt)
        completion = self.client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=self.conversation_history[-1:]
        )
        return completion.choices[0].message.content

    def multi_agent_response(self, user_input):
        """Enhanced reasoning process with dynamic self-prompting"""
        # First, analyze the input
        analysis = self.analyze_input(user_input)
        
        if not analysis:
            return self.get_response(user_input)  # Fallback to simple response
        
        # For simple conversational statements, use basic response
        if not analysis["is_question"] and analysis["complexity"] == "simple":
            return self.get_response(user_input)
        
        # For complex queries, execute each reasoning step
        responses = []
        context = user_input
        
        for step in analysis["steps"]:
            step_response = self.execute_reasoning_step(step, context)
            responses.append(step_response)
            context = f"{context}\n\nStep Result: {step_response}"
        
        # Generate final synthesis
        synthesis_prompt = f"""Based on all the analysis steps:

        Original Input: {user_input}

        Step Results:
        {'\n'.join(f'Step {i+1}: {resp}' for i, resp in enumerate(responses))}

        Please provide a final, comprehensive response that synthesizes all this information 
        in a clear and coherent way. Make sure to:
        1. Address the original input directly
        2. Incorporate insights from all steps
        3. Present the information logically
        4. Keep the tone appropriate for the context"""
        
        self.add_message("user", synthesis_prompt)
        final_completion = self.client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=self.conversation_history[-1:]
        )
        
        return final_completion.choices[0].message.content



def test_different_inputs():
    bot = Chatbot()
    bot.reasoning_enabled = True  # Enable reasoning mode
    
    # Test cases
    test_inputs = [
        # Simple conversation
        "Hello, how are you today?",
        
        # Simple question
        "What is the capital of France?",
        
        # Complex question
        "What are the potential implications of artificial intelligence on the job market in the next decade?",
        
        # Analysis request
        "Can you analyze the causes and effects of climate change?",
        
        # Opinion/creative request
        "What do you think about the future of space exploration?",
        
        # Problem-solving
        "How can we reduce plastic waste in oceans?"
    ]
    
    for input_text in test_inputs:
        print("\n" + "="*50)
        print(f"Testing Input: {input_text}")
        print("="*50)
        
        # Get response
        response = bot.process_input(input_text)
        print("\nResponse:")
        print(response)
        
        # Clear history for next test
        bot.clear_history()

if __name__ == "__main__":
    test_different_inputs()