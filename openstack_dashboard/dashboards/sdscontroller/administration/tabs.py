from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
import json

from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import tables as registry_tables
from openstack_dashboard.dashboards.sdscontroller.administration.filters import tables as filter_tables
from openstack_dashboard.dashboards.sdscontroller.administration.filters import models as filters_models
from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import models as registry_models
from openstack_dashboard.dashboards.sdscontroller.administration.tenants import tables as tenant_tables
from openstack_dashboard.dashboards.sdscontroller.administration.tenants import models as tenant_models
from openstack_dashboard.dashboards.sdscontroller.administration.groups import tables as group_tables
from openstack_dashboard.dashboards.sdscontroller.administration.groups import models as group_models

from openstack_dashboard.dashboards.sdscontroller import api_sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class RegistryTab(tabs.TableTab):
    table_classes = (registry_tables.DslFilterTable,)
    name = _("Registry DSL")
    slug = "registry_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_dsl_filters_data(self):
        try:
            response = api.dsl_get_all_filters(self.request)
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
    table_classes = (tenant_tables.TenantsTable,)
    name = _("Tenant List")
    slug = "tenant_list_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_tenants_data(self):
        try:
            response = api.swift_list_tenants(self.request)
            print "CAMAMILLA ADMINISTRATION tabs tenants response", response.status_code, response.text
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get tenants. %s' % response.text
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "{}"
            exceptions.handle(self.request, _(e.message))

        instances = json.loads(strobj)
        ret = []
        if "tenants" in instances:
            for inst in instances["tenants"]:
                ret.append(tenant_models.Tenant(inst['id'], inst['name'], inst['description'], inst['enabled']))
        return ret


class Filters(tabs.TableTab):
    table_classes = (filter_tables.FilterTable,)
    name = _("Filters")
    slug = "filters_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_filters_data(self):
        try:
            response = api.fil_list_filters(self.request)
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
            ret.append(filters_models.Filter(inst["id"], inst['name'], inst['language'], inst['dependencies'], inst['interface_version'], inst['object_metadata'], inst['main']))
        return ret


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


class Groups(tabs.TableTab):
    table_classes = (group_tables.GroupsTable,)
    name = _("Groups")
    slug = "groups_table"
    template_name = ("horizon/common/_detail_table.html")

    def get_groups_data(self):
        ret = []
        try:
            response = api.dsl_get_all_tenants_groups(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get tenants groups.'
                raise sdsexception.SdsException(error_message)

            instances = eval(strobj)
            for k, v in instances.iteritems():
                ret.append(group_models.Group(k, v))
        except Exception as e:
            exceptions.handle(self.request, _(e.message))

        return ret

class MypanelTabs(tabs.TabGroup):
    slug = "mypanel_tabs"
    tabs = (RegistryTab, Filters, BW, TenantList, Groups,)
    sticky = True

