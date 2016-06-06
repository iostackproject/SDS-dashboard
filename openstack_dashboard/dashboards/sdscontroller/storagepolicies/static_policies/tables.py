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
from models import Policy
from openstack_dashboard.api import sds_controller as api


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreatePolicy(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Policy")
    url = "horizon:sdscontroller:storagepolicies:static_policies:create_policy"
    classes = ("ajax-modal",)
    icon = "plus"


class DeletePolicy(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Policy",
            u"Delete Policies",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Policy",
            u"Deleted Policies",
            count
        )

    name = "delete_policy"
    success_url = "horizon:sdscontroller:storagepolicies:index"

    def delete(self, request, obj_id):
        try:
            response = api.dsl_delete_static_policy(request, obj_id)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully deleted policy/rule: %s') % obj_id)
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:storagepolicies:index")
            error_message = "Unable to remove policy.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdatePolicy(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, policy):
        base_url = reverse("horizon:sdscontroller:storagepolicies:static_policies:update_policy", kwargs={'policy_id': policy.id})
        return base_url


class DeleteMultiplePolicies(DeletePolicy):
    name = "delete_multiple_policies"


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, project, cell):
        return ((cell.column.name == 'object_type') or
                (cell.column.name == 'object_size') or
                (cell.column.name == 'execution_server') or
                (cell.column.name == 'execution_server_reverse') or
                (cell.column.name == 'execution_order') or
                (cell.column.name == 'params'))

    def update_cell(self, request, datum, policy_id, cell_name, new_cell_value):
        try:
            # updating changed value by new value
            response = api.dsl_get_static_policy(request, policy_id)
            data = json.loads(response.text)
            data[cell_name] = new_cell_value

            # TODO: Check only the valid keys, delete the rest
            if 'id' in data:  # PUT does not allow this key
                del data['id']
            if 'target' in data:  # PUT does not allow this key
                del data['target']
            if 'filter' in data:  # PUT does not allow this key
                del data['filter']

            api.dsl_update_static_policy(request, policy_id, data)
        except Conflict:
            # Returning a nice error message about name conflict. The message
            # from exception is not that clear for the user
            message = _("Can't change value")
            raise ValidationError(message)
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, policy_id):
        response = api.dsl_get_static_policy(request, policy_id)
        data = json.loads(response.text)
        policy = Policy(data['id'], data['target'], data['filter_id'],
                        data['object_type'], data['object_size'],
                        data['execution_server'], data['execution_server_reverse'],
                        data['execution_order'], data['params'])

        return policy


class PoliciesTable(tables.DataTable):
    target = tables.Column('target', verbose_name=_("Target"))
    filter = tables.Column('filter', verbose_name=_("Filter"))
    object_type = tables.Column('object_type', verbose_name="Object Type", form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    object_size = tables.Column('object_size', verbose_name=_("Object Size"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    execution_server = tables.Column('execution_server', verbose_name="Execution Server", form_field=forms.ChoiceField(choices=[('proxy', _('Proxy Server')), ('object', _('Object Storage Servers'))]), update_action=UpdateCell)
    execution_server_reverse = tables.Column('execution_server_reverse', verbose_name="Execution Server Reverse", form_field=forms.ChoiceField(choices=[('proxy', _('Proxy Server')), ('object', _('Object Storage Servers'))]), update_action=UpdateCell)
    execution_order = tables.Column('execution_order', verbose_name="Execution Order", form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    params = tables.Column('params', verbose_name="Params", form_field=forms.CharField(max_length=255), update_action=UpdateCell)

    class Meta:
        name = "static_policies"
        verbose_name = _("Policies")
        table_actions = (MyFilterAction, CreatePolicy, DeleteMultiplePolicies,)
        row_actions = (UpdatePolicy, DeletePolicy,)
        row_class = UpdateRow