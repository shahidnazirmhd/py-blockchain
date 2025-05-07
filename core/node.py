from uuid import uuid4
from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet

class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)


    def get_transaction_value(self):
        """Get user input for new transaction to be stored"""
        in_recipient = input("Enter recipient id or name: ")
        in_amount = float(input("Enter Transaction Amount: "))
        return in_recipient, in_amount


    def get_user_input(self):
        """Get user choice"""
        return input("What you choose: ")
    

    def print_blockchain_elements(self):
        #Output
        print("Outputing Block")
        for block in self.blockchain.chain:
            print(block)
        else:
            print("-" * 25)


    def listening_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print("Please choose")
            print("1: Add a new transaction")
            print("2: Mine a new block")
            print("3: Output the blockchain blocks")
            print("4: Check transaction validity")
            print("5: Create wallet")
            print("6: Load wallet")
            print("7: Save wallet")
            print("q: Quit")
            user_choice = self.get_user_input()
            if user_choice == "1":
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, amount, signature):
                    print("Transaction success!")
                else:
                    print("Transaction failX")    
            elif user_choice == "2":
                if not self.blockchain.mine_block():
                    print("mining failed, No wallet?")
            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("All transactions are valid")
                else:
                    print("There are invalid transactions")   
            elif user_choice == "5":
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == "6":
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == "7":
                self.wallet.save_keys()
                self.blockchain = Blockchain(self.wallet.public_key)                
            elif user_choice == "q":
                waiting_for_input = False
            else:
                print("Input was invalid, Pease pick correct")
                continue
            print("Choice fulfilled!")
            if not Verification.verify_chain(self.blockchain.chain):
                print("Invalid Blockchain!")
                break   
            print("Balance of {} : {:6.2f}".format(self.wallet.public_key,self.blockchain.get_balance()))

        else:
            print("User Left!")
            

if __name__ == '__main__': 
    node = Node()
    node.listening_for_input()            