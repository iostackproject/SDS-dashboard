import json

from django import http
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller.administration.filters import forms as filters_forms


class UploadView(forms.ModalFormView):
    form_class = filters_forms.UploadFilter
    form_id = "upload_filter_form"

    modal_header = _("Upload A Filter")
    submit_label = _("Upload Filter")
    submit_url = reverse_lazy('horizon:sdscontroller:administration:filters:upload')
    template_name = "sdscontroller/administration/filters/upload.html"
    context_object_name = 'filter'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Upload A Filter")


def download_filter(request, filter_id):
    try:
        filter_response = api.fil_download_filter_data(request, filter_id)

        # Generate response
        response = http.StreamingHttpResponse(filter_response.content)
        response['Content-Disposition'] = filter_response.headers['Content-Disposition']
        response['Content-Type'] = filter_response.headers['Content-Type']
        response['Content-Length'] = filter_response.headers['Content-Length']
        return response

    except Exception as exc:
        redirect = reverse("horizon:sdscontroller:administration:index")
        exceptions.handle(request, _(exc.message), redirect=redirect)


class UpdateView(forms.ModalFormView):
    form_class = filters_forms.UpdateFilter
    form_id = "update_filter_form"
    modal_header = _("Update A Filter")
    submit_label = _("Update Filter")
    submit_url = "horizon:sdscontroller:administration:filters:update"
    template_name = "sdscontroller/administration/filters/update.html"
    context_object_name = 'filter'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Update A Filter")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['filter_id'] = self.kwargs['filter_id']
        args = (self.kwargs['filter_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        filter_id = self.kwargs['filter_id']
        try:
            filter = api.fil_get_filter_metadata(self.request, filter_id)
            return filter
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve filter details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        filter = self._get_object()
        initial = json.loads(filter.text)
        # initial = super(UpdateView, self).get_initial()
        # initial['name'] = "my filter name"
        return initial


classes = ("ajax-modal",)
