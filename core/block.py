from dataclasses import dataclass
from time import time

@dataclass
class Block:
    index: int
    previous_hash: str
    transactions: list
    proof: int
    timestamp: float

    #Custom init
    def __init__(self, index, previous_hash, transactions, proof, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time