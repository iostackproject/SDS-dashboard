from django.utils.translation import ugettext_lazy as _
from horizon.utils.urlresolvers import reverse
from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class UploadFilter(tables.LinkAction):
    name = "upload"
    verbose_name = _("Upload Filter")
    url = "horizon:sdscontroller:administration:filters:upload"
    classes = ("ajax-modal",)
    icon = "upload"


class FilterTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    language = tables.Column('language', verbose_name=_("Language"))
    interface_version = tables.Column('interface_version', verbose_name=_("Interface Version"))
    dependencies = tables.Column('dependencies', verbose_name=_("Dependencies"))
    object_metadata = tables.Column('object_metadata', verbose_name=_("Object Metadata"))
    main = tables.Column('main', verbose_name=_("Main"))

    class Meta:
        name = "filters"
        verbose_name = _("Filters")
        table_actions = (MyFilterAction, UploadFilter,)
