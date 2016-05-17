class Policy:
    """
        Policy class represents the policy data
    """

    def __init__(self, id_, policy_description, policy_location, alive):
        self.id = id_
        self.policy_description = policy_description
        self.policy_location = policy_location
        self.alive = alive
