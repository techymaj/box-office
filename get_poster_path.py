import os

def get_poster_path(file_path):
    # Get the directory of the given file
    parent_dir = os.path.dirname(file_path)
    # Append "poster.jpg" to the parent directory
    poster_path = os.path.join(parent_dir, "poster.jpg")
    return poster_path