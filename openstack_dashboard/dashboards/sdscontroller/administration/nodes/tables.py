import calendar
import collections
import time

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import register  # noqa

from horizon import tables


class MyProxyFilterAction(tables.FilterAction):
    name = "myproxyfilter"


class RestartProxyAction(tables.LinkAction):
    name = "restart"
    verbose_name = _("Restart Swift")
    # icon = "refresh"

    def get_link_url(self, datum=None):
        # Dummy URL
        base_url = reverse('horizon:sdscontroller:administration:index')
        return base_url


class ProxysTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("Hostname"))
    ip = tables.Column('ip', verbose_name="IP")
    last_ping = tables.Column(lambda obj: '{0} seconds ago'.format(calendar.timegm(time.gmtime()) - int(float(getattr(obj, 'last_ping', '0')))),
                              verbose_name="Last Swift ping")
    node_status = tables.Column(lambda obj: 'UP' if obj is True else 'DOWN', verbose_name="Swift Status", status=True)

    class Meta:
        name = "proxys"
        verbose_name = _("Proxys")
        table_actions = (MyProxyFilterAction,)
        row_actions = (RestartProxyAction,)
        hidden_title = False


@register.filter
def usage_percentage(free, size):
    try:
        usage = float(size - free) * 100 / size
        return "{0:.2f}%".format(usage)
    except (ValueError, ZeroDivisionError):
        return None


def get_devices_info(storage_node):
    template_name = 'sdscontroller/administration/nodes/_devices_info.html'
    ordered_devices = collections.OrderedDict(sorted(storage_node.devices.items()))
    context = {"devices": ordered_devices}
    return template.loader.render_to_string(template_name, context)


STATUS_DISPLAY_CHOICES = (
    (True, 'UP'),
    (False, 'DOWN'),
)


class MyStorageNodeFilterAction(tables.FilterAction):
    name = "mystoragenodefilter"


class RestartStorageNodeAction(tables.LinkAction):
    name = "restart"
    verbose_name = _("Restart Swift")
    # icon = "refresh"

    def get_link_url(self, datum=None):
        # Dummy URL
        base_url = reverse('horizon:sdscontroller:administration:index')
        return base_url


class StorageNodesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("Hostname"))
    ip = tables.Column('ip', verbose_name="IP")
    last_ping = tables.Column(lambda obj: '{0} seconds ago'.format(calendar.timegm(time.gmtime()) - int(float(getattr(obj, 'last_ping', '0')))),
                              verbose_name="Last Swift ping")
    node_status = tables.Column(lambda obj: 'UP' if getattr(obj, 'node_status', False) is True else 'DOWN', verbose_name="Swift Status", status=True)
    devices = tables.Column(get_devices_info, verbose_name=_("Devices"), classes=('nowrap-col', ), sortable=False)

    class Meta:
        name = "storagenodes"
        verbose_name = _("Storage Nodes")
        table_actions = (MyStorageNodeFilterAction,)
        row_actions = (RestartStorageNodeAction,)
        hidden_title = False
