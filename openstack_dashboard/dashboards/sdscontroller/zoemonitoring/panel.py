from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.sdscontroller import dashboard


class Zoemonitoring(horizon.Panel):
    name = _("Zoe Monitoring")
    slug = "zoemonitoring"


dashboard.SDSController.register(Zoemonitoring)
