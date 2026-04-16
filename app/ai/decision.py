from typing import List, Dict


class DecisionEngine:

    def analyze(
        self,
        ai_response: str,
        question: str = "",
        context: Dict = None
    ) -> List[str]:
        """
        Advanced Decision Engine

        Features:
        - Context-aware (client / equipment / history)
        - Industrial logic (مش مجرد keywords)
        - Expandable rules system
        """

        # =========================
        # Safety Checks
        # =========================
        if not ai_response or not isinstance(ai_response, str):
            return []

        context = context or {}

        decisions = []

        text = ai_response.lower()
        q = (question or "").lower()

        client = context.get("client")
        equipment = context.get("equipment")
        history = context.get("history", [])

        equipment_name = (equipment.get("name", "").lower() if equipment else "")
        equipment_type = (equipment.get("type", "").lower() if equipment else "")

        # =========================
        # 1. Ignore non-operational questions
        # =========================
        ignore_keywords = [
            "what", "summary", "note", "analyze",
            "analysis", "report", "describe"
        ]

        if any(word in q for word in ignore_keywords):
            return []

        # =========================
        # 2. Detect Problem Context
        # =========================
        problem_keywords = [
            "error", "alarm", "fault", "not working",
            "fail", "trip", "issue", "problem"
        ]

        is_problem = any(word in q for word in problem_keywords)

        if not is_problem:
            return []

        # =========================
        # 3. History Intelligence 🔥
        # =========================
        repeated_issue = len(history) >= 3

        # =========================
        # 4. Equipment-based Logic
        # =========================

        # 🔧 Pump Logic
        if "pump" in text or "pump" in equipment_name or "pump" in equipment_type:

            if any(k in text for k in ["trip", "fault", "fail"]):
                decisions.append("Create URGENT work order for pump inspection")

            if "low pressure" in text or "pressure low" in text:
                decisions.append("Check suction line and possible cavitation")

            if "high pressure" in text:
                decisions.append("Inspect discharge blockage or valve condition")

        # 🔧 Valve Logic
        if "valve" in text or "valve" in equipment_name:

            if any(k in text for k in ["not open", "not close", "fail"]):
                decisions.append("Check valve actuator and position feedback")

            if "stuck" in text:
                decisions.append("Inspect mechanical obstruction in valve")

        # 🔧 Pressure System
        if "pressure" in text:

            if "high" in text:
                decisions.append("Inspect pressure control loop and relief system")

            if "low" in text:
                decisions.append("Check leaks or pump performance")

        # =========================
        # 5. Smart Escalation (History-based)
        # =========================
        if repeated_issue:
            decisions.append("Escalate issue: repeated failure detected")
            decisions.append("Recommend preventive maintenance plan")

        # =========================
        # 6. Client Importance (Future Ready)
        # =========================
        if client:
            if client.get("industry"):
                decisions.append("Ensure compliance with client industry standards")

        # =========================
        # 7. Fallback
        # =========================
        if not decisions:
            decisions.append("Perform detailed system diagnostic check")

        return list(set(decisions))  # إزالة التكرار
