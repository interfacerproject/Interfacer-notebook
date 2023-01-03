import plotly.graph_objects as go

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

def calc_quantity(dpp_item):
    if 'onhandQuantity' in dpp_item:
        quantity = dpp_item['onhandQuantity']
    elif 'effortQuantity' in dpp_item:
        quantity = dpp_item['effortQuantity']
    else:
        quantity = '1 '
    quantity = int(quantity.split(' ')[0])
    quantity = max(quantity,1)
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
