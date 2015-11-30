from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
import json
from openstack_dashboard import api

from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import tables as registry_tables
from openstack_dashboard.dashboards.sdscontroller.administration.filters import tables as filter_tables
from openstack_dashboard.dashboards.sdscontroller.administration.filters import models as filters_models


class RegistryTab(tabs.TableTab):
    table_classes = (registry_tables.InstancesTable,)
    name = _("Registry DSL")
    slug = "registry_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_instances_data(self):
        try:
            marker = self.request.GET.get(
                        registry_tables.InstancesTable._meta.pagination_param, None)

            instances, self._has_more = api.nova.server_list(
                self.request,
                search_opts={'marker': marker, 'paginate': True})

            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []


class TenantList(tabs.TableTab):
    table_classes = (registry_tables.InstancesTable,)
    name = _("Tenant List")
    slug = "tenant_list_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_instances_data(self):
        try:
            marker = self.request.GET.get(
                        registry_tables.InstancesTable._meta.pagination_param, None)

            instances, self._has_more = api.nova.server_list(
                self.request,
                search_opts={'marker': marker, 'paginate': True})

            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []


class Filters(tabs.TableTab):
    table_classes = (filter_tables.FilterTable,)
    name = _("Filters")
    slug = "filters_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_filters_data(self):
        #strobj call api
        strobj = '[{"id":1445,"name":"filterName","language":"Java","interface_version":"1.0","dependencies":"''","object_metadata":"no","main":"com.urv.filter.uonetrace.UOneTracefilter","deployed":"false"}, {"id":1345,"name":"filterName","language":"Java","interface_version":"1.0","dependencies":"''","object_metadata":"no","main":"com.urv.filter.uonetrace.UOneTracefilter","deployed":"false"}]'
        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            ret.append(filters_models.Filter(inst['id'], inst['name'], inst['language'], inst['interface_version'], inst['dependencies'], inst['object_metadata'], inst['main'], inst['deployed']))
        return ret


class BW(tabs.TableTab):
    table_classes = (registry_tables.InstancesTable,)
    name = _("BW Differentiation")
    slug = "bw__table"
    template_name = ("horizon/common/_detail_table.html")

    def get_instances_data(self):
        try:
            marker = self.request.GET.get(
                        registry_tables.InstancesTable._meta.pagination_param, None)

            instances, self._has_more = api.nova.server_list(
                self.request,
                search_opts={'marker': marker, 'paginate': True})

            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []


class MypanelTabs(tabs.TabGroup):
    slug = "mypanel_tabs"
    tabs = (RegistryTab, Filters, BW, TenantList)
    sticky = True

