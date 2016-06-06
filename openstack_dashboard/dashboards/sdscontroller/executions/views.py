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
from . import tabs as mydashboard_tabs
from . import forms as project_forms

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from horizon import tabs
from horizon import forms
from horizon import exceptions
from horizon.utils import memoized

from openstack_dashboard.api import zoeapi


class IndexView(tabs.TabbedTableView):
    tab_group_class = mydashboard_tabs.MypanelTabs
    template_name = 'sdscontroller/executions/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class CreateExecutionView(forms.ModalFormView):
    form_class = project_forms.CreateExecutionForm
    template_name = 'sdscontroller/executions/create.html'
    success_url = reverse_lazy("horizon:sdscontroller:executions:index")
    modal_id = "create_execution_modal"
    modal_header = _("Create Execution")
    submit_label = _("Create Execution")
    submit_url = "horizon:sdscontroller:executions:create"

    def form_valid(self, form):
        return super(CreateExecutionView, self).form_valid(form)

    def get_initial(self):
        initial = super(CreateExecutionView, self).get_initial()
        initial['name'] = ''
        initial['app_name'] = ''
        return initial

    def get_context_data(self, **kwargs):
        context = super(CreateExecutionView, self).get_context_data(**kwargs)
        return context


class ExecutionDetailsView(forms.ModalFormMixin, generic.TemplateView):
    template_name = 'sdscontroller/executions/details.html'
    page_title = _("Executions Details")

    @memoized.memoized_method
    def get_object(self):
        try:
            return zoeapi.get_execution_details(self.kwargs["instance_id"])
        except Exception:
            redirect = reverse("horizon:sdscontroller:executions:index")
            exceptions.handle(self.request,
                              _('Unable to retrieve details.'),
                              redirect=redirect)

    def get_context_data(self, **kwargs):
        context = super(ExecutionDetailsView, self).get_context_data(**kwargs)
        context['execution'] = self.get_object()
        return context

