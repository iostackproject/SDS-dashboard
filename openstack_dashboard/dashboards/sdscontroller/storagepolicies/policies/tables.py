from django.utils.translation import ugettext_lazy as _

from horizon import tables


class CreatePolicy(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Policy")
    url = "horizon:sdscontroller:storagepolicies:policies:create_policy"
    classes = ("ajax-modal",)
    icon = "plus"


class PoliciesTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("Id"))
    policy_description = tables.Column('policy_description', verbose_name="Policy Description")
    policy_location = tables.Column('policy_location', verbose_name=_("Policy Location"))
    alive = tables.Column('alive', verbose_name="Alive")

    class Meta:
        name = "policies"
        # hidden_title = False
        table_actions = (CreatePolicy,)
        verbose_name = _("Policies")
