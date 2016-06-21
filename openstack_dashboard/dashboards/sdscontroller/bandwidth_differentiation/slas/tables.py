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
from models import SLA
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateSLA(tables.LinkAction):
    name = "create"
    verbose_name = _("Create SLA")
    url = "horizon:sdscontroller:bandwidth_differentiation:slas:create_sla"
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateSLA(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, datum=None):
        base_url = reverse("horizon:sdscontroller:bandwidth_differentiation:slas:update_sla", kwargs={"sla_id": datum.id})
        return base_url


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, project, cell):
        return cell.column.name == "bandwidth"

    def update_cell(self, request, datum, id, cell_name, new_cell_value):
        try:
            # updating changed value by new value
            response = api.bw_get_sla(request, id)
            data = json.loads(response.text)
            data[cell_name] = new_cell_value
            api.bw_update_sla(request, id, data)
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
        response = api.bw_get_sla(request, id)
        data = json.loads(response.text)

        sla = SLA(data["tenant_id"], data["tenant_name"], data["policy_id"], data["policy_name"], data["bandwidth"])
        return sla


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
            response = api.bw_delete_sla(request, obj_id)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Successfully deleted sla: %s") % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to remove sla.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class DeleteMultipleSLAs(DeleteSLA):
    name = "delete_multiple_slas"


class SLAsTable(tables.DataTable):
    tenant_id = tables.Column("tenant_id", verbose_name=_("Tenant ID"))
    tenant_name = tables.Column("tenant_name", verbose_name=_("Tenant Name"))
    policy_name = tables.Column("policy_name", verbose_name=_("Policy"))
    bandwidth = tables.Column("bandwidth", verbose_name=_("Bandwidth"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)

    class Meta:
        name = "slas"
        verbose_name = _("SLAs")
        table_actions = (MyFilterAction, CreateSLA, DeleteMultipleSLAs,)
        row_actions = (UpdateSLA, DeleteSLA,)
        row_class = UpdateRow
