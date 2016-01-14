from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
import json

from openstack_dashboard.dashboards.sdscontroller.rings_and_accounts.storage_policies import tables as storagepolicies_tables


class StoragePolicies(tabs.TableTab):
    table_classes = (storagepolicies_tables.StoragePolicyTable,)
    name = _("Storage Policies")
    slug = "storagepolicies_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_storagepolicies_data(self):
        return []



class MypanelTabs(tabs.TabGroup):
    slug = "mypanel_tabs"
    tabs = (StoragePolicies,)
    sticky = True

