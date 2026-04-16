import threading
from typing import Dict, List, Optional


class ContextManager:
    """
    Production-ready Context Manager

    Features:
    - Multi-session support
    - Thread-safe
    - Isolated user context
    """

    def __init__(self):
        self._lock = threading.Lock()

        # session_id -> context data
        self.sessions: Dict[str, Dict] = {}

    # =========================
    # Session Handling
    # =========================
    def _get_session(self, session_id: str) -> Dict:
        with self._lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    "analysis": None,
                    "history": []
                }
            return self.sessions[session_id]

    # =========================
    # Analysis Data
    # =========================
    def set_data(self, session_id: str, analysis: Dict):
        session = self._get_session(session_id)
        session["analysis"] = analysis

    def get_data(self, session_id: str) -> Optional[Dict]:
        session = self._get_session(session_id)
        return session.get("analysis")

    # =========================
    # History
    # =========================
    def add_history(self, session_id: str, question: str, answer: str):
        session = self._get_session(session_id)

        session["history"].append({
            "question": question,
            "answer": answer
        })

    def get_history(self, session_id: str) -> List[Dict]:
        session = self._get_session(session_id)
        return session.get("history", [])

    # =========================
    # Optional: Clear Session
    # =========================
    def clear_session(self, session_id: str):
        with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
