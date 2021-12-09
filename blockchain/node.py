import os
from urllib.parse import urlparse

from utils.jsonable import Jsonable


class Node(Jsonable):
    address: str
    netloc: str
    scheme: str
    path: str

    def __init__(self, address):
        self.address = address
        # TODO raise if any error
        parsed_address = urlparse(address)
        self.netloc = parsed_address.netloc
        self.scheme = parsed_address.scheme
        self.path = parsed_address.path

    def get_address(self):
        return self.address

    def get_netloc(self):
        return self.netloc

    def get_scheme(self):
        return self.scheme

    def get_path(self):
        return self.path

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.get_address() == other.get_address()

        return False

    def is_self(self):
        return self.address == os.environ.get("APP_ADDRESS")

    @staticmethod
    def from_json(data):
        address = None

        if isinstance(data["address"], str):
            address = data["address"]

        return Node(
            address=address,
        )

    def to_json(self):
        return {
            "address": self.address
        }
