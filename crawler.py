import json
import os
import hashlib

directory = "/media/kali"

tree = {}
hashes = {}

# List of file extensions to hash (case-insensitive)
extensions_to_hash = [".mkv", ".mp4", ".avi", ".flv"]

def hash_file_path(file_path):
    """Generate a SHA-256 hash of the file's absolute path."""
    return hashlib.sha256(file_path.encode()).hexdigest()

def crawl():
    for dirpath, _, filenames in os.walk(directory):
        # Debug: Check the current directory being processed
        # print(f"Processing directory: {dirpath}")

        # Build the directory tree structure
        parts = dirpath.split(os.sep)
        parts = [part for part in parts if part]  # Remove empty parts
        subtree = tree
        for part in parts:
            subtree = subtree.setdefault(part, {})
        
        # Add filenames to the tree
        subtree.update({"_files": filenames})

        # Hash files with specified extensions
        for filename in filenames:
            # Debug: Check each filename
            # print(f"Processing file: {filename}")

            if any(filename.lower().endswith(ext) for ext in extensions_to_hash):
                absolute_path = os.path.join(dirpath, filename)
                file_hash = hash_file_path(absolute_path)
                # Store tuple (hash, absolute_path) in the set
                hashes.update({file_hash: absolute_path})
                # Debug: Log the tuple being added
                # print(f"Hashing file: {absolute_path} -> {file_hash}")

    # Save the directory tree to a JSON file
    with open("tree.json", "w") as json_file:
        json.dump(tree, json_file, indent=4)

    # Save the hashes and paths to a separate file
    with open("hashes.json", "w") as hash_file:
        json.dump(hashes, hash_file, indent=4)

# Run the script
crawl()

# Debug: Final hash set
# print(f"Final hashes: {hashes}")
