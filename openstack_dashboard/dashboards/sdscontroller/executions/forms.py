from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard.api import zoeapi


class CreateExecutionForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Execution Name"))
    app_name = forms.ChoiceField(label=_('App Name'),
                                 choices=[
                                     ('ipython', _('iPython Notebook')),
                                     ('spark', _('Spark Cluster')),
                                     ('mpi', _('MPI'))],
                                 )

    def handle(self, request, data):
         try:
             zoeapi.new_execution(request, data['name'], data['app_name'])
             return True
         except Exception:
             exceptions.handle(request, _('Unable to create execution.'))

