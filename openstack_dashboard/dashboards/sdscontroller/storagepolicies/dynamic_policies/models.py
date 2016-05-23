class Policy:
    """
        Policy class represents the policy data
    """

    def __init__(self, id_, policy, policy_location, alive):
        self.id = id_
        self.policy = policy
        self.policy_location = policy_location
        self.alive = alive
