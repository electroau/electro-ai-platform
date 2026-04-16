import threading
from typing import Dict, List, Optional


class ContextManager:
    """
    Advanced Context Manager (Production Ready)

    Features:
    - Thread-safe
    - Multi-session
    - Structured memory
    - Vision support
    - Ready for DB/Redis upgrade
    """

    def __init__(self):
        self._lock = threading.Lock()
        self.sessions: Dict[str, Dict] = {}

    # =========================
    # Session Handling
    # =========================
    def _get_session(self, session_id: str) -> Dict:
        with self._lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    "analysis": None,
                    "history": [],
                    "vision": None,
                    "metadata": {}
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
    # Vision Memory 🔥
    # =========================
    def set_vision(self, session_id: str, vision_data: Dict):
        session = self._get_session(session_id)
        session["vision"] = vision_data

    def get_vision(self, session_id: str) -> Optional[Dict]:
        session = self._get_session(session_id)
        return session.get("vision")

    # =========================
    # Metadata (Future use)
    # =========================
    def set_metadata(self, session_id: str, key: str, value):
        session = self._get_session(session_id)
        session["metadata"][key] = value

    def get_metadata(self, session_id: str, key: str):
        session = self._get_session(session_id)
        return session["metadata"].get(key)

    # =========================
    # History
    # =========================
    def add_history(self, session_id: str, question: str, answer: str):
        session = self._get_session(session_id)

        session["history"].append({
            "question": question,
            "answer": answer
        })

        # 🔥 Limit history (performance)
        if len(session["history"]) > 20:
            session["history"] = session["history"][-20:]

    def get_history(self, session_id: str) -> List[Dict]:
        session = self._get_session(session_id)
        return session.get("history", [])

    # =========================
    # Clear Session
    # =========================
    def clear_session(self, session_id: str):
        with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
