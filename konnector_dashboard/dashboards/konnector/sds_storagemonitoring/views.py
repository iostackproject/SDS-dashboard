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

from horizon import views
from django.utils.translation import ugettext_lazy as _

from konnector_dashboard.dashboards.konnector.sds_storagemonitoring \
    import tabs as mydashboard_tabs

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormView
from konnector_dashboard.dashboards.konnector.sds_storagemonitoring \
    import forms as monitoring_forms

class IndexView(FormView):
    tab_group_class = mydashboard_tabs.MypanelTabs
    form_class = monitoring_forms.SelectVolume
    template_name = 'konnector/sds_storagemonitoring/index.html'

    def get(self, request, *args, **kwargs):       
        form = self.form_class(request, *args, **kwargs)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, *args, **kwargs)
        volume = request.POST['volume']
        ip ='10.30.1.6:5601'
        return render(request, self.template_name, {'form': form, 'ip': ip, 'volume': volume})
