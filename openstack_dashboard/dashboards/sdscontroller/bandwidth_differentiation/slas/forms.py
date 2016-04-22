from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


# TODO: Check this, we need to add an API call.
class CreateSLA(forms.SelfHandlingForm):
    tenant = forms.CharField(max_length=255,
                             label=_("Tenant"),
                             help_text=_("Tenant identificator."),
                             widget=forms.TextInput(
                                 attrs={"ng-model": "tenant", "not-blank": ""}
                             ))

    bandwidth = forms.CharField(max_length=255,
                                label=_("Bandwidth"),
                                help_text=_("The bandwidth that you want to assign to the specific tenant."),
                                widget=forms.TextInput(
                                    attrs={"ng-model": "bandwidth", "not-blank": ""}
                                ))

    def __init__(self, request, *args, **kwargs):
        super(CreateSLA, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        try:
            raise sdsexception.SdsException(request)
            # response = api.bw_create_sla(request, data)
            # if 200 <= response.status_code < 300:
            #     messages.success(request, _('Successfully dependency creation and upload.'))
            #     return data
            # else:
            #     raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to create sla.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


# TODO: Check this, we need to add an API call.
class UpdateSLA(forms.SelfHandlingForm):
    bandwidth = forms.CharField(max_length=255,
                                label=_("Bandwidth"),
                                required=False,
                                help_text=_("The new bandwidth that you want to assign to the specific tenant."))

    def __init__(self, request, *args, **kwargs):
        super(UpdateSLA, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            raise sdsexception.SdsException(request)
            # sla_id = self.initial['id']
            # response = api.bw_update_sla(request, sla_id, data['bandwidth'])
            # if 200 <= response.status_code < 300:
            #     messages.success(request, _('Successfully sla update.'))
            #     return data
            # else:
            #     raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to update sla.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
