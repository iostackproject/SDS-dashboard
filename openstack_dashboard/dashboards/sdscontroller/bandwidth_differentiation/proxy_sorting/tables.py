from django.utils.translation import ugettext_lazy as _

from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateSortedMethod(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Sorted Method")
    url = "horizon:sdscontroller:bandwidth_differentiation:proxy_sorting:update"
    classes = ("ajax-modal",)
    icon = "plus"


class ProxySortingTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    criterion = tables.Column('criterion', verbose_name=_("Criterion"))

    class Meta:
        name = "proxy_sorting"
        verbose_name = _("Proxy Sorting")
        table_actions = (MyFilterAction, CreateSortedMethod,)
