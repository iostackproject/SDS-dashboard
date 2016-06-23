import json

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from keystoneclient.exceptions import Conflict

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import tables
from models import MetricModule
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class UploadMetricModule(tables.LinkAction):
    name = "upload_metric_module"
    verbose_name = _("Upload Metric Module")
    url = "horizon:sdscontroller:administration:metric_modules:upload_metric_module"
    classes = ("ajax-modal",)
    icon = "upload"


class DeleteMetricModule(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Metric Module",
            u"Delete Metric Modules",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Delete Metric Module",
            u"Delete Metric Modules",
            count
        )

    name = "delete_metric_module"
    success_url = "horizon:sdscontroller:administration:index"

    def delete(self, request, obj_id):
        try:
            # response = api.fil_delete_filter(request, obj_id)
            response = None
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully deleted metric module: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to remove metric module.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleMetricModules(DeleteMetricModule):
    name = "delete_multiple_metric_modules"


class UpdateMetricModule(tables.LinkAction):
    name = "update_metric_module"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:sdscontroller:administration:metric_modules:update_metric_module", kwargs={'metric_module_id': datum.id})
        return base_url


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, project, cell):
        return ((cell.column.name == 'name') or
                (cell.column.name == 'interface_version') or
                (cell.column.name == 'object_metadata') or
                (cell.column.name == 'is_put') or
                (cell.column.name == 'is_get') or
                (cell.column.name == 'execution_server'))

    def update_cell(self, request, datum, id, cell_name, new_cell_value):
        try:
            # updating changed value by new value
            # response = api.mtr_get_metric_module_metadata(request, id)
            response = None
            data = json.loads(response.text)
            data[cell_name] = new_cell_value

            # TODO: Check only the valid keys, delete the rest
            if 'id' in data:  # PUT does not allow this key
                del data['id']
            if 'path' in data:  # PUT does not allow this key
                del data['path']

            # api.mtr_update_metric_module_metadata(request, id, data)
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

    def get_data(self, request, id_):
        # response = api.mtr_get_metric_module_metadata(request, id_)
        response = None
        data = json.loads(response.text)
        filter = MetricModule(data['id'], data['name'], data['interface_version'], data['object_metadata'],
                              data['is_put'], data['is_get'], data['execution_server'])
        return filter


class FilterTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    interface_version = tables.Column('interface_version', verbose_name=_("Interface Version"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    object_metadata = tables.Column('object_metadata', verbose_name=_("Object Metadata"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    is_put = tables.Column('is_put', verbose_name=_("Is Put?"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]), update_action=UpdateCell)
    is_get = tables.Column('is_get', verbose_name=_("Is Get?"), form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]), update_action=UpdateCell)
    execution_server = tables.Column('execution_server', verbose_name=_("Execution Server"), form_field=forms.ChoiceField(choices=[('proxy', _('Proxy Server')), ('object', _('Object Storage Servers'))]), update_action=UpdateCell)

    class Meta:
        name = "metric_modules"
        verbose_name = _("Metric Modules")
        table_actions = (MyFilterAction, UploadMetricModule, DeleteMultipleMetricModules,)
        row_actions = (UpdateMetricModule, DeleteMetricModule,)
        row_class = UpdateRow
