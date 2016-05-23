from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from openstack_dashboard.api import sds_controller as api


class CreatePolicy(forms.SelfHandlingForm):
    policy = forms.CharField(max_length=255,
                             label=_("Policy/Rule"),
                             widget=forms.Textarea(
                                 attrs={"ng-model": "interface_version", "not-blank": ""}
                             ))

    def __init__(self, request, *args, **kwargs):
        super(CreatePolicy, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        try:
            response = api.create_policy(request, data['policy'])
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created policy/rule: %s') % data['policy'])
                return data
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:storagepolicies:index")
            error_message = "Unable to create policy/rule.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
