import json
import os
import importlib.util


def combine_and_test(task_dir):
    with open(os.path.join(task_dir, "prompt.py"), "r") as prompt_file:
        prompt_content = prompt_file.read()

    with open(os.path.join(task_dir, "canonical_solution.py"), "r") as solution_file:
        solution_content = solution_file.read()

    combined_content = prompt_content + "\n" + solution_content

    # Write combined content to a temporary file
    temp_filename = os.path.join(task_dir, "temp_combined.py")
    with open(temp_filename, "w") as temp_file:
        temp_file.write(combined_content)

    # Load the combined content and execute it first
    spec = importlib.util.spec_from_file_location("combined_module", temp_filename)
    combined_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(combined_module)

    # Load the testing function
    spec = importlib.util.spec_from_file_location(
        "test_module", os.path.join(task_dir, "test.py")
    )
    test_module = importlib.util.module_from_spec(spec)

    # Update the test module's globals with the globals from the combined module.
    # This allows the test module to access the functions defined in prompt.py.
    test_module_globals = test_module.__dict__
    for key, value in combined_module.__dict__.items():
        if key not in test_module_globals:
            test_module_globals[key] = value

    spec.loader.exec_module(test_module)

    # Get the entry point function name
    with open(os.path.join(task_dir, "entry_point.txt"), "r") as ep_file:
        entry_point = ep_file.read().strip()

    candidate_function = getattr(combined_module, entry_point)

    # Run the test
    try:
        test_module.check(candidate_function)
        print(f"Tests for {task_dir} passed successfully!")
    except AssertionError as e:
        print(f"Tests for {task_dir} failed. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {task_dir}. Error: {e}")


def get_task_number(task_name):
    # Extract number from the task name, e.g., "task_10" -> 10
    return int(task_name.split("_")[1])


# Iterate over each task directory in 'output' and test them
output_dir = "output"
task_dirs = sorted(os.listdir(output_dir), key=get_task_number)

for task_dir in task_dirs:
    full_task_dir = os.path.join(output_dir, task_dir)
    if os.path.isdir(full_task_dir):
        combine_and_test(full_task_dir)
