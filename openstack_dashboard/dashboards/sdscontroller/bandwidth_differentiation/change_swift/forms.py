import paramiko

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

current_version = 'original'
proxy = 'proxy'

class SelectSwiftVersion(forms.SelfHandlingForm):

    swift_version = forms.ChoiceField(
        label=_('Swift version'),
        choices=[
            ('original', _('Original Swift')),
            ('ioprio', _('IOPrio Swift'))
        ],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'swift_version'
        })
    )

    def __init__(self, request, *args, **kwargs):
        super(SelectSwiftVersion, self).__init__(request, *args, **kwargs)
        self.initial['swift_version'] = get_current_version()

    @staticmethod
    def handle(request, data):
        swift_version = data['swift_version']
        del data['swift_version']

        try:
            change_version(swift_version)

            messages.success(request, _('Swift version successfully changed.'))
            return True

        except Exception as ex:
            redirect = reverse("horizon:sdscontroller:bandwidth_differentiation:index")
            error_message = "Unable to change swift version.\t %s" % ex.message
            exceptions.handle(request, _(error_message), redirect=redirect)

def change_version(swift_version):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(proxy)

    if swift_version == "ioprio":
        stdin, stdout, stderr = ssh.exec_command("cd switch_swift_env; ansible-playbook -s -i swift_dynamic_inventory.py bsc-env.yml")
    elif swift_version == "original":
        stdin, stdout, stderr = ssh.exec_command("cd switch_swift_env; ansible-playbook -s -i swift_dynamic_inventory.py ibm-env.yml")

    response = stdout.readlines()
    print response
    set_current_version(swift_version)

def set_current_version(swift_version):
    global current_version
    current_version = swift_version

def get_current_version():
    return current_version
