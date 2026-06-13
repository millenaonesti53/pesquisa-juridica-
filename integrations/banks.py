"""Bank balance monitoring and tactical drain detection."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
import logging

from config.settings import ABRUPT_VARIATION_THRESHOLD, CRITICAL_BALANCE_FLOOR

logger = logging.getLogger(__name__)


@dataclass
class BankSnapshot:
    institution: str
    account_type: str
    balance: Decimal
    captured_at: datetime
    previous_balance: Optional[Decimal] = None
    previous_captured_at: Optional[datetime] = None

    @property
    def variation_pct(self) -> Optional[float]:
        if self.previous_balance is None or self.previous_balance == 0:
            return None
        return float(
            (self.balance - self.previous_balance) / self.previous_balance * 100
        )

    @property
    def is_tactical_drain(self) -> bool:
        """Detects sudden large outflow before or after judicial order."""
        if self.previous_balance is None:
            return False
        if self.previous_balance < Decimal("10000"):
            return False
        variation = self.balance - self.previous_balance
        variation_pct = variation / self.previous_balance
        return (
            variation_pct < Decimal(str(-ABRUPT_VARIATION_THRESHOLD))
            and float(self.balance) < CRITICAL_BALANCE_FLOOR
        )


# Known monitored snapshots (seeded from investigation data)
KNOWN_SNAPSHOTS: dict[str, list[BankSnapshot]] = {
    "ITAU": [
        BankSnapshot(
            institution="ITAU",
            account_type="CONTA_CORRENTE",
            balance=Decimal("5491.00"),
            captured_at=datetime(2025, 6, 1),
            previous_balance=Decimal("469575.00"),
            previous_captured_at=datetime(2025, 1, 15),
        )
    ],
    "BTG": [
        BankSnapshot(
            institution="BTG",
            account_type="CDB",
            balance=Decimal("0.00"),
            captured_at=datetime(2025, 6, 1),
            previous_balance=Decimal("650758.60"),
            previous_captured_at=datetime(2025, 3, 10),
        )
    ],
}


class BankMonitor:
    """Monitor bank accounts for tactical drain patterns."""

    def __init__(self):
        self.snapshots: dict[str, list[BankSnapshot]] = dict(KNOWN_SNAPSHOTS)

    def add_snapshot(self, snapshot: BankSnapshot) -> None:
        if snapshot.institution not in self.snapshots:
            self.snapshots[snapshot.institution] = []
        self.snapshots[snapshot.institution].append(snapshot)

    def detect_tactical_drains(self) -> list[BankSnapshot]:
        """Return all snapshots exhibiting tactical drain signature."""
        drains = []
        for snapshots in self.snapshots.values():
            for snap in snapshots:
                if snap.is_tactical_drain:
                    drains.append(snap)
                    logger.warning(
                        f"Tactical drain detected: {snap.institution} "
                        f"R${snap.previous_balance:,.2f} -> R${snap.balance:,.2f} "
                        f"({snap.variation_pct:.1f}%)"
                    )
        return drains

    def get_zero_balance_institutions(self) -> list[str]:
        """Identify institutions reporting zero balance after prior activity."""
        result = []
        for inst, snapshots in self.snapshots.items():
            for snap in snapshots:
                if snap.balance == Decimal("0") and snap.previous_balance and snap.previous_balance > Decimal("1000"):
                    result.append(inst)
        return result
