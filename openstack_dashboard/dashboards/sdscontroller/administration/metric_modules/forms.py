from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class UploadMetricModule(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the metric module to be created."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))

    interface_version = forms.CharField(max_length=255,
                                        label=_("Interface Version"),
                                        required=False,
                                        help_text=_("Interface Version"),
                                        widget=forms.TextInput(
                                            attrs={"ng-model": "interface_version", "not-blank": ""}
                                        ))

    object_metadata = forms.CharField(max_length=255,
                                      label=_("Object Metadata"),
                                      required=False,
                                      help_text=_("Currently, not in use, but must appear. Use the value 'no'"),
                                      widget=forms.TextInput(
                                          attrs={"ng-model": "object_metadata"}
                                      ))

    is_put = forms.BooleanField(required=False)
    is_get = forms.BooleanField(required=False)

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[
            ('proxy', _('Proxy Server')),
            ('object', _('Object Storage Servers'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    metric_module_file = forms.FileField(label=_("File"),
                                         required=True,
                                         allow_empty_file=False)

    def __init__(self, request, *args, **kwargs):
        super(UploadMetricModule, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):
        metric_module_file = data['metric_module_file']
        del data['metric_module_file']

        try:
            # response = api.fil_create_filter(request, data)
            response = None
            if 200 <= response.status_code < 300:
                # metric_module_id = json.loads(response.text)["id"]
                # response = api.fil_upload_filter_data(request, metric_module_id, metric_module_file)
                response = None
                if 200 <= response.status_code < 300:
                    messages.success(request, _('Successfully metric module creation and upload.'))
                    return data
                else:
                    raise sdsexception.SdsException(response.text)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to create metric module.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateMetricModule(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Name"), help_text=_("The new name of the metric module to be updated."))

    interface_version = forms.CharField(max_length=255,
                                        label=_("Interface Version"),
                                        required=False,
                                        help_text=_("Interface Version"))

    object_metadata = forms.CharField(max_length=255,
                                      label=_("Object Metadata"),
                                      required=False,
                                      help_text=_("Currently, not in use, but must appear. Use the value 'no'"))

    # TODO: Check this, not works properly on update
    is_put = forms.BooleanField(required=False)
    is_get = forms.BooleanField(required=False)

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[
            ('proxy', _('Proxy Server')),
            ('object', _('Object Storage Servers'))
        ])

    def __init__(self, request, *args, **kwargs):
        super(UpdateMetricModule, self).__init__(request, *args, **kwargs)

    failure_url = 'horizon:sdscontroller:administration:index'

    def handle(self, request, data):
        try:
            # metric_module_id = self.initial['id']
            # print "\n#################\n", request, "\n#################\n", data, "\n#################\n"
            # response = api.fil_update_filter_metadata(request, metric_module_id, data)
            response = None
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully metric module updated.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to update metric module.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
