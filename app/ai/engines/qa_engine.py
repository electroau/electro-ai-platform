from app.ai.engines.base_engine import BaseEngine


class QAEngine(BaseEngine):

    def run(self, question, analysis):

        system_prompt = f"""
You are a business assistant.

Answer clearly and safely.

DATA:
{analysis}
"""

        return self.generate(system_prompt, question)
