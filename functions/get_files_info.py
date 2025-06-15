import os

def get_files_info(working_directory, directory=None):
    try:
        if directory == None:
            directory = "."
        working_directory_path = os.path.abspath(working_directory)
        directory_path = os.path.join(working_directory_path, directory)
        directory_path = os.path.abspath(directory_path)

        if not directory_path.startswith(working_directory_path):
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(directory_path):
            return(f'Error: "{directory}" is not a directory')

        else:
            files = os.listdir(directory_path)
            result = []
            for file in files:
                file_path = os.path.join(directory_path, file)
                result.append(f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
            return str("\n".join(result))
    except Exception as e:
        return f"Error: {str(e)}"