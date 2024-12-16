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
    else:
        print("-" * 25)


def verify_chain():
    is_valid = True
    for blockchain_index in range(len(blockchain)):
        if blockchain_index == 0:
            continue
        elif not blockchain[blockchain_index][0] == blockchain[blockchain_index - 1]:
            is_valid = False
            break
    return is_valid
    # block_index = 0
    # is_valid = True
    # for block in blockchain:
    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     elif not block[0] == blockchain[block_index - 1]:
    #         is_valid = False
    #         break
    #     block_index += 1
    # return is_valid


waiting_for_input = True


while waiting_for_input:
    print("Please choose")
    print("1: Add a new transaction")
    print("2: Output the blockchain blocks")
    print("h: Manipulate the blockchain")
    print("q: Quit")
    user_choice = get_user_input()
    if user_choice == "1":
        tran_amt = get_transaction_value()
        #add_value(tran_amt, get_last())
        add_value(last_value=get_last(), value=tran_amt)
    elif user_choice == "2":
        print_blockchain_elements()
    elif user_choice == "h":
        if len(blockchain) >=1:
            blockchain[0] = [2]
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

else:
    print("User Left!")

