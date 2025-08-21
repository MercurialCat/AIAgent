import os 




def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(path)
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_working_directory):
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(abs_path):
        return(f'Error: "{directory}" is not a directory')

    file_info_lines = []
    names = os.listdir(abs_path)
    excluded_files = ['__pycache__',]
    for name in names:
        if name in excluded_files:
            continue
        full_path = os.path.join(abs_path, name)
        try:  
            if os.path.isdir(full_path) is True:
                is_dir = "is_dir=True"
            else: is_dir = "is_dir=False"
            size = os.path.getsize(full_path)
            formatted_line = f"- {name}: file_size={size} bytes, {is_dir}"
            file_info_lines.append(formatted_line)
        except Exception as e:
            return f"Error: An unexpected problem has occured: {e}"

    return "\n".join(file_info_lines) 