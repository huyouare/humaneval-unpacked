import openai
import os

# Load your API key from an environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")


def get_gpt_solution(prompt):
    """
    Calls the GPT-3.5 chat model and retrieves the solution for the given prompt.
    Args:
    - prompt (str): The coding prompt you want to solve.

    Returns:
    - str: The generated solution from GPT-3.5.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a coding assistant. Write only code. Write the following function, starting from the beginning and reciting what was given to you:\n\n",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message["content"].strip()


if __name__ == "__main__":
    sample_prompt = "Write a Python function that reverses a string."
    solution = get_gpt_solution(sample_prompt)
    print(solution)
