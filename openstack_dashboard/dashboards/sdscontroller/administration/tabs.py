import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception
from openstack_dashboard.dashboards.sdscontroller.administration.dependencies import models as dependency_models
from openstack_dashboard.dashboards.sdscontroller.administration.dependencies import tables as dependency_tables
from openstack_dashboard.dashboards.sdscontroller.administration.filters import models as filters_models
from openstack_dashboard.dashboards.sdscontroller.administration.filters import tables as filter_tables
from openstack_dashboard.dashboards.sdscontroller.administration.groups import models as group_models
from openstack_dashboard.dashboards.sdscontroller.administration.groups import tables as group_tables
from openstack_dashboard.dashboards.sdscontroller.administration.metric_modules import models as metric_module_models
from openstack_dashboard.dashboards.sdscontroller.administration.metric_modules import tables as metric_module_tables
from openstack_dashboard.dashboards.sdscontroller.administration.nodes import models as nodes_models
from openstack_dashboard.dashboards.sdscontroller.administration.nodes import tables as nodes_tables
from openstack_dashboard.dashboards.sdscontroller.administration.object_types import models as object_types_models
from openstack_dashboard.dashboards.sdscontroller.administration.object_types import tables as object_types_tables
from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import models as registry_models
from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import tables as registry_tables


class RegistryTab(tabs.TableTab):
    table_classes = (registry_tables.DslFilterTable,)
    name = _("Registry DSL")
    slug = "registry_table"
    template_name = "horizon/common/_detail_table.html"

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
            response = api.fil_get_filter_metadata(self.request, inst['identifier'])
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get filters.'
                raise ValueError(error_message)
            _filter = json.loads(strobj)
            ret.append(registry_models.Filter(inst['identifier'], inst['name'], inst['activation_url'], inst['valid_parameters'], _filter['filter_name']))
        return ret


