from app.ai.engines.base_engine import BaseEngine
from app.core.knowledge import KnowledgeBase


class TroubleshootingEngine(BaseEngine):

    def __init__(self):
        super().__init__()
        self.kb = KnowledgeBase()

    def run(self, question: str, context: dict):

        # =========================
        # Extract Context 🔥
        # =========================
        client = context.get("client")
        equipment = context.get("equipment")
        history = context.get("history", [])
        analysis = context.get("analysis", {})

        # =========================
        # Knowledge Extraction
        # =========================
        valve_name, valve_data = self.kb.find_valve(question)
        alarm_name, alarm_data = self.kb.find_alarm(question)

        knowledge_text = ""

        if valve_data:
            knowledge_text += f"\n[VALVE]\nName: {valve_name}\nData: {valve_data}\n"

        if alarm_data:
            knowledge_text += f"\n[ALARM]\nName: {alarm_name}\nData: {alarm_data}\n"

        # =========================
        # Equipment Context
        # =========================
        equipment_text = ""
        if equipment:
            equipment_text = f"""
[Equipment]
Name: {equipment.get("name")}
Type: {equipment.get("type")}
"""

        # =========================
        # Client Context
        # =========================
        client_text = ""
        if client:
            client_text = f"""
[Client]
Name: {client.get("name")}
Industry: {client.get("industry")}
"""

        # =========================
        # History Context 🔥
        # =========================
        history_text = ""
        if history:
            history_text = "[Previous Issues]\n"
            for h in history[:5]:  # limit
                history_text += f"- Issue: {h.get('issue')} | Solution: {h.get('solution')}\n"

        # =========================
        # System Prompt 🔥🔥🔥
        # =========================
        system_prompt = f"""
You are a SENIOR INDUSTRIAL AUTOMATION ENGINEER with 20+ years experience.

Your task is to perform ADVANCED troubleshooting using:

1. Equipment context
2. Alarm knowledge
3. Historical failures
4. Data analysis

=========================
CONTEXT
=========================
{client_text}

{equipment_text}

=========================
KNOWLEDGE BASE
=========================
{knowledge_text}

=========================
HISTORICAL DATA
=========================
{history_text}

=========================
LIVE DATA
=========================
{analysis}

=========================
INSTRUCTIONS
=========================
- Correlate between alarms, equipment, and data
- Use history to detect repeated failures
- Do NOT give generic answers
- Think like a field engineer

=========================
OUTPUT FORMAT
=========================
1. Root Cause (MOST LIKELY)
2. Technical Explanation
3. Diagnostic Steps (step-by-step)
4. Recommended Actions (practical)
5. Risk Level (Low / Medium / High)
"""

        # =========================
        # Generate Response
        # =========================
        return self.generate(system_prompt, question)
