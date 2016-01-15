class Tenant:
    """
        Tenant class represents the Projects in the System
    """
    def __init__(self, id, name, description, enabled):
        self.id = id
        self.name = name
        self.description = description
        self.enabled = enabled
