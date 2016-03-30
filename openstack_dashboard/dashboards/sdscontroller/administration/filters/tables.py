import json

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from keystoneclient.exceptions import Conflict

from horizon import tables
from horizon import exceptions
from horizon import messages
from horizon import forms
from models import Filter
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


def get_programming_languages():
    programming_languages = [(u'', u'Select one')]
    programming_languages.extend([('java', 'Java')])
    return programming_languages


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
            response = api.fil_delete_filter(request, obj_id)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully deleted filter: %s') % obj_id)
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:administration:index")
            error_message = "Unable to remove filter.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)


class UpdateFilter(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    icon = "pencil"
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, filter):
        base_url = reverse("horizon:sdscontroller:administration:filters:update", kwargs={'filter_id': filter.id})
        return base_url


class DeleteMultipleFilters(DeleteFilter):
    name = "delete_multiple_filters"


class UpdateCell(tables.UpdateAction):
    def allowed(self, request, project, cell):
        return ((cell.column.name == 'name') or
                (cell.column.name == 'language') or
                (cell.column.name == 'interface_version') or
                (cell.column.name == 'dependencies') or
                (cell.column.name == 'execution_server_default') or
                (cell.column.name == 'execution_server_reverse') or
                (cell.column.name == 'object_metadata') or
                (cell.column.name == 'is_put') or
                (cell.column.name == 'is_get') or
                (cell.column.name == 'has_reverse') or
                (cell.column.name == 'main'))

    def update_cell(self, request, datum, id, cell_name, new_cell_value):
        try:
            # updating changed value by new value
            response = api.fil_get_filter_metadata(request, id)
            data = json.loads(response.text)
            data[cell_name] = new_cell_value

            if 'id' in data:  # PUT does not allow this key
                del data['id']
            if 'path' in data:  # PUT does not allow this key
                del data['path']

            api.fil_update_filter_metadata(request, id, data)
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
        response = api.fil_get_filter_metadata(request, id)
        data = json.loads(response.text)
        filter = Filter(data['id'], data['name'],
                        data['language'], data['dependencies'],
                        data['interface_version'], data['object_metadata'],
                        data['main'], data['is_put'], data['is_get'],
                        data['has_reverse'], data['execution_server'],
                        data['execution_server_reverse'])
        return filter


class FilterTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    language = tables.Column('language', verbose_name=_("Language"), form_field=forms.ChoiceField(choices=get_programming_languages()), update_action=UpdateCell)
    interface_version = tables.Column('interface_version', verbose_name=_("Interface Version"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    dependencies = tables.Column('dependencies', verbose_name=_("Dependencies"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    object_metadata = tables.Column('object_metadata', verbose_name=_("Object Metadata"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    main = tables.Column('main', verbose_name=_("Main"), form_field=forms.CharField(max_length=255), update_action=UpdateCell)
    is_put = tables.Column('is_put', verbose_name=_("Is Put?"), form_field=forms.ChoiceField(choices=[
        ('True', _('True')), ('False', _('False'))
    ]), update_action=UpdateCell)
    is_get = tables.Column('is_get', verbose_name=_("Is Get?"), form_field=forms.ChoiceField(choices=[
        ('True', _('True')), ('False', _('False'))
    ]), update_action=UpdateCell)
    has_reverse = tables.Column('has_reverse', verbose_name=_("Has Reverse?"), form_field=forms.ChoiceField(choices=[
        ('True', _('True')), ('False', _('False'))
    ]), update_action=UpdateCell)
    execution_server = tables.Column('execution_server', verbose_name=_("Execution Server Default"),
                                             form_field=forms.ChoiceField(choices=[
                                                 ('proxy', _('Proxy Server')), ('object', _('Object Storage Servers'))
                                             ]), update_action=UpdateCell)
    execution_server_reverse = tables.Column('execution_server_reverse', verbose_name=_("Execution Server Reverse"),
                                             form_field=forms.ChoiceField(choices=[
                                                 ('proxy', _('Proxy Server')),
                                                 ('object', _('Object Storage Servers'))
                                             ]), update_action=UpdateCell)

    class Meta:
        name = "filters"
        verbose_name = _("Filters")
        table_actions = (MyFilterAction, UploadFilter, DeleteMultipleFilters,)
        row_actions = (UpdateFilter, DeleteFilter,)
        row_class = UpdateRow
