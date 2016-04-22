from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from keystoneclient.exceptions import Conflict

from horizon import exceptions
from horizon import forms
from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateSLA(tables.LinkAction):
    name = "create"
    verbose_name = _("Create SLA")
    url = "horizon:sdscontroller:bandwidth_differentiation:slas:upload"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateSLA(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, sla):
        base_url = reverse("horizon:sdscontroller:bandwidth_differentiation:slas:update", kwargs={'sla_id': sla.id})
        return base_url


# TODO: Check this, we need to add an API call.
class UpdateCell(tables.UpdateAction):
    def allowed(self, request, project, cell):
        return (cell.column.name == 'bandwidth')

    def update_cell(self, request, datum, id, cell_name, new_cell_value):
        try:
            print("DEBUG: Update SLA metadata")
            # updating changed value by new value
            # response = api.bw_get_sla_metadata(request, id)
            # data = json.loads(response.text)
            # data[cell_name] = new_cell_value
            #
            # # TODO: Check only the valid keys, delete the rest
            # if 'id' in data:  # PUT does not allow this key
            #     del data['id']
            # if 'path' in data:  # PUT does not allow this key
            #     del data['path']
            #
            # api.bw_update_sla_metadata(request, id, data['bandwidth'])
        except Conflict:
            # Returning a nice error message about name conflict. The message
            # from exception is not that clear for the user
            message = _("Cant change value")
            raise ValidationError(message)
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True


# TODO: Check this, we need to add an API call.
class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, id):
        print(request)
        # response = api.bw_get_sla_metadata(request, id)
        # data = json.loads(response.text)

        # sla = SLA(data['id'], data['tenant'], data['bandwidth'])
        # return sla


# TODO: Check this, we need to add an API call.
class DeleteSLA(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete SLA",
            u"Delete SLAs",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted SLA",
            u"Deleted SLAs",
            count
        )

    name = "delete_sla"
    success_url = "horizon:sdscontroller:bandwidth_differentiation:index"

    def delete(self, request, obj_id):
        try:
            print(request)
            # response = api.bw_delete_sla(request, obj_id)
            # if 200 <= response.status_code < 300:
            #     messages.success(request, _('Successfully deleted sla: %s') % obj_id)
            # else:
            #     raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to remove sla.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleSLAs(DeleteSLA):
    name = "delete_multiple_slas"


class SLAsTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    tenant = tables.Column('tenant', verbose_name=_("Tenant"))
    bandwidth = tables.Column('bandwidth', verbose_name=_("Bandwidth"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)

    class Meta:
        name = "slas"
        verbose_name = _("SLAs")
        table_actions = (MyFilterAction, CreateSLA, DeleteMultipleSLAs,)
        row_actions = (UpdateSLA, DeleteSLA,)
        row_class = UpdateRow
