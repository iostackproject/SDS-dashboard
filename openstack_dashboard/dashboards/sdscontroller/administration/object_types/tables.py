from django.utils.translation import ugettext_lazy as _

from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class ObjectTypesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    extensions = tables.Column('extensions', verbose_name=_("Extensions"))

    class Meta:
        name = "object_types"
        verbose_name = _("Object Types")
        table_actions = (MyFilterAction,)