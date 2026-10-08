"""Auditable weighted-average portfolio calculations using Decimal only."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable

D = Decimal

@dataclass(frozen=True)
class Trade:
    transaction_date: date
    transaction_id: str
    kind: str
    quantity: Decimal
    gross_amount: Decimal
    fees: Decimal = D("0")
    tax: Decimal = D("0")
    fx_rate: Decimal = D("1")

@dataclass(frozen=True)
class Position:
    quantity: Decimal
    cost_basis_base: Decimal

    @property
    def average_cost_base(self) -> Decimal | None:
        return self.cost_basis_base / self.quantity if self.quantity else None

def calculate_position(trades: Iterable[Trade]) -> Position:
    trades = list(trades)
    seen = set()
    for trade in trades:
        if not trade.transaction_id or trade.transaction_id in seen:
            raise ValueError("trade IDs must be non-empty and unique")
        seen.add(trade.transaction_id)
        values = (trade.quantity, trade.gross_amount, trade.fees, trade.tax, trade.fx_rate)
        if any(not isinstance(v, Decimal) or not v.is_finite() or v < 0 for v in values):
            raise ValueError("trade amounts must be finite non-negative Decimals")
        if trade.quantity == 0 or trade.fx_rate == 0:
            raise ValueError("quantity and FX must be positive")
        if not isinstance(trade.transaction_date, date):
            raise ValueError("trade date must be a date")
    quantity = D("0")
    cost = D("0")
    for trade in sorted(trades, key=lambda t: (t.transaction_date, t.transaction_id)):
        if trade.quantity < 0 or trade.fx_rate <= 0:
            raise ValueError("quantity must be non-negative and fx_rate positive")
        if trade.kind == "buy":
            quantity += trade.quantity
            cost += (trade.gross_amount + trade.fees + trade.tax) * trade.fx_rate
        elif trade.kind == "sell":
            if trade.quantity > quantity:
                raise ValueError("sale exceeds current position")
            average = cost / quantity if quantity else D("0")
            cost -= trade.quantity * average
            quantity -= trade.quantity
            if quantity == 0:
                cost = D("0")
        else:
            raise ValueError(f"unsupported trade kind: {trade.kind}")
    return Position(quantity=quantity, cost_basis_base=cost)
