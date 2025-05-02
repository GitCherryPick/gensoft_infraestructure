import subprocess

def run_code(code: str):
    # Save the code to a temporary file
    with open("temp_script.py", "w") as f:
        f.write(code)

    # Run the code using subprocess
    result = subprocess.run(["python", "temp_script.py"], capture_output=True, text=True, timeout=3)

    # Return the output and error messages
    return result.stdout, result.stderr
