import os 




def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(working_directory):
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(abs_path):
        return(f'Error: "{directory}" is not a directory')

    names = os.listdir(abs_path)
    for name in names:
        full_path = os.path.join(abs_path, name)
        if os.path.isdir(full_path) is True:
            is_dir = "is_dir=True"
        else: is_dir = "is_dir=False"

