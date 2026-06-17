"""
Domain models for the Corporate Cognitive Pipeline.

All monetary values are stored as :class:`decimal.Decimal` to avoid
floating-point rounding errors when dealing with BRL amounts.

SISBAJUD response codes:
    - 98 → institution did not respond (non-compliance)
    - 13 → responded with zero balance
    - 00 → successful block executed

Tracked assets (initial dataset):
    - FRAM XIV FIP      → R$ 3,877,255.47  (side-pocket suspected)
    - LIG Itaú          → R$ 1,250,000.00
    - CDB BTG           → R$   650,758.60
    - Bonifácio FIP     → created post-litigation (retroactive fraud indicator)
    - OSLO FIP          → non-responsive (Code 98)
    - Ajaccio FIP       → temporal inconsistency
    - Itaú account      → tactical emptying R$ 469,575 → R$ 5,491
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class SisbajudCode(Enum):
    """SISBAJUD response codes returned by financial institutions."""

    CODE_00 = "00"  # Successful block executed
    CODE_13 = "13"  # Responded with zero balance
    CODE_98 = "98"  # Institution did not respond — non-compliance


class RiskLevel(Enum):
    """Risk classification for assets, institutions, and alerts."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    def __lt__(self, other: "RiskLevel") -> bool:
        return self.value < other.value

    def __le__(self, other: "RiskLevel") -> bool:
        return self.value <= other.value

    def __gt__(self, other: "RiskLevel") -> bool:
        return self.value > other.value

    def __ge__(self, other: "RiskLevel") -> bool:
        return self.value >= other.value


class AssetStatus(Enum):
    """Operational status of a tracked asset."""

    ACTIVE = "active"
    BLOCKED = "blocked"
    EMPTIED = "emptied"        # Tactical emptying confirmed
    SUSPICIOUS = "suspicious"  # Irregular behaviour detected
    UNRESPONSIVE = "unresponsive"  # Institution returned Code 98


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Asset:
    """Represents a single trackable financial asset under investigation.

    Attributes:
        id: Unique identifier (auto-generated UUID if not provided).
        name: Human-readable asset name (e.g. 'FRAM XIV FIP').
        institution: Name of the custodian/manager institution.
        value_brl: Last known value in Brazilian Real.
        asset_type: E.g. 'FIP', 'CDB', 'LIG', 'conta_corrente'.
        status: Current :class:`AssetStatus`.
        sisbajud_code: Last SISBAJUD response code for this asset.
        risk_level: Assessed :class:`RiskLevel`.
        notes: Free-text observations, legal flags, etc.
        detected_at: When this asset was first detected by the pipeline.
        creation_date: Optional; date the asset/fund was formally created.
        is_post_litigation: True when the asset was created after litigation
            start — a retroactive fraud indicator.
    """

    name: str
    institution: str
    value_brl: Decimal
    asset_type: str
    status: AssetStatus = AssetStatus.ACTIVE
    sisbajud_code: SisbajudCode | None = None
    risk_level: RiskLevel = RiskLevel.MEDIUM
    notes: str = ""
    detected_at: datetime = field(default_factory=datetime.utcnow)
    creation_date: str | None = None          # "YYYY-MM-DD" string
    is_post_litigation: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __str__(self) -> str:
        return (
            f"Asset({self.name}, {self.institution}, "
            f"R$ {self.value_brl:,.2f}, {self.status.value})"
        )


