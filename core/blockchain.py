from functools import reduce
import json

from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

#Initializing blockchain
MINIG_REWARD = 10
blockchain = []
open_transactions = []
owner = "shahid"

def load_data():
    global blockchain, open_transactions
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
            blockchain = updated_blockchain
            open_transactions = json.loads(content[1])
            updated_open_transactions = []
            for tx in open_transactions:
                updated_otx = Transaction(tx["sender"], tx["recipient"], tx["amount"])
                updated_open_transactions.append(updated_otx)
            open_transactions = updated_open_transactions
    except (IOError, IndexError):
        print("Data file not found! - Continuing with initial data")
        genesis_block = Block(0, "", [], 100, 0)
        blockchain = [genesis_block]
        open_transactions = []
    finally:
        print("READY")


load_data()

def save_data():
    try:
        with open("../data/blockchain_data.txt", mode="w") as f:
            dict_blockchain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.to_ordered_dict() for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in blockchain]]
            dict_open_transactions = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(dict_blockchain))
            f.write("\n")
            f.write(json.dumps(dict_open_transactions))
    except IOError:
        print("Saving failed!")


def get_last():
    """Get last stored transaction"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender = owner, amount = 1.0):
    """To store new transaction"""
    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True
    return False    


def get_transaction_value():
    """Get user input for new transaction to be stored"""
    in_recipient = input("Enter recipient id or name: ")
    in_amount = float(input("Enter Transaction Amount: "))
    return in_recipient, in_amount


def get_user_input():
    """Get user choice"""
    return input("What you choose: ")


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = Transaction("MINING", owner, MINIG_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(
        len(blockchain),
        hashed_block,
        copied_transactions,
        proof
    )
    blockchain.append(block)
    return True


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    return amount_received-amount_sent



def print_blockchain_elements():
    #Output
    print("Outputing Block")
    for block in blockchain:
        print(block)
    else:
        print("-" * 25)


waiting_for_input = True


while waiting_for_input:
    print("Please choose")
    print("1: Add a new transaction")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Check transaction validity")
    print("q: Quit")
    user_choice = get_user_input()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print("Transaction success!")
        else:
            print("Transaction failX")    
    elif user_choice == "2":
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        verifier = Verification()
        if verifier.verify_transactions(open_transactions, get_balance):
            print("All transactions are valid")
        else:
            print("There are invalid transactions")   
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Input was invalid, Pease pick correct")
        continue
    print("Choice fulfilled!")
    verifier = Verification()
    if not verifier.verify_chain(blockchain):
        print("Invalid Blockchain!")
        break   
    print("Balance of {} : {:6.2f}".format(owner,get_balance(owner)))

else:
    print("User Left!")

