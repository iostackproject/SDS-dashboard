import requests
from horizon.utils.memoized import memoized  # noqa
import json
from zoe_lib.executions import ZoeExecutionsAPI
from zoe_lib.services import ZoeServiceAPI
from zoe_lib.predefined_apps import spark_interactive
from zoe_lib.predefined_apps import wordcount_iostack
from zoe_lib.predefined_apps import openmpi_iostack

# TODO: Take parameters from a config file
URL_BASIC = "http://127.0.0.1:8777"

ZOE_CONF_FILE = "/root/Development/zoe/zoeconf.json"
with open(ZOE_CONF_FILE ) as conf_file:
    cfg = json.load(conf_file)
    print("Zoe Configuration Loaded")


@memoized
def zoe_api(request):
    return request.user.token.id


def exec_list_cmd(request):
    token = zoe_api(request)
    headers = dict()
    headers["X-Auth-Token"] = str(token)
    headers['Content-Type'] = "text/plain"

    exec_api = ZoeExecutionsAPI(cfg['ZOE_URL'], cfg['ZOE_USER'], cfg['ZOE_PWD'])
    data = exec_api.list()

    url = URL_BASIC + "/sdscontroller/executions"
    r = requests.get(url, headers=headers)
    return r, data


def terminate_exec(request, exec_id):
    print("TO TERMINATE: ", exec_id)
    exec_api = ZoeExecutionsAPI(cfg['ZOE_URL'], cfg['ZOE_USER'], cfg['ZOE_PWD'])
    return exec_api.terminate(exec_id)


def get_execution_details(exec_id):
    #print("zoeapi.py: exec_id = ", exec_id)
    exec_api = ZoeExecutionsAPI(cfg['ZOE_URL'], cfg['ZOE_USER'], cfg['ZOE_PWD'])
    cont_api = ZoeServiceAPI(cfg['ZOE_URL'], cfg['ZOE_USER'], cfg['ZOE_PWD'])
    exec_details = exec_api.execution_get(exec_id)
    for c_id in exec_details['services']:
        c = cont_api.get(c_id)
        ip = list(c['ip_address'].values())[0]  # FIXME how to decide which network is the right one?
        cont_id = c['id']
        cont_name = c['name']
        print("")
        print('Service {} (ID: {})'.format(cont_name, cont_id))
        for p in c['ports']:
            url = "{}://{}:{}{}".format(p['protocol'], ip, p['port_number'], p['path'])
            print(' - {}: {}'.format(p['name'], url))
    return exec_details

def new_execution(request, exec_name, app_name):
    print("zoe api: new execution")
    exec_api = ZoeExecutionsAPI(cfg['ZOE_URL'], cfg['ZOE_USER'], cfg['ZOE_PWD'])
    if app_name == 'ipython':
        print("Starting ipython notebook Zoe execution: ", exec_name)
        app_descr = spark_interactive.spark_jupyter_notebook_app()
    elif app_name == 'spark':
        print("Starting Spark Cluster Zoe execution: ", exec_name)
        app_descr = wordcount_iostack.iostack_wordcount_app()
    elif app_name == 'mpi':
        print("Starting MPI Zoe execution: ", exec_name)
        app_descr = openmpi_iostack.openmpi_hello_app(name="mpihello")
    else:
        print("App not supported.")
        return
    exec_api.execution_start(exec_name, app_descr)
    return "Done"
