import os
import importlib.util
import time
import threading
import gpt

output_dir = "output"
tmp_game_dir = "tmp_game"


def wait_for_save(filename, check_interval=1):
    """Wait for the file to be saved in VSCode."""
    initial_timestamp = os.path.getmtime(filename)
    while True:
        time.sleep(check_interval)
        if os.path.getmtime(filename) != initial_timestamp:
            print(f"{filename} has been saved!")
            break


def open_in_vscode(filename):
    """Open the given filename in VSCode."""
    os.system(f"code {filename}")


def get_task_number(task_name):
    return int(task_name.split("_")[1])


def select_task():
    task_dirs = sorted(os.listdir(output_dir), key=get_task_number)
    for i, task_dir in enumerate(task_dirs, 1):
        print(f"{i}. {task_dir}")
    choice = int(input("Select a task (by number): "))
    return task_dirs[choice - 1]


def create_solution_file(task_dir):
    with open(os.path.join(output_dir, task_dir, "prompt.py"), "r") as prompt_file:
        prompt_content = prompt_file.read()
    solution_template = f"{prompt_content}    # Enter your solution below:\n"
    os.makedirs(tmp_game_dir, exist_ok=True)
    task_tmp_dir = os.path.join(tmp_game_dir, task_dir)
    os.makedirs(task_tmp_dir, exist_ok=True)
    solution_filename = os.path.join(task_tmp_dir, "solution.py")
    with open(solution_filename, "w") as f:
        f.write(solution_template)
    return solution_filename


def test_solution(task_dir, solution_filename, is_gpt=False):
    with open(os.path.join(output_dir, task_dir, "test.py"), "r") as test_file:
        test_content = test_file.read()
    with open(solution_filename, "r") as solution_file:
        solution_content = solution_file.read()
    combined_content = solution_content + "\n\n" + test_content
    combined_filename = os.path.join(tmp_game_dir, task_dir, "temp_combined.py")
    with open(combined_filename, "w") as combined_file:
        combined_file.write(combined_content)
    spec = importlib.util.spec_from_file_location("test_module", combined_filename)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)
    with open(os.path.join(output_dir, task_dir, "entry_point.txt"), "r") as ep_file:
        entry_point = ep_file.read().strip()
    candidate_function = getattr(test_module, entry_point)

    user = "GPT" if is_gpt else "you"

    try:
        test_module.check(candidate_function)
        print(f"[{user}] Your solution passed all tests!")
        return True
    except AssertionError as e:
        print(f"[{user}] Your solution failed. Error: {e}")
        return False
    except Exception as e:
        print(f"[{user}] An unexpected error occurred. Error: {e}")
        return False


def fetch_gpt_solution(task_dir):
    # Sleep for 10 seconds to give the user time to write their solution
    time.sleep(10)
    with open(os.path.join(output_dir, task_dir, "prompt.py"), "r") as prompt_file:
        prompt_content = prompt_file.read()
    gpt_solution = gpt.get_gpt_solution(prompt_content)
    # Prepend the prompt to the solution
    gpt_solution = prompt_content + "\n\n" + gpt_solution
    gpt_filename = os.path.join(tmp_game_dir, task_dir, "gpt_solution.py")
    with open(gpt_filename, "w") as f:
        f.write(gpt_solution)
    return gpt_filename


def test_gpt_solution(task_dir):
    gpt_solution_filename = fetch_gpt_solution(task_dir)
    test_solution(task_dir, gpt_solution_filename, is_gpt=True)


def main():
    print("Welcome to the coding game!")
    task_dir = select_task()
    solution_filename = create_solution_file(task_dir)

    # Start GPT in a separate thread
    gpt_thread = threading.Thread(target=test_gpt_solution, args=(task_dir,))
    gpt_thread.start()

    open_in_vscode(solution_filename)
    wait_for_save(solution_filename)

    # If GPT is still working, inform the user and wait
    if gpt_thread.is_alive():
        print("GPT is still solving the problem. Please wait...")
        gpt_thread.join()

    print("GPT has completed the task!")
    test_solution(task_dir, solution_filename)

    # Here, you can compare the results and inform the user.
    # For instance, if both user and GPT solutions pass the tests,
    # you can print a congratulatory message to the user and provide insights from GPT's solution.


if __name__ == "__main__":
    main()
