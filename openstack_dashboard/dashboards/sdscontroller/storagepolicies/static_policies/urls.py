from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.sdscontroller.storagepolicies.static_policies import views

VIEWS_MOD = 'openstack_dashboard.dashboards.sdscontroller.storagepolicies.static_policies.views'

urlpatterns = patterns(
    VIEWS_MOD,
    url(r'^create_policy/$', views.CreatePolicyView.as_view(), name='create_policy'),
    url(r'^create_policy_dsl/$', views.CreatePolicyDSLView.as_view(), name='create_policy_dsl'),
    url(r'^update_policy/(?P<policy_id>[^/]+)/$', views.UpdatePolicyView.as_view(), name='update_policy'),
)
