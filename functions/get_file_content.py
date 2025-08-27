import os 
from config import MAX_CHARS

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