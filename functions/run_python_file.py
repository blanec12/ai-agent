import os
from subprocess import run


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python3", target_file]

        if args is not None:
            command.extend(args)

        result = run(
            command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30
        )

        output = ""

        if result.stdout is None and result.stderr is None:
            output += "No output produced"
        else:
            output += f"STDOUT:\n{result.stdout}\n"
            output += f"STDERR:\n{result.stderr}\n"

        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
