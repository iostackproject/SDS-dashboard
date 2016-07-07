import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from openstack_dashboard.api import sds_controller as api


# Administration
# ==============

# Filters
def get_filter_type_choices():
    """
    Get a list of filter types

    :return: list with filter types
    """
    return [('', 'Select one'), ('storlet', 'Storlet'), ('native', 'Native')]


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
