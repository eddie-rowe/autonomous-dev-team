from openai import OpenAI
import os
import subprocess
import datetime

# Create a client using your API key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_test_output():
    with open("test_output.txt", "r") as f:
        return f.read()

def run_openai_patch_agent():
    test_output = get_test_output()
    prompt = f"""
You're an expert TypeScript developer. The app has failed tests. Suggest a valid 'diff' to fix the problem.

Test output:
{test_output}

Respond with a unified diff (git diff format) only.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def save_patch(diff):
    patch_path = "ai_patch.diff"
    with open(patch_path, "w") as f:
        f.write(diff)
    return patch_path

if __name__ == "__main__":
    diff = run_openai_patch_agent()
    if "diff" in diff:
        save_patch(diff)
