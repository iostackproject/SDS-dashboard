from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.sdscontroller.storagepolicies.static_policies import views

VIEWS_MOD = 'openstack_dashboard.dashboards.sdscontroller.storagepolicies.static_policies.views'

urlpatterns = patterns(
    VIEWS_MOD,
    url(r'^create_policies', views.CreatePolicyView.as_view(), name='create_policy'),
)
