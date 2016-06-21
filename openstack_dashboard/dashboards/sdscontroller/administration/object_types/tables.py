from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import exceptions
from horizon import messages
from horizon import tables
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateObjectType(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Object Type")
    url = "horizon:sdscontroller:administration:object_types:create"
    classes = ("ajax-modal",)
    icon = "plus"


class DeleteObjectType(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Object Type",
            u"Delete Object Types",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Object Type deleted",
            u"Object Types deleted",
            count
        )

    name = "delete_object_type"
    success_url = "horizon:sdscontroller:administration:index"

    def delete(self, request, obj_id):
        try:
            response = api.dsl_delete_object_type(request, obj_id)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully deleted object type: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to delete object type.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class ObjectTypesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    extensions = tables.Column('extensions', verbose_name=_("Extensions"))

    class Meta:
        name = "object_types"
        verbose_name = _("Object Types")
        table_actions = (MyFilterAction,CreateObjectType,)
        row_actions = (DeleteObjectType,)