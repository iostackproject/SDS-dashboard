class Filter:
    """
        Registry class represents the Registry DSL data
    """
    def __init__(self, id, name, activation_url, valid_parameters):
        self.id = name
        self.name = name
        self.filter_identifier = id
        self.activation_url = activation_url
        self.valid_parameters = valid_parameters
