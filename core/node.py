from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from argparse import ArgumentParser

from wallet import Wallet
from blockchain import Blockchain


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('ui', 'node.html')


@app.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('ui', 'network.html')


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
        blockchain = Blockchain(wallet.public_key, port)
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
        blockchain = Blockchain(wallet.public_key, port)
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
    if blockchain.resolve_conflicts:
        response = {'message': 'Resolve conflicts first, block not added!'}
        return jsonify(response), 409
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


@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    transactions = blockchain.get_open_transactions()
    return jsonify(transactions), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    """NO NEED TO CONVERT TO __dict__ BECAUSE @dataclass USED"""
    # dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    # for dict_block in dict_chain:
    #     dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']] 
    # return jsonify(dict_chain), 200
    return jsonify(chain_snapshot), 200


@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            "message": "Send correct data"
        }
        return jsonify(response), 400
    if 'node' not in values:
        response = {
            "message": "Required fields are missing"
        }
        return jsonify(response), 400
    node = values['node']
    blockchain.add_peer_node(node)
    response = {
            "message": "Node added successfully",
            "all_nodes": blockchain.get_peer_nodes()
        }
    return jsonify(response), 201


@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        response = {
            "message": "No node found"
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
            "message": "Node removed successfully",
            "all_nodes": blockchain.get_peer_nodes()
        }
    return jsonify(response), 200


@app.route('/node', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    response = {
        "all_nodes": nodes
    }
    return jsonify(response), 200


@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    if not request.is_json:
        response = {
            "message": "Send correct data"
        }
        return jsonify(response), 400
    values = request.get_json()
    required_fields = ['sender', 'recipient', 'amount', 'signature']
    if not all(field in values for field in required_fields):
        response = {
            "message": "Required fields are missing"
        }
        return jsonify(response), 400
    success = blockchain.add_transaction(values['recipient'], values['sender'], values['amount'], values['signature'], is_receiving=True)
    if success:
        response = {
            "message": "Transaction completed successfully.",
            "transaction": {
                "sender": values['sender'],
                "recipient": values['recipient'],
                "amount": values['amount'],
                "signature": values['signature']
            }
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "X Creating a transaction failed X."
        }
        return jsonify(response), 500
    

@app.route('/broadcast-block', methods=['POST'])
def broadcast_block():
    if not request.is_json:
        response = {
            "message": "Send correct data"
        }
        return jsonify(response), 400
    values = request.get_json()
    if 'block' not in values:
        response = {
            "message": "Required fields are missing"
        }
        return jsonify(response), 400
    block = values['block']
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {'message': 'Block added'}
            return jsonify(response), 201
        else:
            response = {'message': 'Block invalid'}
            return jsonify(response), 409
    elif block['index'] > blockchain.chain[-1].index:
        response = {
            'message': 'Blockchain seems to be differ from local blockchain.'
        }
        blockchain.resolve_conflicts = True
        return jsonify(response), 200
    else:
        response = {
            'message': 'Blockchain seems to be shorter, block not added'
        }
        return jsonify(response), 409



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args()
    port = args.port
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host='0.0.0.0', port=port)

