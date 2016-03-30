class Filter:
    """
        Filters class represents the filter data
    """
    def __init__(self, id, name, language, dependencies, interface_version, object_metadata, main, is_put, is_get, has_reverse, execution_server_default, execution_server_reverse):
        """

        :param id:
        :param name:
        :param language:
        :param dependencies:
        :param interface_version:
        :param object_metadata:
        :param main:
        :param is_put:
        :param is_get:
        :param has_reverse:
        :param execution_server_default:
        :param execution_server_reverse:
        """
        self.id = id
        self.name = name
        self.language = language
        self.interface_version = interface_version
        self.dependencies = dependencies
        self.object_metadata = object_metadata
        self.main = main
        self.is_put = is_put
        self.is_get = is_get
        self.has_reverse = has_reverse
        self.execution_server = execution_server_default
        self.execution_server_reverse = execution_server_reverse
