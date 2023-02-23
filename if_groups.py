# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2022-2023 Dyne.org foundation <foundation@dyne.org>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
    }""" + PROCESSGRP_FRAG 

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


DEBUG_query_processgrp = False
def query_processgrp(prgp_id, user_data, endpoint):

    variables = {
        "id": prgp_id
    }
    
    query = """query($id:ID!){
        processGroup(id: $id){
            ...processgroup
        }
    }""" + PROCESSGRP_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        assert 1 == 2

    if DEBUG_query_processgrp:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   


    cur_prgp = res_json['data']['processGroup']
    
    return cur_prgp


def get_processgrp(name, user_data, note, processgrp_data, endpoint, processgrp_id=None):
    
    processgrp_data[f'{name}'] = {}
    cur_prgp = processgrp_data[f'{name}']

    cur_prgp["name"] = name

    cur_prgp["note"] = note

    cur_prgp["type"] = "ProcessGroup"
    
    cur_prgp["groupedIn"] = processgrp_id

    cur_prgp["groups"] = []

    create_processgrp(cur_prgp, user_data, endpoint)

    if processgrp_id != None:
        # Need to insert the process group as child of the parent
        for key in processgrp_data.keys():
            # set_trace()
            if processgrp_data[key]['id'] == processgrp_id:
                processgrp_data[key]['groups'].append(cur_prgp['id'])
                return
        # we should not get here
        print(f"Parent {processgrp_id} not found")
        assert 1 == 2



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
    }""" + PROCESS_FRAG + PROCESSGRP_FRAG + PROCESSSPEC_FRAG

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
# {k: v for k, v in dpp.items() if k not in ['children']}

def fill_prcgrp(id, processgrp_data, user_data, endpoint):
    prg_grp = query_processgrp(id, user_data, endpoint)
    
    processgrp_data[prg_grp['name']] = {}
    in_obj = processgrp_data[prg_grp['name']]
    in_obj['id'] = prg_grp['id']
    in_obj['name'] = prg_grp['name']
    in_obj['note'] = prg_grp['note']
    in_obj['type'] = prg_grp['type']
    
    # breakpoint()
    in_obj['groups'] = [node['node']['id'] for node in prg_grp['groups']['edges']]
    if prg_grp['groupedIn'] != None:
        in_obj['groupedIn'] = prg_grp['groupedIn']['id']
        fill_prcgrp(in_obj['groupedIn'], processgrp_data, user_data, endpoint)
    else: 
        in_obj['groupedIn'] = None

def find_procgrp(dpp, processgrp_data, user_data, endpoint):
    present = False
    if dpp['type'] == "Process" and dpp['grouped_in_id'] != None:
        id = dpp['grouped_in_id']
        for key in processgrp_data.keys():
            if processgrp_data[key]['id'] == id:
                present = True
                print(f"Process: {dpp['name']}, Group present: {processgrp_data[key]['name']}")
                # breakpoint()
                break
        if not present:
            fill_prcgrp(id, processgrp_data, user_data, endpoint)
            # print(f"Process: {dpp['name']}, Group not present: {prg_grp['name']}")

    for child in dpp['children']:
        find_procgrp(child, processgrp_data, user_data, endpoint)

