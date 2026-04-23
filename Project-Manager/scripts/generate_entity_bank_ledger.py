#!/usr/bin/env python3
"""Generate a month-by-month bank-account ledger for a target entity."""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path


def parse_date(raw: str) -> date | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        yyyy, mm, dd = raw.split("-")
        return date(int(yyyy), int(mm), int(dd))
    except ValueError:
        return None


def parse_amount(raw: str) -> float:
    raw = (raw or "").replace(",", "").strip()
    if not raw:
        return 0.0
    try:
        return float(raw)
    except ValueError:
        return 0.0


def normalize_account(row: dict[str, str]) -> str:
    account = (row.get("company_or_creditor") or "").strip()
    if account:
        return account
    fallback = (row.get("account") or "").strip()
    return fallback or "Unknown Account"


def normalize_txn_date(row: dict[str, str]) -> date | None:
    due = parse_date(row.get("due_date", ""))
    if due is not None:
        return due
    return parse_date(row.get("source_date", ""))


def month_key(d: date) -> str:
    return f"{d.year:04d}-{d.month:02d}"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_pdf_text(path: Path) -> str:
    return subprocess.check_output(["pdftotext", "-layout", str(path), "-"], text=True)


def list_pdf_inputs(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(p for p in path.iterdir() if p.suffix.lower() == ".pdf")
    return [path]


def normalize_trace_headers(row: dict[str, str]) -> dict[str, str]:
    return {key.strip().lower().replace(" ", "_"): value for key, value in row.items()}


def build_ledger_from_normalized(
    rows: list[dict[str, str]],
    entity: str,
    start_date: date,
) -> tuple[dict[str, dict[str, list[dict[str, str]]]], set[str]]:
    grouped: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    accounts: set[str] = set()
    entity_lower = entity.lower()

    for row in rows:
        row_entity = (row.get("entity") or "").strip().lower()
        if row_entity != entity_lower:
            continue

        txn_date = normalize_txn_date(row)
        if txn_date is None or txn_date < start_date:
            continue

        account = normalize_account(row)
        accounts.add(account)
        month = month_key(txn_date)
        grouped[month][account].append(
            {
                "transaction_date": txn_date.isoformat(),
                "account": account,
                "amount_usd": f"{parse_amount(row.get('amount_usd', '')):.2f}",
                "obligation_type": (row.get("obligation_type") or "").strip(),
                "category": (row.get("category") or "").strip(),
                "subcategory": (row.get("subcategory") or "").strip(),
                "description": (row.get("raw_text_excerpt") or "").replace("\n", " ").strip()[:160],
                "source_title": (row.get("source_title") or "").strip(),
                "source_id": (row.get("source_id") or "").strip(),
            }
        )

    for month in grouped:
        for account in grouped[month]:
            grouped[month][account].sort(key=lambda item: item["transaction_date"])

    return grouped, accounts


def build_ledger_from_trace(
    rows: list[dict[str, str]],
    entity: str,
    start_date: date,
) -> tuple[dict[str, dict[str, list[dict[str, str]]]], set[str]]:
    grouped: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    accounts: set[str] = set()
    entity_lower = entity.lower()

    for raw_row in rows:
        row = normalize_trace_headers(raw_row)
        txn_date = parse_date(row.get("date", ""))
        if txn_date is None or txn_date < start_date:
            continue

        source_entity = (row.get("source_entity") or "").strip()
        destination_entity = (row.get("destination_entity") or "").strip()
        source_entity_lower = source_entity.lower()
        destination_entity_lower = destination_entity.lower()

        if entity_lower not in {source_entity_lower, destination_entity_lower}:
            continue

        if destination_entity_lower == entity_lower:
            account = (row.get("destination_account") or "").strip() or "Unknown Account"
            direction = "incoming"
        else:
            account = (row.get("source_account") or "").strip() or "Unknown Account"
            direction = "outgoing"

        counterparty = source_entity if direction == "incoming" else destination_entity
        accounts.add(account)
        month = month_key(txn_date)
        grouped[month][account].append(
            {
                "transaction_date": txn_date.isoformat(),
                "account": account,
                "amount_usd": f"{parse_amount(row.get('amount', '')):.2f}",
                "obligation_type": direction,
                "category": (row.get("trace_category") or "").strip(),
                "subcategory": (row.get("evidence_strength") or "").strip(),
                "description": (
                    f"{(row.get('statement_description') or '').strip()} | "
                    f"Counterparty: {counterparty or 'Unknown'} | "
                    f"{(row.get('notes') or '').strip()}"
                )[:160],
                "source_title": (row.get("primary_source") or "").strip(),
                "source_id": "",
            }
        )

    for month in grouped:
        for account in grouped[month]:
            grouped[month][account].sort(key=lambda item: item["transaction_date"])

    return grouped, accounts


def build_ledger_from_pdfs(
    pdf_paths: list[Path],
    start_date: date,
) -> tuple[dict[str, dict[str, list[dict[str, str]]]], set[str]]:
    grouped: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    accounts: set[str] = set()
    account_labels = {
        "BUSINESS SAVINGS ACCOUNT": "MJSDS business savings XXXXX57000",
        "PREMIUM BUSINESS CHECKING ACCOUNT": "MJSDS checking XXXXX57071",
    }
    section_labels = {
        "DEPOSITS/CREDITS": "deposit",
        "ATM WITHDRAWALS/DEBIT PURCHASES": "card",
        "WITHDRAWALS/DEBITS": "withdrawal",
    }
    ignored_line_patterns = [
        r"^\s*$",
        r"^\s*STATEMENT PERIOD\b",
        r"^\s*\d{2}/\d{2}/\d{2} to \d{2}/\d{2}/\d{2}\b",
        r"^\s*Page\s+\d+\s+of\s+\d+\b",
        r"^\s*MJS DIGITAL STRATEGY LLC\b",
        r"^\s*MELISSA STOCK\b",
        r"^\s*_{2,}\s*$",
        r"^\s*anchor\s*$",
        r"^\s*BCID\|",
    ]

    def is_ignored_line(text: str) -> bool:
        return any(re.match(pattern, text) for pattern in ignored_line_patterns)

    for pdf_path in pdf_paths:
        text = load_pdf_text(pdf_path)
        lines = text.splitlines()
        statement_year = None
        for line in lines:
            match = re.search(r"(\d{2}/\d{2}/\d{2}) to (\d{2}/\d{2}/\d{2})", line)
            if match:
                statement_year = parse_date(
                    f"20{match.group(2)[6:8]}-{match.group(2)[0:2]}-{match.group(2)[3:5]}"
                )
                break
        if statement_year is None:
            continue

        current_account = ""
        current_section = ""
        current_row: dict[str, str] | None = None
        skip_table_headers = False

        for line in lines:
            stripped = line.rstrip()

            matched_account = next(
                (label for label in account_labels if label in stripped),
                None,
            )
            if matched_account is not None:
                current_account = account_labels[matched_account]
                current_section = ""
                continue

            matched_section = next(
                (label for label in section_labels if label in stripped),
                None,
            )
            if matched_section is not None:
                current_section = section_labels[matched_section]
                skip_table_headers = True
                continue

            if not current_account or not current_section:
                continue

            if skip_table_headers:
                if (
                    "DATE" in stripped
                    or "AMOUNT" in stripped
                    or "TRANSACTION" in stripped
                    or "OTHER DESCRIPTION" in stripped
                ):
                    continue
                if not stripped.strip():
                    continue
                skip_table_headers = False

            row_match = re.match(r"^\s*(\d{2}/\d{2})\s+([0-9,]+\.\d{2})\s+(.+?)\s*$", stripped)
            if row_match is not None:
                row_date = parse_date(
                    f"{statement_year.year:04d}-{row_match.group(1)[:2]}-{row_match.group(1)[3:5]}"
                )
                if row_date is None or row_date < start_date:
                    current_row = None
                    continue

                rest = row_match.group(3)
                parts = [part.strip() for part in re.split(r"\s{2,}", rest.strip()) if part.strip()]
                transaction = parts[0] if parts else ""
                description = " | ".join(parts[1:]) if len(parts) > 1 else ""
                current_row = {
                    "transaction_date": row_date.isoformat(),
                    "account": current_account,
                    "amount_usd": f"{parse_amount(row_match.group(2)):.2f}",
                    "obligation_type": current_section,
                    "category": transaction,
                    "subcategory": pdf_path.stem,
                    "description": description,
                    "source_title": str(pdf_path),
                    "source_id": "",
                }
                grouped[month_key(row_date)][current_account].append(current_row)
                accounts.add(current_account)
                continue

            if current_row is None or is_ignored_line(stripped):
                continue

            continuation = " ".join(part.strip() for part in re.split(r"\s{2,}", stripped.strip()) if part.strip())
            if not continuation:
                continue
            current_row["description"] = (f"{current_row['description']} {continuation}").strip()[:160]

    for month in grouped:
        for account in grouped[month]:
            grouped[month][account].sort(key=lambda item: item["transaction_date"])

    return grouped, accounts


def build_ledger(
    rows: list[dict[str, str]],
    entity: str,
    start_date: date,
) -> tuple[dict[str, dict[str, list[dict[str, str]]]], set[str]]:
    if rows and "entity" in rows[0]:
        return build_ledger_from_normalized(rows, entity, start_date)
    return build_ledger_from_trace(rows, entity, start_date)


def write_monthly_csv(
    ledger: dict[str, dict[str, list[dict[str, str]]]],
    output_csv: Path,
) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        fields = [
            "month",
            "transaction_date",
            "account",
            "amount_usd",
            "obligation_type",
            "category",
            "subcategory",
            "description",
            "source_title",
            "source_id",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for month in sorted(ledger):
            for account in sorted(ledger[month]):
                for row in ledger[month][account]:
                    writer.writerow({"month": month, **row})


def write_markdown(
    ledger: dict[str, dict[str, list[dict[str, str]]]],
    accounts: set[str],
    entity: str,
    start_date: date,
    output_md: Path,
    source_label: str,
) -> None:
    output_md.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append(f"# Bank Account Ledger: {entity}")
    lines.append("")
    lines.append(f"- Date range start: {start_date.isoformat()}")
    lines.append(f"- Source file: {source_label}")
    lines.append(f"- Bank accounts identified: {len(accounts)}")
    lines.append("")

    if accounts:
        for idx, account in enumerate(sorted(accounts), start=1):
            lines.append(f"{idx}. {account}")
        lines.append("")
    else:
        lines.append("No bank accounts were identified for this entity in the selected date range.")
        lines.append("")

    if not ledger:
        lines.append("No transactions were found for the selected criteria.")
    else:
        for month in sorted(ledger):
            lines.append(f"## {month}")
            lines.append("")
            for account in sorted(ledger[month]):
                lines.append(f"### {account}")
                lines.append("")
                lines.append("| Date | Amount (USD) | Type | Category | Subcategory | Source |")
                lines.append("|---|---:|---|---|---|---|")
                for row in ledger[month][account]:
                    source = row["source_title"] or row["source_id"]
                    lines.append(
                        f"| {row['transaction_date']} | {row['amount_usd']} | {row['obligation_type']} | {row['category']} | {row['subcategory']} | {source} |"
                    )
                lines.append("")

    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entity", required=True)
    parser.add_argument("--start-date", default="2025-01-01")
    parser.add_argument("--input", default="outputs/normalized_records.csv")
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    start_date = parse_date(args.start_date)
    if start_date is None:
        raise SystemExit(f"Invalid --start-date: {args.start_date}")

    input_path = Path(args.input)
    if input_path.suffix.lower() == ".pdf" or input_path.is_dir():
        ledger, accounts = build_ledger_from_pdfs(list_pdf_inputs(input_path), start_date)
    else:
        rows = load_rows(input_path)
        ledger, accounts = build_ledger(rows, args.entity, start_date)
    write_monthly_csv(ledger, Path(args.output_csv))
    write_markdown(ledger, accounts, args.entity, start_date, Path(args.output_md), args.input)


if __name__ == "__main__":
    main()
