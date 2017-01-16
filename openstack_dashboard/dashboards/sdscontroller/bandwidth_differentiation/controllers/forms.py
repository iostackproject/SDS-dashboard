from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class CreateGETController(forms.SelfHandlingForm):
    controller_file = forms.FileField(label=_("File"), required=True, allow_empty_file=False)
    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kwargs):
        super(CreateGETController, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        file = data['controller_file']

        try:
            data['name'] = 'test'
            data['type'] = 'get'
            del data['controller_file']
            response = api.bw_add_controller(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Successfully controller creation."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to create controller.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class CreatePUTController(forms.SelfHandlingForm):
    controller_file = forms.FileField(label=_("File"), required=True, allow_empty_file=False)
    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kwargs):
        super(CreatePUTController, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        file = data['controller_file']

        try:
            data['name'] = 'test'
            data['type'] = 'put'
            del data['controller_file']
            response = api.bw_add_controller(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Successfully controller creation."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to create controller.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class CreateReplicationController(forms.SelfHandlingForm):
    controller_file = forms.FileField(label=_("File"), required=True, allow_empty_file=False)
    enabled = forms.BooleanField(required=False)

    def __init__(self, request, *args, **kwargs):
        super(CreateReplicationController, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        file = data['controller_file']

        try:
            data['name'] = 'test'
            data['type'] = 'replication'
            del data['controller_file']
            response = api.bw_add_controller(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Successfully controller creation."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to create controller.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
