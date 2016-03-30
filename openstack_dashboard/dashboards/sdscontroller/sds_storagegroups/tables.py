from django.utils.translation import ugettext_lazy as _

from openstack_dashboard.dashboards.sdscontroller.sds_storagegroups.groups.\
    tables import GroupsTable as tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class InstancesTable(tables):
    id = tables.Column('id', verbose_name=_("ID"))
    group = tables.Column('group', verbose_name=_("Group"))

    class Meta:
        name = "instances"
        verbose_name = _("Instances")
        table_actions = (MyFilterAction,)
