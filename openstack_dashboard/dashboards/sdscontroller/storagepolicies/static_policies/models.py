class Policy:
    """
        Policy class represents the policy data
    """

    def __init__(self, id_, object_type, object_size, execution_server, execution_server_reverse, params):
        self.id = id_
        self.object_type = object_type
        self.object_size = object_size
        self.execution_server = execution_server
        self.execution_server_reverse = execution_server_reverse
        self.params = params
