import os
import subprocess
def run_python_file(working_directory, file_path, args=None):
    try:
        abwdir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abwdir,file_path))
        valid_target_file = os.path.commonpath([abwdir, target_file]) == abwdir
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)
        complete_process = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30 
            )

        ostr = ""
        if complete_process.returncode != 0:
            ostr += f"Process exited with code {complete_process.returncode}\n"
        
        # If no output at all
        if not complete_process.stdout and not complete_process.stderr:
            ostr += "No output produced"
        else:
            if complete_process.stdout:
                ostr += f"STDOUT: {complete_process.stdout}"
            if complete_process.stderr:
                ostr += f"STDERR: {complete_process.stderr}"
        return ostr
    except Exception as e:
        return f'Error: {e}'