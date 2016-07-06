from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard.api import zoeapi


class CreateExecutionForm(forms.SelfHandlingForm):
    app_name = forms.ChoiceField(label=_('App Name'),
                                 choices=[
                                     ('ipython', _('iPython Notebook')),
                                     ('mpi', _('openmpi-dyna'))],
                                 widget=forms.Select(attrs={
                                        'class': 'switchable',
                                        'data-slug': 'app_name'
                                    })
                                 )

    name = forms.CharField(max_length=255, label=_("Execution Name"))

    worker_count = forms.IntegerField(label=_('Worker count'),
                                      initial=2,
                                      required=False)

    worker_cores = forms.IntegerField(label=_('Worker cores'),
                                      initial=6,
                                      required=False)

    worker_memory = forms.IntegerField(label=_('Worker memory limit (GB)'),
                                       initial=12,
                                       required=False)

    master_mem_limit = forms.IntegerField(label=_('Master memory limit (MB)'),
                                          initial=512,
                                          widget=forms.TextInput(attrs={
                                              'class': 'switched',
                                              'data-switch-on': 'app_name',
                                              'data-app_name-ipython': _('Master memory limit')
                                          }), required=False)

    notebook_mem_limit = forms.IntegerField(label=_("Notebook memory limit (GB)"),
                                            initial=4,
                                            widget=forms.TextInput(attrs={
                                                'class': 'switched',
                                                'data-switch-on': 'app_name',
                                                'data-app_name-ipython': _('Notebook memory limit')
                                            }), required=False)

    def handle(self, request, data):
        print("handle {}".format(data))
        to_pass = {}
        try:
            for k in data.items():
                to_pass[k] = data[k]
            print("handle to_pass: {}".format(to_pass))
            zoeapi.new_execution(request, data['name'], data['app_name'], to_pass)
            return True
        except Exception as e:
            print("zoe exception: {}".format(e))
            exceptions.handle(request, _('Unable to create execution.'))
