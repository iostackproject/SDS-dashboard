from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from django.core.urlresolvers import reverse

from horizon import tables
from horizon import exceptions
from horizon import messages

from openstack_dashboard.api import sds_controller as api


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class CreateStoragePolicy(tables.LinkAction):
    name = "create_storage_policy"
    verbose_name = _("Create new policy")
    url = "horizon:sdscontroller:rings_and_accounts:storage_policies:create_storage_policy"
    classes = ("ajax-modal",)
    icon = "plus"

class CreateECStoragePolicy(tables.LinkAction):
    name = "create_ec_storage_policy"
    verbose_name = _("Create EC Storage Policy")
    url = "horizon:sdscontroller:rings_and_accounts:storage_policies:create_ec_storage_policy"
    classes = ("ajax-modal",)
    icon = "plus"

class BindStorageNode(tables.LinkAction):
    name = "bind_storage_node"
    verbose_name = _("Register Storage Node")
    url = "horizon:sdscontroller:rings_and_accounts:storage_policies:bind_storage_node"
    classes = ("ajax-modal",)
    icon = "plus"

class StoragePolicyTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    location = tables.Column('location', verbose_name=_("Location"))
    type = tables.Column('type', verbose_name=_("Type"))

    class Meta:
        name = "storagepolicies"
        verbose_name = _("Storage Policies")
        table_actions = (MyFilterAction, BindStorageNode, CreateStoragePolicy, CreateECStoragePolicy, )
