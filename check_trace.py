
import json

def check_trace_events(trace_items, events):
    # breakpoint()
    # we reverse the events to have last in first out 
    events.reverse()
    print(f'nr trace: {len(trace_items)}, nr events: {len(events)}')
    print("Check whether there are any duplicated trace items")
    item_ids = {}
    for j, item in enumerate(trace_items):
        if not item['id'] in item_ids:
            item_ids[item['id']] = 1
        else:
            item_ids[item['id']] += 1
            print(f"Item {item['id']} of type {item['__typename']} at pos {j} is a duplicate")

    print("Check whether there are any duplicated events")
    events_ids = {}
    for i, event in enumerate(events):
        if not event['event_id'] in events_ids:
            events_ids[event['event_id']] = 1
        else:
            events_ids[event['event_id']] += 1
            print(f"Event {event['event_id']} with action {event['action']} at pos {i} is a duplicate")

    print("Where are trace items in the events?")
    for j, item in enumerate(trace_items):
        found = False
        for i, event in enumerate(events):
            event_id = event['event_id']
            if item['id'] == event_id:
                print(f"trace item {item['id']} at pos {j} found at pos {i}")
                found = True
        if not found:
            print(f"{item['id']} at pos {j} of type {item['__typename']} not found")

    print("Where are events in the trace?")
    for i, event in enumerate(events):
        found = False
        event_id = event['event_id'] if 'event_id' in event else event['process_id']
        for j,item in enumerate(trace_items):
            if item['id'] == event_id:
                print(f'event pos {i} found at pos {j}')
                found = True
        if not found:
            print(f"{event_id} with action {event['action']} not found")

if __name__ == "__main__":
    with open("gownshirt_trace.json", "r") as f:
        tot_dpp = json.loads(f.read())
    with open("gownshirt_trace.backend.json", "r") as f:
        trace = json.loads(f.read())
    with open("gownshirt_events.json", "r") as f:
        events = json.loads(f.read())
    # breakpoint()
    check_trace_events(trace, events)