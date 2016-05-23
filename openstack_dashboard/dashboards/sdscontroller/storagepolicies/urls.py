from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.sdscontroller.storagepolicies import views
from openstack_dashboard.dashboards.sdscontroller.storagepolicies.dynamic_policies import urls as dynamic_policies_urls
from openstack_dashboard.dashboards.sdscontroller.storagepolicies.static_policies import urls as static_policies_urls

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'dynamic_policies/', include(dynamic_policies_urls, namespace='dynamic_policies')),
    url(r'static_policies/', include(static_policies_urls, namespace='static_policies')),
    url(r'^\?tab=policies_group_tab__policy_tab$', views.IndexView.as_view(), name='policy_tab'),
)
