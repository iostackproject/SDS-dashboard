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
Policies for managing storage policies.
"""
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard.api import sds_controller_blockstorage as api
import json

class CreatePolicy(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Name"))
    san_name = forms.CharField(max_length=255, label=_("San Name"), required=False)
    throttle_iops_read = forms.IntegerField(label=_("IO/s read"), required=False)
    throttle_iops_write = forms.IntegerField(label=_("IO/s write"), required=False)
    throttle_mbps_read = forms.IntegerField(label=_("MB/s read"), required=False) 
    throttle_mbps_write = forms.IntegerField(label=_("MB/s write"), required=False)
    tier = forms.ChoiceField(label=_("Tier"))
    filters = forms.CharField(max_length=255, label=_("Filters"), required=False)
    def __init__(self, *args, **kwargs):
        super(CreatePolicy, self).__init__(*args, **kwargs)
        self.fields['tier'].choices = self.tierValues()

    def tierValues(self):
        values = []
        values = (
            ('Mission Critical', 'Mission Critical'),
            ('Business', 'Business'),
            ('Archive', 'Archive'),
        )
        return values

    def handle(self, request, data):
        #
        #Split filters
        filters=data['filters']
        listfilters = [e.strip() for e in filters.split(',')]
        data['filters'] = listfilters
        #
        datasg = {}
        try:
            resp = api.create_policy(self.request, data)
            if 200 <= resp.status_code < 300:
                data = resp.json()
            else:
                error_message = 'Unable to create policy'
                raise ValueError(resp.text)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))
        return data
        
    def manage_filters(self, filters_list):
        data=[e.strip() for e in filters_list.split(',')]
        return filters_list

#updatepolicy
class UpdateForm(forms.SelfHandlingForm):
    id = forms.IntegerField(widget = forms.HiddenInput())
    name = forms.CharField(max_length=255,label=_("Policy Name"),required=False)
    san_name = forms.CharField(max_length=255,label=_("San Name"),required=False)
    throttle_iops_read = forms.IntegerField(label=_("IO/s read"), required=False)
    throttle_iops_write = forms.IntegerField(label=_("IO/s write"), required=False)
    throttle_mbps_read = forms.IntegerField(label=_("MB/s read"), required=False) 
    throttle_mbps_write = forms.IntegerField(label=_("MB/s write"), required=False)
    tier = forms.ChoiceField(label=_("Tier"))
    filters = forms.CharField(max_length=255, label=_("Filters"), required=False)                                  
    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['tier'].choices = self.tierValues()

    def tierValues(self):
        values = []
        values = (
            ('Mission Critical', 'Mission Critical'),
            ('Business', 'Business'),
            ('Archive', 'Archive'),
        )
        return values
                                  
    def handle(self, request, data):
        #
        #Split filters
        filters=data['filters']
        listfilters = [e.strip() for e in filters.split(',')]
        data['filters'] = listfilters
        policy_id = data['id']
        #TODO: receiving error, method not allowed
        del data["id"]
        datasg = {}
        try:
            resp = api.update_policy(self.request, data)
            if 200 <= resp.status_code < 300:
                data = resp.json()
            else:
                error_message = 'Unable to update policy'
                raise ValueError(resp.text)
        except Exception as e:
            strobj = "[]"
            exceptions.handle(self.request, _(e.message))
        return data
        
    def manage_filters(self, filters_list):
        data=[e.strip() for e in filters_list.split(',')]
        return filters_list                                  