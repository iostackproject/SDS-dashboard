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
Views for managing volumes.
"""

import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils import encoding
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import tabs
from horizon.utils import memoized

from openstack_dashboard import api
from openstack_dashboard.api import cinder
from openstack_dashboard import exceptions as dashboard_exception
from openstack_dashboard.usage import quotas
from openstack_dashboard.utils import filters

from openstack_dashboard.dashboards.sdscontroller.sds_volumes \
    .volumes import forms as project_forms
from openstack_dashboard.dashboards.sdscontroller.sds_volumes \
    .volumes import tables as project_tables
from openstack_dashboard.dashboards.sdscontroller.sds_volumes \
    .volumes import tabs as project_tabs

class DetailView(tabs.TabView):
    tab_group_class = project_tabs.VolumeDetailTabs
    template_name = 'horizon/common/_detail.html'
    page_title = "{{ volume.name|default:volume.id }}"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        volume = self.get_data()
        table = project_tables.VolumesTable(self.request)
        context["volume"] = volume
        context["url"] = self.get_redirect_url()
        context["actions"] = table.render_row_actions(volume)
        choices = project_tables.VolumesTableBase.STATUS_DISPLAY_CHOICES
        volume.status_label = filters.get_display_label(choices, volume.status)
        return context

    @memoized.memoized_method
    def get_data(self):
        try:
            volume_id = self.kwargs['volume_id']
            volume = cinder.volume_get(self.request, volume_id)
            for att in volume.attachments:
                att['instance'] = api.nova.server_get(self.request,
                                                      att['server_id'])
        except Exception:
            redirect = self.get_redirect_url()
            exceptions.handle(self.request,
                              _('Unable to retrieve volume details.'),
                              redirect=redirect)
        return volume

    def get_redirect_url(self):
        return reverse('horizon:sdscontroller:sds_volumes:index')

    def get_tabs(self, request, *args, **kwargs):
        volume = self.get_data()
        return self.tab_group_class(request, volume=volume, **kwargs)


class CreateView(forms.ModalFormView):
    form_class = project_forms.CreateForm
    modal_header = _("Create Volume")
    template_name = 'sdscontroller/sds_volumes/volumes/create.html'
    submit_label = _("Create Volume")
    submit_url = reverse_lazy("horizon:sdscontroller:sds_volumes:volumes:create_volume")
    success_url = reverse_lazy("horizon:sdscontroller:sds_volumes:volumes_tab")
    page_title = _("Create a Volume")

    def get_initial(self):
        initial = super(CreateView, self).get_initial()
        self.default_vol_type = None
        try:
            self.default_vol_type = cinder.volume_type_default(self.request)
            initial['type'] = self.default_vol_type.name
        except dashboard_exception.NOT_FOUND:
            pass
        return initial

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        try:
            context['usages'] = quotas.tenant_limit_usages(self.request)
            context['volume_types'] = self._get_volume_types()
        except Exception:
            exceptions.handle(self.request)
        return context

    def _get_volume_types(self):
        try:
            volume_types = cinder.volume_type_list(self.request)
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve volume type list.'))

        # check if we have default volume type so we can present the
        # description of no volume type differently
        no_type_description = None
        if self.default_vol_type is None:
            message = \
                _("If \"No volume type\" is selected, the volume will be "
                  "created without a volume type.")

            no_type_description = encoding.force_text(message)

        type_descriptions = [{'name': 'no_type',
                              'description': no_type_description}] + \
                            [{'name': type.name,
                              'description': getattr(type, "description", "")}
                             for type in volume_types]

        return json.dumps(type_descriptions)   