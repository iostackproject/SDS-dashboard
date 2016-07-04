# Copyright 2012 Nebula, Inc.
# All rights reserved.

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Groups for managing storage groups.
"""
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from django import forms
from horizon import messages
from openstack_dashboard import api
from openstack_dashboard.api import sds_controller_blockstorage as sdsapi
from openstack_dashboard.api import cinder
import json

#create storage group
class SelectVolume(forms.Form):
    volume = forms.ChoiceField(label=_("Volume"))
    def __init__(self, request, *args, **kwargs):
        super(SelectVolume, self).__init__(*args, **kwargs)        
        self.fields['volume'].choices = self.volume_list(request)
        
    def volume_list(self, request):
        try:
            volumes = cinder.volume_list(request)
        except Exception:
            exceptions.handle(request, _('Unable to retrieve volumes.'))
        #
        try:
            resp = sdsapi.list_volumes(request)           
            if resp.status_code == 200:
                data = resp.json()
            else:
                error_message = 'Unable to retrieve volumes.'
                raise ValueError(error_message)
        except Exception:
            exceptions.handle(request, _('Unable to retrieve volumes.'))
        #
        choices = []
        for d in data:
            sid = d['name']
            sserial = d['serial']
            for v in volumes:
                vid = v.id
                if sid == vid:
                    volumeid = sserial
                    volumename = v.name
                    choices.append((volumeid, volumename))
        return choices