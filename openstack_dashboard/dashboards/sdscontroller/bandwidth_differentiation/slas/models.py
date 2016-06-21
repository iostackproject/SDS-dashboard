class SLA:
    """
        SLA class models.
    """

    def __init__(self, tenant_id, tenant_name, policy_id, policy_name, bandwidth):
        self.id = tenant_id + ':' + policy_id
        self.tenant_id = tenant_id
        self.tenant_name = tenant_name
        self.policy_name = policy_name
        self.bandwidth = bandwidth
