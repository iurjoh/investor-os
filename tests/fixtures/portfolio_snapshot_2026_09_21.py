"""Dados sintéticos de teste. Nenhum dado de carteira real.

Fixture fictícia para validar parsing, moedas, quantidades, fundos e caixa.
"""
from decimal import Decimal

SNAPSHOT = {
    "label": "dados sintéticos de teste",
    "quantity_as_of": "2026-09-21",
    "base_currency": "SEK",
    "stocks": [
        # Ticker, MIC, moeda, quantidade, preço, data: dados sintéticos de teste.
        ("SYN1", "XLON", "GBP", "12", "4.25", "2026-09-24"),
        ("SYN2", "XLON", "GBP", "25", "7.10", "2026-09-24"),
        ("SYN3", "XNYS", "USD", "8", "32.50", "2026-09-24"),
        ("SYN4", "XNYS", "USD", "14", "18.75", "2026-09-24"),
        ("SYN5", "XNYS", "USD", "20", "11.20", "2026-09-24"),
        ("SYN6", "XNYS", "USD", "9", "24.40", "2026-09-24"),
        ("SYN7", "XTSE", "CAD", "16", "21.35", "2026-09-23"),
        ("SYN8", "XNYS", "USD", "11", "15.60", "2026-09-24"),
        ("SYN9", "XNYS", "USD", "7", "42.00", "2026-09-24"),
        ("SYN10", "XTSE", "CAD", "30", "9.80", "2026-09-23"),
    ],
    "average_cost_per_unit": None,
    "fund": {"name": "Synthetic Global Fund", "currency": "SEK", "estimated_value": "12500",
             "value_as_of": "2026-09-22", "units": None, "nav": None,
             "average_cost_per_unit": None},
    "cash": {"currency": "SEK", "amount": "2400", "as_of": "2026-09-21"},
}


def preview():
    assert SNAPSHOT["average_cost_per_unit"] is None
    seen = set()
    subtotals = {}
    for ticker, mic, currency, qty, quote, quote_date in SNAPSHOT["stocks"]:
        assert (ticker, mic) not in seen
        seen.add((ticker, mic))
        assert (mic, currency) in {("XLON", "GBP"), ("XNYS", "USD"), ("XTSE", "CAD")}
        assert Decimal(qty) > 0 and Decimal(quote) >= 0
        assert quote_date in {"2026-09-23", "2026-09-24"}
        subtotals[currency] = subtotals.get(currency, Decimal("0")) + Decimal(qty) * Decimal(quote)
    assert len(seen) == 10
    print(SNAPSHOT["label"])
    print("10 synthetic test stocks; indicative quote-currency values only:")
    for currency in sorted(subtotals):
        print(f"  {currency}: {subtotals[currency]:,.2f}")
    fund = SNAPSHOT["fund"]
    cash = SNAPSHOT["cash"]
    assert fund["units"] is None and fund["nav"] is None
    print(f"  SEK: {Decimal(fund['estimated_value']):,.2f} synthetic fund value + "
          f"{Decimal(cash['amount']):,.2f} synthetic cash = "
          f"{Decimal(fund['estimated_value']) + Decimal(cash['amount']):,.2f}")
    print("Synthetic test data only; no real portfolio data.")


if __name__ == "__main__":
    preview()
