from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class CreateSortedMethod(forms.SelfHandlingForm):
    sorted_nodes_method = forms.CharField(max_length=255,
                                          label=_("Sorted Nodes Method:"),
                                          help_text=_("The sorted_method name."),
                                          widget=forms.TextInput(
                                              attrs={"ng-model": "sorted_nodes_method", "not-blank": ""}
                                          ))

    sorted_nodes_criterion = forms.CharField(max_length=255,
                                             label=_("Sorted Nodes Criterion:"),
                                             help_text=_("ascending or descending ."),
                                             widget=forms.TextInput(
                                                 attrs={"ng-model": "sorted_nodes_criterion", "not-blank": ""}
                                             ))

    def __init__(self, request, *args, **kwargs):
        super(CreateSortedMethod, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            response = api.set_sort_nodes(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully sorted method creation.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)

        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to create sorted method.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
