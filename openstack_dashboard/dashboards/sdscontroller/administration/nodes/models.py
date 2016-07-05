class Node:
    """
        Node class defines a swift node. The identifier is the name of the node.
    """
    def __init__(self, name, ip, last_ping, type):
        self.id = name
        self.ip = ip
        self.last_ping = last_ping
        self.type = type