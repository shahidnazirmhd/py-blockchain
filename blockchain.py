#Initializing blockchain
blockchain = []


def get_last():
    """Get last stored transaction"""
    return blockchain[-1]


def add_value(value, last_value=[1]):
    """To store new transaction"""
    blockchain.append([last_value, value])


def get_user_input():
    """Get user input for new transaction to be stored"""
    return float(input("Enter Transaction Amount: "))


tran_amt = get_user_input()
add_value(tran_amt)
tran_amt = get_user_input()
add_value(tran_amt, get_last())
tran_amt = get_user_input()
add_value(last_value=get_last(),
           value=tran_amt)

print(blockchain)