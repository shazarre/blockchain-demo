import time
from typing import List

from blockchain.block import Block
from blockchain.chain import Chain
from blockchain.node import Node
from blockchain.proof_of_work import ProofOfWork
from coin.transaction import Transaction


class Blockchain:
    chain: Chain
    mempool: List[Transaction]
    nodes: List[Node]
    proof_of_work: ProofOfWork

    def __init__(self, proof_of_work: ProofOfWork, chain: Chain):
        self.chain = chain
        self.mempool = []
        genesis_block = self.create_block(proof=1)
        self.add_block(genesis_block)
        self.nodes = []
        self.proof_of_work = proof_of_work

    def create_block(self, proof, data=None) -> Block:
        previous_block = self.chain.get_last_block()

        if data is None:
            data = {}

        block = Block(
            index=len(self.chain),
            timestamp=time.time_ns(),
            proof=proof,
            previous_hash=None if previous_block is None else previous_block.get_hash(),
            data=data,
            transactions=[*self.mempool],
        )

        return block

    def add_node(self, node: Node) -> bool:
        for n in self.nodes:
            if n == node:
                return False

        self.nodes.append(node)

        return True

    def add_block(self, block: Block):
        self.chain.add_block(block)
        self.mempool = []

    # TODO add check not only for the mempool, but also all the blocks
    def add_transaction(self, transaction: Transaction):
        for t in self.mempool:
            if t == transaction:
                return False

        self.mempool.append(transaction)

        return True

    def get_chain(self) -> Chain:
        return self.chain

    def get_nodes(self) -> List[Node]:
        return self.nodes

    def cleanup_transactions(self):
        for block in self.chain.get_blocks():
            for transaction in block.transactions:
                if transaction in self.mempool:
                    self.mempool.remove(transaction)

    def replace_chain(self, chain: Chain):
        self.chain = chain
        self.cleanup_transactions()
