from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.sdscontroller.administration.filters import views

VIEWS_MOD = 'openstack_dashboard.dashboards.sdscontroller.administration.filters.views'

urlpatterns = patterns(
    VIEWS_MOD,
    url(r'^upload/$', views.UploadView.as_view(), name='upload'),
    url(r'^download/(?P<filter_id>[^/]+)/$', views.download_filter, name='download'),
    url(r'^update/(?P<filter_id>[^/]+)/$', views.UpdateView.as_view(), name='update'),
)
