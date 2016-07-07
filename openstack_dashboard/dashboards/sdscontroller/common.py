import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from openstack_dashboard.api import sds_controller as api


# Filter
# ======
def get_filter_type_choices():
    """
    Get a list of filter types

    :return: list with filter types
    """
    return [('', 'Select one'), ('storlet', 'Storlet'), ('native', 'Native')]


# Filter
# ======
def get_filter_list_choices(request):
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
    Get a tuple of object types

    :param request: the request which the dashboard is using
    :return: tuple with object types
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

    choices_list = []
    choices = json.loads(response_text)
    # Iterate choices
    for choice in choices:
        choices_list.append((choice['name'], choice['name']))
    # Return tuple of object types, or none if not exists
    return (('', 'None'), ('Object types', choices_list)) if len(choices_list) > 0 else (('', 'None'),)


# Project
# =======
def get_project_list_choices(request):
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
