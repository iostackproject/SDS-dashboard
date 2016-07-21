from horizon import views


class IndexView(views.APIView):
    template_name = 'sdscontroller/storagemonitoring/system/_swift_project_plots.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        context["ip_host"] = request.META['HTTP_HOST'].split(':')[0]
        return context


class SystemView(views.APIView):
    template_name = 'sdscontroller/storagemonitoring/system/_system_plots.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        context["ip_host"] = request.META['HTTP_HOST'].split(':')[0]
        return context


class SwiftContainerView(views.APIView):
    template_name = 'sdscontroller/storagemonitoring/system/_swift_container_plots.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        context["ip_host"] = request.META['HTTP_HOST'].split(':')[0]
        return context

#
# from horizon import tabs
#
# from openstack_dashboard.dashboards.sdscontroller.administration \
#     import tabs as mydashboard_tabs
#
#
# class IndexView(tabs.TabbedTableView):
#     tab_group_class = mydashboard_tabs.MypanelTabs
#     template_name = 'sdscontroller/administration/index.html'
#
#     def get_data(self, request, context, *args, **kwargs):
#         # Add data to the context here...
#         return context
