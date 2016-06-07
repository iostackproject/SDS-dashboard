import requests
from horizon.utils.memoized import memoized  # noqa
import json
from zoe_lib.executions import ZoeExecutionsAPI
from zoe_lib.services import ZoeServiceAPI
from zoe_lib.query import ZoeQueryAPI
from applications.ibm_notebook import ibm_notebook
from zoe_lib.predefined_apps import spark_interactive
from zoe_lib.predefined_apps import wordcount_iostack
from zoe_lib.predefined_apps import openmpi_iostack

# TODO: Take parameters from a config file
URL_BASIC = "http://127.0.0.1:8777"

ZOE_CONF_FILE = "/root/Development/zoe/zoeconf.json"
with open(ZOE_CONF_FILE) as conf_file:
    cfg = json.load(conf_file)
    print("Zoe Configuration Loaded")

# Default values
ZOE_URL = cfg['ZOE_URL']
ZOE_USER = cfg['ZOE_USER']
ZOE_PWD = cfg['ZOE_PWD']

@memoized
def zoe_api(request):
    return request.user.token.id


def exec_list_cmd(request):
    token = zoe_api(request)
    headers = dict()
    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "text/plain"

    exec_api = ZoeExecutionsAPI(ZOE_URL, ZOE_USER, ZOE_PWD)
    data = exec_api.list()

    url = URL_BASIC + "/sdscontroller/executions"
    r = requests.get(url, headers=headers)
    return r, data


def terminate_exec(request, exec_id):
    print("TO TERMINATE: ", exec_id)
    exec_api = ZoeExecutionsAPI(ZOE_URL, ZOE_USER, ZOE_PWD)
    return exec_api.terminate(exec_id)


def get_user_info(exec_id):
    exec_api = ZoeExecutionsAPI(ZOE_URL, ZOE_USER, ZOE_PWD)
    query_api = ZoeQueryAPI(ZOE_URL, ZOE_USER, ZOE_PWD)

    data = exec_api.list()
    try:
        owner = [e['owner'] for e in data if e['id'] == exec_id][0]
        users = query_api.query('user')
        gateway = [u['gateway_urls'] for u in users if u['name'] == owner][0][0]
        print("zoe owner: {} - {}".format(owner, gateway))
    except Exception as e:
        print("exception: {}".format(e))
        owner = gateway = None
    return owner, gateway


def get_execution_details(exec_id):
    #print("zoeapi.py: exec_id = ", exec_id)
    exec_api = ZoeExecutionsAPI(ZOE_URL, ZOE_USER, ZOE_PWD)
    cont_api = ZoeServiceAPI(ZOE_URL, ZOE_USER, ZOE_PWD)
    owner, gateway = get_user_info(exec_id)
    exec_details = exec_api.execution_get(exec_id)
    service_details = []
    for c_id in exec_details['services']:
        c = cont_api.get(c_id)
        ip = list(c['ip_address'].values())[0]  # FIXME how to decide which network is the right one?
        cont_id = c['id']
        cont_name = c['name']
        tmp = {'name': cont_name, 'details': {}}
        for p in c['ports']:
            url = "{}://{}:{}{}".format(p['protocol'], ip, p['port_number'], p['path'])
            tmp['details'] = {'name': p['name'], 'url': url}
        service_details.append(tmp)
    exec_details.update({'service_details': service_details})
    return exec_details


def new_execution(request, exec_name, app_name):
    print("zoe api: new execution")
    exec_api = ZoeExecutionsAPI(ZOE_URL, ZOE_USER, ZOE_PWD)
    if app_name == 'ipython':
        print("Starting ipython notebook Zoe execution: ", exec_name)
        app_descr = ibm_notebook.create_app(name=exec_name)
    elif app_name == 'mpi':
        print("Starting MPI Zoe execution: ", exec_name)
        app_descr = openmpi_iostack.openmpi_hello_app(name="mpihello")
    else:
        print("App not supported.")
        return
    exec_api.execution_start(exec_name, app_descr)
    return "Done"
