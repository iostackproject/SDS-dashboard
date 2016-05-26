from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


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
            response = api.dsl_add_static_policy(request, data['policy'])
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created policy/rule: %s') % data['policy'])
                return data
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:storagepolicies:index")
            error_message = "Unable to create policy/rule.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdatePolicy(forms.SelfHandlingForm):
    object_type = forms.CharField(max_length=255,
                                  label=_("Object Type"),
                                  help_text=_("The type of object which the rule will be apply."))

    object_size = forms.CharField(max_length=255,
                                  label=_("Object Size"),
                                  help_text=_("The size of object which the rule will be apply."))

    execution_server = forms.CharField(max_length=255,
                                       label=_("Execution Server"))

    execution_server_reverse = forms.CharField(max_length=255,
                                               label=_("Execution Server Reverse"))

    execution_order = forms.CharField(max_length=255,
                                      label=_("Execution Order"),
                                      help_text=_("The order in which the policy will be executed."))

    params = forms.CharField(max_length=255,
                             label=_("Parameters"),
                             help_text=_("Parameters list."))

    def __init__(self, request, *args, **kwargs):
        super(UpdatePolicy, self).__init__(request, *args, **kwargs)

    failure_url = 'horizon:sdscontroller:storagepolicies:index'

    def handle(self, request, data):
        try:
            policy_id = self.initial['id']
            # print "\n#################\n", request, "\n#################\n", data, "\n#################\n"
            response = api.dsl_update_static_policy(request, policy_id, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully policy updated.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:storagepolicies:index")
            error_message = "Unable to update policy.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
