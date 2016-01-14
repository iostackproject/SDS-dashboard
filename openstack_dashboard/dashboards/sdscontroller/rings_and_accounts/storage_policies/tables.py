from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from django.core.urlresolvers import reverse

from horizon import tables
from horizon import exceptions
from horizon import messages

from openstack_dashboard.dashboards.sdscontroller import api_sds_controller as api


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateStoragePolicy(tables.LinkAction):
    name = "create_storage_policy"
    verbose_name = _("Create new policy")
    url = "horizon:sdscontroller:rings_and_accounts:storage_policies:create_storage_policy"
    classes = ("ajax-modal",)
    icon = "upload"

class CreateECStoragePolicy(tables.LinkAction):
    name = "create_ec_storage_policy"
    verbose_name = _("Create EC Storage Policy")
    url = "horizon:sdscontroller:rings_and_accounts:storage_policies:create_ec_storage_policy"
    classes = ("ajax-modal",)
    icon = "new"

class StoragePolicyTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    language = tables.Column('language', verbose_name=_("Language"))
    interface_version = tables.Column('interface_version', verbose_name=_("Interface Version"))
    dependencies = tables.Column('dependencies', verbose_name=_("Dependencies"))
    object_metadata = tables.Column('object_metadata', verbose_name=_("Object Metadata"))
    main = tables.Column('main', verbose_name=_("Main"))

    class Meta:
        name = "storagepolicies"
        verbose_name = _("Storage Policies")
        table_actions = (MyFilterAction, CreateStoragePolicy, CreateECStoragePolicy, )
