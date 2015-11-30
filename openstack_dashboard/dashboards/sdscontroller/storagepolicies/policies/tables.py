from django.utils.translation import ugettext_lazy as _

from horizon import tables


class CreatePolicy(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Policy")
    url = "horizon:sdscontroller:storagepolicies:policies:create_policy"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("volume", "volume_extension:types_manage"),)


class PoliciesTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    policy = tables.Column('policy', verbose_name=_("Policy"))

    def get_object_display(self, policy):
        return policy.policy

    def get_object_id(self, policy):
        return policy.id

    class Meta:
        name = "policies"
        # hidden_title = False
        table_actions = (CreatePolicy,)
        verbose_name = _("Policies")
