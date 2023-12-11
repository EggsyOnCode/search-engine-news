import hashlib

def calculate_hash(title):
    hash_object = hashlib.sha256(title.encode())
    return hash_object.hexdigest()