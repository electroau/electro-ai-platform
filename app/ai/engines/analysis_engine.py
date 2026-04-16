from app.ai.engines.base_engine import BaseEngine


class AnalysisEngine(BaseEngine):

    def run(self, question, analysis):

        system_prompt = f"""
You are a DATA ANALYST.

DATA:
{analysis}

Provide:
- Insights
- Patterns
- Anomalies
- Recommendations
"""

        user_prompt = question

        return self.generate(system_prompt, user_prompt)
