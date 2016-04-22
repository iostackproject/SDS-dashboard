from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.proxy_sorting import views

VIEWS_MOD = ('openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.proxy_sorting.views')

urlpatterns = patterns(
    VIEWS_MOD,
    url(r'^update/$', views.UpdateView.as_view(), name='update'),
)
