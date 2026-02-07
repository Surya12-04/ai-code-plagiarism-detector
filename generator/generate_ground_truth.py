# generator/generate_ground_truth.py

import os
import csv
import random
from itertools import combinations

# ================== CONFIG ==================
SUBMISSIONS_DIR = os.path.join("data", "submissions")
OUTPUT_CSV = os.path.join("data", "ground_truth.csv")

POSITIVE_PAIRS_PER_PROBLEM = 200   # plagiarism pairs
NEGATIVE_PAIRS = 400               # non-plagiarism pairs

random.seed(42)
# ============================================


def main():
    print("📊 Generating ground truth labels...")

    problems = {}

    # ---------------- LOAD FILES ----------------
    for problem in os.listdir(SUBMISSIONS_DIR):
        problem_path = os.path.join(SUBMISSIONS_DIR, problem)

        if not os.path.isdir(problem_path):
            continue

        files = [
            f                                  # ✅ ONLY filename
            for f in os.listdir(problem_path)
            if f.endswith(".py")
        ]

        if len(files) >= 2:
            problems[problem] = files

    if not problems:
        print("❌ No valid problems found.")
        return

    rows = []

    # ---------------- POSITIVE PAIRS ----------------
    for problem, files in problems.items():
        pairs = list(combinations(files, 2))

        sampled_pairs = random.sample(
            pairs,
            min(POSITIVE_PAIRS_PER_PROBLEM, len(pairs))
        )

        for f1, f2 in sampled_pairs:
            rows.append([f1, f2, 1])

    # ---------------- NEGATIVE PAIRS ----------------
    all_files = []
    for files in problems.values():
        all_files.extend(files)

    attempts = 0
    while len([r for r in rows if r[2] == 0]) < NEGATIVE_PAIRS:
        f1, f2 = random.sample(all_files, 2)

        # Ensure they are from DIFFERENT problems
        p1 = next(p for p, fl in problems.items() if f1 in fl)
        p2 = next(p for p, fl in problems.items() if f2 in fl)

        if p1 != p2:
            rows.append([f1, f2, 0])

        attempts += 1
        if attempts > 10000:
            break

    # ---------------- WRITE CSV ----------------
    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file1", "file2", "label"])
        writer.writerows(rows)

    print(f"✅ Ground truth generated: {OUTPUT_CSV}")
    print(f"📈 Total pairs: {len(rows)}")
    print(f"✔ Positive (plagiarism): {sum(r[2] for r in rows)}")
    print(f"✔ Negative (clean): {len(rows) - sum(r[2] for r in rows)}")


if __name__ == "__main__":
    main()
