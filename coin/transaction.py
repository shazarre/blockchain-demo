from utils.jsonable import Jsonable


class Transaction(Jsonable):
    uuid: str
    sender: str
    receiver: str
    amount: int

    def __init__(self, uuid: str, sender: str, receiver: str, amount: int):
        self.uuid = uuid
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __eq__(self, other):
        if isinstance(other, Transaction):
            return self.get_uuid() == other.get_uuid()

        return False

    def get_uuid(self):
        return self.uuid

    def to_json(self) -> dict:
        return {
            "uuid": self.uuid,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
        }

    @staticmethod
    def from_json(data: dict):
        uuid = None
        sender = None
        receiver = None
        amount = None

        if isinstance(data["uuid"], str):
            uuid = data["uuid"]

        if isinstance(data["sender"], str):
            sender = data["sender"]

        if isinstance(data["receiver"], str):
            receiver = data["receiver"]

        if isinstance(data["amount"], int):
            amount = data["amount"]

        # TODO check if anything is None and raise if that's the case

        return Transaction(
            uuid=uuid,
            sender=sender,
            receiver=receiver,
            amount=amount,
        )