class Filters(tabs.TableTab):
    table_classes = (filter_tables.StorletFilterTable, filter_tables.NativeFilterTable, filter_tables.GlobalFilterTable)
    name = _("Filters")
    slug = "filters_table"
    #template_name = "horizon/common/_detail_table.html"
    template_name = "sdscontroller/administration/filters/_detail.html"

    def get_storlet_filters_data(self):
        try:
            response = api.fil_list_filters(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get filters.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            if inst['filter_type'] == 'storlet':
                ret.append(filters_models.Filter(inst['id'], inst['filter_name'], inst['filter_type'], inst['dependencies'],
                                                 inst['interface_version'], inst['object_metadata'], inst['main'], inst['has_reverse'],
                                                 inst['execution_server'], inst['execution_server_reverse'],
                                                 inst['is_pre_put'], inst['is_post_put'], inst['is_pre_get'], inst['is_post_get'], 0, False
                                                 ))
        return ret

    def get_native_filters_data(self):
        try:
            response = api.fil_list_filters(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get filters.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            if inst['filter_type'] == 'native':
                ret.append(filters_models.Filter(inst['id'], inst['filter_name'], inst['filter_type'], inst['dependencies'],
                                                 inst['interface_version'], inst['object_metadata'], inst['main'], inst['has_reverse'],
                                                 inst['execution_server'], inst['execution_server_reverse'],
                                                 inst['is_pre_put'], inst['is_post_put'], inst['is_pre_get'], inst['is_post_get'], 0, False
                                                 ))
        return ret

    def get_global_filters_data(self):
        try:
            response = api.fil_list_filters(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get filters.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            if inst['filter_type'] == 'global':
                ret.append(filters_models.Filter(inst['id'], inst['filter_name'], inst['filter_type'], inst['dependencies'],
                                                 inst['interface_version'], inst['object_metadata'], inst['main'], inst['has_reverse'],
                                                 inst['execution_server'], inst['execution_server_reverse'],
                                                 inst['is_pre_put'], inst['is_post_put'], inst['is_pre_get'], inst['is_post_get'],
                                                 inst['execution_order'], inst['enabled']
                                                 ))
        sorted_list = sorted(ret, key=lambda x: int(x.execution_order))
        return sorted_list


class Dependencies(tabs.TableTab):
    table_classes = (dependency_tables.DependenciesTable,)
    name = _("Dependencies")
    slug = "dependencies_table"
    template_name = "horizon/common/_detail_table.html"

    def get_dependencies_data(self):
        try:
            response = api.fil_list_dependencies(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get dependencies.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))

        dependencies = json.loads(strobj)
        ret = []
        for dep in dependencies:
            ret.append(dependency_models.Dependency(dep['id'], dep['name'], dep['version'], dep['permissions']))
        return ret


class MetricModules(tabs.TableTab):
    table_classes = (metric_module_tables.MetricTable,)
    name = _("Workload Metric Modules")
    slug = "metric_modules_table"
    template_name = "horizon/common/_detail_table.html"

    def get_metric_modules_data(self):
        try:
            response = api.mtr_get_all_metric_modules(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get metric modules.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = '[]'
            exceptions.handle(self.request, _(e.message))

        instances = json.loads(strobj)
        ret = []
        for inst in instances:
            ret.append(metric_module_models.MetricModule(inst['id'], inst['metric_name'], inst['class_name'], inst['out_flow'], inst['in_flow'],
                                                         inst['execution_server'], inst['enabled']))
        return ret


class Nodes(tabs.TableTab):
    table_classes = (nodes_tables.ProxysTable, nodes_tables.StorageNodesTable,)
    name = _("Nodes")
    slug = "nodes_table"
    # template_name = "horizon/common/_detail_table.html"
    template_name = "sdscontroller/administration/nodes/_detail.html"

    def get_proxys_data(self):
        ret = []
        try:
            response = api.dsl_get_all_nodes(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get nodes.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = '[]'
            exceptions.handle(self.request, _(e.message))

        nodes = json.loads(strobj)
        for node in nodes:
            if node['type'] == 'proxy':
                ret.append(nodes_models.ProxyNode(node['name'], node['ip'], node['last_ping']))
        return ret

    def get_storagenodes_data(self):
        ret = []
        try:
            response = api.dsl_get_all_nodes(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get nodes.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = '[]'
            exceptions.handle(self.request, _(e.message))

        nodes = json.loads(strobj)
        for node in nodes:
            if node['type'] == 'object':
                devices = []
                # for k, v in node['devices'].iteritems():
                #     used = v['size'] - v['free']
                #     device_str = k + ': ' + str(float(used)/v['size']) + "% used of " + str(v['size']) + ' bytes'
                #     devices.append(device_str)
                ret.append(nodes_models.StorageNode(node['name'], node['ip'], node['last_ping'], node['devices']))
        return ret


class Groups(tabs.TableTab):
    table_classes = (group_tables.GroupsTable,)
    name = _("Groups")
    slug = "groups_table"
    template_name = "horizon/common/_detail_table.html"

    def get_groups_data(self):
        ret = []
        try:
            response = api.dsl_get_all_tenants_groups(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get project groups.'
                raise sdsexception.SdsException(error_message)

            instances = eval(strobj)
            for k, v in instances.items():
                projects = ', '.join(v)
                ret.append(group_models.Group(k, projects))
        except Exception as e:
            exceptions.handle(self.request, _(e.message))
        return ret


class ObjectTypes(tabs.TableTab):
    table_classes = (object_types_tables.ObjectTypesTable,)
    name = _("Object Types")
    slug = "object_types_table"
    template_name = "horizon/common/_detail_table.html"

    def get_object_types_data(self):
        ret = []
        try:
            response = api.dsl_get_all_object_types(self.request)
            if 200 <= response.status_code < 300:
                strobj = response.text
            else:
                error_message = 'Unable to get object types.'
                raise sdsexception.SdsException(error_message)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))

        object_types = json.loads(strobj)
        for ot in object_types:
            ret.append(object_types_models.ObjectType(ot['name'], ', '.join(ot['types_list'])))
        return ret


class MyPanelTabs(tabs.TabGroup):
    slug = "mypanel_tabs"
    tabs = (RegistryTab, Filters, Dependencies, MetricModules, Nodes, Groups, ObjectTypes,)
    sticky = True
