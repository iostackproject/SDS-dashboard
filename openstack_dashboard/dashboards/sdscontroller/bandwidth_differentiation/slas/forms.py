from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import common
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class CreateSLA(forms.SelfHandlingForm):
    project_choices = []
    project_id = forms.ChoiceField(choices=project_choices,
                                   label=_("Project"),
                                   help_text=_("The project where the rule will be applied."),
                                   required=True)

    policy_choices = []
    policy_id = forms.ChoiceField(choices=policy_choices,
                                  label=_("Storage Policy (Ring)"),
                                  help_text=_("The storage policy that you want to assign to the specific project."),
                                  required=True)

    bandwidth = forms.CharField(max_length=255,
                                label=_("Bandwidth"),
                                help_text=_("The bandwidth that you want to assign to the specific project."),
                                widget=forms.TextInput(
                                    attrs={"ng-model": "bandwidth", "not-blank": ""}
                                ))

    def __init__(self, request, *args, **kwargs):
        # Obtain list of projects
        self.project_choices = common.get_project_list_choices(request)
        # Obtain list of storage policies
        self.storage_policy_choices = common.get_storage_policy_list_choices(request, common.ListOptions.by_id())

        # Initialization
        super(CreateSLA, self).__init__(request, *args, **kwargs)

        # Overwrite target_id input form
        self.fields['project_id'] = forms.ChoiceField(choices=self.project_choices,
                                                      label=_("Project"),
                                                      help_text=_("The project where the rule will be apply."),
                                                      required=True)

        self.fields['policy_id'] = forms.ChoiceField(choices=self.storage_policy_choices,
                                                     label=_("Storage Policy (Ring)"),
                                                     help_text=_("The storage policy that you want to assign to the specific project."),
                                                     required=True)

    @staticmethod
    def handle(request, data):

        try:
            response = api.bw_add_sla(request, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Successfully SLA creation."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to create sla.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdateSLA(forms.SelfHandlingForm):
    bandwidth = forms.CharField(max_length=255,
                                label=_("Bandwidth"),
                                required=False,
                                help_text=_("The new bandwidth that you want to assign to the specific project."))

    def __init__(self, request, *args, **kwargs):
        super(UpdateSLA, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            sla_id = self.initial["id"]
            response = api.bw_update_sla(request, sla_id, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _("Successfully sla update."))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to update sla.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
