# encoding: utf-8
from __future__ import unicode_literals

import requests
import json
from horizon.utils.memoized import memoized  # noqa


# TODO: Take parameters from a config file
URL_BASIC = "http://127.0.0.1:8000"

@memoized
def sds_controller_api(request):
    return request.user.token.id

############################## # Swift API # ##############################


def swift_list_tenants(request):
    token = sds_controller_api(request)

    headers = {}

    url = URL_BASIC + "/swift/tenants"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r

def tenant_create(request, tenant_name, admin_user, admin_pass):
    token = sds_controller_api(request)
    headers = {}
    url = URL_BASIC + "/swift/tenants"
    parameters = {"tenant_name": tenant_name, "user_name": admin_user, "user_password": admin_pass}
    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"
    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r

def new_storage_policy(request, data):
    token = sds_controller_api(request)
    headers = {}
    url = URL_BASIC + "/swift/sdspolicies"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r

############################## # Registry DSL API # ##############################
# # Registry DSL - Policies

def registry_storage_node(request, data):
    token = sds_controller_api(request)
    headers = {}
    print 'api data', data
    url = URL_BASIC + "/registry/snode"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "text/plain"

    r = requests.post(url, json.dumps(data), headers=headers)
    print r.text
    return r


def list_storage_nodes(request):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/snode"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "text/plain"

    r = requests.get(url, headers=headers)
    return r


def create_policy(request, policy):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/policy"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "text/plain"

    r = requests.post(url, policy, headers=headers)
    return r


def list_policies(request):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/policy"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def list_metrics(request):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/metrics"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


# TODO confirm
def remove_policy(request, policy_id):
    token = sds_controller_api(request)

    headers = {}

    url = URL_BASIC + "/registry/policy/" + str(policy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Registry DSL - Metrics Workload
def dsl_add_workload_metric(request, name, network_location, metric_type):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/metrics"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"name": str(name), "network_location": str(network_location), "metric_type": str(metric_type)}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def dsl_get_all_workload_metrics(request):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/metrics"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_workload_metric(request, metric_name, network_location=None, metric_type=None):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/metrics/" + str(metric_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {}
    if network_location is not None:
        parameters["network_location"] = str(network_location)
    if metric_type is not None:
        parameters["metric_type"] = str(metric_type)

    if len(parameters) == 0:
        raise ValueError

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def dsl_get_metric_metadata(request, metric_name):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/metrics/" + str(metric_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_delete_workload_metric(request, metric_name):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/metrics/" + str(metric_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Registry DSL - Filters
def dsl_add_filter(request, name, identifier, activation_url, valid_parameters):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/filters"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"name": str(name), "identifier": str(identifier), "activation_url": str(activation_url), "valid_parameters": str(valid_parameters)}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def dsl_get_all_filters(request):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/filters"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_filter(request, name, data):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/filters/" + str(name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def dsl_get_filter_metadata(request, name):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/filters/" + str(name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_delete_filter(request, name):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/filters/" + str(name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Registry DSL - Tenants Groups
def dsl_create_tenants_group(request, name, tenants_list):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/gtenants"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    # parameters = {"name": str(name), "tenants": str(tenants_list)}
    # r = requests.post(url, json.dumps(parameters), headers=headers)

    r = requests.post(url, json.dumps(tenants_list), headers=headers)
    return r


def dsl_get_all_tenants_groups(request):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/gtenants"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_list_tenants_group(request, group_name):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/gtenants/" + str(group_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_add_tenant_group_member(request, group_name, tenant_id):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/gtenants/" + str(group_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    # TODO
    parameters = {"new": str(tenant_id)}

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def dsl_delete_tenants_group(request, group_name):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/gtenants/" + str(group_name)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def dsl_delete_tenant_group_member(request, group_name, tenant_id):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/registry/gtenants/" + str(group_name) + "/tenants/" + str(tenant_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


############################## # Filters API # ##############################
# Filters - Filters
def fil_create_filter(request, data):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.post(url, json.dumps(data), headers=headers)
    return r


def fil_upload_filter_data(request, filter_id, in_memory_file):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/" + str(filter_id) + "/data"

    headers["X-Auth-Token"] = str(token)

    files = {'file': (in_memory_file.name, in_memory_file.read())}

    r = requests.put(url, files=files, headers=headers)
    return r


def fil_delete_filter(request, filter_id):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def fil_get_filter_metadata(request, filter_id):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_list_filters(request):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_update_filter_metadata(request, filter_id, data):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, json.dumps(data), headers=headers)
    return r


def fil_deploy_filter(request, filter_id, account_id, parameters):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/" + str(account_id) + "/deploy/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"params": str(parameters)}

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def fil_undeploy_filter(request, filter_id, account_id):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/" + str(account_id) + "/undeploy/" + str(filter_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


def fil_list_deployed_filters(request, account_id):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/" + str(account_id) + "/deploy"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


# # Filters - Dependencies
def fil_create_dependency(request, name, version, permissions):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/dependencies"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"name": str(name), "version": str(version), "permissions": str(permissions)}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def fil_upload_dependency_data(request, dependency_id, filter_path):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(dependency_id) + "/data"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "multipart/form-data"

    # TODO?
    with open(filter_path, "r") as my_file:
        data = my_file.read()

    r = requests.put(url, data=data, headers=headers)
    return r


def fil_delete_dependency(request, dependecy_id):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(dependecy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def fil_get_dependency_metadata(request, dependecy_id):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(dependecy_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_list_dependencies(request):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/dependencies"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_update_dependency_metadata(request, dependency_id, version, permissions):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(dependency_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    parameters = {"version": str(version), "permissions": str(permissions)}

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def fil_deploy_dependency(request, dependency_id, account_id):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(account_id) + "/deploy/" + str(dependency_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


def fil_undeploy_dependency(request, dependency_id, account_id):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(account_id) + "/undeploy/" + str(dependency_id)

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


def fil_list_deployed_dependencies(request, account_id):
    token = sds_controller_api(request)
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(account_id) + "/deploy"

    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r
