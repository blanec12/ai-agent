import os


def get_files_info(working_directory, directory="."):

    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = (
        os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    )

    if not valid_target_dir:
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

    if not os.path.isdir(target_dir):
        return f"Error: '{target_dir}' is not a directory"

    try:
        dir_info = []
        for item in os.listdir(target_dir):
            path = os.path.join(target_dir, item)
            size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            dir_info.append(f"- {item}: file_size={size}, is_dir={is_dir}")
        return "\n".join(dir_info)
    except Exception as e:
        return f"Error getting file info {e}"
