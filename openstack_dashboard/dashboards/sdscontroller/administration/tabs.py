from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
import json

from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import tables as registry_tables
from openstack_dashboard.dashboards.sdscontroller.administration.filters import tables as filter_tables
from openstack_dashboard.dashboards.sdscontroller.administration.filters import models as filters_models

from openstack_dashboard.dashboards.sdscontroller import api_sds_controller as api


class RegistryTab(tabs.TableTab):
    table_classes = (registry_tables.InstancesTable,)
    name = _("Registry DSL")
    slug = "registry_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_instances_data(self):
        # try:
        #     marker = self.request.GET.get(
        #                 registry_tables.InstancesTable._meta.pagination_param, None)
        #
        #     instances, self._has_more = api.nova.server_list(
        #         self.request,
        #         search_opts={'marker': marker, 'paginate': True})
        #
        #     return instances
        # except Exception:
        #     self._has_more = False
        #     error_message = _('Unable to get instances')
        #     exceptions.handle(self.request, error_message)

            return []


class TenantList(tabs.TableTab):
    table_classes = (registry_tables.InstancesTable,)
    name = _("Tenant List")
    slug = "tenant_list_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_instances_data(self):
        # try:
        #     marker = self.request.GET.get(
        #                 registry_tables.InstancesTable._meta.pagination_param, None)
        #
        #     instances, self._has_more = api.nova.server_list(
        #         self.request,
        #         search_opts={'marker': marker, 'paginate': True})
        #
        #     return instances
        # except Exception:
        #     self._has_more = False
        #     error_message = _('Unable to get instances')
        #     exceptions.handle(self.request, error_message)

            return []


class Filters(tabs.TableTab):
    table_classes = (filter_tables.FilterTable,)
    name = _("Filters")
    slug = "filters_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_filters_data(self):
        # TODO call sds api

        try:
            response = api.fil_list_filters()
            response.status_code = 201
            print "sdscontroller.administration.filters.getdata response", response.status_code, response.text
            if response.status_code != 200:
                # TODO VERY BIG
                # error_message = _('Unable to get instances')
                # exceptions.handle(self.request, error_message)
                print "ERROR: sdscontroller.administration.filters.getdata response.code", response.status_code
                strobj = '[{ "name": "UOneTrace-1.0.jar", "language": "Java", "interface_version": "1.0", "object_metadata": "no", "dependencies": "", "main_class": "com.urv.storlet.uonetrace.UOneTraceStorlet", "path": "/home/vagrant/src/sds_controller/storlet/storlets_jar/UOneTrace-1.0.jar", "id": "2" }]'
            else:
                strobj = response.text
        except Exception as e:
            print "ERROR: sdscontroller.administration.filters.getdata exception", e
            strobj = '[{ "name": "UOneTrace-1.0.jar", "language": "Java", "interface_version": "1.0", "object_metadata": "no", "dependencies": "", "main_class": "com.urv.storlet.uonetrace.UOneTraceStorlet", "path": "/home/vagrant/src/sds_controller/storlet/storlets_jar/UOneTrace-1.0.jar", "id": "2" }]'

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            ret.append(filters_models.Filter(inst["id"], inst['name'], inst['language'], inst['interface_version'], inst['dependencies'], inst['object_metadata'], inst['main_class']))
        return ret


class BW(tabs.TableTab):
    table_classes = (registry_tables.InstancesTable,)
    name = _("BW Differentiation")
    slug = "bw__table"
    template_name = ("horizon/common/_detail_table.html")

    def get_instances_data(self):
        # try:
        #     marker = self.request.GET.get(
        #                 registry_tables.InstancesTable._meta.pagination_param, None)
        #
        #     instances, self._has_more = api.nova.server_list(
        #         self.request,
        #         search_opts={'marker': marker, 'paginate': True})
        #
        #     return instances
        # except Exception:
        #     self._has_more = False
        #     error_message = _('Unable to get instances')
        #     exceptions.handle(self.request, error_message)

            return []


class MypanelTabs(tabs.TabGroup):
    slug = "mypanel_tabs"
    tabs = (RegistryTab, Filters, BW, TenantList)
    sticky = True

