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
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from horizon import exceptions
from horizon import forms

from horizon.utils import memoized

from openstack_dashboard import api

from openstack_dashboard.dashboards.sdscontroller.executions import forms as project_forms
from openstack_dashboard.dashboards.sdscontroller.executions import tabs as mydashboard_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = mydashboard_tabs.MypanelTabs
    template_name = 'sdscontroller/executions/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class TerminateView(forms.ModalFormView):
    form_class = project_forms.TerminateZoeExecution
    template_name = 'sdscontroller/executions/terminate.html'
    success_url = reverse_lazy("horizon:sdscontroller:executions:index")
    modal_id = "terminate_zoe_execution"
    modal_header = _("Terminate Zoe Execution")
    submit_label = _("Terminate Zoe Execution")
    submit_url = "horizon:sdscontroller:executions:terminate"

    '''
    @memoized.memoized_method
    def get_object(self):
        try:
            return api.nova.server_get(self.request,
                                       self.kwargs["instance_id"])
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to retrieve Zoe execution."))
    '''

    def get_initial(self):
        return {"instance_id": self.kwargs["instance_id"]}

    def get_context_data(self, **kwargs):
        context = super(TerminateView, self).get_context_data(**kwargs)
        instance_id = self.kwargs['instance_id']
        context['instance_id'] = instance_id
        #context['instance'] = self.get_object()
        context['instance'] = None
        context['submit_url'] = reverse(self.submit_url, args=[instance_id])
        return context