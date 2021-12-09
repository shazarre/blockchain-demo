from blockchain.node import Node


class UrlBuilder:
    @staticmethod
    def build_get_chain_url(node: Node) -> str:
        return f'{node.get_scheme()}://{node.get_netloc()}/chain'

    @staticmethod
    def build_get_sync_url(node: Node) -> str:
        return f'{node.get_scheme()}://{node.get_netloc()}/sync'

    @staticmethod
    def build_post_node_url(node: Node) -> str:
        return f'{node.get_scheme()}://{node.get_netloc()}/node'

    @staticmethod
    def build_post_transaction_url(node: Node, propagate: bool) -> str:
        return f'{node.get_scheme()}://{node.get_netloc()}/transaction?propagate={"1" if propagate else "0"}'
