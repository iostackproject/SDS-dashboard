# encoding: utf-8
from __future__ import unicode_literals

import requests
import json


# TODO: Take parameters from a config file
URL_BASIC = "http://10.30.103.250:18000"
TOKEN = "85082f27a14c4db79562b0b4e6df162b"


############################## # Registry DSL API # ##############################
# # Registry DSL - Policies
def create_policy(policy):
    headers = {}

    url = URL_BASIC + "/registry/policy"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "text/plain"

    r = requests.post(url, policy, headers=headers)
    return r


def list_policies():
    headers = {}

    url = URL_BASIC + "/registry/policy"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


# TODO confirm
def remove_policy(policy_id):
    headers = {}

    url = URL_BASIC + "/registry/policy/" + str(policy_id)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r

# # Registry DSL - Metrics Workload
def dsl_add_workload_metric(name, network_location, metric_type):
    headers = {}

    url = URL_BASIC + "/registry/metrics"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    parameters = {"name": str(name), "network_location": str(network_location), "metric_type": str(metric_type)}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def dsl_get_all_workload_metrics():
    headers = {}

    url = URL_BASIC + "/registry/metrics"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_workload_metric(metric_name, network_location=None, metric_type=None):
    headers = {}

    url = URL_BASIC + "/registry/metrics/" + str(metric_name)

    headers["X-Auth-Token"] = str(TOKEN)
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


def dsl_get_metric_metadata(metric_name):
    headers = {}

    url = URL_BASIC + "/registry/metrics/" + str(metric_name)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_delete_workload_metric(metric_name):
    headers = {}

    url = URL_BASIC + "/registry/metrics/" + str(metric_name)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Registry DSL - Filters
def dsl_add_filter(name, identifier, activation_url, valid_parameters):
    headers = {}

    url = URL_BASIC + "/registry/filters"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    parameters = {"name": str(name), "identifier": str(identifier), "activation_url": str(activation_url), "valid_parameters": str(valid_parameters)}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def dsl_get_all_filters():
    headers = {}

    url = URL_BASIC + "/registry/filters"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_update_filter(name, activation_url, valid_parameters):
    headers = {}

    url = URL_BASIC + "/registry/filters/" + str(name)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    parameters = {}
    if name is not None:
        parameters["name"] = str(name)
    if activation_url is not None:
        parameters["activation_url"] = str(activation_url)
    if valid_parameters is not None:
        parameters["valid_parameters"] = str(valid_parameters)

    if len(parameters) == 0:
        raise ValueError

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def dsl_get_filter_metadata(name):
    headers = {}

    url = URL_BASIC + "/registry/filters/" + str(name)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_delete_filter(name):
    headers = {}

    url = URL_BASIC + "/registry/filters/" + str(name)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


# # Registry DSL - Tenants Groups
def dsl_create_tenants_group():
    pass


def dsl_get_all_tenants_groups():
    headers = {}

    url = URL_BASIC + "/registry/gtenants"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_list_tenants_group(group_name):
    headers = {}

    url = URL_BASIC + "/registry/gtenants/" + str(group_name)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def dsl_add_tenant_group_member(group_name, tenant_id):
    headers = {}

    url = URL_BASIC + "/registry/gtenants/" + str(group_name)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    # TODO
    parameters = {"new": str(tenant_id)}

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def dsl_delete_tenants_group(group_name):
    headers = {}

    url = URL_BASIC + "/registry/gtenants/" + str(group_name)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def dsl_delete_tenant_group_member(group_name, tenant_id):
    headers = {}

    url = URL_BASIC + "/registry/gtenants/" + str(group_name) + "/tenants/" + str(tenant_id)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


############################## # Filters API # ##############################
# Filters - Filters
def fil_create_filter(name, language, interface_version, main, dependencies="", object_metadata="no"):
    headers = {}

    url = URL_BASIC + "/filters"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    parameters = {"name": str(name), "language": str(language), "interface_version": str(interface_version),
                  "main": str(main), "dependencies": str(dependencies), "object_metadata": str(object_metadata)}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def fil_upload_filter_data(filter_id, in_memory_file):
    headers = {}

    url = URL_BASIC + "/filters/" + str(filter_id) + "/data"

    headers["X-Auth-Token"] = str(TOKEN)

    files = {'file': (in_memory_file.name, in_memory_file.read())}

    r = requests.put(url, files=files, headers=headers)
    return r


def fil_delete_filter(filter_id):
    headers = {}

    url = URL_BASIC + "/filters/" + str(filter_id)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def fil_get_filter_metadata(filter_id):
    headers = {}

    url = URL_BASIC + "/filters/" + str(filter_id)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_list_filters():
    headers = {}

    url = URL_BASIC + "/filters"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_update_filter_metadata(filter_id, language, interface_version, main, dependencies="", object_metadata="no"):
    headers = {}

    url = URL_BASIC + "/filters/" + str(filter_id)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    parameters = {"language": str(language), "interface_version": str(interface_version),
                  "main": str(main), "dependencies": str(dependencies), "object_metadata": str(object_metadata)}

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def fil_deploy_filter(filter_id, account_id, parameters):
    headers = {}

    url = URL_BASIC + "/filters/" + str(account_id) + "/deploy/" + str(filter_id)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    parameters = {"params": str(parameters)}

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def fil_undeploy_filter(filter_id, account_id):
    headers = {}

    url = URL_BASIC + "/filters/" + str(account_id) + "/undeploy/" + str(filter_id)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


def fil_list_deployed_filters(account_id):
    headers = {}

    url = URL_BASIC + "/filters/" + str(account_id) + "/deploy"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


# # Filters - Dependencies
def fil_create_dependency(name, version, permissions):
    headers = {}

    url = URL_BASIC + "/filters/dependencies"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    parameters = {"name": str(name), "version": str(version), "permissions": str(permissions)}

    r = requests.post(url, json.dumps(parameters), headers=headers)
    return r


def fil_upload_dependency_data(dependency_id, filter_path):
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(dependency_id) + "/data"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "multipart/form-data"

    # TODO?
    with open(filter_path, "r") as my_file:
        data = my_file.read()

    r = requests.put(url, data=data, headers=headers)
    return r


def fil_delete_dependency(dependecy_id):
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(dependecy_id)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.delete(url, headers=headers)
    return r


def fil_get_dependency_metadata(dependecy_id):
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(dependecy_id)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_list_dependencies():
    headers = {}

    url = URL_BASIC + "/filters/dependencies"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r


def fil_update_dependency_metadata(dependency_id, version, permissions):
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(dependency_id)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    parameters = {"version": str(version), "permissions": str(permissions)}

    r = requests.put(url, json.dumps(parameters), headers=headers)
    return r


def fil_deploy_dependency(dependency_id, account_id):
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(account_id) + "/deploy/" + str(dependency_id)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


def fil_undeploy_dependency(dependency_id, account_id):
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(account_id) + "/undeploy/" + str(dependency_id)

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.put(url, headers=headers)
    return r


def fil_list_deployed_dependencies(account_id):
    headers = {}

    url = URL_BASIC + "/filters/dependencies/" + str(account_id) + "/deploy"

    headers["X-Auth-Token"] = str(TOKEN)
    headers['Content-Type'] = "application/json"

    r = requests.get(url, headers=headers)
    return r
