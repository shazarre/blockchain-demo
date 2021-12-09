import hashlib
import json
from typing import List

from coin.transaction import Transaction
from utils.jsonable import Jsonable


class Block(Jsonable):
    data: dict
    transactions: List[Transaction]

    def __init__(self, index, timestamp, proof, previous_hash, data: dict, transactions: List[Transaction]):
        self.index = index
        self.timestamp = timestamp
        self.proof = proof
        self.previous_hash = previous_hash
        self.data = data
        self.transactions = transactions

    def get_hash(self) -> str:
        data_json = json.dumps(self.to_json(), sort_keys=True)

        return hashlib.sha256(data_json.encode()).hexdigest()

    def get_transactions(self) -> List[Transaction]:
        return self.transactions

    def to_json(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "proof": self.proof,
            "previous_hash": self.previous_hash,
            "data": self.data,
            "transactions": list(map(lambda t: t.to_json(), self.transactions)),
        }

    @staticmethod
    def from_json(block_json):
        index = None
        timestamp = None
        proof = None
        previous_hash = None
        data = None
        transactions = None

        if isinstance(block_json["index"], int):
            index = block_json["index"]

        if isinstance(block_json["timestamp"], int):
            timestamp = block_json["timestamp"]

        if isinstance(block_json["proof"], int):
            proof = block_json["proof"]

        if isinstance(block_json["previous_hash"], str):
            previous_hash = block_json["previous_hash"]

        if isinstance(block_json["data"], dict):
            data = block_json["data"]

        if isinstance(block_json["transactions"], list):
            transactions = list(
                map(
                    lambda transaction_data: Transaction.from_json(transaction_data),
                    block_json["transactions"]
                )
            )

        # TODO check if anything is None and raise if that's the case

        return Block(
            index=index,
            timestamp=timestamp,
            proof=proof,
            previous_hash=previous_hash,
            data=data,
            transactions=transactions,
        )
