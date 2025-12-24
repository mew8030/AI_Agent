import os
from config import LIMIT
from google.genai import types
def get_file_content(working_directory, file_path):
    try:
        abwdir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abwdir, file_path))

        valid_target_file = os.path.commonpath([abwdir, target_file]) == abwdir
        if not valid_target_file:
            return f'    Error: Connot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'    Error: File not found or is not a regular file: "{file_path}"'

        content = ""
        with open(target_file) as f:
            print(f"reading file")
            content = f.read(LIMIT)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {LIMIT} characters]'
            print(f"reading complete")
        return content
    except Exception as e:
        return f"    Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents from a specified file in the allowed directory",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to find specified file from"
            ),
        },
    ),
)