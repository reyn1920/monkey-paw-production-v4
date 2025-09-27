from dataclasses import dataclass


@dataclass
class CTRDecision:
    replace: bool
    reason: str


class CTRGuard:
    def __init__(self, min_delta: float = 0.5):
        self.min_delta = min_delta

    def decide(self, historical_ctr: float, candidate_ctr_pred: float) -> CTRDecision:
        if candidate_ctr_pred >= historical_ctr + self.min_delta:
            return CTRDecision(
                True,
                f"predicted uplift {candidate_ctr_pred - historical_ctr:.2f} >= {self.min_delta:.2f}",
            )
        return CTRDecision(False, "kept legacy asset: historical CTR stronger")
