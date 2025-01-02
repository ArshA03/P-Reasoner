# chatbot.py
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os



assistant_prompt ="""You are a reasoning Assistant, designed to solve problems by following the guidance and supervision of Supervisor, another model responsible for overseeing your thought process. Your primary responsibilities include:

1. Structured Problem Solving

Adhere to Defined Steps: Follow the step-by-step procedures outlined by Supervisor to approach and resolve each problem systematically.
Problem Decomposition: Break down complex issues into smaller, manageable components as directed by Supervisor to facilitate thorough analysis.

2. Perspective Integration

Explore Alternative Viewpoints: Consider and analyze different perspectives or angles suggested by Supervisor to ensure a comprehensive understanding of the problem.
Balanced Analysis: Weigh various viewpoints objectively, presenting each with equal consideration and without bias.

3. Collaborative Reasoning

Implement Feedback: Actively incorporate feedback and suggestions from Supervisor to enhance the clarity, logic, and depth of your responses.
Maintain Open Communication: Engage constructively with Supervisor's guidance, seeking clarification when necessary to ensure alignment with supervisory expectations.

4. Neutrality and Objectivity

Avoid Assumptions: Do not presume any information or responses to be correct by default. Verify and validate all data and conclusions through logical reasoning.
Impartial Stance: Maintain an unbiased and objective approach in all analyses and solutions, ensuring that personal judgments do not influence outcomes.

5. Clear and Concise Communication

Structured Responses: Present your solutions in a well-organized manner, following the sequence and format recommended by Supervisor.
Clarity and Precision: Ensure that your explanations are clear, precise, and free from ambiguity, facilitating easy understanding and further supervision.

Guidelines:

- Follow Supervisory Guidance
    Always align your problem-solving approach with the steps, decompositions, and perspectives provided by Supervisor.
- Promote Comprehensive Analysis
    Strive to cover all aspects of the problem by considering multiple viewpoints and breaking down issues as instructed.
- Maintain Professionalism
    Uphold a respectful and cooperative demeanor in all interactions with Supervisor, valuing the supervisory role in enhancing your performance.
- Continuous Improvement
    Use feedback from Supervisor to refine your reasoning processes, aiming for increased accuracy, depth, and effectiveness in your solutions.

Objective:
Effectively solve problems by methodically following Supervisor's guidance to decompose issues, define actionable steps, and explore diverse perspectives. Strive for thorough, unbiased, and logically sound solutions through structured and collaborative reasoning, ensuring that all analyses are comprehensive and well-founded.
"""

supervisor_prompt = """You are a Supervisor, a large language model designed to oversee and guide the thought process of another model called Server. Your primary responsibilities include:
1. Problem Decomposition:
    Break Down Problems: Divide complex issues into smaller, manageable steps or components to facilitate thorough analysis.
2. Step Definition:
    Outline Procedures: Define and sequence the steps Server should follow to approach and solve the given problem systematically.
3. Perspective Expansion:
    Suggest Alternative Viewpoints: Identify and propose different perspectives or angles for Server to consider, ensuring a comprehensive examination of the problem.
4. Process Supervision:
    Monitor Reasoning: Assess Server's reasoning and responses, providing constructive feedback to enhance clarity, logic, and thoroughness without dictating solutions.

Guidelines:
    - Neutrality:
    Maintain an impartial and unbiased stance. Do not assume any of Server's responses are correct by default.
    - Reasonableness:
    Ensure all guidance and feedback are logical, practical, and aligned with effective problem-solving practices.
    - Non-Interventionist Approach:
    Do not provide direct answers or solutions. Focus solely on facilitating Server's independent reasoning and analysis.

Objective:
    Support Server in developing a structured, well-rounded approach to problem-solving by supervising its thought process effectively. Your role is to guide, not to decide; to suggest, not to conclude.

    You should always ask what could go wrong! Never assume an initial resposne is correct,and never rate the satsifaction or accuracy high in first reasoning step!
"""

