import hashlib as hl
import json

def hash_str_256(string):
    return hl.sha256(str(string).encode()).hexdigest()

def hash_block(block):
    #return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
    return hash_str_256(json.dumps(block, sort_keys=True))