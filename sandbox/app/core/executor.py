import subprocess
import tempfile
import os
import re

def run_code(code: str):
    with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp.flush()
    result = subprocess.run(["python", tmp.name], capture_output=True, text=True, timeout=3)

    return result.stdout, result.stderr

def execute_code(code: str, call: str):
    full_code = code + f"\n\nprint({call})\n"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_script:
        temp_script.write(full_code.encode("utf-8"))
        temp_script_path = temp_script.name

    try:
        result = subprocess.run(
            ["python", temp_script_path],
            capture_output=True,
            text=True,
            timeout=3
        )
    except subprocess.TimeoutExpired:
        os.remove(temp_script_path)
        return {"output": "", "error": "TimeOut: Code execution timed out", "line": ""}
    
    os.remove(temp_script_path)
    return {
        "output": result.stdout,
        "error": result.stderr.strip().split("\n")[-1] if result.stderr else "",
        "line": re.findall("line \d", result.stderr)[-1][-1] if result.stderr else ""
    }