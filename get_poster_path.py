import os

def get_poster_path(file_path, default_poster_path):
    """
    Checks if 'poster.jpg' exists in the parent directory of the given file path.
    If it exists, returns its path. Otherwise, returns the default poster path.

    :param file_path: Path of the file whose parent directory will be checked.
    :param default_poster_path: Path to the default poster image.
    :return: Path to 'poster.jpg' if it exists, otherwise the default poster path.
    """
    # Get the directory of the given file
    parent_dir = os.path.dirname(file_path)
    # Path for 'poster.jpg'
    poster_path = os.path.join(parent_dir, "poster.jpg")
    # Check if 'poster.jpg' exists
    if os.path.exists(poster_path):
        return poster_path
    else:
        return default_poster_path