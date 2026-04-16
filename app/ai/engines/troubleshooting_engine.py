from app.ai.engines.base_engine import BaseEngine


class TroubleshootingEngine(BaseEngine):

    def run(self, question, analysis):

        system_prompt = f"""
You are an INDUSTRIAL TROUBLESHOOTING EXPERT.

DATA:
{analysis}

Give:
- Root cause
- Step-by-step troubleshooting
- Safety notes
"""

        user_prompt = question

        return self.generate(system_prompt, user_prompt)
