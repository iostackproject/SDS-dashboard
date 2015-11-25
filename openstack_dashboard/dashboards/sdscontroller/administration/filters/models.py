class Filter:
    """
        Filters class represents the filter data
    """
    def __init__(self, id, name, lenguage, dependencies, interface_version, object_metadata, main, deployed):
        self.id = id
        self.name = name
        self.lenguage = lenguage
        self.interface_version = interface_version
        self.dependencies = dependencies
        self.object_metadata = object_metadata
        self.main = main
        self.deployed = deployed

