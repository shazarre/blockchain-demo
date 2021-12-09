import hashlib


# TODO add methods to change the target
class ProofOfWork:
    target: int

    def __init__(self, target: int):
        self.target = target

    def check(self, proof_of_work: int, previous_block_hash: str):
        digest = hashlib.sha256(' '.join([str(proof_of_work), previous_block_hash]).encode()).hexdigest()

        if int(digest, 16) <= self.target:
            return True

        return False

    def find_next(self, previous_block_hash: str):
        new_proof = 1
        check_proof = False

        while not check_proof:
            if self.check(new_proof, previous_block_hash):
                return new_proof
            else:
                new_proof += 1

        return new_proof
