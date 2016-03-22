import requests
from horizon.utils.memoized import memoized  # noqa
import json
from zoe_lib.executions import ZoeExecutionsAPI
from zoe_lib.predefined_frameworks import jupyter_spark, spark, openmpi

# TODO: Take parameters from a config file
URL_BASIC = "http://127.0.0.1:8000"

ZOE_CONF_FILE = "/home/swift/github/zoeconf.json"
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
    exec_details = exec_api.execution_get(exec_id)
    return exec_details

def new_execution(request, exec_name, app_name):
    print("zoe api: new execution")
    exec_api = ZoeExecutionsAPI(cfg['ZOE_URL'], cfg['ZOE_USER'], cfg['ZOE_PWD'])
    if app_name == 'ipython':
        print("Starting ipython notebook Zoe execution: ", exec_name)
        app_descr = jupyter_spark.spark_jupyter_notebook_app()
    elif app_name == 'spark':
        print("Starting Spark Cluster Zoe execution: ", exec_name)
        app_descr = spark.spark_submit_service()
    elif app_name == 'mpi':
        print("Starting MPI Zoe execution: ", exec_name)
        app_descr = openmpi.openmpi_mpirun_service()
    else:
        print("App not supported.")
        return
    exec_api.execution_start(exec_name, app_descr)
    return "Done"
