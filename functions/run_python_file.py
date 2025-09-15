import os 

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
    