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
Groups for managing storage groups.
"""
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard.api import sds_controller_blockstorage as api
import json

class CreateGroup(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Name"))
    policy = forms.ChoiceField(label=_("Policy"))
    def __init__(self, *args, **kwargs):
        super(CreateGroup, self).__init__(*args, **kwargs)
        self.fields['policy'].choices = self.policyValues()
        self.fields['nodes'] = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=self.storageNodesValues(), required=True, label=_("Storage Nodes"))        

    def policyValues(self):
        resp = api.list_policies(self.request)
        if resp.status_code == 200:
            data = resp.json()
        else:
            error_message = 'Unable to retrieve policies information.'
            raise ValueError(error_message)
        #
        policies_list = []
        for d in data:
            name = d['name']
            id = d['id']
            policies_list.append((id, '%s' % name))        
        return policies_list

    def storageNodesValues(self):
        resp = api.list_controllers(self.request)
        if resp.status_code == 200:
            data = resp.json()
        else:
            error_message = 'Unable to retrieve Storage Nodes information.'
            raise ValueError(error_message)
        #
        storage_nodes_list = []
        storage_nodes_list_test = []        
        for d in data:
            name = d['hostname']
            id = d['node']
            if id not in storage_nodes_list_test: 
                storage_nodes_list_test.append(id)
                storage_nodes_list.append((id, '%s' % name))        
        return storage_nodes_list

    def handle(self, request, data):
        #
        data_values = data
        nodes = data["nodes"]
        del data["nodes"]
        #
        # Create Storage group
        try:
            resp = api.create_storagegroup(self.request, data)
            if 200 <= resp.status_code < 300:
                data = resp.json()
            else:
                error_message = 'Unable to create group'                
                raise ValueError(resp.text)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))
        #
        # Assign storage nodes to storage group
        groupid = data["id"]
        groupid = str(groupid)
        count = 0
        for node in nodes:
            count = count + 1
            try:
                resp = api.associate_group_node(self.request, groupid, node)
                if 200 <= resp.status_code < 300:
                    pass
                else:
                    error_message = 'Unable to associate group and storage node'
                    raise ValueError(resp.text)
            except Exception as e:                  
                strobj = "[]"
                exceptions.handle(self.request, _(e.message))
        return data_values
        
#updategroup
class UpdateForm(forms.SelfHandlingForm):
    id = forms.IntegerField(widget = forms.HiddenInput())
    name = forms.CharField(max_length=255,label=_("Storage Group Name"),required=False)
    policy = forms.ChoiceField(label=_("Policy"))
    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['policy'].choices = self.policyValues()
        self.fields['nodes'] = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=self.storageNodesValues(), required=True, label=_("Storage Nodes"))

    def policyValues(self):
        resp = api.list_policies(self.request)
        if resp.status_code == 200:
            data = resp.json()
        else:
            error_message = 'Unable to retrieve policies information.'
            raise ValueError(error_message)
        #
        policies_list = []
        for d in data:
            name = d['name']
            id = d['id']
            policies_list.append((id, '%s' % name))        
        return policies_list

    def storageNodesValues(self):
        resp = api.list_controllers(self.request)
        if resp.status_code == 200:
            data = resp.json()
        else:
            error_message = 'Unable to retrieve Storage Nodes information.'
            raise ValueError(error_message)
        #
        storage_nodes_list = []
        storage_nodes_list_test = []        
        for d in data:
            name = d['hostname']
            id = d['node']
            if id not in storage_nodes_list_test: 
                storage_nodes_list_test.append(id)
                storage_nodes_list.append((id, '%s' % name))        
        return storage_nodes_list
                                  
    def handle(self, request, data):
        #
        groupid = data['id']
        groupid = str(groupid)
        #TOFIX: receiving error, "method not allowed"
        #
        datasg = {}
        try:
            resp = api.update_storagegroup(self.request, groupid, data)
            if 200 <= resp.status_code < 300:
                data = resp.json()
            else:
                error_message = 'Unable to update Storage Group'
                raise ValueError(resp.text)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))
        return data
        
    def manage_filters(self, filters_list):
        data=[e.strip() for e in filters_list.split(',')]
        return filters_list