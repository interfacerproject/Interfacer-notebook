# Let's start with some lovely imports that should have been installed if not available by default
import json
import requests
import os
from zenroom import zenroom
import base64
from datetime import datetime, timezone
import random
from pdb import set_trace


from if_consts import SUPPORTED_ACTIONS, IN_PR_ACTIONS, OUT_PR_ACTIONS, IN_OUT_PR_ACTIONS
from if_consts import EVENT_FRAG, AGENT_FRAG, QUANTITY_FRAG, RESOURCE_FRAG, PROPOSAL_FRAG, \
    INTENT_FRAG, PROPINT_FRAG, LOCATION_FRAG, ACTION_FRAG, PROCESS_FRAG, PROCESSSPEC_FRAG, \
        UNIT_FRAG, RESSPEC_FRAG, PROCESSGRP_FRAG

from if_lib import send_signed

DEBUG_create_processgrp = False
def create_processgrp(cur_prgp, user_data, endpoint):

    variables = {
        "processGroup": {
            "groupedIn": cur_prgp['groupedIn'] if cur_prgp['groupedIn'] != None else None,
            "name": cur_prgp['name'],
            "note": cur_prgp['note']
        }
    }
    
    query = """mutation($processGroup: ProcessGroupCreateParams!){
        createProcessGroup(processGroup:$processGroup){
            processGroup{
                ...processgroup
            }
        }
    }""" + PROCESSGRP_FRAG + PROCESS_FRAG + PROCESSSPEC_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        assert 1 == 2

    if DEBUG_create_processgrp:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   


    cur_prgp['id'] = res_json['data']['createProcessGroup']['processGroup']['id']


def get_processgrp(name, user_data, note, processgrp_data, endpoint, processgrp_id=None):
    
    processgrp_data[f'{name}'] = {}
    cur_prgp = processgrp_data[f'{name}']

    cur_prgp["name"] = name

    cur_prgp["note"] = note
    
    cur_prgp["groupedIn"] = processgrp_id

    cur_prgp["groups"] = []

    create_processgrp(cur_prgp, user_data, endpoint)


DEBUG_insert_procingrp = False
def insert_procingrp(user_data, processgrp, process, endpoint):

    variables = {
        "process": {
            "id": process['id'],
            "groupedIn": processgrp['id']
        }
    }
    
    query = """mutation($process: ProcessUpdateParams!){
        updateProcess(process:$process){
            Process {
                ...process
            }
        }
    }""" + PROCESS_FRAG + PROCESSSPEC_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        assert 1 == 2

    if DEBUG_insert_procingrp:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   


    processgrp['groups'].append(process['id'])
    process['groupedIn'] = processgrp['id']


# query {
#   processGroup(id: id) {
#     id
#     name
#     note
#     groupedIn
#     groups(first: 50, after: $handle) {
#       edges {
#         node {
#           ... on Process {
#           }
#           ... on ProcessGroup {
#           }
#         }
#       }
#     }
#   }

#   process(id: id) {
#     id
#     name
#     note
#     groupedIn {}
#   }

#   processGroups(first: 50, after: $handle) {
#     edges {
#       node {
#       }
#     }
#   }
# }