import os
import json

def create_outputs_directory():
    outputs_dir = os.path.join(os.getcwd(), "outputs")
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    return outputs_dir

def log(message, silent):
    if not silent:
        print(message)

def save_json_file(data, file_path, silent):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    log(f"Data saved to: {file_path}", silent)