from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from django.core.urlresolvers import reverse

from horizon import tables
from horizon import exceptions
from horizon import messages

from openstack_dashboard.api import sds_controller_blockstorage as api
import requests
import json


class CreateGroup(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Group")
    url = "horizon:sdscontroller:sds_storagegroups:groups:create_group"
    classes = ("ajax-modal",)
    icon = "plus"
    
#updatepolicy
class UpdateGroup(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit Storage Groups")
    url = "horizon:sdscontroller:sds_storagegroups:groups:update"
    classes = ("ajax-modal",)
    icon = "pencil"
    #policy_rules = (('sdscontroller', 'sdscontroller:update_project'),)    

class DeleteGroup(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Group",
            u"Delete Groups",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Group",
            u"Deleted Groups",
            count
        )

    name = "delete_group"
    success_url = "horizon:sdscontroller:sds_storagegroups:index"

    def delete(self, request, obj_id):
        try:
            resp = resp = api.delete_storagegroup(obj_id)
            if 200 <= resp.status_code < 300:
                messages.success(request, _('Successfully deleted group/rule: %s') % obj_id)
            else:
                raise ValueError(resp.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:sds_storagegroups:index")
            error_message = "Unable to remove group.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)

class DeleteMultipleGroups(DeleteGroup):
    name = "delete_multiple_groups"

def get_policy_name(group):
    storage_policy_name = ""
    policyid = str(group.policy)
    try:               
        resp = api.retrieve_policy(policyid)
        if 200 <= resp.status_code < 300:        
            data = resp.json()
            storage_policy_name = data.get('name')
        else:
            error_message = 'Unable to retrieve policies information.'
            raise ValueError(error_message)            
    except Exception as e:
        pass    
    return storage_policy_name

def get_storage_nodes(group):
    storage_nodes_name = []
    group_nodes = str(group.nodes)
    for node in group_nodes:
        try:
            resp = api.retrieve_controller(node) #requests.get(sds_api + "controllers/" + node, headers=headers)
            if 200 <= resp.status_code < 300:        
                data = resp.json()
                storage_nodes_name.append(data.get('hostname'))
            else:
                error_message = 'Unable to retrieve storage nodes information.'
                raise ValueError(error_message)            
        except Exception as e:
            pass
    return (", ".join(storage_nodes_name))

class GroupsTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("Id"))
    name = tables.Column('name', verbose_name="Name")
    policy = tables.Column(get_policy_name, verbose_name="Policy")
    nodes = tables.Column(get_storage_nodes, verbose_name="Storage Nodes")
    created_at = tables.Column('created_at', verbose_name=_("Created at"))

    class Meta:
        name = "groups"
        verbose_name = _("Groups")
        table_actions = (CreateGroup, DeleteMultipleGroups,)
        row_actions = (UpdateGroup, DeleteGroup,)