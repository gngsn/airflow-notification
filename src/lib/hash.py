import hashlib

__all__ = ["hash_md5"]

md5 = hashlib.md5()


def hash_md5(*args) -> str:
    md5.update(*args)
    return md5.hexdigest()
