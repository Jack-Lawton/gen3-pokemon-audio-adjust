
import os
import json

with open('config.json', 'r') as f:
    config = json.load(f)

DIRECTORY = config["game_sound_directory"]


def crawl_directory(directory):
    # Iterate over all files and subdirectories in the given directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Construct the absolute path to each file
            file_path = os.path.join(root, file)
            # Print or process the file however you want
            yield file_path


if __name__ == "__main__":
    for path in crawl_directory(DIRECTORY):
        print(path)
        if path[-7:] == ".backup":
            os.replace(path, path[:-7])
