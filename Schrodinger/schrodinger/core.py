import os
import shutil
# from .logger import log (Need to work on hierarchy/dependencies)
import structlog # Temporary import

log = structlog.stdlib.get_logger() # Temporary

def clone_directory_structure(src_direct: str, dest_direct: str, extension: str):

    for curr_folder, sub_folder, files in os.walk(src_direct):

        # Calculates the 'distance' between curr_folder and 'root'
        rel_path = os.path.relpath(curr_folder, src_direct)

        # Combines the rel_path and makes a new directory
        new_dir = os.path.join(dest_direct, rel_path)

        # Creates new directory (Only if it doesn't exist yet)
        os.makedirs(new_dir, exist_ok=True)

        for file in files:
            if file.endswith(extension):
                src_file = os.path.join(curr_folder, file)
                dst_file = os.path.join(new_dir, file)
                shutil.copy2(src_file, dst_file) # Is file metadata (Timestamp) needed?

                log.info(
                    "file_cloned",
                    source=src_file,
                    destination=dst_file,
                    status="success"
                )


"""
Once testing is implemented:

SOURCE:
data/en/
├── intro.en
└── chapter1/
    └── story.en

RUNNING THE FOLLOWING:
clone_directory_structure("data/en", "data/hu", ".en")

EXPECTED OUTPUT:
data/hu/
├── intro.en
└── chapter1/
    └── story.en
"""