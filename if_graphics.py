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

import plotly.graph_objects as go
from pdb import set_trace

def make_sankey(srcs, trgs, lbls, vls, clr_nodes, clr_links):
    # data to dict, dict to sankey
    link = dict(source = srcs, target = trgs, value = vls, color=clr_links)
    node = dict(label = lbls, pad=10, thickness=5, color=clr_nodes)
    data = go.Sankey(link = link, node=node)
    # plot
    fig = go.Figure(data)
    fig.show()

dict_node_colors = {'EconomicResource': '#e41a1c', 'EconomicEvent': '#377eb8', 'Process': '#4daf4a', 'Transfer': '#984ea3'}
dict_link_colors = {'EconomicResource': '#fb6a4a', 'EconomicEvent': '#92c5de', 'Process': '#99d8c9', 'Transfer': '#bcbddc'}

# def calc_quantity(dpp_item):
    
#     if 'onhandQuantity' in dpp_item:
#         quantity = dpp_item['onhandQuantity']
#     elif 'effortQuantity' in dpp_item:
#         quantity = dpp_item['effortQuantity']
#     elif 'resourceQuantity' in dpp_item:
#         quantity = dpp_item['resourceQuantity']
#     elif 'accounting_quantity_has_numerical_value' in dpp_item:
#         quantity = dpp_item['accounting_quantity_has_numerical_value']
#     elif 'onhand_quantity_has_numerical_value' in dpp_item:
#         quantity = dpp_item['onhand_quantity_has_numerical_value']
#     elif 'resource_quantity_has_numerical_value' in dpp_item:
#         quantity = dpp_item['resource_quantity_has_numerical_value']
#     elif 'effort_quantity_has_numerical_value' in dpp_item:
#         quantity = dpp_item['effort_quantity_has_numerical_value']
#     else:
#         # breakpoint()
#         quantity = '1 '

#     quantity = int(quantity.split(' ')[0])
#     quantity = max(quantity,1)
#     return quantity
    

def calc_quantity(dpp_item):
    quantity = .1
    if dpp_item['type'] == "Process":
        # quantity = 0
        # for child in dpp_item['children']:
        #     quantity = max(quantity,calc_quantity(child))
        quantity = .1
    elif dpp_item['type'] == "EconomicEvent":
        if 'resourceQuantity' in dpp_item and dpp_item['resourceQuantity'] != None:
            quantity = float(dpp_item['resourceQuantity']['hasNumericalValue'])
        elif 'effortQuantity' in dpp_item and dpp_item['effortQuantity'] != None:
            quantity = float(dpp_item['effortQuantity']['hasNumericalValue'])
            # quantity = dpp_item['effortQuantity']
        else:
            print("No quantity specified for EconomicEvent")
    elif dpp_item['type'] == "EconomicResource":
        if 'onhandQuantity' in dpp_item and dpp_item['onhandQuantity'] != None:
            quantity = float(dpp_item['onhandQuantity']['hasNumericalValue'])
        elif 'accountingQuantity' in dpp_item and dpp_item['accountingQuantity'] != None:
            quantity = float(dpp_item['accountingQuantity']['hasNumericalValue'])
        else:
            print("No quantity specified for EconomicResource")
    else:
        print(f"Unkwnon type {dpp_item['type']}")
        assert 1 == 2
    
    quantity = max(quantity,0.1)
    return quantity
    
def vis_dpp(dpp_item, count, assigned, labels, targets, sources, values, color_nodes, color_links):
    name = dpp_item['name']
#     print(f"vis name: {name}, count: {count}")
    if dpp_item['type'] != "EconomicResource":
        if dpp_item['id'] in assigned:
            assigned[dpp_item['id']].append(count)
        else:
            assigned[dpp_item['id']] = [count]
    quantity = calc_quantity(dpp_item)
    labels.append(name)
    el_type = 'Transfer' if dpp_item['type'] == 'EconomicEvent' and 'transfer' in dpp_item['name'].lower() else dpp_item['type']
    color_nodes.append(dict_node_colors[el_type])
    nr_ch = len(dpp_item['children'])
    new_count = count + 1
    for ch in range(nr_ch):
        targets.append(count)
        sources.append(new_count)
        ch_dpp = dpp_item['children'][ch]
        el_type = 'Transfer' if ch_dpp['type'] == 'EconomicEvent' and 'transfer' in ch_dpp['name'].lower() else ch_dpp['type']
        color_links.append(dict_link_colors[el_type])
        if quantity == 0:
            breakpoint()
        values.append(quantity)
#         values.append(1)
        new_count = vis_dpp(ch_dpp, new_count, assigned=assigned, labels=labels, targets=targets, sources=sources, values=values, color_nodes=color_nodes, color_links=color_links)
    return new_count

def consol_trace(assigned, sources, targets):
    for key in assigned.keys():
        if len(assigned[key]) > 1:
            # print(key)
            vl0 = assigned[key][0]
            for vl_idx in range(1,len(assigned[key])):
                vl = assigned[key][vl_idx]
                sources = [i if i != vl else vl0 for i in sources]
                targets = [i if i != vl else vl0 for i in targets]
    return sources, targets
