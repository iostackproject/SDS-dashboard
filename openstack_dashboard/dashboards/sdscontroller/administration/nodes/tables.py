import calendar
import collections
import json
import time

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django.template.defaultfilters import register  # noqa

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import tables
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception
from openstack_dashboard.dashboards.sdscontroller.administration.nodes.models import ProxyNode, StorageNode


class MyProxyFilterAction(tables.FilterAction):
    name = "myproxyfilter"


class ProxysTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("Hostname"))
    ip = tables.Column('ip', verbose_name="IP")
    last_ping = tables.Column(lambda obj: '{0} seconds ago'.format(calendar.timegm(time.gmtime()) - int(float(getattr(obj, 'last_ping', '0')))),
                              verbose_name="Last ping")
    # last_ping = tables.Column(lambda obj: str(calendar.timegm(time.gmtime()) - int(float(getattr(obj, 'last_ping', '0')))) + _(' seconds ago'),
    #                          verbose_name=_("Last ping"))

    class Meta:
        name = "proxys"
        verbose_name = _("Proxys")
        table_actions = (MyProxyFilterAction,)
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


class MyStorageNodeFilterAction(tables.FilterAction):
    name = "mystoragenodefilter"


class StorageNodesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("Hostname"))
    ip = tables.Column('ip', verbose_name="IP")
    last_ping = tables.Column(lambda obj: '{0} seconds ago'.format(calendar.timegm(time.gmtime()) - int(float(getattr(obj, 'last_ping', '0')))),
                              verbose_name="Last ping")
    devices = tables.Column(get_devices_info, verbose_name=_("Devices"), classes=('nowrap-col', ), sortable=False)

    class Meta:
        name = "storagenodes"
        verbose_name = _("Storage Nodes")
        table_actions = (MyStorageNodeFilterAction,)
        hidden_title = False
