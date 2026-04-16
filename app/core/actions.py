from app.core.database import Database


class ActionExecutor:

    def __init__(self):
        self.db = Database()

    def execute(self, decisions):

        results = []

        for decision in decisions:

            if "work order" in decision.lower():
                results.append(self.create_work_order(decision))

            elif "check valve" in decision.lower():
                results.append(self.log_action(decision))

            else:
                results.append(f"No action for: {decision}")

        return results

    def create_work_order(self, text):
        self.db.insert_work_order(text)
        return f"✅ Work Order Saved: {text}"

    def log_action(self, text):
        return f"📝 Logged: {text}"
