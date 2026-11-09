import csv
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


def load_reference_hashes(csv_path):
    """Read the reference CSV and return a dictionary of {sha256: label}."""
    reference = {}

    try:
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                sha = (row.get("sha256") or "").strip().lower()
                label = (row.get("label") or "").strip()

                if len(sha) == 64 and all(c in "0123456789abcdef" for c in sha):
                    reference[sha] = label
                else:
                    print(f"Warning: skipping invalid reference row: {row}")

    except FileNotFoundError:
        print(f"Error: reference file not found: {csv_path}")

    return reference


def classify_files(files, reference):
    """Add a KNOWN/UNKNOWN status and label to each file dictionary."""
    for file in files:
        if file["sha256"] in reference:
            file["status"] = "KNOWN"
            file["label"] = reference[file["sha256"]]
        else:
            file["status"] = "UNKNOWN"
            file["label"] = "-"

    return files


# Temporary test - we'll remove this later
files = scan_folder("data/samples")
reference = load_reference_hashes("data/hashes_reference.csv")

for file in classify_files(files, reference):
    print(f"{file['filename']:<15} {file['status']:<8} {file['label']}")