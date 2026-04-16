from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class BaseEngine:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv(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))
        self.model = "gpt-4o-mini"

    def generate(self, system_prompt, user_prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        return response.choices[0].message.content
