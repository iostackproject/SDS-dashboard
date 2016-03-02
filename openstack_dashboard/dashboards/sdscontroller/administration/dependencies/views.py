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

"""
Views for managing SDS Dependencies.
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from horizon import forms

from openstack_dashboard.dashboards.sdscontroller.administration.dependencies import forms as dependencies_forms


class UploadView(forms.ModalFormView):
    form_class = dependencies_forms.UploadDependency
    form_id = "upload_dependency_form"

    modal_header = _("Upload A Dependency")
    submit_label = _("Upload Dependency")
    submit_url = reverse_lazy('horizon:sdscontroller:administration:dependencies:upload')
    template_name = "sdscontroller/administration/dependencies/upload.html"
    context_object_name = 'dependency'
    success_url = reverse_lazy('horizon:sdscontroller:administration:index')
    page_title = _("Upload A Dependency")

