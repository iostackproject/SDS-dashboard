from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from horizon import exceptions

from openstack_dashboard.dashboards.sdscontroller.sds_storagepolicies.policies import tables as policies_tables
from openstack_dashboard.dashboards.sdscontroller.sds_storagepolicies.policies import models as policies_models

from openstack_dashboard.api import sds_controller_blockstorage as api
import json
import requests


class PolicyTab(tabs.TableTab):
    name = _("Policy Tab")
    slug = "policy_tab"
    table_classes = (policies_tables.PoliciesTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def get_policies_data(self):
        ret = []
        try:           
            resp = api.list_policies(self.request)
            if 200 <= resp.status_code < 300:
                data = resp.json()
                for value in data:
                    ret.append(policies_models.Policy(value["id"], value["name"], value["san_name"], value["throttle_iops_read"], value["throttle_iops_write"], value["throttle_mbps_read"], value["throttle_mbps_write"], value["tier"], value["filters"], value["created_at"]))
            else:
                error_message = 'Unable to retrieve policies information.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))
        return ret

class PoliciesGroupTabs(tabs.TabGroup):
    slug = "policies_group_tabs"
    tabs = (PolicyTab,)
    sticky = True
