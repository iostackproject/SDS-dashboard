class Policy:
    """
        Policy class represents the policy data
    """

    def __init__(self, id_, target, object_type, object_size, execution_server, execution_server_reverse, execution_order, params):
        self.id = id_
        self.target = target
        self.object_type = object_type
        self.object_size = object_size
        self.execution_server = execution_server
        self.execution_server_reverse = execution_server_reverse
        self.execution_order = execution_order
        self.params = params
