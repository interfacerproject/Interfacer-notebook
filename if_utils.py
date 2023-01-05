import json
import urllib.parse
import re
from pathlib import Path

# Function to show all the data
def show_data(users_data, locs_data, res_data, units_data, res_spec_data, process_data, event_seq):
    print("Users")
    print(json.dumps(users_data, indent=2))
    print("Locations")
    print(json.dumps(locs_data, indent=2))

    print("Resources")
    print(json.dumps(res_data, indent=2))
    print("Units")
    print(json.dumps(units_data, indent=2))

    print("Resource Specifications")
    print(json.dumps(res_spec_data, indent=2))

    print("Process Definitions")
    print(json.dumps(process_data, indent=2))

    print("Event sequence")
    print(json.dumps(event_seq, indent=2))

def get_filename(filename, ep, uc):
    pattern = r'http[s]?://'
    strp_endpoint = re.sub(pattern, '', ep)
    # new_filename = f'./{uc}/{urllib.parse.quote_plus(strp_endpoint)}/{filename}'
    my_dir = Path('use_cases', uc, urllib.parse.quote_plus(strp_endpoint))
    if not my_dir.is_dir():
        my_dir.mkdir(parents=True)

    new_filename = Path(my_dir, filename)
    return new_filename

# this function is equivalent to JSON.stringify in javascript, i.e. it does not add spaces
# Although it does not seem to matter as Zenroom removes spaces
def stringify(json_obj):
    return json.dumps(json_obj, separators=(',',':'))

def save_traces(use_case, tot_dpp, trace, be_dpp, event_seq):
    # Writing dpp to file
    my_dir = Path('traces')
    if not my_dir.is_dir():
        my_dir.mkdir(parents=True)

    file = Path(my_dir, f'{use_case}_fe_trace.json')
    with open(file, "w") as f:
        f.write(json.dumps(tot_dpp, indent=2))
    
    file = Path(my_dir, f'{use_case}_be_trace.json')
    with open(file, "w") as f:
        f.write(json.dumps(trace, indent=2))

    file = Path(my_dir, f'{use_case}_be_impl_fe_trace.json')
    with open(file, "w") as f:
        f.write(json.dumps(be_dpp, indent=2))
    
    file = Path(my_dir, f'{use_case}_events.json')
    with open(file, "w") as f:
        f.write(json.dumps(event_seq, indent=2))

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

