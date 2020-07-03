from base64 import b64decode, b64encode
import json
from typing import *


def decode_data_str(data_str: str, key: str) -> dict:
    byte_arr = b64decode(data_str)
    bytes_processed = ''.join([chr(n ^ ord(key[i % len(key)])) for i, n in enumerate(byte_arr)])
    return json.loads(bytes_processed)


def encode_dict(d: Dict, key: str) -> bytes:
    json_str = json.dumps(d)
    processed = ''.join([chr(ord(n) ^ ord(key[i % len(key)])) for i, n in enumerate(json_str)]).encode('ascii')
    return b64encode(processed)
