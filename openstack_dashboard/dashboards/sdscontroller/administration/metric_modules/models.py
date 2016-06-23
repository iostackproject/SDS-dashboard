class MetricModule:
    """
        Metric Module class represents the metric module data
    """

    def __init__(self, id_, name, interface_version, object_metadata, is_put, is_get, execution_server):
        """

        :param id_:
        :param name:
        :param interface_version:
        :param object_metadata:
        :param is_put:
        :param is_get:
        :param execution_server:
        """
        self.id = id_
        self.name = name
        self.interface_version = interface_version
        self.object_metadata = object_metadata
        self.is_put = is_put
        self.is_get = is_get
        self.execution_server = execution_server
