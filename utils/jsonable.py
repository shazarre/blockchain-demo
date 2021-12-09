import abc


class Jsonable(abc.ABC):
    @abc.abstractmethod
    def to_json(self):
        raise NotImplementedError("to_json not implemented")

    @staticmethod
    @abc.abstractmethod
    def from_json(data):
        raise NotImplementedError("from_json not implemented")
