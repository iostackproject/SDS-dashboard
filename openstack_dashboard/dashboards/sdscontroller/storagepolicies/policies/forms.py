from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from openstack_dashboard.api import sds_controller as api
from openstack_dashboard.dashboards.sdscontroller import common
from openstack_dashboard.dashboards.sdscontroller import exceptions as sdsexception


class CreateDSLPolicy(forms.SelfHandlingForm):
    policy = forms.CharField(max_length=255,
                             label=_("Policy/Rule"),
                             widget=forms.Textarea(
                                 attrs={"ng-model": "interface_version", "not-blank": ""}
                             ))

    def __init__(self, request, *args, **kwargs):
        super(CreateDSLPolicy, self).__init__(request, *args, **kwargs)

    @staticmethod
    def handle(request, data):

        try:
            response = api.dsl_add_policy(request, data['policy'])
            if 200 <= response.status_code < 300:
                messages.success(request, _('Successfully created policy/rule: %s') % data['policy'])
                return data
            else:
                raise ValueError(response.text)
        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:storagepolicies:index")
            error_message = "Unable to create policy/rule.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)


class CreateSimplePolicy(forms.SelfHandlingForm):
    target_choices = []
    target_id = forms.ChoiceField(choices=target_choices,
                                  label=_("Project"),
                                  help_text=_("The project where the rule will be apply."),
                                  required=True)

    container_choices = [('', 'None')]
    container_id = forms.CharField(label=_("Container"),
                                   help_text=_("The container where the rule will be apply."),
                                   required=False,
                                   widget=forms.Select(choices=container_choices))

    filter_dsl_choices = []
    filter_id = forms.ChoiceField(choices=filter_dsl_choices,
                                  label=_("Filter"),
                                  help_text=_("The id of the filter which will be used."),
                                  required=True)

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
        # Obtain list of projects
        self.target_choices = common.get_project_list_choices(request)
        # Obtain list of dsl filters
        self.dsl_filter_choices = common.get_dsl_filter_list_choices(request)
        # Obtain list of object types
        self.object_type_choices = common.get_object_type_choices(request)

        # Initialization
        super(CreateSimplePolicy, self).__init__(request, *args, **kwargs)

        # Overwrite target_id input form
        self.fields['target_id'] = forms.ChoiceField(choices=self.target_choices,
                                                     label=_("Project"),
                                                     help_text=_("The project where the rule will be apply."),
                                                     required=True)
        # Overwrite filter_id input form
        self.fields['filter_id'] = forms.ChoiceField(choices=self.dsl_filter_choices,
                                                     label=_("Filter"),
                                                     help_text=_("The id of the filter which will be used."),
                                                     required=True)
        # Overwrite object_type input form
        self.fields['object_type'] = forms.ChoiceField(choices=self.object_type_choices,
                                                       label=_("Object Type"),
                                                       help_text=_("The type of object the rule will be applied to."),
                                                       required=False)

    @staticmethod
    def handle(request, data):
        try:
            if data['container_id'] != '':
                response = api.fil_deploy_filter_with_container(request, data['filter_id'], data['target_id'], data['container_id'], data)
            else:
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
        self.object_type_choices = common.get_object_type_choices(request)
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
