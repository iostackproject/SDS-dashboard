from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables


class CreatePolicy(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Policy")
    url = "horizon:sdscontroller:storagepolicies:policies:create_policy"
    classes = ("ajax-modal",)
    icon = "plus"


# class DeletePolicies(tables.DeleteAction):
#     @staticmethod
#     def action_present(count):
#         return ungettext_lazy(
#             u"Delete Filter",
#             u"Delete Filters",
#             count
#         )
#
#     @staticmethod
#     def action_past(count):
#         return ungettext_lazy(
#             u"Deleted Filter",
#             u"Deleted Filters",
#             count
#         )
#
#     success_url = "horizon:sdscontroller:storagepolicies:index"
#
#     def delete(self, request, obj_id):
#         print "POLICIES DELETE ID", obj_id, "request", request
#         # try:
#         #     api.swift.swift_delete_container(request, obj_id)
#         # except exceptions.Conflict as exc:
#         #     exceptions.handle(request, exc, redirect=self.success_url)
#         # except Exception:
#         #     exceptions.handle(request,
#         #                       _('Unable to delete container.'),
#         #                       redirect=self.success_url)


class PoliciesTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("Id"))
    policy_description = tables.Column('policy_description', verbose_name="Policy Description")
    policy_location = tables.Column('policy_location', verbose_name=_("Policy Location"))
    alive = tables.Column('alive', verbose_name="Alive")

    class Meta:
        name = "policies"
        verbose_name = _("Policies")
        table_actions = (CreatePolicy,)
        # row_actions = (DeletePolicies,)

