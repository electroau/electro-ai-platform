from app.ai.engines.base_engine import BaseEngine


class TroubleshootingEngine(BaseEngine):

    def run(self, question: str, context: dict):

        rag = context.get("rag", [])

        rag_text = "\n\n".join([
            f"[SOURCE: {r['source']}]\n{r['content']}"
            for r in rag
        ])

        system_prompt = f"""
You are a SENIOR INDUSTRIAL ENGINEER.

Use manuals + reasoning.

MANUAL DATA:
{rag_text}

INSTRUCTIONS:
- Use manual knowledge
- Connect it to real system behavior
- Think like field engineer

OUTPUT:
1. Root Cause
2. Explanation
3. Steps
4. Actions
"""

        return self.generate(system_prompt, question)
