import os
def get_files_info(working_directory, directory="."):
    try:
        info = ""
        abwdir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abwdir, directory))
        #will be true or false
        valid_target_dir = os.path.commonpath([abwdir, target_dir]) == abwdir
        info = (f"Result for {"current" if directory == '.' else directory} directory")
        if not valid_target_dir:
            info += (f'\n    Error: Cannot list "{directory}" as it is outside the permitted working directory')
            return info
        if not os.path.isdir(target_dir):
            info += (f'\n    "Error: {directory}" is not a directory')
            return info
        for f in os.listdir(target_dir):
            if f == "__pycache__":
                continue
            info += (f"\n  - {f}: file_size={os.path.getsize(os.path.join(target_dir, f))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, f))}")
        return info
    except Exception as e:
        return f"Error: {e}"