from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
import json

from openstack_dashboard.dashboards.sdscontroller.rings_and_accounts.storage_policies import tables as storagepolicies_tables
from openstack_dashboard.dashboards.sdscontroller.rings_and_accounts.storage_policies import models as storage_policies_models

from openstack_dashboard.api import sds_controller as api

class StoragePolicies(tabs.TableTab):
    table_classes = (storagepolicies_tables.StoragePolicyTable,)
    name = _("Storage Policies")
    slug = "storagepolicies_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_storagepolicies_data(self):
        try:
            response = api.list_storage_nodes(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
                print 'strobj', strobj
            else:
                error_message = 'Unable to get storage nodes.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            ret.append(storage_policies_models.StorageNode(inst['id'], inst['name'], inst['location'], inst['type']))
        return ret


class MypanelTabs(tabs.TabGroup):
    slug = "mypanel_tabs"
    tabs = (StoragePolicies,)
    sticky = True

