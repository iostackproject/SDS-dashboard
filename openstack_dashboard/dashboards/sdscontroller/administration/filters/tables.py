from django.utils.translation import ugettext_lazy as _

from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class FilterTable(tables.DataTable):

    id = tables.Column('id', \
                         verbose_name=_("ID"))
    name = tables.Column('name', \
                         verbose_name=_("Name"))
    interface_version = tables.Column('interface_version', \
                           verbose_name=_("Interface Version"))
    dependencies = tables.Column('dependencies', \
                         verbose_name=_("Dependencies"))
    object_metadata = tables.Column('object_metadata', \
                               verbose_name=_("Object Metadata"))
    main = tables.Column('main', \
                               verbose_name=_("Main"))
    deployed = tables.Column('deployed', \
                               verbose_name=_("Deployed"))

    class Meta:
        name = "filters"
        verbose_name = _("Filters")
        table_actions = (MyFilterAction,)

