from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables
from openstack_dashboard.api import zoeapi
from horizon import exceptions


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateExecutionAction(tables.LinkAction):
    name = "execution"
    verbose_name = _("Create Execution")
    url = "horizon:sdscontroller:executions:create"
    classes = ("ajax-modal",)
    icon = "pencil"

    def allowed(self, request, instance=None):
        return True


class TerminateAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Terminate Execution",
            u"Terminate Executions",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Terminated Execution",
            u"Terminated Executions",
            count
        )

    icon = "camera"
    name = "terminate"
    verbose_name = _("Terminate Execution")
    url = "horizon:sdscontroller:executions:index"

    # This action should be disabled if the instance
    # is not active, or the instance is being deleted
    def allowed(self, request, execution_instance=None):
        exec_id = execution_instance.id
        execution = zoeapi.get_execution_details(exec_id)
        return execution['status'] == "running"

    def delete(self, request, obj_id):
        try:
            zoeapi.terminate_exec(request, obj_id)
            print("Zoe exec terminated")
        except exceptions.Conflict as exc:
            exceptions.handle(request, exc, redirect=self.success_url)
        except Exception:
            exceptions.handle(request,
                              _('Unable to terminate execution.'),
                              redirect=self.success_url)

    def get_success_url(self, request=None):
        """Returns the URL to redirect to after a successful action.
        """
        current_exec = self.table.kwargs.get("exec_name", None)

        # If the current_container is deleted, then redirect to the default
        # completion url
        if current_exec in self.success_ids:
            return self.success_url
        return request.get_full_path()


class ExecutionsTable(tables.DataTable):
    exec_name = tables.Column('exec_name', verbose_name=_("Execution Name"))
    app_name = tables.Column('app_name', verbose_name=_("Application Name"))
    submit_date = tables.Column('submit_date', verbose_name=_("Submitted"))
    sched_date = tables.Column('sched_date', verbose_name=_("Scheduled"))
    finish_date = tables.Column('fin_date', verbose_name=_("Terminated"))
    status = tables.Column('status', verbose_name=_("Status"))

    class Meta:
        name = "executions"
        verbose_name = _("Executions")
        table_actions = (CreateExecutionAction, MyFilterAction)
        row_actions = (TerminateAction,)



