import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception
from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.proxy_sorting import models as proxy_sorting_models
from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.proxy_sorting import tables as proxy_sorting_tables
from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.slas import models as slas_models
from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.slas import tables as slas_tables


class SLAsTab(tabs.TableTab):
    table_classes = (slas_tables.SLAsTable,)
    name = _("SLAs")
    slug = "slas_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_slas_data(self):
        try:
            response = api.bw_get_all_slas(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get instances.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            ret.append(slas_models.SLA(inst['project_id'], inst['project_name'], inst['policy_id'], inst['policy_name'], inst['bandwidth']))
        return ret


class ProxySortingTab(tabs.TableTab):
    table_classes = (proxy_sorting_tables.ProxySortingTable,)
    name = _("Proxy Sorting")
    slug = "proxy_sorting_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_proxy_sorting_data(self):
        try:
            response = api.bw_get_all_sort_method(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get instances.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            ret.append(proxy_sorting_models.ProxySorting(inst['id'], inst['name'], inst['criterion']))
        return ret


class MypanelTabs(tabs.TabGroup):
    slug = "mypanel_tabs"
    #tabs = (SLAsTab, ProxySortingTab,)
    tabs = (SLAsTab, )
    sticky = True
