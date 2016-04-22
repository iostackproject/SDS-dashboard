from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.proxy_sorting import forms as proxy_sorting_forms


class UpdateView(forms.ModalFormView):
    form_class = proxy_sorting_forms.CreateSortedMethod
    form_id = "update_proxy_sorting_form"

    modal_header = _("Create Sort Method")
    submit_label = _("Create Sort Method")
    submit_url = reverse_lazy('horizon:sdscontroller:bandwidth_differentiation:proxy_sorting:update')
    template_name = "sdscontroller/bandwidth_differentiation/proxy_sorting/update.html"
    context_object_name = 'proxy_sorting'
    success_url = reverse_lazy('horizon:sdscontroller:bandwidth_differentiation:index')
    page_title = _("Create Sort Method")
