from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from openstack_dashboard.dashboards.sdscontroller.bandwidth_differentiation.change_swift import \
    forms as change_swift_forms


class CSwiftView(forms.ModalFormView):
    form_class = change_swift_forms.SelectSwiftVersion
    form_id = "change_swift_form"

    modal_header = _("Change Swift")
    submit_label = _("Change")
    submit_url = reverse_lazy('horizon:sdscontroller:bandwidth_differentiation:change_swift:change')
    template_name = "sdscontroller/bandwidth_differentiation/change_swift/change_swift.html"
    # context_object_name = 'filter'
    success_url = reverse_lazy('horizon:sdscontroller:bandwidth_differentiation:index')
    page_title = _("Change Filter")

