from flask import Flask, jsonify, request
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain


app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)

@app.route('/', methods=['GET'])
def greet():
    return 'Hello!...'


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = {
            "message": "No wallet set up."
        }
        return jsonify(response), 400
    if not request.is_json:
        response = {
            "message": "Send correct data"
        }
        return jsonify(response), 400
    values = request.get_json()
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        response = {
            "message": "Required fields are missing"
        }
        return jsonify(response), 400
    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(recipient, wallet.public_key, amount, signature)
    if success:
        response = {
            "message": "Transaction completed successfully.",
            "transaction": {
                "sender": wallet.public_key,
                "recipient": recipient,
                "amount": amount,
                "signature": signature
            },
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "X Creating a transaction failed X."
        }
        return jsonify(response), 500




@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain 
        blockchain = Blockchain(wallet.public_key)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Saving the keys failed"
        }
        return jsonify(response), 500
    

@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain 
        blockchain = Blockchain(wallet.public_key)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Loading the keys failed"
        }
        return jsonify(response), 500
    

@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            "message": "Balance fetched sucessfully.",
            "funds":balance,
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Loading balance failed.",
            "wallet_set_up": wallet.public_key != None
        }
        return jsonify(response), 406   



@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.mine_block()
    """NO NEED TO CONVERT TO __dict__ BECAUSE @dataclass USED"""
    if block != None:
        response = {
            "message": "Block added sucessfully.",
            "block":block,
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Adding a block failed.",
            "wallet_set_up": wallet.public_key != None
        }
        return jsonify(response), 406


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    """NO NEED TO CONVERT TO __dict__ BECAUSE @dataclass USED"""
    # dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    # for dict_block in dict_chain:
    #     dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']] 
    # return jsonify(dict_chain), 200
    return jsonify(chain_snapshot), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

