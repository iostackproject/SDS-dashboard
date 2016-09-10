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

from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.sdscontroller.sds_storagegroups \
    .groups import views


VIEWS_MOD = ('openstack_dashboard.dashboards.sdscontroller.sds_storagegroups.groups.views')

urlpatterns = patterns(
    'VIEWS_MOD',
    url(r'^create_groups', views.CreateGroupView.as_view(),
        name='create_group'),
    url(r'^(?P<id>[^/]+)/update/$', views.UpdateGroupView.as_view(), 
        name='update'),
)
