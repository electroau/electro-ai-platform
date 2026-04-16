from typing import List, Dict


class DecisionEngine:

    def analyze(
        self,
        ai_response: str,
        question: str = "",
        context: Dict = None
    ) -> List[str]:
        """
        Intelligent Decision Engine (Next Gen)

        - Uses AI output (diagnosis)
        - Uses vision insights
        - Uses system context
        - Not keyword-based only
        """

        # =========================
        # Safety
        # =========================
        if not ai_response or not isinstance(ai_response, str):
            return ["No decisions generated"]

        context = context or {}

        decisions = []

        text = ai_response.lower()

        # =========================
        # 1. Detect Critical State 🔥
        # =========================
        critical_patterns = [
            "critical", "failure", "fault", "alarm",
            "shutdown", "trip", "overheat", "emergency"
        ]

        if any(word in text for word in critical_patterns):
            decisions.append("🚨 URGENT: Immediate system inspection required")

        # =========================
        # 2. Extract AI Diagnosis Insight 🔥
        # =========================
        if "root cause" in text:
            decisions.append("📌 Root cause identified → take corrective action")

        if "possible" in text and "cause" in text:
            decisions.append("🔍 Investigate suspected cause")

        # =========================
        # 3. Vision-Based Decisions 🔥
        # =========================
        vision = context.get("vision", {})
        vision_text = str(vision.get("analysis", "")).lower()

        if "alarm" in vision_text:
            decisions.append("🚨 Visual alarm detected → immediate inspection")

        if "red" in vision_text or "warning" in vision_text:
            decisions.append("⚠️ Critical visual indicator ON")

        if "stopped" in vision_text or "not running" in vision_text:
            decisions.append("⚙️ System appears stopped → verify operation state")

        # =========================
        # 4. RAG-Based Decisions 🔥
        # =========================
        rag = context.get("rag", [])

        if rag:
            decisions.append("📚 Use manual references for verification")

        # =========================
        # 5. System Context Awareness 🔥
        # =========================
        system = context.get("system", {})
        observations = system.get("observations", [])

        if "system_failure" in observations:
            decisions.append("🚨 System failure detected → initiate troubleshooting")

        if "system_stopped" in observations:
            decisions.append("⚙️ System stopped → check startup conditions")

        # =========================
        # 6. Smart Escalation 🔥
        # =========================
        history = context.get("history", [])

        if len(history) >= 3:
            decisions.append("📈 Repeated issue → escalate to maintenance team")

        # =========================
        # 7. Intelligent Default
        # =========================
        if not decisions:
            decisions.append("Perform full system diagnostic analysis")

        # إزالة التكرار
        return list(set(decisions))
