import os
import random


def get_random_file_from_dir(directory : str = "assets") -> str:
    
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            raise FileNotFoundError("No files found in the specified directory.")
        return random.choice(files)
    except Exception as e:
        return str(e)