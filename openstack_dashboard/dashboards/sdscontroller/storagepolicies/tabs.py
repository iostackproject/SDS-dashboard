from django.utils.translation import ugettext_lazy as _

from horizon import tabs

from openstack_dashboard.dashboards.sdscontroller.storagepolicies.policies import tables as policies_tables


class PolicyTab(tabs.TableTab):
    name = _("Policy Tab")
    slug = "policy_tab"
    table_classes = (policies_tables.PoliciesTable,)
    # template_name = ("sdscontroller/storagepolicies/policies/policies.html")
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def get_policies_data(self):
        return []


class PoliciesGroupTabs(tabs.TabGroup):
    slug = "policies_group_tabs"
    tabs = (PolicyTab,)
    sticky = True
