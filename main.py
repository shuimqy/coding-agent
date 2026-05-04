import sys
import json
import csv
import os
from agent import code_paper


def append_to_csv(data: dict, csv_path: str):
    info = data.get("paper_info", {})
    coding = data.get("coding", {})
    rq1 = coding.get("RQ1", {})
    rq2 = coding.get("RQ2", {})
    rq3 = coding.get("RQ3", {})
    rq4 = coding.get("RQ4", {})

    row = {
        "title": info.get("title"),
        "authors": "; ".join(a.get("name", "") for a in info.get("authors", [])),
        "year": info.get("year"),
        "venue": info.get("venue"),
        "publication_type": info.get("publication_type"),
        "peer_reviewed": info.get("peer_reviewed"),
        "open_source_artifact": info.get("open_source_artifact"),
        "affiliation_region": info.get("affiliation_region"),
        "included": data.get("included"),
        "exclusion_reason": data.get("exclusion_reason"),
        # RQ1: presence flags
        **{f"RQ1_{k}": "yes" if v else "no" for k, v in rq1.items()},
        # RQ2
        "RQ2_primary_form": rq2.get("primary_form"),
        "RQ2_secondary_form": rq2.get("secondary_form"),
        # RQ3
        "RQ3_application_domain": rq3.get("application_domain"),
        "RQ3_task_context": rq3.get("task_context"),
        "RQ3_target_users": rq3.get("target_users"),
        "RQ3_digital_artifacts": "; ".join(rq3.get("digital_artifacts") or []),
        "RQ3_domain_tools": "; ".join(rq3.get("domain_tools") or []),
        # RQ4
        "RQ4_evaluation_type": "; ".join(rq4.get("evaluation_type") or []),
        "RQ4_benchmarks_datasets": "; ".join(rq4.get("benchmarks_datasets") or []),
        "RQ4_baselines": rq4.get("baselines"),
        "RQ4_metrics": "; ".join(rq4.get("metrics") or []),
        "RQ4_reproducibility": rq4.get("reproducibility"),
        "RQ4_validity_discussion": rq4.get("validity_discussion"),
        "RQ4_domain_validation": rq4.get("domain_validation"),
        "RQ4_statistical_analysis": rq4.get("statistical_analysis"),
    }

    file_exists = os.path.exists(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <paper1> [paper2] ...")
        sys.exit(1)

    result_dir = os.path.join(os.path.dirname(__file__), "result")
    csv_path = os.path.join(result_dir, "summary.csv")
    os.makedirs(result_dir, exist_ok=True)

    for file_path in sys.argv[1:]:
        file_path = os.path.normpath(file_path)
        print(f"\n>>> Coding: {file_path}")
        code_paper(file_path)

        # Read the most recently saved JSON in result/
        json_files = sorted(
            [f for f in os.listdir(result_dir) if f.endswith(".json")],
            key=lambda f: os.path.getmtime(os.path.join(result_dir, f)),
        )
        if not json_files:
            print("    Warning: no JSON result found")
            continue

        latest = os.path.join(result_dir, json_files[-1])
        with open(latest, encoding="utf-8") as f:
            data = json.load(f)
        append_to_csv(data, csv_path)
        print(f"    Saved: {latest}")
        print(f"    CSV:   {csv_path}")
