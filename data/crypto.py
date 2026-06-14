# data/crypto.py
import os

def _load_binary_msg(filename: str) -> str:
    """Read a binary file from the data directory and decode it to UTF-8 string."""
    base_dir = os.path.dirname(__file__)          # current directory (data/)
    file_path = os.path.join(base_dir, filename)
    with open(file_path, 'rb') as f:
        raw_bytes = f.read()
    return raw_bytes.decode('utf-8')

def get_ok_message() -> str:
    """Return the message shown when user clicks 'Yes'."""
    return _load_binary_msg('msg_ok.bin')

def get_warn_message() -> str:
    """Return the warning message shown when user clicks 'No'."""
    return _load_binary_msg('msg_warn.bin')
