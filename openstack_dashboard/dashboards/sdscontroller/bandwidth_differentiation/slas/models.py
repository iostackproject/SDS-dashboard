class SLA:
    """
        SLA class models.
    """

    def __init__(self, tenant, policy, bandwidth):
        self.policy = policy
        self.tenant = tenant
        self.bandwidth = bandwidth
