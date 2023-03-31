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

import json
import inspect
from pdb import set_trace
import copy

from if_consts import MAX_DEPTH
from if_consts import AGENT_FRAG, QUANTITY_FRAG, RESOURCE_FRAG, PROPOSAL_FRAG, INTENT_FRAG, PROPINT_FRAG, LOCATION_FRAG, ACTION_FRAG, \
    PROCESS_FRAG, PROCESSGRP_FRAG, PROCESSSPEC_FRAG, EVENT_FRAG, RESSPEC_FRAG, UNIT_FRAG
from if_lib import send_signed

DEBUG_trace_query = False


def trace_query(id, user_data, endpoint):
    """
        This function encapsulate the trace
        algorithm implemented by the back-end
    """

    variables = {
        "id": id
    }

    query = """query($id:ID!) {
    economicResource(id:$id) {
        trace {
          __typename
          ... on EconomicEvent {
            ...event
          }
          ... on EconomicResource {...resource}
          ... on Process {...process}
        }
      }
    }

    """ + AGENT_FRAG + LOCATION_FRAG + RESOURCE_FRAG + QUANTITY_FRAG + EVENT_FRAG + PROCESS_FRAG + PROCESSGRP_FRAG + ACTION_FRAG + RESSPEC_FRAG + PROCESSSPEC_FRAG + UNIT_FRAG

    res_json = send_signed(
        query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if DEBUG_trace_query:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        raise Exception(f"Error in function {inspect.stack()[0][3]}")

    return res_json['data']['economicResource']['trace']


# VERBOSE = True


# def fill_loc(a_dpp_item, item, field):
#     if item[field] == None:
#         return
#     loc_item = item[field]
#     a_dpp_item[field] = {}
#     for key in loc_item.keys():
#         a_dpp_item[field][key] = loc_item[key]


# def fill_quantity(a_dpp_item, item, field):
#     if item[field] != None:
#         quan_item = item[field]
#         a_dpp_item[field] = {}
#         for key in quan_item.keys():
#             a_dpp_item[field][key] = quan_item[key]


# def fill_agent(a_dpp_item, item):
#     a_dpp_item['id'] = item['id']
#     a_dpp_item['name'] = item['name']
#     a_dpp_item['type'] = item['__typename']
#     a_dpp_item['note'] = item['note']
#     fill_loc(a_dpp_item, item, 'primaryLocation')

#     # set_trace()


# def fill_event(a_dpp_item, item):
#     assert item['__typename'] == 'EconomicEvent'
#     a_dpp_item['id'] = item['id']
#     a_dpp_item['name'] = item['action']['id']
#     a_dpp_item['type'] = item['__typename']
# #     breakpoint()
#     if VERBOSE:
#         a_dpp_item['provider'] = {}
#         fill_agent(a_dpp_item['provider'], item['provider'])
#         a_dpp_item['receiver'] = {}
#         fill_agent(a_dpp_item['receiver'], item['receiver'])
#         fill_loc(a_dpp_item, item, 'atLocation')
#         fill_loc(a_dpp_item, item, 'toLocation')
#         if 'effortQuantity' in item and item['effortQuantity'] != None:
#             fill_quantity(a_dpp_item, item, 'effortQuantity')
#         elif 'resourceQuantity' in item and item['resourceQuantity'] != None:
#             fill_quantity(a_dpp_item, item, 'resourceQuantity')
# #         elif 'resourceInventoriedAs' in item and item['resourceInventoriedAs'] != None:
# #             fill_quantity(a_dpp_item, item['resourceInventoriedAs'], 'onhandQuantity')


# def fill_res(a_dpp_item, item):
#     #     print(item['__typename'])
#     assert item['__typename'] == 'EconomicResource'
#     a_dpp_item['id'] = item['id']
#     a_dpp_item['name'] = item['name']
#     a_dpp_item['trackingIdentifier'] = item['trackingIdentifier']
#     a_dpp_item['type'] = item['__typename']
#     if VERBOSE:
#         a_dpp_item['primaryAccountable'] = item['primaryAccountable']['name']
#         a_dpp_item['custodian'] = item['custodian']['name']
#         a_dpp_item['metadata'] = item['metadata']
#         fill_loc(a_dpp_item, item, 'currentLocation')
#         fill_quantity(a_dpp_item, item, 'accountingQuantity')
#         fill_quantity(a_dpp_item, item, 'onhandQuantity')


# def fill_process(a_dpp_item, item):
#     assert item['__typename'] == 'Process'
#     a_dpp_item['id'] = item['id']
#     a_dpp_item['name'] = item['name']
#     a_dpp_item['type'] = item['__typename']
#     if VERBOSE:
#         a_dpp_item['note'] = item['note']


DEBUG_er_before = False


def er_before(id, user_data, dpp_children, depth, visited, endpoint):

    if depth > MAX_DEPTH:
        raise Exception(f"Max depth reached in function {inspect.stack()[0][3]}")
    depth += 1

    variables = {
        "id": id
    }

    query = """query($id:ID!) {
        economicResource(id:$id) {
            ...resource
            previous{
                __typename
                ... on EconomicEvent {
                    id
                    action {
                        id
                    }
                }
            }
        }
    }
    """ + RESOURCE_FRAG + LOCATION_FRAG + QUANTITY_FRAG + AGENT_FRAG

    res_json = send_signed(
        query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if DEBUG_er_before:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        raise Exception(f"Error in function {inspect.stack()[0][3]}")

    # dpp_item = {}
    # fill_res(dpp_item, res_json['data']['economicResource'])
    dpp_item = copy.deepcopy(res_json['data']['economicResource'])
    dpp_item.pop('previous')
    dpp_item['children'] = []

    dpp_children.append(dpp_item)

    events = res_json['data']['economicResource']['previous']
    while events != []:
        # We get the first event
        event = events.pop(0)
        # This must be of type EconomicEvent since the call only returns that
        assert event['__typename'] == "EconomicEvent"
        # We include the raise event as it can be reached from more branches
        # and it is assumed to be the starting point
#         if not event['action']['id'] == 'raise':
        while event['id'] in visited:
            #                breakpoint()
            # if DEBUG_er_before:
            print(f"id {event['id']} already in visited in {inspect.stack()[0][3]}")
            if events == []:
                return
            event = events.pop(0)
        visited.add(event['id'])

        ee_before(event['id'], user_data, dpp_item['children'],
                  depth, visited, endpoint)


DEBUG_ee_before = False


def ee_before(id, user_data, dpp_children, depth, visited, endpoint):

    if depth > MAX_DEPTH:
        raise Exception(f"Max depth reached in function {inspect.stack()[0][3]}")
    depth += 1

    variables = {
        "id": id
    }

    query = """query($id:ID!) {
        economicEvent(id:$id) {
            ...event
            previous{
                __typename
                ... on  EconomicResource {
                    id
                    name
                }
                ... on EconomicEvent {
                    id
                    action {
                        id
                    }
                }
                ... on Process {
                    id
                    name
                }
            }
          }
        }
    """ + EVENT_FRAG + LOCATION_FRAG + QUANTITY_FRAG + AGENT_FRAG + ACTION_FRAG + PROCESS_FRAG + PROCESSGRP_FRAG + \
        RESSPEC_FRAG + RESOURCE_FRAG + UNIT_FRAG + PROCESSSPEC_FRAG

    res_json = send_signed(
        query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if DEBUG_ee_before:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        raise Exception(f"Error in function {inspect.stack()[0][3]}")

    # dpp_item = {}
    # fill_event(dpp_item, res_json['data']['economicEvent'])
    dpp_item = copy.deepcopy(res_json['data']['economicEvent'])
    # Add a name field which events do not have
    dpp_item['name'] = res_json['data']['economicEvent']['action']['id']
    dpp_item.pop('previous')
    dpp_item['children'] = []

    dpp_children.append(dpp_item)

    pf_items = res_json['data']['economicEvent']['previous']
    if DEBUG_ee_before:
        print("pf_items")
        print(pf_items)

    if pf_items == None:
        return
    if type(pf_items) is dict:
        pf_items = [pf_items]
    if pf_items != []:
        pf_item = pf_items[0]
        if pf_item['id'] in visited:
            print(f"id {pf_item['id']} already in visited in {inspect.stack()[0][3]}")
            return

        if pf_item['__typename'] == "EconomicEvent":
            visited.add(pf_item['id'])
            ee_before(pf_item['id'], user_data,
                      dpp_item['children'], depth, visited, endpoint)
        if pf_item['__typename'] == "EconomicResource":
            er_before(pf_item['id'], user_data,
                      dpp_item['children'], depth, visited, endpoint)
        if pf_item['__typename'] == "Process":
            visited.add(pf_item['id'])
            pr_before(pf_item['id'], user_data,
                      dpp_item['children'], depth, visited, endpoint)


DEBUG_pr_before = False


def pr_before(id, user_data, dpp_children, depth, visited, endpoint):

    if depth > MAX_DEPTH:
        raise Exception(f"Max depth reached in function {inspect.stack()[0][3]}")
    depth += 1

    variables = {
        "id": id
    }

    query = """query($id:ID!) {
      process(id:$id) {
          ...process
          previous{
            __typename
            ... on EconomicEvent {
                id
                action {
                    id
                }
            }
        }
      }
    }
    """ + PROCESS_FRAG + PROCESSGRP_FRAG + PROCESSSPEC_FRAG

    res_json = send_signed(
        query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if DEBUG_pr_before:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        raise Exception(f"Error in function {inspect.stack()[0][3]}")

    # dpp_item = {}
    # fill_process(dpp_item, res_json['data']['process'])
    dpp_item = copy.deepcopy(res_json['data']['process'])
    dpp_item.pop('previous')
    dpp_item['children'] = []

    dpp_children.append(dpp_item)

    events = res_json['data']['process']['previous']
    if events != []:
        for event in events:
            # This must be of type EconomicEvent since the call only returns that
            assert event['__typename'] == "EconomicEvent"
            if event['id'] in visited:
                print(f"id {event['id']} already in visited in {inspect.stack()[0][3]}")
                continue
            visited.add(event['id'])
            ee_before(event['id'], user_data,
                      dpp_item['children'], depth, visited, endpoint)


DEBUG_get_ddp = False


def get_dpp(res_id, user_data, endpoint):

    variables = {
        "id": res_id
    }

    query = """query($id:ID!){
        economicResource(id: $id) {
            traceDpp
        }
    }
    """

    res_json = send_signed(
        query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if DEBUG_get_ddp:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        raise Exception(f"Error in function {inspect.stack()[0][3]}")

    be_dpp = res_json['data']['economicResource']['traceDpp']

    return be_dpp


BANNER = "#" * 80


def list_nodes(item, assigned):
    """
        This function assign each node to a dict
        with the count of how many times the node is present
        in the dpp.
    """
    id = item['id'] if 'id' in item else item['node']['id']
    if id in assigned:
        assigned[id]['count'] += 1
    else:
        if 'node' not in item and 'name' not in item:
            raise Exception(f"Item's format is not expected: {item}. Error in function {inspect.stack()[0][3]}")
        assigned[id] = {
            'count': 1,
            'type': item['type'],
            'name': item['name'] if 'name' in item else item['node']['name'] if 'name' in item['node'] else item['node']['action']['id'],
        }

    nr_ch = len(item['children'])

    for ch in range(nr_ch):
        ch_dpp = item['children'][ch]
        list_nodes(ch_dpp, assigned)


def check_duplicates(trace, events, fe_assigned, be_assigned):
    """
        This function looks at the four types of trace
        and check for duplicates
    """
    print(BANNER)
    print("Check whether there are any duplicated trace items")
    item_ids = {}
    for j, item in enumerate(trace):
        if not item['id'] in item_ids:
            item_ids[item['id']] = 1
        else:
            item_ids[item['id']] += 1
            print(
                f"Item {item['id']} of type {item['__typename']} at pos {j} is a duplicate")

    print(BANNER)
    print("Check whether there are any duplicated events")
    events_proc_ids = {}
    for i, evt_prc in enumerate(events):
        id = evt_prc['event_id'] if 'event_id' in evt_prc else evt_prc['process_id']
        if not id in events_proc_ids:
            events_proc_ids[id] = 1
        else:
            events_proc_ids[id] += 1
            print(
                f"{'Event' if 'event_id' in evt_prc else 'Process'} {id} with {'action' if 'event_id' in evt_prc else 'name'} {evt_prc['action'] if 'event_id' in evt_prc else evt_prc['name']} at pos {i} is a duplicate")

    print(BANNER)
    print("Check whether there are any duplicated nodes in front-end dpp")
    for id in fe_assigned.keys():
        el = fe_assigned[id]
        if el['count'] > 1:
            print(
                f"Element {el['name']} with id {id} with type {el['type']} has {el['count']-1} duplicates")

    print(BANNER)
    print("Check whether there are any duplicated nodes in back-end dpp")
    for id in be_assigned.keys():
        el = be_assigned[id]
        if el['count'] > 1:
            print(
                f"Element {el['name']} with id {id} with type {el['type']} has {el['count']-1} duplicates")

def check_trace_events(trace, events):
    """
        This function compares the trace to the event list,
        which is not useful when looking whether trace items are in events,
        as the latter misses all resources, but it can be usefull to see
        whether all items from events are in the trace as they should.
    """
    # we reverse the events to have last in first out
    events.reverse()

    print(BANNER)
    print("Are trace items in the events?")
    for j, item in enumerate(trace):
        found = False
        name = item['name'] if 'name' in item else item['action']['id']
        pref = f"trace item {name} id: {item['id']} of type {item['__typename']}"
        for i, evt_prc in enumerate(events):
            id = evt_prc['event_id'] if 'event_id' in evt_prc else evt_prc['process_id']
            if item['id'] == id:
                # print(f"{pref} at pos {j} found at pos {i}")
                found = True
        if not found:
            print(f"NOT FOUND: {pref}")

    print(BANNER)
    print("Are events in the trace?")
    for i, evt_prc in enumerate(events):
        found = False
        id = evt_prc['event_id'] if 'event_id' in evt_prc else evt_prc['process_id']
        name = evt_prc['action'] if 'event_id' in evt_prc else evt_prc['name']
        pref = f'{"Event" if "event_id" in evt_prc else "Process"} {name} with id {id}'
        for j, item in enumerate(trace):
            if item['id'] == id:
                # print(f'{pref} pos {i} found at pos {j}')
                found = True
        if not found:
            print(f"NOT FOUND: {pref}")


def check_trace_dpp(trace, assigned):
    print(BANNER)
    print("Are trace items in the dpp?")
    for j, item in enumerate(trace):
        found = False
        if item['id'] not in assigned:
            name = item['name'] if 'name' in item else item['action']['id']
            pref = f"trace item {name} id: {item['id']} of type {item['__typename']}"
            print(f"NOT FOUND: {pref} at pos {j}")

    print(BANNER)
    print("Are dpp elements in the trace?")
    for id in assigned.keys():
        el = assigned[id]
        pref = f"Element {el['name']} with id {id} of type {el['type']}"
        found = False
        for j, item in enumerate(trace):
            if item['id'] == id:
                # print(f"{pref} found at pos {j}")
                found = True
        if not found:
            print(f"NOT FOUND: {pref}")


def check_betrace(tot_dpp, be_dpp):
    # set_trace()
    if tot_dpp['id'] == be_dpp['node']['id']:
        nr_ch = len(tot_dpp['children'])
        nr_ch_be = len(be_dpp['children'])
        if nr_ch == nr_ch_be:
            if nr_ch == 0:
                return
            elif nr_ch == 1:
                check_betrace(tot_dpp['children'][0], be_dpp['children'][0])
            else:
                for ch in tot_dpp['children']:
                    found = False
                    for ch_be in be_dpp['children']:
                        if ch['id'] == ch_be['node']['id']:
                            found = True
                            check_betrace(ch, ch_be)
                    if not found:
                        raise Exception(f"Children {tot_dpp['id']} and {be_dpp['node']['id']} differ in ids")
                return
        else:
            print(f"Children of id {tot_dpp['id']} differ in number")
            print(f"Children of back-end")
            for ch in be_dpp['children']:
                name = ch['node']['name'] if 'name' in ch['node'] else ch['node']['action']['id']
                print(f"Name: {name}, id {ch['node']['id']}")
            print(f"Children of front-end")
            for ch in tot_dpp['children']:
                print(f"Name: {ch['name']}, id {ch['id']}")
            raise Exception(f"Children of id {tot_dpp['id']} differ in number")

    else:
        raise Exception(f"{tot_dpp['id']} different from {be_dpp['node']['id']}")


def check_traces(trace, events, fe_dpp, be_dpp):
    """
        This function checks the different traces
        to see whether they are consistent.
        <events> is a data structure containing only events and processes
        as recorded by the front-end.
    """
    # set_trace()
    fe_assigned = {}
    list_nodes(fe_dpp[0], fe_assigned)
    be_assigned = {}
    # set_trace()
    if type(be_dpp) == dict:
        list_nodes(be_dpp, be_assigned)
    elif type(be_dpp) == list and len(be_dpp) == 1:
        list_nodes(be_dpp[0], be_assigned)
    else:
        raise Exception(f"Unknown type of be_dpp. Error in function {inspect.stack()[0][3]}")
    print(BANNER)
    print(
        f'nr trace: {len(trace)}, nr events: {len(events)}, nr front-end dpp: {len(fe_assigned)}, nr back-end dpp: {len(be_assigned)}')
    check_duplicates(trace, events, fe_assigned, be_assigned)
    check_trace_events(trace, events)
    check_trace_dpp(trace, fe_assigned)
    print(BANNER)
    print("Are back-end and my trace the same?")

    check_betrace(fe_dpp[0], be_dpp[0])


def convert_bedpp(dpp):
    # set_trace()
    conv_dpp = {k: v for k, v in dpp['node'].items()}
    conv_dpp['type'] = dpp['type']
    name = dpp['node']['name'] if 'name' in dpp['node'] else dpp['node']['action']['id']
    conv_dpp['name'] = name
    dl = len(dpp['children'])
    conv_dpp['children'] = [{} for i in range(dl)]
    for ch in range(dl):
        conv_dpp['children'][ch] = convert_bedpp(dpp['children'][ch])
    return conv_dpp

def differentiate_resources(dpp_item):
    if dpp_item['type'] == 'EconomicResource':
        for child in dpp_item['children']:
            # breakpoint()
            if child['name'] == 'modify':
                # breakpoint()
                dpp_item['id'] = dpp_item['id'] + child['id']
                break
    for child in dpp_item['children']:
        differentiate_resources(child)
