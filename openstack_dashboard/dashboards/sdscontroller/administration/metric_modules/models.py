class MetricModule:
    """
        Metric Module class represents the metric module data
    """

    def __init__(self, metric_module_id, class_name, out_flow, in_flow, execution_server):
        """

        :param metric_module_id:
        :param out_flow:
        :param in_flow:
        :param execution_server:
        """
        self.id = metric_module_id
        self.class_name = class_name
        self.out_flow = out_flow
        self.in_flow = in_flow
        self.execution_server = execution_server
