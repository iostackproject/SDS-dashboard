import requests
from horizon.utils.memoized import memoized  # noqa
import json
from zoe_lib.executions import ZoeExecutionsAPI
from zoe_lib.services import ZoeServiceAPI
from zoe_lib.query import ZoeQueryAPI
from zoe_lib.users import ZoeUserAPI

import openstack_dashboard.api.zoeapps as zapps


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

vault = {}

def exec_list_cmd(request):
    print("zoe api: exec_list_cmd")
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
    print("zoe api: terminate_exec")
    print("TO TERMINATE: ", exec_id)
    exec_api = ZoeExecutionsAPI(ZOE_URL, ZOE_USER, ZOE_PWD)
    return exec_api.terminate(exec_id)


def get_user_info(exec_details):
    print("zoe api: get_user_info")
    user_api = ZoeUserAPI(ZOE_URL, ZOE_USER, ZOE_PWD)
    owner = user_api.get(exec_details['owner'])
    name = owner['owner']
    gateway = owner['gateway_urls'][0]
    return name, gateway


def get_execution_details(exec_id):
    print("zoe api: get_execution_details")
    try:
        print("zoe api: get_execution_details: found in vault with id = {}".format(exec_id))
        return vault[exec_id]
    except KeyError:
        print("zoe api: get_execution_details: no execution found with id = {}".format(exec_id))
        vault[exec_id] = {}
        exec_api = ZoeExecutionsAPI(ZOE_URL, ZOE_USER, ZOE_PWD)
        cont_api = ZoeServiceAPI(ZOE_URL, ZOE_USER, ZOE_PWD)
        exec_details = exec_api.execution_get(exec_id)
        owner, gateway = get_user_info(exec_details)
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
        exec_details.update({'service_details': service_details, 'owner': owner, 'gateway': gateway})
        vault[exec_id].update(exec_details)
        return vault[exec_id]


def new_execution(request, exec_name, app_name, **kwargs):
    print("zoe api: new execution")
    print("zoe api: new execution {} - {}: arguments {}".format(exec_name, app_name, kwargs))
    exec_api = ZoeExecutionsAPI(ZOE_URL, ZOE_USER, ZOE_PWD)
    if app_name == 'ipython':
        try:
            notebook_memory_limit = kwargs['notebook_mem_limit'] * (1024 ** 3)      # GB
            spark_master_memory_limit = kwargs['master_mem_limit'] * (1024 ** 2)    # MB
            spark_worker_memory_limit = kwargs['worker_memory'] * (1024 ** 3)       # GB
            spark_worker_cores = kwargs['worker_cores']
            spark_worker_count = kwargs['worker_count']
            app_descr = zapps.create_notebook_app(notebook_memory_limit=notebook_memory_limit,
                                                  spark_master_memory_limit=spark_master_memory_limit,
                                                  spark_worker_memory_limit=spark_worker_memory_limit,
                                                  spark_worker_cores=spark_worker_cores,
                                                  spark_worker_count=spark_worker_count
                                                  )
        except:
            app_descr = zapps.create_notebook_app()
        exec_api.execution_start(exec_name, app_descr)
    elif app_name == 'mpi':
        try:
            in_wm = int(kwargs['worker_memory'])
            assert in_wm > 0
            wm = in_wm * (1024 ** 3)
            app_descr = zapps.create_idiada_app(worker_memory=wm)
        except:
            app_descr = zapps.create_idiada_app()
        exec_api.execution_start('mpidynademo', app_descr)
    else:
        print("App not supported.")
        return

    return "Done"
