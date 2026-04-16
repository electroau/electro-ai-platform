from app.ai.engines.base_engine import BaseEngine


class TroubleshootingEngine(BaseEngine):

    def run(self, question: str, context: dict):

        # =========================
        # Extract Context 🔥
        # =========================
        rag = context.get("rag", [])
        system = context.get("system", {})
        history = context.get("history", [])
        external = context.get("external_knowledge", {})
        vision = context.get("vision", {})

        # =========================
        # Prepare RAG
        # =========================
        rag_text = "\n\n".join([
            f"[SOURCE: {r.get('source')}]\n{r.get('content')}"
            for r in rag
        ])

        # =========================
        # Prepare Vision
        # =========================
        vision_text = vision.get("analysis", "No image provided")

        # =========================
        # Prepare History
        # =========================
        history_text = "\n".join([
            f"Q: {h.get('question')} | A: {h.get('answer')}"
            for h in history[-5:]
        ])

        # =========================
        # System Prompt 🔥 (Core Intelligence)
        # =========================
        system_prompt = f"""
You are a TOP-TIER INDUSTRIAL TROUBLESHOOTING EXPERT.

You analyze systems using:
- Vision (image understanding)
- Manuals (RAG)
- Context
- Engineering reasoning

=========================
SYSTEM CONTEXT
=========================
{system}

=========================
VISION ANALYSIS
=========================
{vision_text}

=========================
MANUAL DATA (RAG)
=========================
{rag_text}

=========================
EXTERNAL KNOWLEDGE
=========================
{external}

=========================
HISTORY
=========================
{history_text}

=========================
CRITICAL THINKING RULES
=========================
- DO NOT describe only → DIAGNOSE
- Correlate between vision and manuals
- Think in cause-effect relationships
- Prioritize most probable failure
- Avoid generic answers

=========================
OUTPUT FORMAT
=========================
1. System Understanding (short)
2. Most Likely Root Cause
3. Technical Explanation
4. Diagnostic Steps (practical)
5. Recommended Actions (clear)
"""

        return self.generate(system_prompt, question)
