class ActionExecutor:

    def __init__(self):
        from app.core.database import Database
        self.db = Database()

    def execute(self, decisions):

        if not decisions:
            return ["No decisions generated"]

        results = []

        for decision in decisions:

            if not isinstance(decision, str):
                continue

            if "work order" in decision.lower():
                results.append(self.create_work_order(decision))

            elif "check valve" in decision.lower():
                results.append(self.log_action(decision))

            else:
                results.append(f"No action for: {decision}")

        return results

    def create_work_order(self, text):
        try:
            self.db.insert_work_order(text)
            return f"✅ Work Order Saved: {text}"
        except Exception as e:
            return f"❌ DB Error: {str(e)}"

    def log_action(self, text):
        return f"📝 Logged: {text}"
