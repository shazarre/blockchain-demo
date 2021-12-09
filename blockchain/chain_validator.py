from blockchain.chain import Chain
from blockchain.proof_of_work import ProofOfWork


class ChainValidator:
    proof_of_work: ProofOfWork

    def __init__(self, proof_of_work: ProofOfWork):
        self.proof_of_work = proof_of_work

    def validate(self, chain: Chain) -> bool:
        blocks = chain.get_blocks()
        genesis_blocks = [b for b in blocks if b.previous_hash is None]

        if len(genesis_blocks) != 1:
            return False

        processed_blocks = 0
        previous_block = genesis_blocks[0]

        while True:
            processed_blocks += 1
            previous_block_hash = previous_block.get_hash()
            next_blocks = [b for b in blocks if b.previous_hash == previous_block_hash]

            if len(next_blocks) == 0:
                break

            if len(next_blocks) > 1:
                return False

            if not self.proof_of_work.check(next_blocks[0].proof, previous_block.get_hash()):
                return False

            previous_block = next_blocks[0]

        return processed_blocks == len(blocks)
