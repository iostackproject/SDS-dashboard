from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from openstack_dashboard.dashboards.sdscontroller.storagepolicies.static_policies import forms as policies_forms


class CreatePolicyView(forms.ModalFormView):
    form_class = policies_forms.CreatePolicy
    modal_header = _("Create Policy")
    modal_id = "create_policy_modal"
    template_name = 'sdscontroller/storagepolicies/static_policies/create_policy.html'
    success_url = reverse_lazy('horizon:sdscontroller:storagepolicies:policy_tab')
    page_title = _("Create a Policy")
    submit_label = _("Create")
    submit_url = reverse_lazy("horizon:sdscontroller:storagepolicies:static_policies:create_policy")
