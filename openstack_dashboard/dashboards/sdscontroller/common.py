import json

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from openstack_dashboard.api import sds_controller as api


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
