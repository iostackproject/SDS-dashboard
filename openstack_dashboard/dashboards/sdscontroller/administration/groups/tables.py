from django.utils.translation import ugettext_lazy as _

from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class GroupsTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    tenants = tables.Column('tenants', verbose_name=_("Tenants"))

    class Meta:
        name = "groups"
        verbose_name = _("Groups")
        table_actions = (MyFilterAction,)