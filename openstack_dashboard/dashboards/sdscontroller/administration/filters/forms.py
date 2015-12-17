# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError  # noqa
from django.core.urlresolvers import reverse

from horizon import exceptions
from horizon import forms
from horizon import messages

import json

from openstack_dashboard.dashboards.sdscontroller import api_sds_controller as api


class UploadFilter(forms.SelfHandlingForm):

    name = forms.CharField(max_length=255,
                           label=_("Name"),
                           help_text=_("The name of the filter to be created."),
                           widget=forms.TextInput(
                               attrs={"ng-model": "name", "not-blank": ""}
                           ))

    language = forms.CharField(max_length=255,
                           label=_("Program Language"),
                           help_text=_("The written language of the filter."),
                           widget=forms.TextInput(
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

    path = forms.CharField(max_length=255,
                           required=False,
                           widget=forms.HiddenInput)

    filter_file = forms.FileField(label=_("File"),
                                  required=True,
                                  allow_empty_file=False)

    def __init__(self, request, *args, **kwargs):
        super(UploadFilter, self).__init__(request, *args, **kwargs)

    # def _set_filter_path(self, data):
    #     if data['path']:
    #         filter_path = "/".join([data['path'].rstrip("/"), data['name']])
    #     else:
    #         filter_path = data['name']
    #     return filter_path

    # def clean(self):
    #     data = super(UploadFilter, self).clean()
    #
    #     image_file = data.get('filter_file', None)
    #     image_url = data.get('image_url', None)
    #
    #     if not image_url and not image_file:
    #         raise ValidationError(
    #             _("A external file must be specified."))
    #     else:
    #         return data

    def handle(self, request, data):
        filter_file = data['filter_file']

        name = data["name"]
        language = data["language"]
        interface_version = data["interface_version"]
        dependencies = data["dependencies"]
        object_metadata = data["object_metadata"]
        main = data["main"]

        if object_metadata is None or object_metadata is "":
            object_metadata = "no"
        if dependencies is None or dependencies is "":
            dependencies = ""
        try:
            response = api.fil_create_filter(name, language, interface_version, main, dependencies, object_metadata)

            if 200 <= response.status_code < 300:
                filter_id = json.loads(response.text)["id"]
                response = api.fil_upload_filter_data(filter_id, filter_file)

                if 200 <= response.status_code < 300:
                    messages.success(request, _('Successfully filter creation and upload.'))
                    return data
                else:
                    raise ValueError(response.text)
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to create filter.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)
