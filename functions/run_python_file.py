import os 
import subprocess
import sys 
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(path)
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        command = [sys.executable, file_path] + list(args)
        process = subprocess.run(
            command, 
            capture_output=True,
            timeout=30, 
            cwd=abs_working_directory, 
            text=True,
        )
    except Exception as e:    
        return f"Error: executing Python file: {e}"
    if (not process.stdout and not process.stderr) and process.returncode == 0:
        return "No output produced."
    output = f'STDOUT:{process.stdout}\nSTDERR:{process.stderr}'
    if process.returncode != 0:
        output += f'\nProcess exited with code {process.returncode}'
    return output

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Exceute Python files with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)