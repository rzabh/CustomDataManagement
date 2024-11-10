import os
import shutil

def clear_directory(directory_path, file_extensions=None, remove_folders=False):
    """
    Clears the specified directory of files (and optionally subfolders).
    
    Parameters:
    - directory_path (str): The path of the directory to clear.
    - file_extensions (list or tuple, optional): A list or tuple of file extensions to delete (e.g., ['.txt', '.log']).
                                                 If None, all files will be deleted.
    - remove_folders (bool, optional): Whether to delete subfolders as well. Default is False.
    
    Returns:
    - None
    """
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return

    try:
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)

            # Remove files
            if os.path.isfile(item_path):
                if file_extensions is None or item_path.endswith(tuple(file_extensions)):
                    os.remove(item_path)
                    print(f"Deleted file: {item_path}")
            
            # Remove folders
            elif os.path.isdir(item_path) and remove_folders:
                shutil.rmtree(item_path)
                print(f"Deleted folder: {item_path}")
    
        print(f"Directory '{directory_path}' cleared successfully.")
    except Exception as e:
        print(f"Error clearing directory '{directory_path}': {e}")



