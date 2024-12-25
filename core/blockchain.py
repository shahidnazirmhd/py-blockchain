from functools import reduce
from collections import OrderedDict
import json

from hash_util import hash_str_256, hash_block
from block import Block

#Initializing blockchain
MINIG_REWARD = 10
blockchain = []
open_transactions = []
owner = "shahid"
participants = {"shahid"}

def load_data():
    global blockchain, open_transactions
    try:
        with open("blockchain_data.txt", mode="r") as f:
            content = f.readlines()
            blockchain = json.loads(content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [OrderedDict([("sender", tx["sender"]), ("recipient", tx["recipient"]), ("amount", tx["amount"])]) for tx in block["transactions"]]
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
                updated_otx = OrderedDict([("sender", tx["sender"]), ("recipient", tx["recipient"]), ("amount", tx["amount"])])
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
        with open("blockchain_data.txt", mode="w") as f:
            dict_blockchain = [block.__dict__ for block in blockchain]
            f.write(json.dumps(dict_blockchain))
            f.write("\n")
            f.write(json.dumps(open_transactions))
    except IOError:
        print("Saving failed!")


def get_last():
    """Get last stored transaction"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender = owner, amount = 1.0):
    """To store new transaction"""
    transaction = OrderedDict([("sender", sender), ("recipient", recipient), ("amount", amount)])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False    


def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])
    return sender_balance >= transaction["amount"]


def get_transaction_value():
    """Get user input for new transaction to be stored"""
    in_recipient = input("Enter recipient id or name: ")
    in_amount = float(input("Enter Transaction Amount: "))
    return in_recipient, in_amount


def get_user_input():
    """Get user choice"""
    return input("What you choose: ")


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof))
    guess_hash = hash_str_256(guess)
    return guess_hash[0:2] == "00"


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = OrderedDict([
    ("sender", "MINING"),
    ("recipient", owner),
    ("amount", MINIG_REWARD)
    ])
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
    tx_sender = [[tx["amount"] for tx in block.transactions if tx["sender"] == participant] for block in blockchain]
    open_tx_sender = [tx["amount"] for tx in open_transactions if tx["sender"] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    tx_recipient = [[tx["amount"] for tx in block.transactions if tx["recipient"] == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    return amount_received-amount_sent



def print_blockchain_elements():
    #Output
    print("Outputing Block")
    for block in blockchain:
        print(block)
    else:
        print("-" * 25)


def print_participants():
    #Output
    print("Outputing Participants")
    for name in participants:
        print(name)
    else:
        print("-" * 25)


def verify_chain():
    """verify current blockchain"""
    for index, block in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index-1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print("PoW Invalid")
            return False
    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True


while waiting_for_input:
    print("Please choose")
    print("1: Add a new transaction")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Output participants")
    print("5: Check transaction validity")
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
        print_participants()
    elif user_choice == "5":
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transactions")   
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Input was invalid, Pease pick correct")
        continue
    print("Choice fulfilled!")
    if not verify_chain():
        print("Invalid Blockchain!")
        break   
    print("Balance of {} : {:6.2f}".format(owner,get_balance(owner)))

else:
    print("User Left!")

