import json

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import common
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class UploadFilter(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the filter to be created."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))

    language = forms.ChoiceField(choices=common.get_filter_type_choices(),
                                 label=_("Program Language"),
                                 help_text=_("The written language of the filter."),
                                 required=True,
                                 widget=forms.Select(
                                     attrs={"ng-model": "language", "not-blank": ""}
                                 ))

    interface_version = forms.CharField(max_length=255,
                                        label=_("Interface Version"),
                                        required=False,
                                        help_text=_("Interface Version"),
                                        widget=forms.TextInput(
                                            attrs={"ng-model": "interface_version", "not-blank": ""}
                                        ))

    dependencies = forms.CharField(max_length=255,
                                   label=_("Dependencies"),
                                   required=False,
                                   help_text=_("A comma separated list of dependencies"),
                                   widget=forms.TextInput(
                                       attrs={"ng-model": "dependencies"}
                                   ))

    object_metadata = forms.CharField(max_length=255,
                                      label=_("Object Metadata"),
                                      required=False,
                                      help_text=_("Currently, not in use, but must appear. Use the value 'no'"),
                                      widget=forms.TextInput(
                                          attrs={"ng-model": "object_metadata"}
                                      ))
    main = forms.CharField(max_length=255,
                           label=_("Main Class"),
                           help_text=_("The name of the class that implements the Filters API."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "main", "not-blank": ""}
                           ))

    is_put = forms.BooleanField(required=False)
    is_get = forms.BooleanField(required=False)
    has_reverse = forms.BooleanField(required=False)

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

    execution_server_reverse = forms.ChoiceField(
        label=_('Execution Server Reverse'),
        choices=[
            ('proxy', _('Proxy Server')),
            ('object', _('Object Storage Servers'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    filter_file = forms.FileField(label=_("File"),
                                  required=True,
                                  allow_empty_file=False)

    def __init__(self, request, *args, **kwargs):
        super(UploadFilter, self).__init__(request, *args, **kwargs)
        common.get_filter_type_choices()

    @staticmethod
    def handle(request, data):
        filter_file = data['filter_file']
        del data['filter_file']

        try:
            response = api.fil_create_filter(request, data)

            if 200 <= response.status_code < 300:
                filter_id = json.loads(response.text)["id"]
                response = api.fil_upload_filter_data(request, filter_id, filter_file)

                if 200 <= response.status_code < 300:
                    messages.success(request, _('Successfully filter creation and upload.'))
                    return data
                else:
                    raise sdsexception.SdsException(response.text)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to create filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateFilter(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Name"), help_text=_("The name of the filter to be created."))

    language = forms.ChoiceField(choices=common.get_filter_type_choices(), label=_("Program Language"), help_text=_("The written language of the filter."),
                                 required=True)

    interface_version = forms.CharField(max_length=255,
                                        label=_("Interface Version"),
                                        required=False,
                                        help_text=_("Interface Version"))

    dependencies = forms.CharField(max_length=255,
                                   label=_("Dependencies"),
                                   required=False,
                                   help_text=_("A comma separated list of dependencies"))

    object_metadata = forms.CharField(max_length=255,
                                      label=_("Object Metadata"),
                                      required=False,
                                      help_text=_("Currently, not in use, but must appear. Use the value 'no'"))

    main = forms.CharField(max_length=255,
                           label=_("Main Class"),
                           help_text=_("The name of the class that implements the Filters API."))

    # TODO: Check this, not works properly on update
    is_put = forms.BooleanField(required=False)
    is_get = forms.BooleanField(required=False)
    has_reverse = forms.BooleanField(required=False)

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[
            ('proxy', _('Proxy Server')),
            ('object', _('Object Storage Servers'))
        ])

    execution_server_reverse = forms.ChoiceField(
        label=_('Execution Server Reverse'),
        choices=[
            ('proxy', _('Proxy Server')),
            ('object', _('Object Storage Servers'))
        ]
    )

    def __init__(self, request, *args, **kwargs):
        super(UpdateFilter, self).__init__(request, *args, **kwargs)
        common.get_filter_type_choices()

    failure_url = 'horizon:sdscontroller:administration:index'

    def handle(self, request, data):
        try:
            filter_id = self.initial['id']
            # print "\n#################\n", request, "\n#################\n", data, "\n#################\n"
            response = api.fil_update_filter_metadata(request, filter_id, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully filter updated.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to update filter.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
