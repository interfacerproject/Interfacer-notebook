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
import urllib.parse
import re
from pathlib import Path
from collections.abc import MutableMapping
from pdb import set_trace

def _flatten_dict_gen(d, parent_key, sep):
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, sep=sep).items()
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '.'):
    return dict(_flatten_dict_gen(d, parent_key, sep))

# Function to show all the data
def show_data(users_data:dict, locs_data:dict, res_data:dict, units_data:dict, res_spec_data:dict, process_data:dict, event_seq:dict, \
    proposal_data:dict={}, intent_data:dict={}, prop_int_data:dict={}, satisfaction_data:dict={}, processgrp_data:dict={}):
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

    print("Proposal data")
    print(json.dumps(proposal_data, indent=2))

    print("Intent data")
    print(json.dumps(intent_data, indent=2))

    print("Proposed Intent data")
    print(json.dumps(prop_int_data, indent=2))

    print("Satisfaction data")
    print(json.dumps(satisfaction_data, indent=2))
    
    print("Process Groups data")
    print(json.dumps(processgrp_data, indent=2))
    

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

def save_traces(use_case, tot_dpp, trace, be_dpp, event_seq, process_grps:dict={}):
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

    if process_grps != {}:
        file = Path(my_dir, f'{use_case}_proc_grp.json')
        with open(file, "w") as f:
            f.write(json.dumps(process_grps, indent=2))
    
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

