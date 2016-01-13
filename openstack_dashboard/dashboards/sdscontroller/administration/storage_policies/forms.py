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
import subprocess
import json

from openstack_dashboard.dashboards.sdscontroller import api_sds_controller as api


class CreateStoragePolicy(forms.SelfHandlingForm):

    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the new policy."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))
    policy_id = forms.CharField(max_length=5,
                           label=_("Policy ID"),
                           help_text=_("The unique ID to identify the policy."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "policy_id", "not-blank": ""}
                           ))
    storage_node = forms.CharField(max_length=255,
                           label=_("Storage Node"),
                           help_text=_("Example: r1z1-STORAGE_NODE_MANAGEMENT_INTERFACE_IP_ADDRESS:6000/DEVICE_NAME DEVICE_WEIGHT"),
                           widget=forms.TextInput(
                               attrs={"ng-model": "storage_node", "not-blank": ""}
                           ))

    replicas = forms.CharField(max_length=255,
                           label=_("Num. Replicas"),
                           required=False,
                           help_text=_("Number of replicas"),
                           widget=forms.TextInput(
                               attrs={"ng-model": "replicas", "not-blank": ""}
                           ))

    partitions = forms.CharField(max_length=255,
                           label=_("Num. Partitions"),
                           required=False,
                           help_text=_("If the value is x the num of partitions will be 2^x"),
                           widget=forms.TextInput(
                               attrs={"ng-model": "partitions", "not-blank": ""}
                           ))

    time = forms.CharField(max_length=255,
                           label=_("Time"),
                           required=False,
                           help_text=_("Time between moving a partition more than once. In hours"),
                            widget=forms.TextInput(
                               attrs={"ng-model": "time", "not-blank": ""}
                           ))


    def __init__(self, request, *args, **kwargs):
        super(CreateStoragePolicy, self).__init__(request, *args, **kwargs)

    # def _set_filter_path(self, data):
    #     if data['path']:
    #         filter_path = "/".join([data['path'].rstrip("/"), data['name']])
    #     else:
    #         filter_path = data['name']
    #     return filter_path

    # def clean(self):
    #     data = super(UploadFilter, self).clean()
    #
    #     image_file = data.get('filter_file', None)
    #     image_url = data.get('image_url', None)
    #
    #     if not image_url and not image_file:
    #         raise ValidationError(
    #             _("A external file must be specified."))
    #     else:
    #         return data

    def handle(self, request, data):
        name = data["name"]
        policy_id = data["policy_id"]
        storage_node = data["storage_node"]
        replicas = data["replicas"]
        partitions = data["partitions"]
        time = data["time"]
        print name, policy_id, storage_node, replicas, partitions, time
        # try:
            #Call the script (reboot
            #Rebbot swift
            #response = api.fil_create_filter(name, language, interface_version, main, dependencies, object_metadata)
        ret = subprocess.call(['/home/swift/SDS-dashboard/openstack_dashboard/dashboards/sdscontroller/administration/storage_policies/script.sh'])
        print 'return script', ret
        return data

        # except Exception as ex:
        #     redirect = reverse("horizon:sdscontroller:administration:index")
        #     error_message = "Unable to create filter.\t %s" % ex.message
        #     exceptions.handle(request,
        #                       _(error_message),
        #                       redirect=redirect)
