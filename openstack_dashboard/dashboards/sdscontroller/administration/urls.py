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
from django.conf.urls import patterns
from django.conf.urls import url
from django.conf.urls import include

from openstack_dashboard.dashboards.sdscontroller.administration import views
from openstack_dashboard.dashboards.sdscontroller.administration.filters import urls as filter_urls
from openstack_dashboard.dashboards.sdscontroller.administration.dependencies import urls as dependencies_urls
from openstack_dashboard.dashboards.sdscontroller.administration.registry_dsl import urls as registry_urls
from openstack_dashboard.dashboards.sdscontroller.administration.bw import urls as bw_urls


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'dependencies/', include(dependencies_urls, namespace="dependencies")),
    url(r'filters/', include(filter_urls, namespace="filters")),
    url(r'bw/', include(bw_urls, namespace="bw")),
    url(r'', include(registry_urls, namespace="registry_dsl")),
)

