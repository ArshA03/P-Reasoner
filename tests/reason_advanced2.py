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

        
    def analyze_input(self, user_input):
        """Analyze the input to determine the appropriate reasoning approach"""
        analysis_prompt = f"""Analyze this input and help me determine:
        1. Is this a question or a conversational statement?
        2. What is the complexity level (simple/medium/complex)?
        3. What type of reasoning steps would be most appropriate?
        4. What different perspectives should be considered?
        5. List the suggested reasoning steps in order.

        Format your response as JSON:
        {{
            "is_question": true/false,
            "complexity": "simple/medium/complex",
            "reasoning_type": "logical/analytical/creative/etc",
            "perspectives": ["perspective1", "perspective2", ...],
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

    def generate_critical_analysis(self, original_response, perspectives):
        """Generate critical analysis and alternative viewpoints"""
        critical_prompt = f"""Given this initial response:
        {original_response}

        Please analyze it critically from different perspectives:

        1. Challenge the assumptions in the response
        2. Consider alternative viewpoints
        3. Identify potential biases or limitations
        4. Explore counter-arguments
        5. Consider edge cases or exceptions

        For each of these perspectives:
        {', '.join(perspectives)}

        Format your response to include:
        - Critical Analysis:
        - Alternative Viewpoints:
        - Potential Limitations:
        - Counter-Arguments:
        - Synthesis of Different Perspectives:
        """

        self.add_message("user", critical_prompt)
        completion = self.client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=self.conversation_history[-1:]
        )
        return completion.choices[0].message.content

    def synthesize_final_response(self, original_response, critical_analysis):
        """Synthesize a final response incorporating all perspectives"""
        synthesis_prompt = f"""Now, create a comprehensive final response that:

        1. Integrates the initial analysis:
        {original_response}

        2. Incorporates the critical perspectives:
        {critical_analysis}

        The final response should:
        - Present a balanced view of the topic
        - Acknowledge different perspectives
        - Address potential counter-arguments
        - Provide a nuanced conclusion
        - Maintain intellectual honesty about uncertainties or limitations

        Format the response in a clear, engaging, and well-structured manner."""

        self.add_message("user", synthesis_prompt)
        completion = self.client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=self.conversation_history[-1:]
        )
        return completion.choices[0].message.content

    def multi_agent_response(self, user_input):
        """Enhanced reasoning process with critical analysis"""
        # First, analyze the input
        analysis = self.analyze_input(user_input)
        
        if not analysis:
            return self.get_response(user_input)
        
        # For simple conversational statements, use basic response
        if not analysis["is_question"] and analysis["complexity"] == "simple":
            return self.get_response(user_input)
        
        # Execute initial reasoning steps
        responses = []
        context = user_input
        
        for step in analysis["steps"]:
            step_response = self.execute_reasoning_step(step, context)
            responses.append(step_response)
            context = f"{context}\n\nStep Result: {step_response}"
        
        # Generate initial synthesis
        initial_synthesis = f"""Based on the analysis steps:
        {'\n'.join(f'Step {i+1}: {resp}' for i, resp in enumerate(responses))}
        """
        
        # Generate critical analysis from different perspectives
        critical_analysis = self.generate_critical_analysis(
            initial_synthesis, 
            analysis.get("perspectives", ["general"])
        )
        
        # Generate final response
        final_response = self.synthesize_final_response(
            initial_synthesis,
            critical_analysis
        )
        
        return final_response
    
    

def test_critical_reasoning():
    bot = Chatbot()
    bot.reasoning_enabled = True

    test_cases = [
        {
            "category": "Controversial Topic",
            "input": "Should artificial intelligence be regulated?",
            "description": "Tests handling of complex policy questions"
        },
        {
            "category": "Scientific Analysis",
            "input": "What are the best solutions for climate change?",
            "description": "Tests handling of complex scientific issues"
        },
        {
            "category": "Ethical Dilemma",
            "input": "Is genetic engineering of humans ethical?",
            "description": "Tests handling of ethical considerations"
        },
        {
            "category": "Economic Analysis",
            "input": "What would be the impact of implementing universal basic income?",
            "description": "Tests handling of complex economic scenarios"
        },
        {
            "category": "Social Issue",
            "input": "How can we address income inequality in modern societies?",
            "description": "Tests handling of complex social issues"
        }
    ]

    for case in test_cases:
        print("\n" + "="*80)
        print(f"Test Category: {case['category']}")
        print(f"Input: {case['input']}")
        print(f"Description: {case['description']}")
        print("="*80 + "\n")

        response = bot.process_input(case['input'])
        
        print("Response:")
        print(response)

        print("\n" + "-"*80 + "\n")
        
        # Clear history for next test
        bot.clear_history()

if __name__ == "__main__":
    test_critical_reasoning()