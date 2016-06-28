import json

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


def get_filter_list(self, request):
    try:
        response = api.fil_list_filters(request)
        if 200 <= response.status_code < 300:
            strobj = response.text
        else:
            error_message = 'Unable to get filters.'
            raise ValueError(error_message)
    except Exception as e:
        strobj = "[]"
        exceptions.handle(self.request, _(e.message))
    instances = json.loads(strobj)
    FILTER_IDENTIFIERS = []
    for inst in instances:
        FILTER_IDENTIFIERS.append((inst['id'], inst['name']))
    return FILTER_IDENTIFIERS


class CreateFilter(forms.SelfHandlingForm):
    filter_list = []

    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the filter to be created."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))

    filter_identifier = forms.ChoiceField(choices=filter_list,
                                          label=_("Filter identifier"),
                                          help_text=_("Filter identifier to be used."),
                                          required=False,
                                          widget=forms.Select(
                                              attrs={"ng-model": "filter_identifiers", "not-blank": ""}
                                          ))

    activation_url = forms.CharField(max_length=255,
                                     label=_("Activation Url"),
                                     help_text=_("Activation Url"),
                                     widget=forms.TextInput(
                                         attrs={"ng-model": "activation_url", "not-blank": ""}
                                     ))

    valid_parameters = forms.CharField(max_length=255,
                                       label=_("valid_parameters"),
                                       required=False,
                                       help_text=_("A comma separated list of tuples of data, as Python dictionary. Ex: param2: integer, param1: bool"),
                                       widget=forms.TextInput(
                                           attrs={"ng-model": "valid_parameters"}
                                       ))

    def __init__(self, request, *args, **kwargs):
        self.filter_list = get_filter_list(self, request)
        super(CreateFilter, self).__init__(request, *args, **kwargs)
        self.fields['filter_identifier'] = forms.ChoiceField(choices=self.filter_list,
                                                             label=_("Filter identifier"),
                                                             help_text=_("Filter identifier to be used."),
                                                             required=False,
                                                             widget=forms.Select(
                                                                 attrs={"ng-model": "filter_identifiers", "not-blank": ""}
                                                             ))

    def handle(self, request, data):
        name = data["name"]
        filter_identifier = data["filter_identifier"]
        activation_url = data["activation_url"]
        # TODO convert string to dict or change input format
        string_parameters = "{" + data["valid_parameters"] + "}"

        try:
            response = api.dsl_add_filter(request, name, filter_identifier, activation_url, string_parameters)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created filter: %s') % data['name'])
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to create filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateFilter(forms.SelfHandlingForm):
    filter_list = []

    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           widget=forms.TextInput(attrs={'readonly': 'readonly'})
                           )

    filter_identifier = forms.ChoiceField(choices=filter_list,
                                          label=_("Filter identifier"),
                                          help_text=_("Filter identifier to be used."),
                                          required=False)

    activation_url = forms.CharField(max_length=255,
                                     label=_("Activation Url"),
                                     help_text=_("Activation Url"))

    valid_parameters = forms.CharField(max_length=255,
                                       label=_("valid_parameters"),
                                       required=False,
                                       help_text=_("A comma separated list of tuples of data, as Python dictionary. Ex: param2: integer, param1: bool"))

    def __init__(self, request, *args, **kwargs):
        self.filter_list = get_filter_list(self, request)
        super(UpdateFilter, self).__init__(request, *args, **kwargs)
        self.fields['filter_identifier'] = forms.ChoiceField(choices=self.filter_list,
                                                             label=_("Filter identifier"),
                                                             help_text=_("Filter identifier to be used."),
                                                             required=False)

    def handle(self, request, data):
        name = data["name"]
        # TODO convert string to dict or change input format
        string_parameters = "{" + data["valid_parameters"] + "}"

        try:
            response = api.dsl_update_filter(request, name, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created filter: %s') % data['name'])
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to create filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
