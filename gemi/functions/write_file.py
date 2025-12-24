import os
from google.genai import types
def write_file(working_directory, file_path, content):
    try:
        abwdir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abwdir, file_path))
        valid_target_file = os.path.commonpath([abwdir, target_file]) == abwdir
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write to specified file, relative to workind directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file."
            )
        }
    )
)