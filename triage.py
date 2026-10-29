import hashlib


def calculate_sha256(file_path):
    """Return the SHA-256 hash of a file as a hex string."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


# Temporary test - we'll remove this later
print(calculate_sha256("data/samples/sample_c.txt"))