from functools import reduce
import hashlib as hl
import json
from collections import OrderedDict
#Initializing blockchain
MINIG_REWARD = 10
genesis_block = {
        "previous_hash": "",
        "index": 0,
        "transactions": [],
        "proof": 100
    }
blockchain = [genesis_block]
open_transactions = []
owner = "shahid"
participants = {"shahid"}


def get_last():
    """Get last stored transaction"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender = owner, amount = 1.0):
    """To store new transaction"""
    #transaction = {"sender": sender, "recipient": recipient, "amount": amount}
    transaction = OrderedDict([("sender", sender), ("recipient", recipient), ("amount", amount)])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
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


def hash_block(block):
    return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hl.sha256(guess).hexdigest()
    #print(guess_hash)
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
    # reward_transaction = {
    #     "sender": "MINING",
    #     "recipient": owner,
    #     "amount": MINIG_REWARD
    # }
    reward_transaction = OrderedDict([
    ("sender", "MINING"),
    ("recipient", owner),
    ("amount", MINIG_REWARD)
    ])
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": copied_transactions,
        "proof" : proof
    }
    blockchain.append(block)
    return True


def get_balance(participant):
    tx_sender = [[tx["amount"] for tx in block["transactions"] if tx["sender"] == participant] for block in blockchain]
    open_tx_sender = [tx["amount"] for tx in open_transactions if tx["sender"] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)  #Bug fixed
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #         amount_sent += tx[0]
    tx_recipient = [[tx["amount"] for tx in block["transactions"] if tx["recipient"] == participant] for block in blockchain]
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
        if block["previous_hash"] != hash_block(blockchain[index-1]):
            return False
        if not valid_proof(block["transactions"][:-1], block["previous_hash"], block["proof"]):
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
    print("h: Manipulate the blockchain")
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
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        print_participants()
    elif user_choice == "5":
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == "h":
        if len(blockchain) >=1:
            blockchain[0] = {
                "previous_hash": "",
                "index": 0,
                "transactions": [{'sender': 'SomeOne', 'recipient': 'SomeWho', 'amount': 1.0}]
            }
        else:
            continue    
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

