from app.ai.engines.base_engine import BaseEngine
from app.core.knowledge import KnowledgeBase


class TroubleshootingEngine(BaseEngine):

    def __init__(self):
        super().__init__()
        self.kb = KnowledgeBase()

    def run(self, question, analysis):

        valve_name, valve_data = self.kb.find_valve(question)
        alarm_name, alarm_data = self.kb.find_alarm(question)

        knowledge_text = ""

        if valve_data:
            knowledge_text += f"\nValve: {valve_name}\nData: {valve_data}\n"

        if alarm_data:
            knowledge_text += f"\nAlarm: {alarm_name}\nData: {alarm_data}\n"

        system_prompt = f"""
You are an INDUSTRIAL EXPERT.

Use ALL available knowledge to correlate between:
- Equipment
- Alarms
- Data

KNOWLEDGE:
{knowledge_text}

DATA:
{analysis}

Provide:
1. Root Cause (based on correlation)
2. Explanation
3. Diagnostic Steps
4. Recommended Actions
"""

        return self.generate(system_prompt, question)
