from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables
from openstack_dashboard.api import zoeapi


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


def is_terminating(execution):
    exec_state = getattr(execution, "status", None)
    if not exec_state:
        return False
    return exec_state.lower() == "terminating"


class TerminateAction(tables.LinkAction):
    icon = "camera"
    name = "terminate"
    verbose_name = _("Terminate Execution")
    url = "horizon:sdscontroller:executions:terminate"
    classes = ("ajax-modal",)

    # This action should be disabled if the instance
    # is not active, or the instance is being deleted
    def allowed(self, request, execution=None):
        return execution.status in ("running",) \
            and not is_terminating(execution)


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
        table_actions = (MyFilterAction,)
        row_actions = (TerminateAction,)



