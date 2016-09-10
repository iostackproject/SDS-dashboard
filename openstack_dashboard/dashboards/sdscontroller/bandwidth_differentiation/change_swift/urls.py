from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.change_swift import views

VIEWS_MOD = ('openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.change_swift.views')

urlpatterns = patterns(
    VIEWS_MOD,
    url(r'^change/$', views.CSwiftView.as_view(), name='change'),
    #url(r'^change/$', views.CSwiftView.as_view(), name='change'),
    # url(r'^changer/$', views.Changer, name='changer'),

)
