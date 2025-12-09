import re
import os
import pathlib

def match_extension(filename, pattern):

    return re.search(pattern, filename) is not None


def ensure_directory(path): #Create directory if it does not exist

    #if Path(path).is_dir():
    if not os.path.exists(path):
        os.makedirs(path)

# To be implemented in core.py
# To be implemented in cli.py
# Integrate with argparse?