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


class CreateFilter(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Filter")
    url = "horizon:sdscontroller:administration:registry_dsl:create_filter"
    classes = ("ajax-modal",)
    icon = "plus"


class DeleteDslFilter(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Filter",
            u"Delete Filters",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Filter",
            u"Deleted Filters",
            count
        )

    name = "delete_filter"
    success_url = "horizon:sdscontroller:administration:index"

    def delete(self, request, obj_id):
        try:
            datum = self.table.get_object_by_id(obj_id)
            obj_name = datum.name
            response = api.dsl_delete_filter(request, obj_name)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully deleted filter: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to remove filter.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class DeleteMultipleDslFilters(DeleteDslFilter):
    name = "delete_multiple_filters"


class DslFilterTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    filter_identifier = tables.Column('filter_identifier', verbose_name=_("Filter Identifier"))
    activation_url = tables.Column('activation_url', verbose_name=_("Activation Url"))
    valid_parameters = tables.Column('valid_parameters', verbose_name=_("Valid Parameters"))

    class Meta:
        name = "dsl_filters"
        verbose_name = _("Filters")
        table_actions = (MyFilterAction, CreateFilter, DeleteMultipleDslFilters,)


class InstancesTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    status = tables.Column('status', verbose_name=_("Status"))
    zone = tables.Column('availability_zone', verbose_name=_("Availability Zone"))
    image_name = tables.Column('image_name', verbose_name=_("Image Name"))

    class Meta:
        name = "instances"
        verbose_name = _("Instances")
        table_actions = (MyFilterAction,)
