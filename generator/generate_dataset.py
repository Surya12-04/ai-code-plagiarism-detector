# generator/generate_dataset.py

import os
import random
from problems import PROBLEMS
from transformations import apply_random_transformations

BASE_DIR = os.path.join("data", "submissions")
FILES_PER_PROBLEM = 50   # 5 problems × 50 = 250 files

os.makedirs(BASE_DIR, exist_ok=True)

def save_code(folder, filename, code):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
        f.write(code)


def main():
    print("Generating dataset...")

    for problem, base_code in PROBLEMS.items():
        problem_dir = os.path.join(BASE_DIR, problem)

        # Save original
        save_code(problem_dir, "solution_0.py", base_code)

        for i in range(1, FILES_PER_PROBLEM):
            variant = apply_random_transformations(
                base_code,
                k=random.randint(1, 3)
            )
            save_code(problem_dir, f"solution_{i}.py", variant)

        print(f"✔ Generated {FILES_PER_PROBLEM} files for {problem}")

    print("\n✅ Dataset generation complete.")
    print(f"📁 Files saved in: {BASE_DIR}")


if __name__ == "__main__":
    main()
