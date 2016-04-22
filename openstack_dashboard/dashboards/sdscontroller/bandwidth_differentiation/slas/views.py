import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.slas import forms as slas_forms


class UploadView(forms.ModalFormView):
    form_class = slas_forms.CreateSLA
    form_id = "create_sla_form"

    modal_header = _("Upload A SLA")
    submit_label = _("Upload SLA")
    submit_url = reverse_lazy('horizon:sdscontroller:bandwidth_differentiation:slas:upload')
    template_name = "sdscontroller/bandwidth_differentiation/slas/upload.html"
    context_object_name = 'sla'
    success_url = reverse_lazy('horizon:sdscontroller:bandwidth_differentiation:index')
    page_title = _("Upload A SLA")


class UpdateView(forms.ModalFormView):
    form_class = slas_forms.UpdateSLA
    form_id = "update_sla_form"
    modal_header = _("Update A SLA")
    submit_label = _("Update SLA")
    submit_url = "horizon:sdscontroller:bandwidth_differentiation:slas:update"
    template_name = "sdscontroller/bandwidth_differentiation/slas/update.html"
    context_object_name = 'sla'
    success_url = reverse_lazy('horizon:sdscontroller:bandwidth_differentiation:index')
    page_title = _("Update A SLA")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['sla_id'] = self.kwargs['sla_id']
        args = (self.kwargs['sla_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        sla_id = self.kwargs['sla_id']
        try:
            redirect = self.success_url
            msg = _('Unable to retrieve sla details.')
            exceptions.handle(self.request, msg, redirect=redirect)
            # sla = api.bw_get_sla_metadata(self.request, sla_id)
            # return sla
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve sla details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        sla = self._get_object()
        initial = json.loads(sla.text)
        return initial
