import re

def match_extension(filename, pattern):

    return re.search(pattern, filename) is not None

# To be implemented in core.py
# To be implemented in cli.py
# Integrate with argparse?