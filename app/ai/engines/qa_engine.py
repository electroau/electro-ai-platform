from app.ai.engines.base_engine import BaseEngine


class QAEngine(BaseEngine):

    def run(self, question, analysis):

        system_prompt = f"""
You are a BUSINESS & TECHNICAL ASSISTANT.

DATA:
{analysis}

Answer clearly and directly.
"""

        user_prompt = question

        return self.generate(system_prompt, user_prompt)
