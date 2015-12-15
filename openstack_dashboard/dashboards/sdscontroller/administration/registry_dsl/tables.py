from django.utils.translation import ugettext_lazy as _

from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateFilter(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Filter")
    url = "horizon:sdscontroller:administration:registry_dsl:create_filter"
    classes = ("ajax-modal",)
    icon = "plus"


class DslFilterTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    filter_identifier = tables.Column('filter_identifier', verbose_name=_("Filter Identifier"))
    activation_url = tables.Column('activation_url', verbose_name=_("Activation Url"))
    valid_parameters = tables.Column('valid_parameters', verbose_name=_("Valid Parameters"))

    class Meta:
        name = "dsl_filters"
        verbose_name = _("Filters")
        table_actions = (MyFilterAction, CreateFilter,)


class InstancesTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    status = tables.Column('status', verbose_name=_("Status"))
    zone = tables.Column('availability_zone', verbose_name=_("Availability Zone"))
    image_name = tables.Column('image_name', verbose_name=_("Image Name"))

    class Meta:
        name = "instances"
        verbose_name = _("Instances")
        table_actions = (MyFilterAction,)