@dataclass
class Institution:
    """Represents a financial institution under surveillance.

    Attributes:
        name: Institution name (e.g. 'BTG Pactual').
        type: E.g. 'banco', 'gestora_fip', 'corretora'.
        sisbajud_code: Most recent SISBAJUD response code.
        last_response: ISO-8601 datetime string of last interaction.
        balance_history: Ordered list of (date_str, Decimal) tuples.
        risk_level: Current :class:`RiskLevel`.
        alerts: List of alert ids associated with this institution.
    """

    name: str
    type: str
    sisbajud_code: SisbajudCode | None = None
    last_response: str | None = None
    balance_history: list[tuple[str, Decimal]] = field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.MEDIUM
    alerts: list[str] = field(default_factory=list)  # Alert.id references

    def latest_balance(self) -> Decimal | None:
        """Return the most recent balance in the history, or None."""
        if self.balance_history:
            return self.balance_history[-1][1]
        return None

    def previous_balance(self) -> Decimal | None:
        """Return the second-to-last balance, or None."""
        if len(self.balance_history) >= 2:
            return self.balance_history[-2][1]
        return None


@dataclass
class Alert:
    """An alert generated by any pipeline module.

    Attributes:
        id: UUID string.
        timestamp: When the alert was generated.
        level: :class:`RiskLevel` severity.
        category: Short category tag (e.g. 'non_response', 'emptying').
        description: Human-readable description of the alert.
        institution: Optional institution name this alert concerns.
        asset: Optional :class:`Asset` this alert concerns.
        legal_refs: List of applicable legal references (e.g. 'art_171_cp').
        recommended_action: Suggested next step for the legal team.
        module: Pipeline module that raised this alert.
    """

    level: RiskLevel
    category: str
    description: str
    legal_refs: list[str] = field(default_factory=list)
    recommended_action: str = ""
    institution: str | None = None
    asset: Asset | None = None
    module: str = "unknown"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __str__(self) -> str:
        return f"[{self.level.name}] {self.category}: {self.description}"


@dataclass
class WholeMoneyTrail:
    """Snapshot of the full money trail at a given investigation date.

    Attributes:
        date: Investigation date string ("YYYY-MM-DD").
        assets: All tracked :class:`Asset` objects.
        total_tracked: Sum of all known asset values in BRL.
        total_blocked: Sum of successfully blocked assets (Code 00).
        total_evaded: Estimated value that has evaded attachment.
        alerts: Active :class:`Alert` objects from the most recent run.
        institutions: Institutions under surveillance.
    """

    date: str
    assets: list[Asset] = field(default_factory=list)
    total_tracked: Decimal = Decimal("0.00")
    total_blocked: Decimal = Decimal("0.00")
    total_evaded: Decimal = Decimal("0.00")
    alerts: list[Alert] = field(default_factory=list)
    institutions: list[Institution] = field(default_factory=list)

    def compute_totals(self) -> None:
        """Recompute aggregate totals from the current asset list."""
        self.total_tracked = sum(
            (a.value_brl for a in self.assets), Decimal("0.00")
        )
        self.total_blocked = sum(
            (a.value_brl for a in self.assets if a.sisbajud_code == SisbajudCode.CODE_00),
            Decimal("0.00"),
        )
        self.total_evaded = sum(
            (
                a.value_brl
                for a in self.assets
                if a.status in {AssetStatus.EMPTIED, AssetStatus.UNRESPONSIVE}
            ),
            Decimal("0.00"),
        )


@dataclass
class PipelineReport:
    """Output produced by a single pipeline module after execution.

    Attributes:
        timestamp: When this report was generated.
        module: Name of the module that produced this report.
        status: 'ok', 'warning', 'error', or 'critical'.
        findings: Dict of structured findings specific to the module.
        alerts: Alerts raised during this module run.
        recommendations: Ordered list of recommended actions.
    """

    module: str
    status: str  # "ok" | "warning" | "error" | "critical"
    findings: dict[str, Any] = field(default_factory=dict)
    alerts: list[Alert] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def worst_risk_level(self) -> RiskLevel | None:
        """Return the highest risk level among all alerts in this report."""
        if not self.alerts:
            return None
        return max(a.level for a in self.alerts)

    def alert_count_by_level(self) -> dict[str, int]:
        """Return a count of alerts grouped by risk level name."""
        counts: dict[str, int] = {lvl.name: 0 for lvl in RiskLevel}
        for alert in self.alerts:
            counts[alert.level.name] += 1
        return counts
