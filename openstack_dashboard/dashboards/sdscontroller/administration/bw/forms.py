# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError  # noqa
from django.core.urlresolvers import reverse

from horizon import exceptions
from horizon import forms
from horizon import messages

import json

from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class UpdateSortedMethod(forms.SelfHandlingForm):

    sorted_nodes_method = forms.CharField(max_length=255,
                           label=_("Sorted Nodes Method:"),
                           help_text=_("The sorted_method name."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))

    sorted_nodes_criterion = forms.CharField(max_length=255,
                           label=_("Sorted Nodes Criterion:"),
                           help_text=_("ascending or descending ."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "language", "not-blank": ""}
                           ))


    def __init__(self, request, *args, **kwargs):
        super(UpdateSortedMethod, self).__init__(request, *args, **kwargs)


    def handle(self, request, data):

        print 'data', data
        try:
            response = api.set_sort_nodes(request, data)

            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully filter creation and upload.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)

        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to update sorted method.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)
