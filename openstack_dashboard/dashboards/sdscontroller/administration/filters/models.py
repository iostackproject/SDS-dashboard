class Filter:
    """
        Filters class represents the filter data
    """

    def __init__(self, filter_id, filter_name, filter_type, dependencies, interface_version, object_metadata, main, is_put, is_get, has_reverse,
                 execution_server, execution_server_reverse, is_pre_put, is_post_put, is_pre_get, is_post_get):
        """

        :param filter_id:
        :param filter_name:
        :param filter_type:
        :param dependencies:
        :param interface_version:
        :param object_metadata:
        :param main:
        :param is_put:
        :param is_get:
        :param has_reverse:
        :param execution_server:
        :param execution_server_reverse:
        :param is_pre_put:
        :param is_post_put:
        :param is_pre_get:
        :param is_post_get:
        """
        self.id = filter_id
        self.filter_name = filter_name
        self.filter_type = filter_type
        self.interface_version = interface_version
        self.dependencies = dependencies
        self.object_metadata = object_metadata
        self.main = main
        self.is_put = is_put
        self.is_get = is_get
        self.has_reverse = has_reverse
        self.execution_server = execution_server
        self.execution_server_reverse = execution_server_reverse

        self.is_pre_put = is_pre_put
        self.is_post_put = is_post_put
        self.is_pre_get = is_pre_get
        self.is_post_get = is_post_get
