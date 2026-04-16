from app.ai.engines.base_engine import BaseEngine
from app.core.knowledge import KnowledgeBase


class TroubleshootingEngine(BaseEngine):

    def __init__(self):
        super().__init__()
        self.kb = KnowledgeBase()

    def run(self, question, analysis):

        valve_name, valve_data = self.kb.find_valve(question)

        knowledge_text = ""

        if valve_data:
            knowledge_text = f"""
Valve: {valve_name}
Data: {valve_data}
"""

        system_prompt = f"""
You are an INDUSTRIAL TROUBLESHOOTING EXPERT.

Use the knowledge below if available.

KNOWLEDGE:
{knowledge_text}

DATA:
{analysis}

Provide:
- Root cause
- Step-by-step troubleshooting
- Technical explanation
"""

        return self.generate(system_prompt, question)
