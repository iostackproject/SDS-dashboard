from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from horizon import exceptions

from openstack_dashboard.dashboards.sdscontroller.storagepolicies.policies import tables as policies_tables
from openstack_dashboard.dashboards.sdscontroller.storagepolicies.policies import models as policies_models

from openstack_dashboard.dashboards.sdscontroller import api_sds_controller as api
import json


class PolicyTab(tabs.TableTab):
    name = _("Policy Tab")
    slug = "policy_tab"
    table_classes = (policies_tables.PoliciesTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def get_policies_data(self):
        try:
            response = api.list_policies()
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to retrieve policies information.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            ret.append(policies_models.Policy(inst["id"], inst['policy_description'], inst['policy_location'], inst['alive']))
        return ret


class PoliciesGroupTabs(tabs.TabGroup):
    slug = "policies_group_tabs"
    tabs = (PolicyTab,)
    sticky = True
