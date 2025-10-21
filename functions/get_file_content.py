import os 
from config import MAX_CHARS
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(path)
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_working_directory):
        return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(abs_path):
        return(f'Error: File not found or is not a regular file: "{file_path}"')
    
    try:
        with open(abs_path, "r") as f:
            file_content = f.read(MAX_CHARS)
            character_check = f.read(1)
            if len(character_check) > 0:
                file_content = file_content + (f"[...File '{file_path}' truncated at '{MAX_CHARS}' characters]")
    except Exception as e:
        return f"Error: An unexpected problem has occured: {e}"
    return file_content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the full text contents of a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)