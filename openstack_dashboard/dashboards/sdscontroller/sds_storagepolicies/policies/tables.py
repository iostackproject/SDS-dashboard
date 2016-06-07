from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from django.core.urlresolvers import reverse

from horizon import tables
from horizon import exceptions
from horizon import messages

from openstack_dashboard.api import sds_controller_blockstorage as api

import json


class CreatePolicy(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Policy")
    url = "horizon:sdscontroller:sds_storagepolicies:policies:create_policy"
    classes = ("ajax-modal",)
    icon = "plus"

#updatepolicy
class UpdatePolicy(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit Policy")
    url = "horizon:sdscontroller:sds_storagepolicies:policies:update"
    classes = ("ajax-modal",)
    icon = "pencil"
    #policy_rules = (('sdscontroller', 'sdscontroller:update_project'),)

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
    success_url = "horizon:sdscontroller:sds_storagepolicies:index"

    def delete(self, request, obj_id):
        try:
            resp = api.delete_policy(obj_id)
            if 200 <= resp.status_code < 300:
                messages.success(request, _('Successfully deleted policy/rule: %s') % obj_id)
            else:
                raise ValueError(resp.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:sds_storagepolicies:index")
            error_message = "Unable to remove policy.\t %s" % ex.message
            exceptions.handle(request,
                              _(error_message),
                              redirect=redirect)

class DeleteMultiplePolicies(DeletePolicy):
    name = "delete_multiple_policies"

def get_filters_name(policy):
    filters_name = []
    policyid = str(policy.id)
    try:
        resp = api.retrieve_policy(policyid)
        if 200 <= resp.status_code < 300:        
            data = resp.json()
            filters_name = data.get('filters')
        else:
            error_message = 'Unable to retrieve storage nodes information.'
            raise ValueError(error_message)            
    except Exception as e:
        pass
    return (", ".join(filters_name))

class PoliciesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("Id"))
    name = tables.Column('name', verbose_name="Name")
    san_name = tables.Column('san_name', verbose_name="San name")
    throttle_iops_read = tables.Column('throttle_iops_read', verbose_name="IO/s read")
    throttle_iops_write = tables.Column('throttle_iops_write', verbose_name="IO/s write") 
    throttle_mbps_read = tables.Column('throttle_mbps_read', verbose_name="MB/s read")
    throttle_mbps_write = tables.Column('throttle_mbps_write', verbose_name="MB/s write")
    tier = tables.Column('tier', verbose_name="Tier")
    filters = tables.Column(get_filters_name, verbose_name="Filters")
    created_at = tables.Column('created_at', verbose_name=_("Created at"))

    class Meta:
        name = "policies"
        verbose_name = _("Policies")
        table_actions = (CreatePolicy, DeleteMultiplePolicies,)
        row_actions = (UpdatePolicy, DeletePolicy,)
        #updatepolicy