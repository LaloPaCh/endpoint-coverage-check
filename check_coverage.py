import csv
from collections import Counter
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent


def load_records(filename, required_columns):
    records = {}

    with (PROJECT_DIR / filename).open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(f"{filename}: missing required columns")

        for row in reader:
            asset_id = (row["asset_id"] or "").strip().lower()
            if not asset_id or asset_id in records:
                raise ValueError(
                    f"{filename}, line {reader.line_num}: empty or duplicate asset_id"
                )
            records[asset_id] = row

    return records


def main():
    inventory = load_records("inventory.csv", {"asset_id"})
    agents = load_records("agents.csv", {"asset_id", "status"})
    if not inventory:
        raise ValueError("inventory.csv: no assets to assess")

    outcomes = {
        "active": ("PASS", "Agent reported active"),
        "disconnected": ("FAIL", "Agent reported disconnected"),
    }
    counts = Counter()
    report = PROJECT_DIR / "coverage_report.csv"

    with report.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["asset_id", "agent_status", "result", "reason"])

        for asset_id in sorted(inventory):
            agent = agents.get(asset_id)
            if agent is None:
                status = "missing"
                result, reason = "FAIL", "No matching agent record"
            else:
                status = (agent["status"] or "").strip().lower()
                result, reason = outcomes.get(
                    status, ("INCONCLUSIVE", "Unrecognized or empty agent status")
                )

            writer.writerow([asset_id, status, result, reason])
            counts[result] += 1

    coverage = counts["PASS"] / len(inventory)
    print(f"Confirmed coverage: {coverage:.1%} ({counts['PASS']}/{len(inventory)})")
    print(
        f"PASS: {counts['PASS']} | FAIL: {counts['FAIL']} | "
        f"INCONCLUSIVE: {counts['INCONCLUSIVE']}"
    )
    print(f"Report: {report.name}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(f"Evidence error: {error}") from error