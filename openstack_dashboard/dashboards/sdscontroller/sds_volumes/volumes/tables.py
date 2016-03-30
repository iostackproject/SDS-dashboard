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

from django.core.urlresolvers import NoReverseMatch  # noqa
from django.core.urlresolvers import reverse
from django.http import HttpResponse  # noqa
from django.template import defaultfilters as filters
from django.utils import html
from django.utils.http import urlencode
from django.utils import safestring
from django.utils.translation import pgettext_lazy
from django.utils.translation import string_concat  # noqa
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import exceptions
from horizon import messages
from horizon import tables

from openstack_dashboard import api
from openstack_dashboard.api import cinder
from openstack_dashboard import policy
from openstack_dashboard.api import sds_controller_blockstorage as sdsapi
import json

DELETABLE_STATES = ("available", "error", "error_extending")

class VolumePolicyTargetMixin(policy.PolicyTargetMixin):
    policy_target_attrs = (("project_id", 'os-vol-tenant-attr:tenant_id'),)


class DeleteVolume(VolumePolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Volume",
            u"Delete Volumes",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of Volume",
            u"Scheduled deletion of Volumes",
            count
        )

    policy_rules = (("volume", "volume:delete"),)

    def delete(self, request, obj_id):
        cinder.volume_delete(request, obj_id)

    def allowed(self, request, volume=None):
        if volume:
            return (volume.status in DELETABLE_STATES and
                    not getattr(volume, 'has_snapshot', False))
        return True


class CreateVolume(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Volume")
    url = "horizon:sdscontroller:sds_volumes:volumes:create_volume"
    classes = ("ajax-modal", "btn-create")
    icon = "plus"
    policy_rules = (("volume", "volume:create"),)
    ajax = True

    def __init__(self, attrs=None, **kwargs):
        kwargs['preempt'] = True
        super(CreateVolume, self).__init__(attrs, **kwargs)

    def allowed(self, request, volume=None):
        limits = api.cinder.tenant_absolute_limits(request)

        gb_available = (limits.get('maxTotalVolumeGigabytes', float("inf"))
                        - limits.get('totalGigabytesUsed', 0))
        volumes_available = (limits.get('maxTotalVolumes', float("inf"))
                             - limits.get('totalVolumesUsed', 0))

        if gb_available <= 0 or volumes_available <= 0:
            if "disabled" not in self.classes:
                self.classes = [c for c in self.classes] + ['disabled']
                self.verbose_name = string_concat(self.verbose_name, ' ',
                                                  _("(Quota exceeded)"))
        else:
            self.verbose_name = _("Create Volume")
            classes = [c for c in self.classes if c != "disabled"]
            self.classes = classes
        return True

    def single(self, table, request, object_id=None):
        self.allowed(request, None)
        return HttpResponse(self.render())

class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, volume_id):
        volume = cinder.volume_get(request, volume_id)
        return volume


def get_size(volume):
    return _("%sGB") % volume.size

class AttachmentColumn(tables.Column):
    """Customized column class.

    So it that does complex processing on the attachments
    for a volume instance.
    """
    def get_raw_data(self, volume):
        request = self.table.request
        link = _('Attached to %(instance)s on %(dev)s')
        attachments = []
        # Filter out "empty" attachments which the client returns...
        for attachment in [att for att in volume.attachments if att]:
            # When a volume is attached it may return the server_id
            # without the server name...
            instance = get_attachment_name(request, attachment)
            vals = {"instance": instance,
                    "dev": html.escape(attachment.get("device", ""))}
            attachments.append(link % vals)
        return safestring.mark_safe(", ".join(attachments))


def get_volume_type(volume):
    return volume.volume_type if volume.volume_type != "None" else None

def get_storage_group(volume):
    volume_metadata = {}
    volume_metadata = volume.metadata
    groupid = volume_metadata.get('storage_group')
    storage_group_name = ""
    try:               
        resp = sdsapi.retrieve_storagegroup(groupid)
        data = resp.json()
        storage_group_name = data.get('name')
    except Exception as e:
        pass    
    return storage_group_name

