from django.utils.translation import ugettext_lazy as _

from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class InstancesTable(tables.DataTable):
    exec_name = tables.Column('exec_name', verbose_name=_("Execution Name"))
    app_name = tables.Column('app_name', verbose_name=_("Application Name"))
    submit_date = tables.Column('submit_date', verbose_name=_("Submitted"))
    sched_date = tables.Column('sched_date', verbose_name=_("Scheduled"))
    finish_date = tables.Column('fin_date', verbose_name=_("Terminated"))
    status = tables.Column('status', verbose_name=_("Status"))
    #zone = tables.Column('availability_zone', verbose_name=_("Availability Zone"))
    #image_name = tables.Column('image_name', verbose_name=_("Image Name"))

    class Meta:
        name = "instances"
        verbose_name = _("Instances")
        table_actions = (MyFilterAction,)
