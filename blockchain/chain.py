from typing import List, Optional

from blockchain.block import Block
from utils.jsonable import Jsonable


class Chain(Jsonable):
    blocks: List[Block]

    def __init__(self, blocks: List[Block]):
        self.blocks = blocks

    def add_block(self, block: Block):
        self.blocks.append(block)

    def get_blocks(self):
        return self.blocks

    def get_last_block(self) -> Optional[Block]:
        if len(self.blocks) > 0:
            return self.blocks[-1]

        return None

    def __len__(self):
        return len(self.blocks)

    def to_json(self):
        return list(map(lambda b: b.to_json(), self.blocks))

    @staticmethod
    def from_json(data):
        if isinstance(data, list):
            return Chain(
                blocks=list(map(lambda item: Block.from_json(item), data))
            )

        # raise otherwise
