from app.ai.engines.base_engine import BaseEngine


class TroubleshootingEngine(BaseEngine):

    def run(self, question: str, context: dict):

        system = context.get("system", {})
        history = context.get("history", [])
        analysis = context.get("analysis", {})
        external = context.get("external_knowledge", {})

        system_prompt = f"""
You are a SENIOR INDUSTRIAL ENGINEER.

You can analyze ANY system using:
- Context
- Data
- External knowledge (manuals / models)

=========================
SYSTEM
=========================
{system}

=========================
EXTERNAL KNOWLEDGE
=========================
{external}

=========================
HISTORY
=========================
{history}

=========================
DATA
=========================
{analysis}

=========================
INSTRUCTIONS
=========================
- Use model knowledge if available
- Reconstruct how the system works
- Identify root cause logically
- Do not assume anything blindly

=========================
OUTPUT
=========================
1. System Understanding
2. Root Cause
3. Explanation
4. Diagnostic Steps
5. Actions
"""

        return self.generate(system_prompt, question)
