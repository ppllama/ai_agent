import os, subprocess


def run_python_file(working_directory, file_path):
    
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        output = subprocess.run(["python3", abs_file_path], timeout=30, capture_output=True, text=True)
        if output.stdout == "" and output.stderr == "":
            return "No output produced"
        if output.returncode != 0:
            return f"stdout:\n{output.stdout}\nstderr: {output.stderr}\nProcess exited with code {output.returncode}"
        return f"stdout:\n{output.stdout}\nstderr: {output.stderr}\n"
    
    except Exception as e:
        return f"Error: {e}"