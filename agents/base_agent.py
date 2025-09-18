# agents/base_agent.py

from openai import OpenAI
import os

class Agent:
    def __init__(self, role, goal, backstory):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def run(self, task_description):
        # A basic method to interact with the LLM
        prompt = f"""
        Role: {self.role}
        Goal: {self.goal}
        Backstory: {self.backstory}
        
        Task: {task_description}
        """
        response = self.llm.chat.completions.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