class Chatbot:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv("env/.env")
        
        # Initialize OpenAI client
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("API_KEY"),
        )
        self.assistant_model = "anthropic/claude-3.5-haiku"
        self.supervisor_model = "openai/gpt-4o-mini"
        self.assistant_prompt = assistant_prompt
        self.supervisor_prompt = supervisor_prompt

        # Initialize conversation history and system prompt
        self.conversation_history = []
        self.conversation_history.append({"role": "system", "content": self.assistant_prompt})

        self.reasoning_history = []
        self.reasoning_history.append({"role": "system", "content": self.supervisor_prompt})

        self.reasoning_enabled = False  # Default state
        
    class SupervisorJSON(BaseModel):
        is_question: str
        complexity: str
        reasoning_type: str
        perspectives: list[str]
        steps: list[str]
        explanation: str

    class SupervisorRater(BaseModel):
        satisfaction: str
        accuracy: str
        instructions: str
        failure: bool

    def add_message_supervisor(self, role, content, name=None):
        """Add a message to the conversation history for supervisor"""
        self.reasoning_history.append({"role": role, "content": content}) if name is None else self.reasoning_history.append({"role": role, "name": name, "content": content})

    def add_message_assistant(self, role, content, name=None):
        """Add a message to the conversation history for assistant"""
        self.conversation_history.append({"role": role, "content": content}) if name is None else self.conversation_history.append({"role": role, "name": name, "content": content})
        
    def get_response(self, user_input):
        """Get a response from the chatbot"""
        # Add user input to conversation history
        self.add_message_assistant("user", user_input)
        
        try:
            # Get completion from OpenAI
            completion = self.client.chat.completions.create(
                model=self.assistant_model,
                messages=self.conversation_history
            )
            
            # Get the assistant's response
            assistant_response = completion.choices[0].message.content
            
            # Add assistant's response to conversation history
            self.add_message_assistant("assistant", assistant_response)
            
            return assistant_response
            
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        self.conversation_history.append({"role": "system", "content": self.assistant_prompt})

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
        
    def execute_reasoning_step(self, step_prompt):
        """Execute a single reasoning step"""
        # Track conversation history for this step
        prompt = f"""The supervisor suggests the follwing action for next step:
        {step_prompt}
        Provide a clear and concise response that directly addresses this step.
        """
        self.add_message_assistant("user", prompt)
        completion = self.client.chat.completions.create(
            model=self.assistant_model,
            messages=self.conversation_history
        )
        assistant_response = completion.choices[0].message.content
        self.add_message_assistant("assistant", assistant_response)

        return assistant_response
        
    def analyze_input(self, user_input):
        """Analyze the input to determine the appropriate reasoning approach"""

        supervisor_prompt = f"""Analyze the following input for the Server and determine:
        1. Is this a question or a conversational statement?
        2. What type of reasoning steps would be most appropriate?
        3. What different perspectives should be considered?
        4. List the suggested initial reasoning steps in order.
        5. Give extra explanation about the user prompt, inlcuding hat they ar asking exactly, and how it is usually answered. Do not try answering the prompt directly, rather analyze the user prompt carefully and explain how such prompt or quesion is usually answered, and break it into smaller parts.

        Format your response as JSON:
        {{
            "is_question": true/false,
            "complexity": "simple/medium/complex",
            "reasoning_type": "logical/analytical/creative/etc",
            "perspectives": ["perspective1", "perspective2", ...],
            "steps": ["step1", "step2", ...],
            "explanation": "extra explanation"
        }}

        --------------- The Server chat is as follows ---------------
        {'\n'.join(f'{msg["role"]}: "{msg["content"]}"' for msg in self.conversation_history[1:])}
        
        user: "{user_input}"
        """
        
        self.add_message_supervisor("user", supervisor_prompt)
        completion = self.client.beta.chat.completions.parse(
            model=self.supervisor_model,
            messages=self.reasoning_history,
            response_format=self.SupervisorJSON
        )

        supervisor_response = completion.choices[0].message
        
        return supervisor_response

    def generate_critical_analysis(self):
        """Generate critical analysis and alternative viewpoints"""

        critical_prompt = f"""Ther Server followed your suggested steps and came up with the responses below.

        Critically analyze the response. Provide a detailed analysis of the response, highlighting any logical flaws, assumptions, or missing information. Give actionable insights.

        Your output should be in the followinf JSON format:
        {{
            "satisfaction": "high/medium/low",
            "accuracy": "high/medium/low",
            "instructions": "detailed analysis and actionable instructions",
            "failure": true/false
        }}

        You should not acknowledge whether the respose is correct or not, but rather focus on the reasoning process and the clarity of the response.
        You should rate high in accuracy only if there is no way to challenge the response critically and every aspect is considered!
        Also only rate high in satisfaction if the response has shown a reasonable thought process, otherwise, if it is not clear how it was reached, rate low in satisfaction.
        Check the thought process and see if it is logically sound. There should be a thought process.
        Give exact instructions on how to improve the response and get a better rating on accuracy and satisfaction.

        If the server's response is not stil satisfying or accurate after 5 reasoning steps in the chat history, put the failure to true.
        --------------- The Server chat is as follows ---------------
        {'\n'.join(f'{msg["role"]}: "{msg["content"]}"' for msg in self.conversation_history[1:])}
        """
        
        self.reasoning_history.pop()
        self.add_message_supervisor("user", critical_prompt)
        completion = self.client.beta.chat.completions.parse(
            model=self.supervisor_model,
            messages=self.reasoning_history,
            response_format=self.SupervisorRater
        )

        supervisor_response = completion.choices[0].message.parsed

        return supervisor_response

    def reasoning_response(self, critical_analysis, steps):
        """Synthesize a final response incorporating all perspectives"""
        synthesis_prompt = f"""### Reasoning Step {steps}\nI reviewed your responses, here are your instructions:\n"{critical_analysis}"\nRefine your answer based on the review.

        Ask yourself, am i missing any important information? Are there any logical flaws in my reasoning? Have I considered all relevant perspectives? How can I improve the clarity and depth of my response?

        Format the response in a clear, succinct, and well-structured manner. Do not include unnecessary information. Be succinct and to the point. Keep it as short as possible, only give the required answer!
        Do not talk bout the supervision process.
        """

        self.add_message_assistant("user", synthesis_prompt, name="supervisor")
        completion = self.client.chat.completions.create(
            model=self.assistant_model,
            messages=self.conversation_history
        )
        assistant_prompt = completion.choices[0].message.content
        self.add_message_assistant("assistant", assistant_prompt)

    def multi_agent_response(self, user_input):
        """Enhanced reasoning process with critical analysis"""
        # First, analyze the input
        analysis = self.analyze_input(user_input)
        
        if analysis.refusal:
            # handle refusal
            return self.get_response(user_input)
        
        # Execute initial reasoning steps
        responses = []
        self.add_message_assistant("user", user_input)
        self.add_message_assistant("user", f"consider the guidance from the supervisor: {analysis.parsed.explanation}")
        
        for step in analysis.parsed.steps:
            step_response = self.execute_reasoning_step(step)
            responses.append(step_response)
        
        # Generate critical analysis from different perspectives

        steps = 0
        # critical_analysis = self.generate_critical_analysis()
        while True:
            steps += 1
            critical_analysis = self.generate_critical_analysis()
            if critical_analysis.accuracy == "high" and critical_analysis.satisfaction == "high":
                break
            elif critical_analysis.failure:
                print("Reasoning failed")
                break
            print("Step:", steps)
            print("Critical Analysis:", critical_analysis)
            self.reasoning_response(critical_analysis.instructions, steps)

        print(f"Critical analysis completed in {steps} steps")
        
        # Generate final response
        final_response = self.conversation_history[-1]["content"]
        
        return final_response



def test_critical_reasoning():
    bot = Chatbot()
    bot.reasoning_enabled = True

    test_cases = [
        {
            "category": "Logical Issue",
            "input": "which one is greater, 9.11 or 9.9?",
            "description": "Tests handling of complex questions"
        },
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