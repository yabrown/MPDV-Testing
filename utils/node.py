class Node:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

class NodeRequestError(Exception):
    """Raised when there is an issue with a node request."""
    pass

class NodeResponseError(Exception):
    """Raised when the node response is invalid."""
    pass