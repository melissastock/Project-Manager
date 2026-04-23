#!/usr/bin/env python3
"""Build a combined monthly P&L summary and transaction support CSV for MJSDS."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def parse_amount(raw: str) -> float:
    raw = (raw or "").replace(",", "").strip()
    if not raw:
        return 0.0
    return float(raw)


def classify_transaction(row: dict[str, str]) -> tuple[str, str, bool]:
    amount = parse_amount(row["amount_usd"])
    obligation_type = (row.get("obligation_type") or "").strip().lower()
    category = (row.get("category") or "").strip().upper()
    description = (row.get("description") or "").strip().upper()

    if "TRANSFER TO MJS DIGITAL STR" in description or "TRANSFER FROM MJS DIGITAL STR" in description:
        return "internal_transfer", "Internal transfer between MJSDS accounts.", False

    if "TRIPP" in description or "ANEUMIND" in description:
        if obligation_type == "deposit":
            return "loan_inflow", "Incoming transfer from TC/Aneumind treated as loan repayment.", False
        return "loan_outflow", "Outgoing transfer to TC/Aneumind treated as loan.", False

    if "M STOCK" in description:
        if obligation_type == "deposit":
            return "owner_contribution", "Incoming personal transfer from Melissa treated as owner contribution.", False
        return "owner_draw", "Outgoing transfer to Melissa treated as owner draw.", False

    if category in {"ACH NSF FEE", "DB CRD OD FEE", "SERVICE CHARGE", "ATM FEE", "OD FEE"}:
        return "bank_fees", "Bank, overdraft, or service fee counted as business expense.", True

    if "ZOOM.COM" in description or "GOOGLE *GSUITE" in description or "BEAUTIFUL.AI" in description:
        return "software_expense", "Software or account service treated as business expense.", True

    if any(token in description for token in ("PAYPAL", "VENMO", "STRIPE", "SQSP*", "SQUARE", "CASH APP", "SHOPIFY")):
        return "pass_through_consulting", "Processor/platform activity treated as pass-through consulting activity, not MJSDS revenue.", False

    if "U OF DIGITAL" in description:
        if obligation_type == "deposit":
            return "u_of_digital_revenue", "True business revenue from U of Digital.", True
        return "business_expense", "Expense clearly tied to U of Digital work.", True

    if category in {"MOBILE DEPOSIT", "ACI DEPOSIT", "OD CL WR/OFF", "POS CREDIT"}:
        return "unverified_inflow", "Deposit/credit not clearly identified as U of Digital revenue, so left out of the P&L.", False

    if "LIQUOR" in description or "ROSIE" in description or "DRAFTKINGS" in description or "CANNAB" in description:
        return "personal_excluded", "Personal-looking purchase excluded from business P&L.", False

    if "KING SOOP" in description or "7-ELEVEN" in description or "MAVERIK" in description:
        return "personal_excluded", "Consumer purchase excluded by default as personal unless clearly business.", False

    if obligation_type in {"card", "withdrawal"}:
        return "personal_excluded", "Not clearly business under the default rule, so excluded as personal.", False

    if obligation_type == "deposit":
        return "unverified_inflow", "Deposit not clearly identified as U of Digital revenue, so left out of the P&L.", False

    return "uncategorized", "Uncategorized transaction.", False


def write_combined_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    support_rows: list[dict[str, str]] = []
    summary_totals: dict[tuple[str, str], float] = defaultdict(float)
    month_rollups: dict[str, float] = defaultdict(float)

    for row in rows:
        pnl_category, note, included_in_pnl = classify_transaction(row)
        amount = parse_amount(row["amount_usd"])
        signed_amount = amount
        if row["obligation_type"] in {"withdrawal", "card"}:
            signed_amount = -amount

        support_rows.append(
            {
                "row_type": "transaction_support",
                "year": row["month"][:4],
                "month": row["month"],
                "summary_category": "",
                "pnl_category": pnl_category,
                "included_in_pnl": "yes" if included_in_pnl else "no",
                "amount_usd": f"{signed_amount:.2f}",
                "transaction_date": row["transaction_date"],
                "account": row["account"],
                "bank_activity_type": row["obligation_type"],
                "bank_category": row["category"],
                "source_period": row["subcategory"],
                "description": row["description"],
                "source_title": row["source_title"],
                "notes": note,
            }
        )

        summary_totals[(row["month"], pnl_category)] += signed_amount
        if included_in_pnl:
            month_rollups[row["month"]] += signed_amount

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "row_type",
        "year",
        "month",
        "summary_category",
        "pnl_category",
        "included_in_pnl",
        "amount_usd",
        "transaction_date",
        "account",
        "bank_activity_type",
        "bank_category",
        "source_period",
        "description",
        "source_title",
        "notes",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()

        for month, category in sorted(summary_totals):
            writer.writerow(
                {
                    "row_type": "monthly_summary",
                    "year": month[:4],
                    "month": month,
                    "summary_category": "category_total",
                    "pnl_category": category,
                    "included_in_pnl": "",
                    "amount_usd": f"{summary_totals[(month, category)]:.2f}",
                    "transaction_date": "",
                    "account": "",
                    "bank_activity_type": "",
                    "bank_category": "",
                    "source_period": "",
                    "description": "",
                    "source_title": "",
                    "notes": "",
                }
            )

        for month in sorted(month_rollups):
            writer.writerow(
                {
                    "row_type": "monthly_summary",
                    "year": month[:4],
                    "month": month,
                    "summary_category": "net_pnl_included_transactions",
                    "pnl_category": "net_pnl",
                    "included_in_pnl": "",
                    "amount_usd": f"{month_rollups[month]:.2f}",
                    "transaction_date": "",
                    "account": "",
                    "bank_activity_type": "",
                    "bank_category": "",
                    "source_period": "",
                    "description": "",
                    "source_title": "",
                    "notes": "",
                }
            )

        for row in support_rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with Path(args.input).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    write_combined_csv(rows, Path(args.output))


if __name__ == "__main__":
    main()
