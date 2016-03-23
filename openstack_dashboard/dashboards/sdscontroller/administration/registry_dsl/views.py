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
Views for managing filters.
"""
import json

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from horizon import forms
from horizon.utils import memoized
from horizon import exceptions

from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl \
    import forms as policies_forms
from openstack_dashboard.api import sds_controller as api

class CreateFilterView(forms.ModalFormView):
    form_class = policies_forms.CreateFilter
    modal_header = _("Create Filter")
    modal_id = "create_filter_modal"
    template_name = 'sdscontroller/administration/registry_dsl/create_filter.html'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Create a Filter")
    submit_label = _("Create")
    submit_url = reverse_lazy(
        "horizon:sdscontroller:administration:registry_dsl:create_filter")

class UpdateFilterView(forms.ModalFormView):
    form_class = policies_forms.UpdateFilter
    form_id = "update_filter_form"
    modal_header = _("Update A Filter")
    submit_label = _("Update Filter")
    submit_url = "horizon:sdscontroller:administration:registry_dsl:update_filter"
    template_name = "sdscontroller/administration/registry_dsl/update_filter.html"
    context_object_name = 'filter'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Update A Filter")

    def get_context_data(self, **kwargs):
        context = super(UpdateFilterView, self).get_context_data(**kwargs)
        context['name'] = self.kwargs['name']
        args = (self.kwargs['name'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        name = self.kwargs['name']
        try:
            filter = api.dsl_get_filter_metadata(self.request, name)
	    return filter
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve filter details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        filter = self._get_object()
	name = self.kwargs['name']
        initial = json.loads(filter.text)
	initial['name']=name
	print(initial)
	return initial
