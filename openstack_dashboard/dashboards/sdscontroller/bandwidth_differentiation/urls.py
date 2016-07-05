from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation import views
from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.proxy_sorting import urls as proxy_sorting_urls
from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.slas import urls as slas_urls
from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.change_swift import urls as change_swift_urls

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'slas/', include(slas_urls, namespace="slas")),
                       url(r'proxy_sorting/', include(proxy_sorting_urls, namespace="proxy_sorting")),
                       url(r'change_swift/', include(change_swift_urls, namespace="change_swift")),
                       )
