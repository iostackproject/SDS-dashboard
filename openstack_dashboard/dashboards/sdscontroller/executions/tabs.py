from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

#from openstack_dashboard import api
from openstack_dashboard.api import zoeapi
from openstack_dashboard.dashboards.sdscontroller.executions import tables
from openstack_dashboard.dashboards.sdscontroller.executions.models import Execution
import json

class ExecutionsTab(tabs.TableTab):
    name = _("Executions Tab")
    slug = "executions_tab"
    table_classes = (tables.ExecutionsTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False


    def get_executions_data(self):
        executions = []
        try:
            res = zoeapi.exec_list_cmd(self.request)
            executionsdata = zoeapi.list_zoe_exec()
            for e in executionsdata:
                try:
                    ex = Execution(e['id'], e['application']['name'], e['name'], e['time_started'], e['time_scheduled'], e['time_finished'], e['status'])
                except:
                    print("Unable to build Execution from {}".format(e))
                    continue
                executions.append(ex)
        except Exception:
            error_message = _('Unable to get zoe executions')
            exceptions.handle(self.request, error_message)
        return executions


class MypanelTabs(tabs.TabGroup):
    slug = "mypanel_tabs"
    tabs = (ExecutionsTab,)
    sticky = True