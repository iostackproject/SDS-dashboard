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
Forms for managing tenants.
"""
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard.dashboards.sdscontroller import api_sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


# TODO in construction
class CreateGroup(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the group to be created."),
                           required=True,
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))

    tenant_ids = forms.CharField(max_length=255,
                           label=_("Tenant Id List"),
                           help_text=_("A comma spared list with tenant ids."),
                           required=True,
                           widget=forms.TextInput(
                               attrs={"ng-model": "tenant_ids", "not-blank": ""}
                           ))

    def handle(self, request, data):
        name = data["name"]
        tenant_ids = data["tenant_ids"]

        try:
            response = api.dsl_create_tenants_group(request, name, tenant_ids)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created group: %s') % data['name'])
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to create group.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
