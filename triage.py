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


# Temporary test - we'll remove this later
print(get_file_info("data/samples/sample_d.bin"))