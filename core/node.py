from flask import Flask, jsonify
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


@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain 
        blockchain = Blockchain(wallet.public_key)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Saving the keys failed, but created"
        }
        return jsonify(response), 500


@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.mine_block()
    """NO NEED TO CONVERT TO __dict__ BECAUSE @dataclass USED"""
    if block != None:
        response = {
            "message": "Block added sucessfully.",
            "block":block
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

