# Copyright 2012 Nebula, Inc.
# All rights reserved.

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Forms for managing filters.
"""
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard.dashboards.sdscontroller import api_sds_controller as api


class CreateFilter(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the filter to be created."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))

    filter_identifier = forms.CharField(max_length=255,
                           label=_("Filter identifier"),
                           help_text=_("Filter identifier to be used."),
                           required=False,
                           widget=forms.TextInput(
                               attrs={"ng-model": "filter_identifier", "not-blank": ""}
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

    def handle(self, request, data):
        name = data["name"]
        filter_identifier = data["filter_identifier"]
        activation_url = data["activation_url"]
        # TODO convert string to dict or change input format
        string_parameters = "{"+data["valid_parameters"]+"}"

        try:
            response = api.dsl_add_filter(request, name, filter_identifier, activation_url, string_parameters)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created filter: %s') % data['name'])
                return data
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to create filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
