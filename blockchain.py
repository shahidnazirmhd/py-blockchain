#Initializing blockchain
genesis_block = {
        "previous_hash": "",
        "index": 0,
        "transactions": []
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
    transaction = {"sender": sender, "recipient": recipient, "amount": amount}
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)


def get_transaction_value():
    """Get user input for new transaction to be stored"""
    in_recipient = input("Enter recipient id or name: ")
    in_amount = float(input("Enter Transaction Amount: "))
    return in_recipient, in_amount


def get_user_input():
    """Get user choice"""
    return input("What you choose: ")


def hash_block(block):
    return "-".join([str(block[key]) for key in block])


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": open_transactions
    }
    blockchain.append(block)
    return True


def get_balance(participant):
    tx_sender = [[tx["amount"] for tx in block["transactions"] if tx["sender"] == participant] for block in blockchain]
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx["amount"] for tx in block["transactions"] if tx["recipient"] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
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
    return True


waiting_for_input = True


while waiting_for_input:
    print("Please choose")
    print("1: Add a new transaction")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Output participants")
    print("h: Manipulate the blockchain")
    print("q: Quit")
    user_choice = get_user_input()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == "2":
        if mine_block():
            open_transactions = []
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        print_participants()
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
    print(get_balance("shahid"))

else:
    print("User Left!")

