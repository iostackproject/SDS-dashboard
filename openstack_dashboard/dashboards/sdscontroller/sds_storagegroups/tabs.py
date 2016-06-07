from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from horizon import exceptions

from openstack_dashboard.dashboards.sdscontroller.sds_storagegroups.groups import tables as groups_tables
from openstack_dashboard.dashboards.sdscontroller.sds_storagegroups.groups import models as groups_models

from openstack_dashboard.api import sds_controller_blockstorage as api
import json
import requests


class GroupTab(tabs.TableTab):
    name = _("Group Tab")
    slug = "group_tab"
    table_classes = (groups_tables.GroupsTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def get_groups_data(self):
        #
        ret = []
        try:           
            resp = api.list_storagegroups()
            if 200 <= resp.status_code < 300:
                data = resp.json()
                for value in data:
                    ret.append(groups_models.Group(value["id"], value["name"], value["policy"], value["nodes"],value["created_at"]))
            else:
                error_message = 'Unable to retrieve groups information.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))
        return ret

class GroupsGroupTabs(tabs.TabGroup):
    slug = "groups_group_tabs"
    tabs = (GroupTab,)
    sticky = True
