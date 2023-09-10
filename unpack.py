import json
import os


def process_line(entry):
    task_id = entry["task_id"].split("/")[-1].replace("/", "_")
    dir_name = os.path.join("output", f"task_{task_id}")
    os.makedirs(dir_name, exist_ok=True)

    # Create 'prompt.py'
    prompt_content = entry["prompt"]
    with open(os.path.join(dir_name, "prompt.py"), "w") as file:
        file.write(prompt_content)

    # Create 'canonical_solution.py'
    canonical_solution_content = entry["canonical_solution"]
    with open(os.path.join(dir_name, "canonical_solution.py"), "w") as file:
        file.write(canonical_solution_content)

    # Create 'test.py'
    test_content = entry["test"].lstrip("\n")
    with open(os.path.join(dir_name, "test.py"), "w") as file:
        file.write(test_content)

    # Create 'info.md'
    with open(os.path.join(dir_name, "info.md"), "w") as file:
        file.write(f"## Task ID\n\n{entry['task_id']}\n\n")
        file.write(f"## Entry Point\n\n{entry['entry_point']}\n\n")
        file.write(f"## Prompt\n\n```python\n{prompt_content}\n```\n\n")
        file.write(
            f"## Canonical Solution\n\n```python\n{canonical_solution_content}\n```\n\n"
        )
        file.write(f"## Test\n\n```python\n{test_content}\n```\n")

    # Create 'entry_point.txt'
    with open(os.path.join(dir_name, "entry_point.txt"), "w") as file:
        file.write(entry["entry_point"])


# Open the JSONL file and read each line
with open("HumanEval.jsonl", "r") as file:
    for line in file:
        entry = json.loads(line)
        process_line(entry)

print("Processing complete.")
