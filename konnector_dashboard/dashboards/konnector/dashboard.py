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

from django.utils.translation import ugettext_lazy as _

import horizon

class Blockstorage(horizon.PanelGroup):
    slug = "blockstorage"
    name = _("Block Storage")
    panels = ('sds_storagepolicies', 'sds_storagegroups','sds_volumes','sds_storagemonitoring', )

class KonnectorController(horizon.Dashboard):
    name = _("Konnector")
    slug = "konnector"
    panels = (Blockstorage,)  # Add your panels here.
    default_panel = 'sds_storagepolicies'  # Specify the slug of the default panel.
    permissions = ('openstack.roles.admin',)


horizon.register(KonnectorController)