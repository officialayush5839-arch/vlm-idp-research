"""src/reliability/abstention.py
Multi-level decision policy and threshold enforcement.
Maps calibrated confidence and uncertainty vector to actions:
- ACCEPT
- ACCEPT_WITH_WARNING
- ESCALATE
- ABSTAIN
"""

from typing import Optional
from src.reliability.schema import ReliabilityAction, ReliabilityDecision


class AbstentionPolicy:
    """Evaluates confidence and uncertainty against operating thresholds."""

    def __init__(
        self,
        tau_accept: float = 0.85,
        tau_warning: float = 0.65,
        tau_escalate: float = 0.45,
        u_max_accept: float = 0.25,
        u_max_warning: float = 0.50,
        u_max_escalate: float = 0.70,
        operating_point: str = "balanced",
    ):
        self.tau_accept = tau_accept
        self.tau_warning = tau_warning
        self.tau_escalate = tau_escalate
        self.u_max_accept = u_max_accept
        self.u_max_warning = u_max_warning
        self.u_max_escalate = u_max_escalate
        self.operating_point = operating_point

    def evaluate(
        self,
        confidence: float,
        uncertainty_norm: float,
        warning_flag: Optional[str] = None,
    ) -> ReliabilityDecision:
        conf = max(0.0, min(1.0, float(confidence)))
        unc = max(0.0, min(1.0, float(uncertainty_norm)))

        # Multi-level decision cascade
        if conf >= self.tau_accept and unc <= self.u_max_accept:
            action = ReliabilityAction.ACCEPT
            reason = "High confidence and low multi-modal uncertainty"
        elif conf >= self.tau_warning and unc <= self.u_max_warning:
            action = ReliabilityAction.ACCEPT_WITH_WARNING
            reason = "Moderate confidence with minor uncertainty detected"
        elif conf >= self.tau_escalate and unc <= self.u_max_escalate:
            action = ReliabilityAction.ESCALATE
            reason = "Substantial uncertainty or degraded evidence; human escalation advised"
        else:
            action = ReliabilityAction.ABSTAIN
            reason = "Severe uncertainty or confidence below safety threshold; abstaining"

        return ReliabilityDecision(
            action=action,
            confidence=conf,
            uncertainty_norm=unc,
            operating_point=self.operating_point,
            reason=reason,
            warning_flag=warning_flag,
        )
