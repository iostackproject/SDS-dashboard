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

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import forms

from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl \
    import forms as policies_forms


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
