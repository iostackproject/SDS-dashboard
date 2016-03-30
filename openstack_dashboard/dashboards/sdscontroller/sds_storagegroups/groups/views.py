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
Views for managing groups.
"""
from django.core.urlresolvers import reverse
from django.utils import encoding
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import forms

from openstack_dashboard.dashboards.sdscontroller.sds_storagegroups.groups \
    import forms as groups_forms
from openstack_dashboard.api import sds_controller_blockstorage as api
import json    


class CreateGroupView(forms.ModalFormView):
    form_class = groups_forms.CreateGroup
    modal_header = _("Create Group")
    modal_id = "create_group_modal"
    template_name = 'sdscontroller/sds_storagegroups/groups/create_group.html'
    success_url = reverse_lazy('horizon:sdscontroller:sds_storagegroups:group_tab')
    page_title = _("Create a Group")
    submit_label = _("Create")
    submit_url = reverse_lazy(
        "horizon:sdscontroller:sds_storagegroups:groups:create_group")
        
#updategroup        
class UpdateGroupView(forms.ModalFormView):
    form_class = groups_forms.UpdateForm
    modal_header = _("Edit Group")
    modal_id = "update_volume_modal"
    template_name = 'sdscontroller/sds_storagegroups/groups/update_group.html'
    submit_url = "horizon:sdscontroller:sds_storagegroups:groups:update"
    success_url = reverse_lazy("horizon:sdscontroller:sds_storagegroups:group_tab")
    page_title = _("Edit Group")

    def get_object(self):
        if not hasattr(self, "_object"):
            groupid = self.kwargs['id']
            try:
                resp = api.retrieve_storagegroup(groupid)
                if 200 <= resp.status_code < 300:        
                    data = resp.json()
                else:
                    error_message = 'Unable to retrieve storage nodes information.'
                    raise ValueError(error_message)            
            except Exception as e:
                msg = _('Unable to retrieve storage group.')
                url = reverse('horizon:sdscontroller:sds_storagegroups:index')
                exceptions.handle(self.request, msg, redirect=url)
            return data            

    def get_context_data(self, **kwargs):
        context = super(UpdateGroupView, self).get_context_data(**kwargs)
        context['group'] = self.get_object()
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_initial(self):
        group = self.get_object()
        return {'id': group["id"],
                'name': group["name"],
                'policy': group["policy"],
                'nodes': group["nodes"],
                }