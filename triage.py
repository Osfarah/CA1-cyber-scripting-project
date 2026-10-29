import hashlib
import os
from datetime import datetime


def calculate_sha256(file_path):
    """Return the SHA-256 hash of a file as a hex string."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_file_info(file_path):
    """Return a dictionary with basic details about one file."""
    stats = os.stat(file_path)
    modified = datetime.fromtimestamp(stats.st_mtime)

    return {
        "filename": os.path.basename(file_path),
        "extension": os.path.splitext(file_path)[1],
        "size_bytes": stats.st_size,
        "modified": modified.strftime("%Y-%m-%d %H:%M:%S"),
        "sha256": calculate_sha256(file_path),
    }


def scan_folder(folder_path):
    """Return a list of file-info dictionaries for every file in a folder."""
    results = []

    for name in sorted(os.listdir(folder_path)):
        full_path = os.path.join(folder_path, name)

        if os.path.isfile(full_path):
            info = get_file_info(full_path)
            results.append(info)

    return results


# Temporary test - we'll remove this later
for file in scan_folder("data/samples"):
    print(file["filename"], file["size_bytes"], file["sha256"])