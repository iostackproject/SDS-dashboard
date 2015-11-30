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
Policies for managing volumes.
"""
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages


class CreatePolicy(forms.SelfHandlingForm):
    policy = forms.CharField(max_length=255, label=_("Policy/Rule"))

    def handle(self, request, data):
        try:
            print "CAMAMILLA request", request
            print "CAMAMILLA data", data
            print "CAMAMILLA policy/rule to parse :=>", data["policy"]

            messages.success(request,
                             _('Successfully created policy/rule: %s')
                             % data['policy'])
            # TODO Control correct return
            return data
        except Exception as ex:
            # TODO CAMAMILLA
            print "CAMAMILLA Error", getattr(ex, 'code', None)
            if getattr(ex, 'code', None) == 409:
                msg = _('QoS Spec name "%s" already '
                        'exists.') % data['name']
                self._errors['name'] = self.error_class([msg])
            else:
                redirect = reverse("horizon:sdscontroller:storagepolicies:index")
                exceptions.handle(request,
                                  _('Unable to create policy/rule.'),
                                  redirect=redirect)
