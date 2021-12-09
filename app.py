import os
import sys
from typing import Optional

import requests
from flask import Flask, request, abort

from blockchain.blockchain import Blockchain
from blockchain.chain import Chain
from blockchain.chain_validator import ChainValidator
from blockchain.node import Node
from blockchain.proof_of_work import ProofOfWork
from coin.transaction import Transaction
from utils.url_builder import UrlBuilder

app = Flask(__name__)

# TODO inject via config/env
mining_target = int("00000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16)
proof_of_work = ProofOfWork(target=mining_target)
blockchain = Blockchain(proof_of_work=proof_of_work, chain=Chain(blocks=[]))

blockchain.add_node(Node(address=os.environ["APP_ADDRESS"]))


@app.route('/mine')
def mine():
    proof = proof_of_work.find_next(blockchain.get_chain().get_last_block().get_hash())
    block = blockchain.create_block(proof)

    blockchain.add_block(block)

    # TODO parallelize and extract the logic to a separate class
    for node in blockchain.get_nodes():
        if node.is_self():
            continue

        requests.get(UrlBuilder.build_get_sync_url(node))

    return {
        "block": block.to_json(),
    }


@app.route('/chain')
def get_chain():
    return {
        "chain": blockchain.get_chain().to_json()
    }


@app.route('/sync')
def get_sync():
    chain = blockchain.chain
    longest_chain: Optional[Chain] = None
    max_length = len(chain)

    # TODO parallelize and extract the logic to a separate class
    for node in blockchain.get_nodes():
        if node.is_self():
            continue

        response = requests.get(UrlBuilder.build_get_chain_url(node))
        validator = ChainValidator(proof_of_work=proof_of_work)

        if response.status_code == 200:
            try:
                chain = Chain.from_json(response.json()["chain"])

                if validator.validate(chain):
                    chain_length = len(chain)

                    if chain_length > max_length:
                        longest_chain = chain
            except Exception as e:
                # TODO add proper logging
                print(e, file=sys.stderr)
                pass

    if longest_chain:
        blockchain.replace_chain(longest_chain)

    return {
        "chain": blockchain.get_chain().to_json(),
    }


@app.route('/nodes')
def get_nodes():
    return {"nodes": list(map(lambda n: n.to_json(), blockchain.get_nodes()))}


@app.route('/transaction', methods=['POST'])
def post_transaction():
    propagate_transaction = request.args.get("propagate", "1") == "1"
    transaction_data = request.get_json()
    transaction: Optional[Transaction] = None

    try:
        transaction = Transaction.from_json(transaction_data)

        blockchain.add_transaction(transaction)
    except Exception:
        # TODO add logging
        return abort(400, "Wrong transaction data")

    if transaction and propagate_transaction:
        nodes = blockchain.get_nodes()

        # TODO parallelize and extract the logic to a separate class
        for node in nodes:
            if node.is_self():
                continue
            try:
                requests.post(UrlBuilder.build_post_transaction_url(
                    node=node,
                    propagate=False
                ), json=transaction.to_json())
            except Exception as e:
                # TODO add proper logging
                print(e, file=sys.stderr)
                pass

    return transaction.to_json()


@app.route('/node', methods=['POST'])
def post_node():
    node_data = request.get_json()
    node: Optional[Node] = None

    try:
        node = Node.from_json(node_data)
    except Exception:
        # TODO add logging
        return abort(400, "Wrong node data")

    # TODO parallelize and extract the logic to a separate class
    if node:
        original_nodes = blockchain.get_nodes()

        if blockchain.add_node(node):
            for original_node in original_nodes:
                try:
                    requests.post(UrlBuilder.build_post_node_url(node), json=original_node.to_json())
                except Exception as e:
                    # TODO add proper logging
                    print(e, file=sys.stderr)
                    pass

    return node.to_json()


if __name__ == '__main__':
    app.run(port=os.environ.get("APP_PORT", "5000"))
