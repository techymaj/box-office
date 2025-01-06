import json

with open("tree.json", "r") as content:
    tree = json.load(content)


def traverse_tree(drive, folders):
    results = {}

    def recursive_traverse(node, path=""):
        if not isinstance(node, dict):
            return

        for key, value in node.items():
            if key in folders:
                results[key] = value
            elif isinstance(value, dict):
                recursive_traverse(value, f"{path}/{key}")

    recursive_traverse(drive)
    return results

def movies():
    # Specify the keys to search for
    target_keys = ["movies".casefold()]
    
    # Traverse and retrieve the dictionaries
    result = traverse_tree(tree, target_keys)
    
    # Print the results
    for _, v in result.items():
        return v


def series():
    # Specify the keys to search for
    target_keys = ["series".casefold()]

    # Traverse and retrieve the dictionaries
    result = traverse_tree(tree, target_keys)

    # Print the results
    for _, v in result.items():
        return v
