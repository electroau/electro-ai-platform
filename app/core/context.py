class ContextManager:
    def __init__(self):
        self.current_data = None
        self.history = []

    def set_data(self, analysis):
        self.current_data = analysis

    def get_data(self):
        return self.current_data

    def add_history(self, question, answer):
        self.history.append({
            "question": question,
            "answer": answer
        })

    def get_history(self):
        return self.history
