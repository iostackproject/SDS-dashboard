from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
import json

from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import tables as registry_tables
from openstack_dashboard.dashboards.sdscontroller.administration.filters import tables as filter_tables
from openstack_dashboard.dashboards.sdscontroller.administration.filters import models as filters_models
from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import models as registry_models
from openstack_dashboard.dashboards.sdscontroller.administration.storage_policies import tables as storagepolicies_tables

storagepolicies_tables
from openstack_dashboard.dashboards.sdscontroller import api_sds_controller as api


class RegistryTab(tabs.TableTab):
    table_classes = (registry_tables.DslFilterTable,)
    name = _("Registry DSL")
    slug = "registry_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_dsl_filters_data(self):
        try:
            response = api.dsl_get_all_filters()
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get filters.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            ret.append(registry_models.Filter(inst['identifier'], inst['name'], inst['activation_url'], inst['valid_parameters']))
        return ret


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
        try:
            response = api.fil_list_filters()
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get instances.'
                raise ValueError(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            ret.append(filters_models.Filter(inst["id"], inst['name'], inst['language'], inst['dependencies'], inst['interface_version'], inst['object_metadata'], inst['main']))
        return ret

class StoragePolicies(tabs.TableTab):
    table_classes = (storagepolicies_tables.StoragePolicyTable,)
    name = _("Storage Policies")
    slug = "storagepolicies_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_storagepolicies_data(self):
        return []

class BW(tabs.TableTab):
    table_classes = (registry_tables.InstancesTable,)
    name = _("BW Differentiation")
    slug = "bw_table"
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
    tabs = (RegistryTab, Filters, BW, TenantList, StoragePolicies)
    sticky = True

