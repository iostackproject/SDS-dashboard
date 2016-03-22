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



class UpdateDependency(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal","btn-update",)
    def get_link_url(self, dependency):
        base_url = reverse("horizon:sdscontroller:administration:dependencies:update", kwargs={'dependency_id': dependency.id})
        return base_url

class UpdateCell(tables.UpdateAction):
    def allowed(self, request, project, cell):
	return((cell.column.name== 'name')or
		(cell.column.name== 'version')or
		(cell.column.name== 'permission'))	

    def update_cell(self, request,datum, id,cell_name, new_cell_value):
        try:
            # updating changed value by new value
            response = api.fil_get_dependency_metadata(request, id)
            data = json.loads(response.text)
            data[cell_name] = new_cell_value
            api.fil_update_dependency_metadata(request,id,data)
        except Conflict:
            # Returning a nice error message about name conflict. The message
            # from exception is not that clear for the user
            message = _("Cant change value")
            raise ValidationError(message)
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True


class UpdateRow(tables.Row):
    ajax = True
    def get_data(self, request, id):
        response = api.fil_get_dependency_metadata(request, id)
        data = json.loads(response.text)
	filter = Dependency(data['id'],data['name'],
		data['version'],data['permission'])
        return filter


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
	row_actions = (UpdateDependency, DeleteDependency)
	row_class = UpdateRow
