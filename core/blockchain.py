from functools import reduce
import json

from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

#Initializing blockchain
MINIG_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0, "", [], 100, 0)
        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id


    def get_chain(self):
        return self.__chain[:]


    def get_open_transaction(self):
        return self.__open_transactions[:]        


    def load_data(self):
        try:
            with open("../data/blockchain_data.txt", mode="r") as f:
                content = f.readlines()
                blockchain = json.loads(content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx["sender"], tx["recipient"], tx["amount"]) for tx in block["transactions"]]
                    updated_block = Block(
                        block["index"],
                        block["previous_hash"],
                        converted_tx,
                        block["proof"],
                        block["timestamp"]
                    )
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain
                open_transactions = json.loads(content[1])
                updated_open_transactions = []
                for tx in open_transactions:
                    updated_otx = Transaction(tx["sender"], tx["recipient"], tx["amount"])
                    updated_open_transactions.append(updated_otx)
                self.__open_transactions = updated_open_transactions
        except (IOError, IndexError):
            print("Handled Exception...Data file not found! - Continuing with initial data")
            pass
        finally:
            print("READY")


    def save_data(self):
        try:
            with open("../data/blockchain_data.txt", mode="w") as f:
                dict_blockchain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.to_ordered_dict() for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                dict_open_transactions = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(dict_blockchain))
                f.write("\n")
                f.write(json.dumps(dict_open_transactions))
        except IOError:
            print("Saving failed!")


    def get_last(self):
        """Get last stored transaction"""
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]


    def add_transaction(self,recipient, sender, amount):
        """To store new transaction"""
        transaction = Transaction(sender, recipient, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False    


    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof


    def mine_block(self):
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction("MINING", self.hosting_node, MINIG_REWARD)
        copied_transactions = self.__open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(
            len(self.__chain),
            hashed_block,
            copied_transactions,
            proof
        )
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True


    def get_balance(self):
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        return amount_received-amount_sent





