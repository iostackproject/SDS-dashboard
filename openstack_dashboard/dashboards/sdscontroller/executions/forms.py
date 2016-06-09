from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard.api import zoeapi


class CreateExecutionForm(forms.SelfHandlingForm):
    app_name = forms.ChoiceField(label=_('App Name'),
                                 choices=[
                                     ('ipython', _('iPython Notebook')),
                                     ('mpi', _('MPI'))],
                                 widget=forms.Select(attrs={
                                        'class': 'switchable',
                                        'data-slug': 'app_name'
                                    })
                                 )

    name = forms.CharField(max_length=255, label=_("Execution Name"))
    worker_count = forms.IntegerField(label=_('Worker count'),
                              widget=forms.TextInput(attrs={
                                'class': 'switched',
                                'data-switch-on': 'app_name',
                                'data-app_name-ipython': _('Worker count')
                                }), required=False)

    worker_memory = forms.IntegerField(label=_('Worker memory limit'),
                              widget=forms.TextInput(attrs={
                                'class': 'switched',
                                'data-switch-on': 'app_name',
                                'data-app_name-ipython': _('Worker memory limit')
                                }), required=False)

    worker_cores = forms.IntegerField(label=_('Worker cores'),
                              widget=forms.TextInput(attrs={
                                'class': 'switched',
                                'data-switch-on': 'app_name',
                                'data-app_name-ipython': _('Worker cores')
                                }), required=False)

    master_mem_limit = forms.IntegerField(label=_('Master memory limit'),
                              widget=forms.TextInput(attrs={
                                'class': 'switched',
                                'data-switch-on': 'app_name',
                                'data-app_name-ipython': _('Master memory limit')
                                }), required=False)

    notebook_mem_limit = forms.IntegerField(label=_("Notebook memory limit"),
                              widget=forms.TextInput(attrs={
                                'class': 'switched',
                                'data-switch-on': 'app_name',
                                'data-app_name-ipython': _('Notebook memory limit')
                                }), required=False)

    # mpicmdline = forms.CharField(max_length=255,
    #                              initial='mpirun -np 4 --hostfile ./mpi-helloworld/mpihosts ./mpi-helloworld/MPI_Hello',
    #                              label=_("MPI"),
    #                           widget=forms.TextInput(attrs={
    #                             'class': 'switched',
    #                             'data-switch-on': 'app_name',
    #                             'data-app_name-mpi': _('MPI Cmdline')
    #                             }), required=False)

    def handle(self, request, data):
        print("executions form: handle")
        try:
            zoeapi.new_execution(request, data['name'], data['app_name'])
            return True
        except Exception as e:
            print("zoe exception: {}".format(e))
            exceptions.handle(request, _('Unable to create execution.'))

# class CreateExecutionForm(forms.SelfHandlingForm):
#     name = forms.CharField(max_length=255, label=_("Execution Name"))
#     app_name = forms.ChoiceField(label=_('App Name'),
#                                  choices=[
#                                      ('ipython', _('iPython Notebook')),
#                                      ('spark', _('Spark Cluster')),
#                                      ('mpi', _('MPI'))],
#                                  )
#     num_workers = forms.IntegerField(label=_("Number of workers"))
#     max_memory = forms.IntegerField(label=_("Max requested memory (MB)"))
#
#     def handle(self, request, data):
#         assert data['name'] and data['app_name']
#         if data['max_memory']:
#             max_memory = data['max_memory'] * 1024
#         try:
#             zoeapi.new_execution(request, data['name'], data['app_name'])
#             return True
#         except Exception:
#             exceptions.handle(request, _('Unable to create execution.'))

