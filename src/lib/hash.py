import hashlib

__all__ = ["hash_md5"]

md5 = hashlib.md5()


def hash_md5(source: str) -> str:
    byte = bytes(source, 'UTF-8')
    md5.update(byte)
    return md5.hexdigest()
