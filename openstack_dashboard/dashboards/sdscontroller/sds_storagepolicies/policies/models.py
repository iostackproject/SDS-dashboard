class Policy:
    """
        Policy class represents the storage policy
    """
    def __init__(self, id, name, san_name, throttle_iops_read, throttle_iops_write, throttle_mbps_read, throttle_mbps_write, tier, filters, created_at):
        self.id = id
        self.name = name
        self.san_name = san_name
        self.throttle_iops_read = throttle_iops_read
        self.throttle_iops_write = throttle_iops_write 
        self.throttle_mbps_read = throttle_mbps_read 
        self.throttle_mbps_write = throttle_mbps_write
        self.tier = tier        
        self.filters = filters
        self.created_at = created_at