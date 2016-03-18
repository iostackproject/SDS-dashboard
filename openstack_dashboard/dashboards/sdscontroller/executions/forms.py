from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard.api import zoeapi


class TerminateZoeExecution(forms.SelfHandlingForm):
    instance_id = forms.CharField(label=_("Instance ID"),
                                  widget=forms.HiddenInput(),
                                  required=False)

    def handle(self, request, data):
        try:
            print("Terminate: ", data['instance_id'])
            zoeapi.terminate_exec(request, data['instance_id'])
            return True
        except Exception:
            exceptions.handle(request, _('Unable to terminate.'))

