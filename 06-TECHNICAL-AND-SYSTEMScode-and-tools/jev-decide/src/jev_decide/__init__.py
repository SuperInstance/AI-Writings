"""
jev-decide: Thin Python client for JEV (TypeSafe System One).

Three primitives (Choice, Score, Noul). Schema-bounded. Cannot hallucinate outside
your schema. The substrate's superego, in 4 lines.

Usage:
    from jev_decide import Jev
    jev = Jev()  # uses https://ai-writings.pages.dev/api/jev by default
    r = jev.decide(
        state="What should the substrate do?",
        questions={
            "q1": {"type":"noul","question":"this is a worthy commit","instructions":"yes if significant"},
            "q2": {"type":"choice","question":"which path?","criteria":{"a":"alpha","b":"beta","c":"gamma"},"options":["a","b","c"]}
        }
    )
    print(r["answers"]["q1"]["choice"])  # 'yes'
"""

import urllib.request
import urllib.error
import json
from typing import Dict, Any, Optional

DEFAULT_ENDPOINT = "https://ai-writings.pages.dev/api/jev/decide"
DEFAULT_USER_AGENT = "jev-decide/0.1.0"

class Jev:
    """Thin client for the JEV (TypeSafe System One) decision model."""

    def __init__(self, endpoint: str = DEFAULT_ENDPOINT, user_agent: str = DEFAULT_USER_AGENT):
        self.endpoint = endpoint
        self.user_agent = user_agent

    def decide(self, state: Any, questions: Dict[str, Dict[str, Any]], model: str = "jev-latest") -> Dict[str, Any]:
        """Make a decision. Returns JEV's typed response."""
        payload = {
            "model": model,
            "state": state if isinstance(state, str) else json.dumps(state),
            "questions": questions,
        }
        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "User-Agent": self.user_agent},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())

    def noul(self, state: Any, question: str, instructions: str) -> Dict[str, Any]:
        """Single yes/no question."""
        return self.decide(state, {
            "q": {"type": "noul", "question": question, "instructions": instructions}
        })

    def choice(self, state: Any, question: str, options: list, criteria: Dict[str, str]) -> Dict[str, Any]:
        """Multiple-choice question with rubric."""
        return self.decide(state, {
            "q": {"type": "choice", "question": question, "criteria": criteria, "options": options}
        })

    def score(self, state: Any, question: str, criteria: list, scale: Optional[list] = None) -> Dict[str, Any]:
        """Score against a rubric."""
        return self.decide(state, {
            "q": {
                "type": "score",
                "question": question,
                "criteria": criteria,
                "scale": scale or criteria,
            }
        })

__version__ = "0.1.0"
__all__ = ["Jev"]
