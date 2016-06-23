import json

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from openstack_dashboard.dashboards.sdscontroller.administration.metric_modules import forms as metric_modules_forms


class UploadView(forms.ModalFormView):
    form_class = metric_modules_forms.UploadMetricModule
    form_id = "upload_metric_module_form"
    modal_header = _("Upload Metric Module")
    submit_label = _("Upload Metric Module")
    submit_url = reverse_lazy('horizon:sdscontroller:administration:metric_modules:upload_metric_module')
    template_name = "sdscontroller/administration/metric_modules/upload_metric_module.html"
    context_object_name = 'metric_module'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Upload Metric Module")


class UpdateView(forms.ModalFormView):
    form_class = metric_modules_forms.UpdateMetricModule
    form_id = "update_metric_module_form"
    modal_header = _("Update Metric Module")
    submit_label = _("Update Metric Module")
    submit_url = "horizon:sdscontroller:administration:metric_modules:update_metric_module"
    template_name = "sdscontroller/administration/filters/update_metric_module.html"
    context_object_name = 'metric_module'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Update Metric Module")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['metric_module_id'] = self.kwargs['metric_module_id']
        args = (self.kwargs['metric_module_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    # TODO: Change '_get_object' method
    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        metric_module_id = self.kwargs['metric_module_id']
        try:
            # metric_module = api.mtr_get_metric_module_metadata(self.request, metric_module_id)
            # return metric_module
            return None
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve metric modules details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        metric_module = self._get_object()
        initial = json.loads(metric_module.text)
        return initial


classes = ("ajax-modal",)
