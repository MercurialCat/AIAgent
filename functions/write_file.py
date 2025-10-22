import os 
from google import genai
from google.genai import types


def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(path)
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_working_directory):
       return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    parent = os.path.dirname(abs_path)
    try:
        if not os.path.exists(parent):
            os.makedirs(parent)
        with open(abs_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file at the file_path with the provided content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write or overwrite to the file.",
            )
        },
        required=["file_path", "content"]
    ),
)
