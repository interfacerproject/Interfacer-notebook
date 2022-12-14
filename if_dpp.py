import json

from if_consts import MAX_DEPTH, AGENT_FRAG, LOCATION_FRAG, QUANTITY_FRAG
from if_lib import send_signed

DEBUG_trace_query = False

def trace_query(id, user_data, endpoint):

    variables = {
        "id": id
    }
    
    query = """query($id:ID!) {
    economicResource(id:$id) {
        trace {
          __typename
          ... on EconomicEvent {
            id
            action {id}
            provider {...agent}
            receiver {...agent}
            resourceConformsTo {id name note}
            resourceInventoriedAs {...resource}
            resourceQuantity {...measure}
          }
          ... on EconomicResource {...resource}
          ... on Process {id name note}
        }
      }
    }

    fragment measure on Measure {
      hasNumericalValue
      hasUnit {id label symbol}
    }

    fragment agent on Agent {
      id name
    }

    fragment resource on EconomicResource {
      id name note
      primaryAccountable {...agent}
      custodian {id name}
      onhandQuantity {...measure}
      accountingQuantity {...measure}
      classifiedAs
    }
    """

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)
    
    if DEBUG_trace_query:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   

    return res_json['data']['economicResource']['trace']



VERBOSE = True
def fill_loc(a_dpp_item, item, field):
    if item[field] == None:
        return
    loc_item = item[field]
    a_dpp_item[field] = {}
    a_dpp_item[field]['id'] = loc_item['id']
    a_dpp_item[field]['name'] = loc_item['name']
    a_dpp_item[field]['alt'] = loc_item['alt']
    a_dpp_item[field]['lat'] = loc_item['lat']
    a_dpp_item[field]['long'] = loc_item['long']                    
    a_dpp_item[field]['mappableAddress'] = loc_item['mappableAddress']                    
    a_dpp_item[field]['note'] = loc_item['note']                                    
    
def fill_quantity(a_dpp_item, item, field):
    if item[field] != None:
        a_dpp_item[field] = f"{item[field]['hasNumericalValue']} ({item[field]['hasUnit']['symbol']})"

    
def fill_event(a_dpp_item, item):
    assert item['__typename'] == 'EconomicEvent'
    a_dpp_item['id'] = item['id']
    a_dpp_item['name'] = item['action']['id']
    a_dpp_item['type'] = item['__typename']
#     breakpoint()
    if VERBOSE:
        a_dpp_item['provider'] = item['provider']['name']
        a_dpp_item['receiver'] = item['receiver']['name']
        fill_loc(a_dpp_item, item, 'atLocation')
        fill_loc(a_dpp_item, item, 'toLocation')
        if 'effortQuantity' in item and item['effortQuantity'] != None:
            fill_quantity(a_dpp_item, item, 'effortQuantity')
        elif 'resourceQuantity' in item and item['resourceQuantity'] != None:
            fill_quantity(a_dpp_item, item, 'resourceQuantity')
#         elif 'resourceInventoriedAs' in item and item['resourceInventoriedAs'] != None:
#             fill_quantity(a_dpp_item, item['resourceInventoriedAs'], 'onhandQuantity')
        
def fill_res(a_dpp_item, item):
#     print(item['__typename'])
    assert item['__typename'] == 'EconomicResource'
    a_dpp_item['id'] = item['id']
    a_dpp_item['name'] = item['name']
    a_dpp_item['trackingIdentifier'] = item['trackingIdentifier']
    a_dpp_item['type'] = item['__typename']
    if VERBOSE:
        a_dpp_item['primaryAccountable'] = item['primaryAccountable']['name']
        a_dpp_item['custodian'] = item['custodian']['name']
        a_dpp_item['metadata'] = item['metadata']
        fill_loc(a_dpp_item, item, 'currentLocation')
        fill_quantity(a_dpp_item, item, 'accountingQuantity')
        fill_quantity(a_dpp_item, item, 'onhandQuantity')

def fill_process(a_dpp_item, item):
    assert item['__typename'] == 'Process'
    a_dpp_item['id'] = item['id']
    a_dpp_item['name'] = item['name']
    a_dpp_item['type'] = item['__typename']
    if VERBOSE:
        a_dpp_item['note'] = item['note']



DEBUG_er_before = False

