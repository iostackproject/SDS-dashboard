import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from openstack_dashboard.api import sds_controller as api


# Filter Type
# ===========
def get_filter_type_choices():
    """
    Get a tuple of filter types

    :return: tuple with filter types
    """
    return ('', 'Select one'), ('Filter Types', [('storlet', 'Storlet'), ('native', 'Native')])


# Filter
# ======
def get_filter_list_choices(request):
    """
    Get a tuple of filters

    :param request: the request which the dashboard is using
    :return: tuple with filters
    """
    return ('', 'Select one'), ('Filters', get_filter_list(request))


def get_filter_list(request):
    """
    Get a list of filters

    :param request: the request which the dashboard is using
    :return: list with filters
    """
    try:
        response = api.fil_list_filters(request)
        if 200 <= response.status_code < 300:
            response_text = response.text
        else:
            raise ValueError('Unable to get filters.')
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    filters_list = []
    filters = json.loads(response_text)
    # Iterate filters
    for filter_ in filters:
        filters_list.append((filter_['id'], filter_['filter_name']))
    return filters_list


# DSL Filter
# ==========
def get_dsl_filter_list_choices(request):
    """
    Get a tuple of dsl filters

    :param request: the request which the dashboard is using
    :return: tuple with dsl filters
    """
    return ('', 'Select one'), ('DSL Filters', get_dsl_filter_list(request))


def get_dsl_filter_list(request):
    """
    Get a list of dsl filters

    :param request: the request which the dashboard is using
    :return: list with dsl filters
    """
    try:
        response = api.dsl_get_all_filters(request)
        if 200 <= response.status_code < 300:
            response_text = response.text
        else:
            raise ValueError('Unable to get dsl filters.')
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    dsl_filters_list = []
    dsl_filters = json.loads(response_text)
    # Iterate dsl filters
    for dsl_filter in dsl_filters:
        dsl_filters_list.append((dsl_filter['identifier'], dsl_filter['name']))
    return dsl_filters_list


# Object Type
# ===========
def get_object_type_choices(request):
    """
    Get a tuple of object type choices

    :param request: the request which the dashboard is using
    :return: tuple with object types
    """
    object_type_list = get_object_type_list(request)
    return (('', 'None'), ('Object Types', object_type_list)) if len(object_type_list) > 0 else (('', 'None'),)


def get_object_type_list(request):
    """
    Get a list of object types

    :param request: the request which the dashboard is using
    :return: list with object types
    """
    try:
        response = api.dsl_get_all_object_types(request)
        if 200 <= response.status_code < 300:
            response_text = response.text
        else:
            raise ValueError('Unable to get object types.')
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    object_types_list = []
    object_types = json.loads(response_text)
    # Iterate object types
    for object_type in object_types:
        object_types_list.append((object_type['name'], object_type['name']))
    return object_types_list


# Project
# =======
def get_project_list_choices(request):
    """
    Get a tuple of project choices

    :param request: the request which the dashboard is using
    :return: tuple with project choices
    """
    return ('', 'Select one'), ('Projects', get_project_list(request))


def get_project_list(request):
    """
    Get a list of projects

    :param request: the request which the dashboard is using
    :return: list with projects
    """
    try:
        response = api.swift_list_tenants(request)
        if 200 <= response.status_code < 300:
            response_text = response.text
        else:
            raise ValueError('Unable to get projects.')
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    projects_list = []
    projects = json.loads(response_text)['tenants']
    # Iterate projects
    for project in projects:
        projects_list.append((project['id'], project['name']))
    return projects_list


# Storage Policy
# ==============
def get_storage_policy_list_choices(request):
    """
    Get a tuple of storage policy choices

    :param request: the request which the dashboard is using
    :return: tuple with storage policy choices
    """
    return ('', 'Select one'), ('Storage Policies', get_storage_policy_list(request))


def get_storage_policy_list(request):
    """
    Get a list of storage policies

    :param request: the request which the dashboard is using
    :return: list with storage policies
    """
    try:
        response = api.swift_list_storage_policies(request)
        if 200 <= response.status_code < 300:
            response_text = response.text
        else:
            raise ValueError('Unable to get storage policies.')
    except Exception as exc:
        response_text = '[]'
        exceptions.handle(request, _(exc.message))

    storage_policies_list = []
    storage_policies = json.loads(response_text)
    # Iterate storage policies
    for storage_policy in storage_policies:
        storage_policies_list.append((storage_policy['id'], storage_policy['name']))
    return storage_policies_list
