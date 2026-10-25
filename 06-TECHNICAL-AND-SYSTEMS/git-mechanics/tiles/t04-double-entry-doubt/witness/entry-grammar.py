"""A doubt: what you stopped checking, why, what covers it, when to look again."""
import time
import uuid

FIELDS = ["stopped_checking", "because", "covered_by", "revisit_trigger"]


class Entry:
    def __init__(self, stopped_checking=None, because=None, covered_by=None,
                 revisit_trigger=None, kind="event", status="open", ts=None,
                 id=None, expr=None, discharge_reason=None):
        self.id = id or uuid.uuid4().hex[:12]
        self.ts = ts or int(time.time())
        self.stopped_checking = stopped_checking
        self.because = because
        self.covered_by = covered_by
        self.revisit_trigger = revisit_trigger
        self.kind = kind
        self.expr = expr
        self.status = status
        self.discharge_reason = discharge_reason
        missing = [f for f in FIELDS if not getattr(self, f)]
        if missing:
            raise ValueError("entry missing required field(s): " + ", ".join(missing))

    def to_dict(self):
        return {k: getattr(self, k) for k in
                ["id", "ts", "stopped_checking", "because", "covered_by",
                 "revisit_trigger", "kind", "expr", "status",
                 "discharge_reason"]}

    @staticmethod
    def from_dict(d):
        return Entry(**d)

