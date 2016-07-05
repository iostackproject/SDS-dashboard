import calendar
import json
import time

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import tables
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception
from openstack_dashboard.dashboards.sdscontroller.administration.nodes.models import Node


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class NodesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    ip = tables.Column('ip', verbose_name="IP")
    last_ping = tables.Column(lambda obj: '{0} seconds ago'.format(calendar.timegm(time.gmtime()) - int(float(getattr(obj, 'last_ping', '0')))),
                              verbose_name="Last ping")

    # last_ping = tables.Column(lambda obj: str(calendar.timegm(time.gmtime()) - int(float(getattr(obj, 'last_ping', '0')))) + _(' seconds ago'),
    #                          verbose_name=_("Last ping"))
    type = tables.Column('type', verbose_name=_("Type"))

    class Meta:
        name = "nodes"
        verbose_name = _("Nodes")
        table_actions = (MyFilterAction,)