def er_before(id, user_data, dpp_children, depth, visited, endpoint):

    if depth > MAX_DEPTH:
        return
    depth += 1

    variables = {
        "id": id
    }
    
    query = """query($id:ID!) {
        economicResource(id:$id) {
            id
            name
            trackingIdentifier
            __typename
            metadata
            primaryAccountable {
              ...agent
            }
            custodian {
              ...agent
            }
            accountingQuantity {
                ...quantity
            }
            onhandQuantity{
                ...quantity
            }
            currentLocation {
                ...location
            }
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
    """ + LOCATION_FRAG + QUANTITY_FRAG + AGENT_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)
    
    if DEBUG_er_before:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   

    dpp_item = {}    
    fill_res(dpp_item, res_json['data']['economicResource'])
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
            if DEBUG_er_before:
                print(f"id {event['id']} already in visited")
            if events == []:
                return
            event = events.pop(0)
        visited[event['id']] = {}            
            
        ee_before(event['id'], user_data, dpp_item['children'], depth, visited, endpoint)         

DEBUG_ee_before = False

def ee_before(id, user_data, dpp_children, depth, visited, endpoint):

    if depth > MAX_DEPTH:
        return
    depth += 1

    variables = {
        "id": id
    }
    
    query = """query($id:ID!) {
        economicEvent(id:$id) {
            id
            __typename
            action {
                id
                label
            }
            provider {
                ...agent
            }
            receiver {
                ...agent
            }
            atLocation {
                ...location
            }
            toLocation {
                ...location
            }
            effortQuantity {
                ...quantity
            }
            resourceQuantity {
                ...quantity
            }
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
    """ + LOCATION_FRAG + QUANTITY_FRAG + AGENT_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)
    
    if DEBUG_ee_before:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   

    dpp_item = {}    
    fill_event(dpp_item, res_json['data']['economicEvent'])
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
            print(f"id {pf_item['id']} already in visited")
            return

        if pf_item['__typename'] == "EconomicEvent":
            visited[pf_item['id']] = {}
            ee_before(pf_item['id'], user_data, dpp_item['children'], depth, visited, endpoint)
        if pf_item['__typename'] == "EconomicResource":
            er_before(pf_item['id'], user_data, dpp_item['children'], depth, visited, endpoint)
        if pf_item['__typename'] == "Process":
            visited[pf_item['id']] = {}
            pr_before(pf_item['id'], user_data, dpp_item['children'], depth, visited, endpoint)


DEBUG_pr_before = False

def pr_before(id, user_data, dpp_children, depth, visited, endpoint):

    if depth > MAX_DEPTH:
        return
    depth += 1

    variables = {
        "id": id
    }
    
    query = """query($id:ID!) {
      process(id:$id) {
          id
          name
          note
          __typename
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
    """

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)
    
    if DEBUG_pr_before:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   

    dpp_item = {}    
    fill_process(dpp_item, res_json['data']['process'])
    dpp_item['children'] = []
    
    dpp_children.append(dpp_item)

    events = res_json['data']['process']['previous']
    if events != []:
        for event in events:
            # This must be of type EconomicEvent since the call only returns that
            assert event['__typename'] == "EconomicEvent"
            if event['id'] in visited:
                print(f"id {event['id']} already in visited")
                continue
            visited[event['id']] = {}
            ee_before(event['id'], user_data, dpp_item['children'], depth, visited, endpoint)


DEBUG_get_ddp = True

def get_ddp(res_id, user_data, endpoint):

    variables = {
        "id": res_id
    }
    
    query = """query($id:ID!){
        economicResource(id: $id) {
            traceDpp
        }
    }
    """

    
    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)
    
    if DEBUG_get_ddp:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))
        
    be_dpp = res_json['data']['economicResource']['traceDpp']
    
    return be_dpp

BANNER = "#" * 80

def get_nodes(item, assigned):
    if item['id'] in assigned:
        assigned[item['id']]['count'] += 1
    else:
        assigned[item['id']] = {
            'count': 1,
            'type' : item['type'],
            'name' : item['name'],
        }

    nr_ch = len(item['children'])

    for ch in range(nr_ch):
        ch_dpp = item['children'][ch]
        get_nodes(ch_dpp, assigned)
    
