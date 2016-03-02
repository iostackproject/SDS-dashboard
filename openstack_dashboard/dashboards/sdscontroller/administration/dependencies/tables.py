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


class UploadDependency(tables.LinkAction):
    name = "upload"
    verbose_name = _("Upload Dependency")
    url = "horizon:sdscontroller:administration:dependencies:upload"
    classes = ("ajax-modal",)
    icon = "upload"


class DeleteDependency(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Dependency",
            u"Delete Dependencies",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Dependency",
            u"Deleted Dependencies",
            count
        )

    name = "delete_dependency"
    success_url = "horizon:sdscontroller:administration:index"

    def delete(self, request, obj_id):
        try:
            response = api.fil_delete_dependency(request, obj_id)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully deleted dependency: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to remove dependency.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class DeleteMultipleDependencies(DeleteDependency):
    name = "delete_multiple_dependencies"


class DependenciesTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    version = tables.Column('version', verbose_name=_("Version"))
    permissions = tables.Column('permissions', verbose_name=_("Permissions"))

    class Meta:
        name = "dependencies"
        verbose_name = _("Dependencies")
        table_actions = (MyFilterAction, UploadDependency, DeleteMultipleDependencies,)
