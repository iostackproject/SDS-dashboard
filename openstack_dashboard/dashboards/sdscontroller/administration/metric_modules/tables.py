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


class DownloadMetricModule(tables.LinkAction):
    name = "download"
    verbose_name = _("Download")
    icon = "download"

    def get_link_url(self, datum=None):
        base_url = reverse('horizon:sdscontroller:administration:metric_modules:download_metric_module', kwargs={'metric_module_id': datum.id})
        return base_url


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
            response = api.mtr_delete_metric_module(request, obj_id)
            if 200 <= response.status_code < 300:
                pass
                # messages.success(request, _('Successfully deleted metric module: %s') % obj_id)
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
        return ((cell.column.name == 'class_name') or
                (cell.column.name == 'out_flow') or
                (cell.column.name == 'in_flow') or
                (cell.column.name == 'execution_server') or
                (cell.column.name == 'enabled'))

    def update_cell(self, request, datum, metric_module_id, cell_name, new_cell_value):
        try:
            # updating changed value by new value
            response = api.mtr_get_metric_module(request, metric_module_id)
            data = json.loads(response.text)
            data[cell_name] = new_cell_value

            # TODO: Check only the valid keys, delete the rest
            if 'id' in data:  # PUT does not allow this key
                del data['id']
            if 'path' in data:  # PUT does not allow this key
                del data['path']

            api.mtr_update_metric_module(request, metric_module_id, data)
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

    def get_data(self, request, metric_module_id):
        response = api.mtr_get_metric_module(request, metric_module_id)
        data = json.loads(response.text)
        filter = MetricModule(data['id'], data['metric_name'], data['class_name'], data['out_flow'],
                              data['in_flow'], data['execution_server'], data['enabled'])
        return filter


class MetricTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    metric_name = tables.Column('metric_name', verbose_name=_("Metric Name"))
    class_name = tables.Column('class_name', verbose_name=_("Class Name"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    out_flow = tables.Column('out_flow', verbose_name=_("Out Flow"),
                             form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]), update_action=UpdateCell)
    in_flow = tables.Column('in_flow', verbose_name=_("In Flow"),
                            form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]), update_action=UpdateCell)
    execution_server = tables.Column('execution_server', verbose_name=_("Execution Server"),
                                     form_field=forms.ChoiceField(choices=[('proxy', _('Proxy Server')), ('object', _('Object Storage Servers'))]),
                                     update_action=UpdateCell)
    enabled = tables.Column('enabled',
                            verbose_name=_("Enabled"),
                            status=True,
                            form_field=forms.ChoiceField(choices=[('True', _('True')), ('False', _('False'))]),
                            update_action=UpdateCell)


    class Meta:
        name = "metric_modules"
        verbose_name = _("Metric Modules")
        table_actions = (MyFilterAction, UploadMetricModule, DeleteMultipleMetricModules,)
        row_actions = (UpdateMetricModule, DownloadMetricModule, DeleteMetricModule,)
        row_class = UpdateRow
