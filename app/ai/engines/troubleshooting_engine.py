from app.ai.engines.base_engine import BaseEngine


class TroubleshootingEngine(BaseEngine):

    def run(self, question: str, context: dict):

        system = context.get("system", {})
        history = context.get("history", [])
        analysis = context.get("analysis", {})

        system_prompt = f"""
You are a SENIOR INDUSTRIAL ENGINEER.

You are NOT limited to any specific equipment.

You must analyze ANY system using:

- Data
- Observations
- Context
- Logical reasoning

=========================
SYSTEM CONTEXT
=========================
{system}

=========================
HISTORY
=========================
{history}

=========================
DATA
=========================
{analysis}

=========================
IMPORTANT RULES
=========================
- Do NOT assume equipment type
- Do NOT rely on predefined rules
- Think from first principles
- Reconstruct how the system works
- Identify failure points

=========================
OUTPUT
=========================
1. System Understanding
2. Most Likely Root Cause
3. Reasoning
4. Diagnostic Steps
5. Recommended Actions
"""

        return self.generate(system_prompt, question)
