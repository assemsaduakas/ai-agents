import os
import json
from openai import OpenAI

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def parse_user_query(self, text: str) -> dict:
        """
        Uses OpenAI to extract intent and parameters from user input.
        Returns structured JSON.
        """

        prompt = f"""
You are an assistant that extracts structured data from user input.

Return ONLY valid JSON.
Possible intents: weather, news, unknown.

Examples:
User: What's the weather in London?
Output: {{"intent": "weather", "city": "london"}}

User: Latest news about AI
Output: {{"intent": "news", "topic": "AI"}}

User: Hello
Output: {{"intent": "unknown"}}

User input:
{text}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"intent": "unknown"}