def get_encrypted_value(volume):
    if not hasattr(volume, 'encrypted') or volume.encrypted is None:
        return _("-")
    elif volume.encrypted is False:
        return _("No")
    else:
        return _("Yes")

def get_attachment_name(request, attachment):
    server_id = attachment.get("server_id", None)
    if "instance" in attachment and attachment['instance']:
        name = attachment["instance"].name
    else:
        try:
            server = api.nova.server_get(request, server_id)
            name = server.name
        except Exception:
            name = None
            exceptions.handle(request, _("Unable to retrieve "
                                         "attachment information."))
    try:
        url = reverse("horizon:project:instances:detail", args=(server_id,))
        instance = '<a href="%s">%s</a>' % (url, html.escape(name))
    except NoReverseMatch:
        instance = html.escape(name)
    return instance                      
    
class VolumesTableBase(tables.DataTable):
    STATUS_CHOICES = (
        ("in-use", True),
        ("available", True),
        ("creating", None),
        ("error", False),
        ("error_extending", False),
        ("maintenance", False),
    )
    STATUS_DISPLAY_CHOICES = (
        ("available", pgettext_lazy("Current status of a Volume",
                                    u"Available")),
        ("in-use", pgettext_lazy("Current status of a Volume", u"In-use")),
        ("error", pgettext_lazy("Current status of a Volume", u"Error")),
        ("creating", pgettext_lazy("Current status of a Volume",
                                   u"Creating")),
        ("error_extending", pgettext_lazy("Current status of a Volume",
                                          u"Error Extending")),
        ("extending", pgettext_lazy("Current status of a Volume",
                                    u"Extending")),
        ("attaching", pgettext_lazy("Current status of a Volume",
                                    u"Attaching")),
        ("detaching", pgettext_lazy("Current status of a Volume",
                                    u"Detaching")),
        ("deleting", pgettext_lazy("Current status of a Volume",
                                   u"Deleting")),
        ("error_deleting", pgettext_lazy("Current status of a Volume",
                                         u"Error deleting")),
        ("backing-up", pgettext_lazy("Current status of a Volume",
                                     u"Backing Up")),
        ("restoring-backup", pgettext_lazy("Current status of a Volume",
                                           u"Restoring Backup")),
        ("error_restoring", pgettext_lazy("Current status of a Volume",
                                          u"Error Restoring")),
        ("maintenance", pgettext_lazy("Current status of a Volume",
                                      u"Maintenance")),
    )
    name = tables.Column("name",
                         verbose_name=_("Name"))
    description = tables.Column("description",
                                verbose_name=_("Description"),
                                truncate=40)
    size = tables.Column(get_size,
                         verbose_name=_("Size"),
                         attrs={'data-type': 'size'})
    status = tables.Column("status",
                           verbose_name=_("Status"),
                           status=True,
                           status_choices=STATUS_CHOICES,
                           display_choices=STATUS_DISPLAY_CHOICES)

    def get_object_display(self, obj):
        return obj.name


class VolumesFilterAction(tables.FilterAction):

    def filter(self, table, volumes, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [volume for volume in volumes
                if q in volume.name.lower()]


class VolumesTable(VolumesTableBase):
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link="horizon:sdscontroller:sds_volumes:volumes:detail")
    volume_type = tables.Column(get_volume_type,
                                verbose_name=_("Type"))
    attachments = AttachmentColumn("attachments",
                                   verbose_name=_("Attached To"))
    availability_zone = tables.Column("availability_zone",
                                      verbose_name=_("Availability Zone"))
    bootable = tables.Column('is_bootable',
                             verbose_name=_("Bootable"),
                             filters=(filters.yesno, filters.capfirst))
    encryption = tables.Column(get_encrypted_value,
                               verbose_name=_("Encrypted"))
    metadata =  tables.Column(get_storage_group,
                                verbose_name=_("Storage Group"))

    class Meta(object):
        name = "volumes"
        verbose_name = _("Volumes")
        status_columns = ["status"]
        row_class = UpdateRow
        table_actions = (CreateVolume, DeleteVolume,)
        row_actions = (DeleteVolume,)