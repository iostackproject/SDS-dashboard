from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from django.core.urlresolvers import reverse

from horizon import tables
from horizon import exceptions
from horizon import messages

from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception

class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class UpdateSortedMethod(tables.LinkAction):
    name = "update"
    verbose_name = _("Update Sorted Method")
    url = "horizon:sdscontroller:administration:bw:update"
    classes = ("ajax-modal",)
    icon = "update"



class BWTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))

    class Meta:
        name = "bw"
        verbose_name = _("BW")
        table_actions = (MyFilterAction, UpdateSortedMethod,)
