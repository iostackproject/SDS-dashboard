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

"""
Views for managing SDS Dependencies.
"""
import json
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse

from horizon import forms
from horizon.utils import memoized
from horizon import exceptions

from openstack_dashboard.dashboards.sdscontroller.administration.dependencies import forms as dependencies_forms
from openstack_dashboard.api import sds_controller as api

class UploadView(forms.ModalFormView):
    form_class = dependencies_forms.UploadDependency
    form_id = "upload_dependency_form"

    modal_header = _("Upload A Dependency")
    submit_label = _("Upload Dependency")
    submit_url = reverse_lazy('horizon:sdscontroller:administration:dependencies:upload')
    template_name = "sdscontroller/administration/dependencies/upload.html"
    context_object_name = 'dependency'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Upload A Dependency")

class UpdateView(forms.ModalFormView):
    form_class = dependencies_forms.UpdateDependency
    form_id = "update_dependency_form"
    modal_header = _("Update A Dependency")
    submit_label = _("Update Dependency")
    submit_url = "horizon:sdscontroller:administration:dependencies:update"
    template_name = "sdscontroller/administration/dependencies/update.html"
    context_object_name = 'dependency'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Update A Dependency")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['dependency_id'] = self.kwargs['dependency_id']
        args = (self.kwargs['dependency_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        dependency_id = self.kwargs['dependency_id']
        try:
            dependency = api.fil_get_dependency_metadata(self.request, dependency_id)
	    return dependency
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve dependency details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        dependency = self._get_object()
        initial = json.loads(dependency.text)
	return initial
