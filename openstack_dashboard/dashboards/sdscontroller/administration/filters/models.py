class Filter:
    """
        Filters class represents the filter data
    """
    def __init__(self, id, name, language, dependencies, interface_version, object_metadata, main):
        self.id = id
        self.name = name
        self.language = language
        self.interface_version = interface_version
        self.dependencies = dependencies
        self.object_metadata = object_metadata
        self.main = main

