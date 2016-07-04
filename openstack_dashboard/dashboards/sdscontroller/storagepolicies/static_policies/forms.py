import json

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


def get_object_type_choices(request):
    try:
        response = api.dsl_get_all_object_types(request)
        if 200 <= response.status_code < 300:
            strobj = response.text
        else:
            error_message = 'Unable to get object types.'
            raise ValueError(error_message)
    except Exception as e:
        strobj = "[]"
        exceptions.handle(request, _(e.message))
    instances = json.loads(strobj)
    choices = []
    for inst in instances:
        choices.append((inst['name'], inst['name']))
    object_type_choices = (('', 'None'), ('Object types', choices))
    return object_type_choices


class CreatePolicyDSL(forms.SelfHandlingForm):
    policy = forms.CharField(max_length=255,
                             label=_("Policy/Rule"),
                             widget=forms.Textarea(
                                 attrs={"ng-model": "interface_version", "not-blank": ""}
                             ))

    def __init__(self, request, *args, **kwargs):
        super(CreatePolicyDSL, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        try:
            response = api.dsl_add_static_policy_dsl(request, data['policy'])
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created policy/rule: %s') % data['policy'])
                return data
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:storagepolicies:index")
            error_message = "Unable to create policy/rule.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class CreatePolicy(forms.SelfHandlingForm):
    target_id = forms.CharField(max_length=255,
                                label=_("Target ID"),
                                required=True,
                                help_text=_("The target where the rule will be apply."))

    filter_id = forms.CharField(max_length=255,
                                label=_("Filter ID"),
                                required=True,
                                help_text=_("The id of the filter which will be used."))

    # Empty definition
    object_type_choices = []
    object_type = forms.ChoiceField(choices=object_type_choices,
                                    label=_("Object Type"),
                                    help_text=_("The type of object the rule will be applied to."),
                                    required=False)

    object_size = forms.CharField(max_length=255,
                                  label=_("Object Size"),
                                  required=False,
                                  help_text=_("The size of object which the rule will be apply."))

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[
            ('proxy', _('Proxy Server')),
            ('object', _('Object Storage Servers'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    execution_server_reverse = forms.ChoiceField(
        label=_('Execution Server Reverse'),
        choices=[
            ('proxy', _('Proxy Server')),
            ('object', _('Object Storage Servers'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    params = forms.CharField(max_length=255,
                             label=_("Parameters"),
                             required=False,
                             help_text=_("Parameters list."))

    def __init__(self, request, *args, **kwargs):
        super(CreatePolicy, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        try:
            response = api.fil_deploy_filter(request, data['filter_id'], data['target_id'], data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created simple policy/rule!'))
                return data
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:storagepolicies:index")
            error_message = "Unable to create policy/rule.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class UpdatePolicy(forms.SelfHandlingForm):
    # object_type = forms.CharField(max_length=255,
    #                               label=_("Object Type"),
    #                               required=False,
    #                               help_text=_("The type of object the rule will be applied to."))

    # Empty definition
    object_type_choices = []
    object_type = forms.ChoiceField(choices=object_type_choices,
                                    label=_("Object Type"),
                                    help_text=_("The type of object the rule will be applied to."),
                                    required=False)

    object_size = forms.CharField(max_length=255,
                                  label=_("Object Size"),
                                  required=False,
                                  help_text=_("The size of object which the rule will be apply."))

    execution_server = forms.ChoiceField(
        label=_('Execution Server'),
        choices=[
            ('proxy', _('Proxy Server')),
            ('object', _('Object Storage Servers'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    execution_server_reverse = forms.ChoiceField(
        label=_('Execution Server Reverse'),
        choices=[
            ('proxy', _('Proxy Server')),
            ('object', _('Object Storage Servers'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'
        })
    )

    execution_order = forms.CharField(max_length=255,
                                      label=_("Execution Order"),
                                      help_text=_("The order in which the policy will be executed."))

    params = forms.CharField(max_length=255,
                             label=_("Parameters"),
                             required=False,
                             help_text=_("Parameters list."))

    def __init__(self, request, *args, **kwargs):
        # Obtain list of object types
        self.object_type_choices = get_object_type_choices(request)
        # initialization
        super(UpdatePolicy, self).__init__(request, *args, **kwargs)
        # overwrite object_type input form
        self.fields['object_type'] = forms.ChoiceField(choices=self.object_type_choices,
                                                       label=_("Object Type"),
                                                       help_text=_("The type of object the rule will be applied to."),
                                                       required=False)

    failure_url = 'horizon:sdscontroller:storagepolicies:index'

    def handle(self, request, data):
        try:
            policy_id = self.initial['target_id'] + ':' + self.initial['id']
            response = api.dsl_update_static_policy(request, policy_id, data)
            if 200 <= response.status_code < 300:
                messages.success(request, _('Policy successfully updated.'))
                return data
            else:
                raise sdsexception.SdsException(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:storagepolicies:index")
            error_message = "Unable to update policy.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)
