class ActionExecutor:

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
        return f"✅ Work Order Created: {text}"

    def log_action(self, text):
        return f"📝 Logged: {text}"
