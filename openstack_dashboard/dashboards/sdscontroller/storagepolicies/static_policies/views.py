import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller.storagepolicies.static_policies import forms as policies_forms


class CreatePolicyView(forms.ModalFormView):
    form_class = policies_forms.CreatePolicy
    form_id = "create_policy_form"

    modal_header = _("Create Policy")
    modal_id = "create_policy_modal"
    submit_label = _("Create")
    submit_url = reverse_lazy("horizon:sdscontroller:storagepolicies:static_policies:create_policy")
    template_name = 'sdscontroller/storagepolicies/static_policies/create_policy.html'
    content_object_name = 'policy'
    success_url = reverse_lazy('horizon:sdscontroller:storagepolicies:policy_tab')
    page_title = _("Create a Policy")


class UpdatePolicyView(forms.ModalFormView):
    form_class = policies_forms.UpdatePolicy
    form_id = "update_policy_form"
    modal_header = _("Update Policy")
    submit_label = _("Update Policy")
    submit_url = "horizon:sdscontroller:storagepolicies:static_policies:update_policy"
    template_name = "sdscontroller/storagepolicies/static_policies/update_policy.html"
    context_object_name = 'policy'
    success_url = reverse_lazy('horizon:sdscontroller:storagepolicies:index')
    page_title = _("Update Policy")

    def get_context_data(self, **kwargs):
        context = super(UpdatePolicyView, self).get_context_data(**kwargs)
        context['policy_id'] = self.kwargs['policy_id']
        args = (self.kwargs['policy_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        policy_id = self.kwargs['policy_id']
        try:
            policy = api.dsl_get_static_policy(self.request, policy_id)
            return policy
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve policy details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        policy = self._get_object()
        initial = json.loads(policy.text)
        return initial


classes = ("ajax-modal",)
