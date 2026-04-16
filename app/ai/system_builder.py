from typing import Dict, Any


class SystemContextBuilder:
    """
    Universal System Understanding Builder

    DOES NOT rely on predefined equipment types.
    Builds understanding from:
    - Data
    - Context
    - Structure
    """

    def build(self, question: str, context: Dict) -> Dict:

        client = context.get("client")
        equipment = context.get("equipment")
        history = context.get("history", [])
        analysis = context.get("analysis", {})

        system_context = {
            "raw_question": question,
            "client": client,
            "equipment": equipment,
            "history_summary": history[:5],
            "data_points": [],
            "observations": [],
            "unknowns": []
        }

        # =========================
        # Extract Data Signals (Generic)
        # =========================
        if isinstance(analysis, dict):
            for col in analysis.get("columns", []):
                system_context["data_points"].append(col)

        # =========================
        # Observations (from question)
        # =========================
        text = (question or "").lower()

        if "not working" in text or "fail" in text:
            system_context["observations"].append("system_failure")

        if "stop" in text:
            system_context["observations"].append("system_stopped")

        if "delay" in text:
            system_context["observations"].append("timing_issue")

        # =========================
        # Unknowns (important for AI reasoning)
        # =========================
        if not equipment:
            system_context["unknowns"].append("equipment_type_unknown")

        if not analysis:
            system_context["unknowns"].append("no_data_provided")

        return system_context
