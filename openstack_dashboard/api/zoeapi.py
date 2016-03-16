import requests
from horizon.utils.memoized import memoized  # noqa
import json
from zoe_lib.executions import ZoeExecutionsAPI

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

    url = URL_BASIC + "/sdscontroller/executions"
    r = requests.get(url, headers=headers)
    return r


def list_zoe_exec():
    exec_api = ZoeExecutionsAPI(cfg['ZOE_URL'], cfg['ZOE_USER'], cfg['ZOE_PWD'])
    data = exec_api.list()
    return data
