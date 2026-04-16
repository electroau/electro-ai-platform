class ActionExecutor:

    def __init__(self):
        from app.core.database import Database
        self.db = Database()

    def execute(self, decisions):

        if not decisions:
            return ["No actions executed"]

        results = []

        for decision in decisions:

            if not isinstance(decision, str):
                continue

            d = decision.lower()

            # =========================
            # 🚨 CRITICAL ALERT
            # =========================
            if "urgent" in d or "alarm" in d or "critical" in d:
                results.append(self.send_alert(decision))

            # =========================
            # 🛠 WORK ORDER (Smart)
            # =========================
            elif any(k in d for k in ["inspect", "inspection", "check", "maintenance"]):
                results.append(self.create_work_order(decision))

            # =========================
            # 📚 MANUAL / REFERENCE
            # =========================
            elif "manual" in d or "reference" in d:
                results.append(self.log_action(f"Review manual: {decision}"))

            # =========================
            # 📈 ESCALATION
            # =========================
            elif "escalate" in d:
                results.append(self.escalate_issue(decision))

            # =========================
            # DEFAULT
            # =========================
            else:
                results.append(self.log_action(decision))

        return results

    # =========================
    # CREATE WORK ORDER 🔥
    # =========================
    def create_work_order(self, text):
        try:
            self.db.insert_work_order(text)
            return f"🛠 Work Order Created & Saved: {text}"
        except Exception as e:
            return f"❌ Work Order Failed: {str(e)}"

    # =========================
    # ALERT SYSTEM 🔥
    # =========================
    def send_alert(self, text):
        # مستقبلاً: Email / SMS / SCADA alert
        return f"🚨 ALERT TRIGGERED: {text}"

    # =========================
    # ESCALATION 🔥
    # =========================
    def escalate_issue(self, text):
        return f"📈 ESCALATED TO MAINTENANCE TEAM: {text}"

    # =========================
    # LOGGING
    # =========================
    def log_action(self, text):
        return f"📝 Logged Action: {text}"
