
import json
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
    events_ids = {}
    for i, event in enumerate(events):
        if not event['event_id'] in events_ids:
            events_ids[event['event_id']] = 1
        else:
            events_ids[event['event_id']] += 1
            print(f"Event {event['event_id']} with action {event['action']} at pos {i} is a duplicate")

    print(BANNER)
    print("Check whether there are any duplicated in dpp")
    for id in assigned.keys():
        el = assigned[id]
        if el['count'] > 1:
            print(f"Element {el['name']} with id {id} with type {el['type']} has {el['count']-1} duplicates")
    

def check_trace_events(trace, events):
    # breakpoint()
    # we reverse the events to have last in first out 
    events.reverse()

    print(BANNER)
    print("Where are trace items in the events?")
    for j, item in enumerate(trace):
        found = False
        name = item['name'] if 'name' in item else item['action']['id']
        pref = f"trace item {name} id: {item['id']} of type {item['__typename']}"
        for i, event in enumerate(events):
            event_id = event['event_id']
            if item['id'] == event_id:
                print(f"{pref} at pos {j} found at pos {i}")
                found = True
        if not found:
            print(f"NOT FOUND: {pref}")

    print(BANNER)
    print("Where are events in the trace?")
    for i, event in enumerate(events):
        found = False
        event_id = event['event_id'] if 'event_id' in event else event['process_id']
        name = event['action']
        pref = f'Event {name} with id {event_id}'
        # breakpoint()
        for j,item in enumerate(trace):
            if item['id'] == event_id:
                print(f'{pref} pos {i} found at pos {j}')
                found = True
        if not found:
            print(f"NOT FOUND: {pref}")

def check_trace_dpp(trace, assigned):
    print(BANNER)
    print("Are trace items in the dpp?")
    for j, item in enumerate(trace):
        found = False
        # breakpoint()
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
    # breakpoint()
    if tot_dpp['id'] == be_dpp['node']['id']:
        nr_ch = len(tot_dpp['children'])
        nr_ch_be = len(be_dpp['children'])
        if nr_ch == nr_ch_be:
            if nr_ch == 0:
                return
            elif nr_ch == 1:
                # breakpoint()
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
                # breakpoint()
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


if __name__ == "__main__":
    # pref = 'gownshirt'
    pref = 'isogown'
    with open(f"{pref}_trace.json", "r") as f:
        tot_dpp = json.loads(f.read())
    with open(f"{pref}_trace.list.json", "r") as f:
        trace = json.loads(f.read())
    with open(f"{pref}_events.json", "r") as f:
        events = json.loads(f.read())
    with open(f"{pref}_trace.tree.json", "r") as f:
        be_dpp = json.loads(f.read())

    # breakpoint()
    check_traces(trace, events, tot_dpp, be_dpp)
