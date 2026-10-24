#!/usr/bin/env python3
"""
Temporal Validity — every witness entry + every cell state has a lifecycle.

Adapted from SuperInstance/plato-temporal-validity (Rust). Three states:
- Valid: full read/write access, high trust
- Grace: degraded access, JEV validation required for reads
- Expired: read-only, no new writes allowed, witness log still queryable

Transitions:
Valid → Grace: when wall_time > valid_until (but < grace_until)
Grace → Expired: when wall_time > grace_until
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime, timezone, timedelta


class ValidityState(Enum):
    VALID = "valid"      # full access
    GRACE = "grace"      # degraded, JEV required
    EXPIRED = "expired"  # read-only


@dataclass
class TemporalValidity:
    """Temporal validity for a witness entry or cell state."""
    created_at: datetime
    valid_duration: timedelta  # how long in Valid state
    grace_duration: timedelta  # how long in Grace after Valid expires
    state: ValidityState = ValidityState.VALID

    @property
    def valid_until(self) -> datetime:
        return self.created_at + self.valid_duration

    @property
    def grace_until(self) -> datetime:
        return self.valid_until + self.grace_duration

    def check_state(self, now: Optional[datetime] = None) -> ValidityState:
        """Update and return the current state based on wall time."""
        now = now or datetime.now(timezone.utc)
        if now < self.valid_until:
            self.state = ValidityState.VALID
        elif now < self.grace_until:
            self.state = ValidityState.GRACE
        else:
            self.state = ValidityState.EXPIRED
        return self.state

    def can_read(self, now: Optional[datetime] = None) -> bool:
        """Read access in any state."""
        return True  # all states allow reads

    def can_write(self, now: Optional[datetime] = None) -> bool:
        """Write access only in Valid state."""
        return self.check_state(now) == ValidityState.VALID

    def requires_jev_validation(self, now: Optional[datetime] = None) -> bool:
        """Reads require JEV validation in Grace state."""
        return self.check_state(now) == ValidityState.GRACE

    def summary(self) -> dict:
        return {
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "valid_until": self.valid_until.isoformat(),
            "grace_until": self.grace_until.isoformat(),
            "can_write": self.can_write(),
            "requires_jev": self.requires_jev_validation(),
        }


if __name__ == "__main__":
    print("=== Temporal Validity ===\n")

    now = datetime.now(timezone.utc)
    # Fresh: valid 1 hour, grace 30 min
    tv_fresh = TemporalValidity(
        created_at=now,
        valid_duration=timedelta(hours=1),
        grace_duration=timedelta(minutes=30),
    )

    # Old: created 2 hours ago, valid 1 hour, grace 30 min → should be Expired
    tv_old = TemporalValidity(
        created_at=now - timedelta(hours=2),
        valid_duration=timedelta(hours=1),
        grace_duration=timedelta(minutes=30),
    )

    # Grace: created 1.5 hours ago, valid 1 hour, grace 30 min → should be Grace
    tv_grace = TemporalValidity(
        created_at=now - timedelta(hours=1, minutes=20),
        valid_duration=timedelta(hours=1),
        grace_duration=timedelta(minutes=30),
    )

    for label, tv in [("Fresh", tv_fresh), ("Grace", tv_grace), ("Old", tv_old)]:
        state = tv.check_state(now)
        print(f"{label}: state={state.value}, can_write={tv.can_write()}, requires_jev={tv.requires_jev_validation()}")
