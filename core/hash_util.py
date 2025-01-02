import hashlib as hl
import json

def hash_str_256(string):
    return hl.sha256(str(string).encode()).hexdigest()

def hash_block(block):
    dict_block = block.__dict__.copy() #Returing the shallow copy of dict
    dict_block["transactions"] = [tx.to_ordered_dict() for tx in dict_block["transactions"]]
    return hash_str_256(json.dumps(dict_block, sort_keys=True))