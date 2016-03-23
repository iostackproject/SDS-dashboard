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
Views for managing SDS Filters.
"""
import json

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse_lazy

from horizon import forms
from horizon.utils import memoized
from horizon import exceptions
from openstack_dashboard.dashboards.sdscontroller.administration.filters import forms as filters_forms
from openstack_dashboard.api import sds_controller as api


class UploadView(forms.ModalFormView):
    form_class = filters_forms.UploadFilter
    form_id = "upload_filter_form"

    modal_header = _("Upload A Filter")
    submit_label = _("Upload Filter")
    submit_url = reverse_lazy('horizon:sdscontroller:administration:filters:upload')
    template_name = "sdscontroller/administration/filters/upload.html"
    context_object_name = 'filter'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Upload A Filter")


class UpdateView(forms.ModalFormView):
    form_class = filters_forms.UpdateFilter
    form_id = "update_filter_form"
    modal_header = _("Update A Filter")
    submit_label = _("Update Filter")
    submit_url = "horizon:sdscontroller:administration:filters:update"
    template_name = "sdscontroller/administration/filters/update.html"
    context_object_name = 'filter'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Update A Filter")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['filter_id'] = self.kwargs['filter_id']
        args = (self.kwargs['filter_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        filter_id = self.kwargs['filter_id']
        try:
            filter = api.fil_get_filter_metadata(self.request, filter_id)
            return filter
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve filter details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        filter = self._get_object()
        initial = json.loads(filter.text)
        # initial = super(UpdateView, self).get_initial()
        # initial['name'] = "my filter name"
        return initial


classes = ("ajax-modal",)
