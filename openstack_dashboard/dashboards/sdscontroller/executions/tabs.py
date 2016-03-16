from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

#from openstack_dashboard import api
from openstack_dashboard.api import zoeapi
from openstack_dashboard.dashboards.sdscontroller.executions import tables
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
            print("Zoe API executed")
            executionsdata = zoeapi.list_zoe_exec()
            print("LEN: ", len(executionsdata))
            for el in executionsdata:
                #Execution(id, app_name, exec_name, submit_date, sched_date, fin_date, status)
                #keys() = [u'status', u'time_finished', u'time_started', u'time_scheduled', u'application', u'owner', u'id', u'containers', u'name']
                try:
                    ex = Execution(el['id'], el['application'], el['exec'], el['time_started'], el['time_scheduled'], el['time_finished'], el['status'])
                except:
                    print(el['id'], el['application'], el['exec'], el['time_started'], el['time_scheduled'], el['time_finished'], el['status'])
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