# encoding: utf-8
from __future__ import unicode_literals

import requests
import json
from horizon.utils.memoized import memoized  # noqa


# TODO: Take parameters from a config file
URL_BASIC = "http://10.0.2.55:8080/"

#@memoized
#def sds_controller_api(request):
#    return request.user.token.id

############################## # Storage groups API # ##############################
def list_storagegroups():
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "groups"

    r = requests.get(url, headers=headers)
    return r
    
def retrieve_storagegroup(groupid):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "groups/" + groupid

    r = requests.get(url, headers=headers)
    return r        

def delete_storagegroup(obj_id):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "groups/" + obj_id

    r = requests.delete(url, headers=headers)
    return r  

def create_storagegroup(request, data):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "groups"

    r = requests.post(url, headers=headers, data=json.dumps(data))
    return r
    
def associate_group_node(request, groupid, node):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "groups/" + groupid + "/nodes/" + node

    r = requests.put(url, headers=headers)
    return r    

def disassociate_group_node(request, groupid, node):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "groups/" + groupid + "/nodes/" + node

    r = requests.delete(url, headers=headers)
    return r 
    
def list_groups_nodes(request, groupid):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "groups/" + groupid + "/nodes"

    r = requests.get(url, headers=headers)
    return r

def update_storagegroup(request, groupid, data):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "groups/" + groupid

    r = requests.patch(url, headers=headers, data=json.dumps(data))
    return r 

################################# Policies ##################################
def create_policy(request, data):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "policies"

    r = requests.post(url, headers=headers, data=json.dumps(data))
    return r

def update_policy(request, policy_id, data):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "policies/" + policy_id

    r = requests.patch(url, headers=headers, data=json.dumps(data))
    return r
    
def list_policies(request):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "policies"

    r = requests.get(url, headers=headers)
    return r
    
def retrieve_policy(policyid):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "policies/" + policyid

    r = requests.get(url, headers=headers)
    return r

def delete_policy(obj_id):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "policies/" + obj_id

    r = requests.delete(url, headers=headers)
    return r     

################################# Controllers ##################################
def list_controllers(request):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "controllers"

    r = requests.get(url, headers=headers)
    return r

def retrieve_controller(node):
    #token = sds_controller_api(request)
    headers = {'API-Version':'0'}

    url = URL_BASIC + "controllers/" + node

    r = requests.get(url, headers=headers)
    return r