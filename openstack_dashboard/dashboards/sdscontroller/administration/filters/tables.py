from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from django.core.urlresolvers import reverse

from horizon import tables
from horizon import exceptions
from horizon import messages

from openstack_dashboard.dashboards.sdscontroller import api_sds_controller as api


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class UploadFilter(tables.LinkAction):
    name = "upload"
    verbose_name = _("Upload Filter")
    url = "horizon:sdscontroller:administration:filters:upload"
    classes = ("ajax-modal",)
    icon = "upload"


class DeleteFilter(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Filter",
            u"Delete Filters",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Filter",
            u"Deleted Filters",
            count
        )

    name = "delete_filter"
    success_url = "horizon:sdscontroller:administration:index"

    def delete(self, request, obj_id):
        try:
            response = api.fil_delete_filter(obj_id)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully deleted filter: %s') % obj_id)
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to remove filter.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class DeleteMultipleFilters(DeleteFilter):
    name = "delete_multiple_filters"


class FilterTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    language = tables.Column('language', verbose_name=_("Language"))
    interface_version = tables.Column('interface_version', verbose_name=_("Interface Version"))
    dependencies = tables.Column('dependencies', verbose_name=_("Dependencies"))
    object_metadata = tables.Column('object_metadata', verbose_name=_("Object Metadata"))
    main = tables.Column('main', verbose_name=_("Main"))

    class Meta:
        name = "filters"
        verbose_name = _("Filters")
        table_actions = (MyFilterAction, UploadFilter, DeleteMultipleFilters,)
