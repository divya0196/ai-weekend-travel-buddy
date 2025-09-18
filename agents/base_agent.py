# agents/base_agent.py

import os
import openai

class Agent:
    def __init__(self, role, goal, backstory):
        # It's recommended to handle the API key securely, e.g., via environment variables
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = f"""
        You are an AI assistant designed for a multi-agent travel planning system.
        Your persona and instructions are defined below. Strictly adhere to them.

        Role: {role}
        Goal: {goal}
        Backstory: {backstory}
        
        You MUST ONLY respond with a valid JSON object. Do not add any text before or after the JSON.
        """

    def chat(self, user_message, additional_messages=None):
        messages = [{"role": "system", "content": self.system_prompt}]
        if additional_messages:
            messages.extend(additional_messages)
        messages.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using a cost-effective and powerful model
                messages=messages,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            return f'{{"error": "An error occurred while communicating with the AI model.", "details": "{str(e)}"}}'
