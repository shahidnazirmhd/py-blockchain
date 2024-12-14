#Initializing blockchain
blockchain = []


def get_last():
    """Get last stored transaction"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_value(value, last_value=[1]):
    """To store new transaction"""
    if last_value == None:
        last_value = [1]
    blockchain.append([last_value, value])


def get_transaction_value():
    """Get user input for new transaction to be stored"""
    return float(input("Enter Transaction Amount: "))


def get_user_input():
    """Get user choice"""
    return input("What you choose: ")


def print_blockchain_elements():
    #Output
    print("Outputing Block")
    for block in blockchain:
        print(block)
    print("-" * 25)    


while True:
    print("Please choose")
    print("1: Add a new transaction")
    print("2: Output the blockchain blocks")
    print("q: Quit")
    user_choice = get_user_input()
    if user_choice == "1":
        tran_amt = get_transaction_value()
        add_value(tran_amt, get_last())
    elif user_choice == "2":
        print_blockchain_elements()
    elif user_choice == "q":
        break
    else:
        print("Input was invalid, Pease pick correct")
        continue
    print("Choice fulfilled!")    


print("Done!")

