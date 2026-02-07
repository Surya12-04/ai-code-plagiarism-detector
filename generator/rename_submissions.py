import os

BASE_DIR = os.path.join("data", "submissions")

def rename_files():
    print("🔁 Renaming submission files safely...")

    for problem in os.listdir(BASE_DIR):
        problem_path = os.path.join(BASE_DIR, problem)

        if not os.path.isdir(problem_path):
            continue

        for fname in os.listdir(problem_path):
            if not fname.endswith(".py"):
                continue

            old_path = os.path.join(problem_path, fname)

            # New filename: problem_solution_x.py
            new_name = f"{problem}_{fname}"
            new_path = os.path.join(problem_path, new_name)

            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"✔ {fname} → {new_name}")

    print("✅ Renaming complete.")


if __name__ == "__main__":
    rename_files()
