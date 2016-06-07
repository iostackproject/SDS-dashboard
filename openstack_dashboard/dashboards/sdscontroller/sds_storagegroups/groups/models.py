class Group:
    """
        Group class represents the storage group
    """
    def __init__(self, id, name, policy, nodes, created_at):
        self.id = id
        self.name = name
        self.policy = policy
        self.nodes = nodes
        self.created_at = created_at