def check_duplicates(trace, events, assigned):
    print(BANNER)
    print("Check whether there are any duplicated trace items")
    item_ids = {}
    for j, item in enumerate(trace):
        if not item['id'] in item_ids:
            item_ids[item['id']] = 1
        else:
            item_ids[item['id']] += 1
            print(f"Item {item['id']} of type {item['__typename']} at pos {j} is a duplicate")

    print(BANNER)
    print("Check whether there are any duplicated events")
    events_proc_ids = {}
    for i, evt_prc in enumerate(events):
        id = evt_prc['event_id'] if 'event_id' in evt_prc else evt_prc['process_id']
        if not id in events_proc_ids:
            events_proc_ids[id] = 1
        else:
            events_proc_ids[id] += 1
            print(f"{'Event' if 'event_id' in evt_prc else 'Process'} {id} with {'action' if 'event_id' in evt_prc else 'name'} {evt_prc['action'] if 'event_id' in evt_prc else evt_prc['name']} at pos {i} is a duplicate")

    print(BANNER)
    print("Check whether there are any duplicated in dpp")
    for id in assigned.keys():
        el = assigned[id]
        if el['count'] > 1:
            print(f"Element {el['name']} with id {id} with type {el['type']} has {el['count']-1} duplicates")
    

def check_trace_events(trace, events):
    # we reverse the events to have last in first out 
    events.reverse()

    print(BANNER)
    print("Where are trace items in the events?")
    for j, item in enumerate(trace):
        found = False
        name = item['name'] if 'name' in item else item['action']['id']
        pref = f"trace item {name} id: {item['id']} of type {item['__typename']}"
        for i, evt_prc in enumerate(events):
            id = evt_prc['event_id'] if 'event_id' in evt_prc else evt_prc['process_id']
            if item['id'] == id:
                print(f"{pref} at pos {j} found at pos {i}")
                found = True
        if not found:
            print(f"NOT FOUND: {pref}")

    print(BANNER)
    print("Where are events in the trace?")
    for i, evt_prc in enumerate(events):
        found = False
        id = evt_prc['event_id'] if 'event_id' in evt_prc else evt_prc['process_id']
        name = evt_prc['action'] if 'event_id' in evt_prc else evt_prc['name']
        pref = f'{"Event" if "event_id" in evt_prc else "Process"} {name} with id {id}'
        for j,item in enumerate(trace):
            if item['id'] == id:
                print(f'{pref} pos {i} found at pos {j}')
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
        for j,item in enumerate(trace):
            if item['id'] == id:
                print(f"{pref} found at pos {j}")
                found = True
        if not found:
            print(f"NOT FOUND: {pref}")

def check_betrace(tot_dpp, be_dpp):
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
                        print(f"Children {tot_dpp['id']} and {be_dpp['node']['id']} differ in ids")
                        break
                return
        else:
            print(f"Children of id {tot_dpp['id']} differ in number")
            print(f"Children of back-end")
            for ch in be_dpp['children']:
                name = ch['node']['name'] if 'name' in ch['node'] else ch['node']['action_id']
                print(f"Name: {name}, id {ch['node']['id']}")
            print(f"Children of front-end")
            for ch in tot_dpp['children']:
                print(f"Name: {ch['name']}, id {ch['id']}")
            
    else:
        print(f"{tot_dpp['id']} different from {be_dpp['node']['id']}")


def check_traces(trace, events, tot_dpp, be_dpp):
    assigned = {}
    get_nodes(tot_dpp[0], assigned)
    print(BANNER)
    print(f'nr trace: {len(trace)}, nr events: {len(events)}, nr dpp: {len(assigned)}')
    check_duplicates(trace, events,assigned)
    check_trace_events(trace, events)
    check_trace_dpp(trace, assigned)
    print(BANNER)
    print("Are back-end and my trace the same?")

    check_betrace(tot_dpp[0], be_dpp)


def convert_bedpp(dpp):
    # breakpoint()
    conv_dpp = {k:v for k,v in dpp['node'].items()}
    conv_dpp['type'] = dpp['type']
    name = dpp['node']['name'] if 'name' in dpp['node'] else dpp['node']['action_id']
    conv_dpp['name'] = name
    dl = len(dpp['children'])
    conv_dpp['children'] = [{} for i in range(dl)]
    for ch in range(dl):
        conv_dpp['children'][ch] = convert_bedpp(dpp['children'][ch])
    return conv_dpp
