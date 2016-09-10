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

"""
Views for managing policies.
"""
from django.core.urlresolvers import reverse
from django.utils import encoding
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard.dashboards.sdscontroller.sds_storagepolicies.policies \
    import forms as policies_forms
from openstack_dashboard.api import sds_controller_blockstorage as api
import json


class CreatePolicyView(forms.ModalFormView):
    form_class = policies_forms.CreatePolicy
    modal_header = _("Create Policy")
    modal_id = "create_policy_modal"
    template_name = 'sdscontroller/sds_storagepolicies/policies/create_policy.html'
    success_url = reverse_lazy('horizon:sdscontroller:sds_storagepolicies:policy_tab')
    page_title = _("Create a Policy")
    submit_label = _("Create")
    submit_url = reverse_lazy(
        "horizon:sdscontroller:sds_storagepolicies:policies:create_policy")

#updatepolicy        
class UpdatePolicyView(forms.ModalFormView):
    form_class = policies_forms.UpdateForm
    modal_header = _("Edit Policy")
    modal_id = "update_volume_modal"
    template_name = 'sdscontroller/sds_storagepolicies/policies/update_policy.html'
    submit_url = "horizon:sdscontroller:sds_storagepolicies:policies:update"
    success_url = reverse_lazy("horizon:sdscontroller:sds_storagepolicies:policy_tab")
    page_title = _("Edit Policy")

    def get_object(self):
        if not hasattr(self, "_object"):
            policyid = self.kwargs['id']
            try:
                resp = api.retrieve_policy(policyid)
                if 200 <= resp.status_code < 300:        
                    data = resp.json()
                else:
                    error_message = 'Unable to retrieve storage nodes information.'
                    raise ValueError(error_message)            
            except Exception as e:
                msg = _('Unable to retrieve policy.')
                url = reverse('horizon:sdscontroller:sds_storagepolicies:index')
                exceptions.handle(self.request, msg, redirect=url)
            return data            

    def get_context_data(self, **kwargs):
        context = super(UpdatePolicyView, self).get_context_data(**kwargs)
        context['policy'] = self.get_object()
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_initial(self):
        policy = self.get_object()
        filters = policy['filters']
        filters = (", ".join(filters))
        return {'id': policy["id"],
                'name': policy["name"],
                'san_name': policy["san_name"],
                'tier': policy["tier"],
                'throttle_iops_read': policy["throttle_iops_read"],
                'throttle_iops_write': policy["throttle_iops_write"],
                'throttle_mbps_read': policy["throttle_mbps_read"],
                'throttle_mbps_write': policy["throttle_mbps_write"],
                'filters': filters,
                }        
