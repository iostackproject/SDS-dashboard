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

from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception
from openstack_dashboard.api import sds_controller as api


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
                                   help_text=_(
                                       "Example: r1z1-STORAGE_NODE_MANAGEMENT_INTERFACE_IP_ADDRESS:6000/DEVICE_NAME DEVICE_WEIGHT"),
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

        #TODO: After rebuild the form this code should disappear
        try:
            storage_nodes_response = api.list_storage_nodes(request)
            if storage_nodes_response.text:
                storage_nodes = json.loads(storage_nodes_response.text)
                storage_nodes_form = data['storage_node'].split(',')
		data["storage_node"] = {}
                for i in range(0, len(storage_nodes_form), 2):
                    for storage_node in storage_nodes:
			if storage_node["id"] == storage_nodes_form[i]:
			    location = storage_node['location']
                            data["storage_node"][location] = storage_nodes_form[i+1]
            else:
                raise Exception
        except Exception, e:
            redirect = reverse("horizon:sdscontroller:rings_and_accounts:index")
            error_message = "Storage nodes not found"
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)
        try:
            response = api.new_storage_policy(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully EC Storage Policy created.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:rings_and_accounts:index")
            error_message = "Unable to EC Storage Policy.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)

class CreateECStoragePolicy(forms.SelfHandlingForm):
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
                                   help_text=_(
                                       "Example: r1z1-STORAGE_NODE_MANAGEMENT_INTERFACE_IP_ADDRESS:6000/DEVICE_NAME DEVICE_WEIGHT"),
                                   widget=forms.TextInput(
                                       attrs={"ng-model": "storage_node", "not-blank": ""}
                                   ))

    ec_type = forms.CharField(max_length=255,
                              label=_("EC Type"),
                              required=False,
                              help_text=_("Is chosen from the list of EC backends supported by PyECLib"),
                              widget=forms.TextInput(
                                  attrs={"ng-model": "ec_type", "not-blank": ""}
                              ))

    ec_num_data_fragments = forms.CharField(max_length=255,
                                            label=_("Num. Data Fragments"),
                                            required=False,
                                            help_text=_("Num. Data Fragments"),
                                            widget=forms.TextInput(
                                                attrs={"ng-model": "ec_num_data_fragments", "not-blank": ""}
                                            ))

    ec_num_parity_fragments = forms.CharField(max_length=255,
                                              label=_("Num. Parity Fragments"),
                                              required=False,
                                              help_text=_("Num parity fragments"),
                                              widget=forms.TextInput(
                                                  attrs={"ng-model": "ec_num_parity_fragments", "not-blank": ""}
                                              ))

    ec_object_segment_size = forms.CharField(max_length=255,
                                             label=_("Object Segment Size"),
                                             required=False,
                                             help_text=_("Object Segment Size"),
                                             widget=forms.TextInput(
                                                 attrs={"ng-model": "ec_object_segment_size", "not-blank": ""}
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
        super(CreateECStoragePolicy, self).__init__(request, *args, **kwargs)

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

        #TODO: After rebuild the form this code should disappear
        try:
            storage_nodes_response = api.list_storage_nodes(request)

            if storage_nodes_response.text:
                storage_nodes = json.loads(storage_nodes_response.text)
                storage_nodes_form = data['storage_node'].split(',')
                data["storage_node"] = {}
                for i in range(0, len(storage_nodes_form), 2):

                    location = str(storage_nodes[int(storage_nodes_form[i])-1]['location'])
                    data["storage_node"][location] = storage_nodes_form[i+1]
            else:
                raise Exception
        except Exception, e:
            redirect = reverse("horizon:sdscontroller:rings_and_accounts:index")
            error_message = "Storage nodes not found"
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)

        try:
            data['replicas'] = int(data["ec_num_data_fragments"]) + int(data["ec_num_parity_fragments"])
            response = api.new_storage_policy(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully EC Storage Policy created.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:rings_and_accounts:index")
            error_message = "Unable to EC Storage Policy.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)

class BindStorageNode(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name assigned to new storage node."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))
    location = forms.CharField(max_length=255,
                                label=_("Location"),
                                help_text=_("The location from new storage node. Example: r1z1-STORAGE_NODE_MANAGEMENT_INTERFACE_IP_ADDRESS:6000/DEVICE_NAME"),
                                widget=forms.TextInput(
                                    attrs={"ng-model": "location", "not-blank": ""}
                                ))
    type = forms.CharField(max_length=255,
                                   label=_("Type"),
                                   help_text=_("SSD or HDD"),
                                   widget=forms.TextInput(
                                       attrs={"ng-model": "type", "not-blank": ""}
                                   ))


    def __init__(self, request, *args, **kwargs):
        super(BindStorageNode, self).__init__(request, *args, **kwargs)


    def handle(self, request, data):
        api.registry_storage_node(request, data)
        return data
