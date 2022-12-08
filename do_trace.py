# Let's start with some lovely imports that should have been installed if not available by default
import json
import requests
import os
import urllib.parse
from zenroom import zenroom

# What endpoint are we talking to?
# testing
# ENDPOINT = 'http://65.109.11.42:9000/api'
ENDPOINT = 'http://65.109.11.42:10000/api'
IN_PR_ACTIONS = ['accept', 'consume', 'work']
OUT_PR_ACTIONS = ['modify', 'produce']

users_data = {
  "one": {
    "userChallenges": {
      "whereParentsMet": "London",
      "nameFirstPet": "Fuffy",
      "nameFirstTeacher": "Jim",
      "whereHomeTown": "Paris",
      "nameMotherMaid": "Wright"
    },
    "name": "User One",
    "username": "user1_username",
    "email": "user1@example.org",
    "note": "me.user1.org",
    "seedServerSideShard.HMAC": "8w3LSkq59PPWslUc/iQaI6eSqj6ZLpMRZywvaWRSdfA=",
    "seed": "solution garage know special trap wheel timber raven measure miracle achieve horn",
    "eddsa_public_key": "8omSqFVUxnZKwijpfrLroDQkn6qis41WrxXE4CYA4rL9",
    "keyring": {
      "eddsa": "EfBiDDepXrmEn6kafxVMY52hWicKx2b5uM5vESceUDin"
    },
    "id": "0629XVVJV2B9ZPEEG3V73ER2HG"
  },
  "two": {
    "userChallenges": {
      "whereParentsMet": "Amsterdam",
      "nameFirstPet": "Toby",
      "nameFirstTeacher": "Juliet",
      "whereHomeTown": "Rome",
      "nameMotherMaid": "Banks"
    },
    "name": "User Two",
    "username": "user2",
    "email": "user2@example.org",
    "note": "me.user2.org",
    "seedServerSideShard.HMAC": "WiWxQYpeDn4ESAOxxY3Jjg4RKvw0J4iVDzgKmKSoR2s=",
    "seed": "laundry arrest purpose enlist portion tourist zero robot loyal afraid liquid address",
    "eddsa_public_key": "4TZnzSmKkEJdvyCF8gh5ezSEbpstTiRvZuokjoqANyh3",
    "keyring": {
      "eddsa": "6iLUmRcHYQBkqJNgoinctm1gkcSKo3mEBYJ6y17r5A7s"
    },
    "id": "0629XVVKAN9W9PA6W6894X7V74"
  }
}
res_data = {
  "soap_res": {
    "res_ref_id": "soap-626",
    "name": "soap",
    "spec_id": "0629XVVQHHNA1JATPVC4GVZB1C",
    "id": "062AKE8VNDSK7Q0858QWWJ9RVM"
  },
  "water_res": {
    "res_ref_id": "water-1227",
    "name": "water",
    "spec_id": "0629XVVR291FGJ0KP6PATHQ9AR",
    "id": "062AKE8WBHCEJWA61CRSXV3ZZC"
  },
  "cotton_res": {
    "res_ref_id": "cotton-1767",
    "name": "cotton",
    "spec_id": "0629XVVRKH9PNAW9NG6GGT631W",
    "id": "062AKE8X08TNWYEZ47HJ2S1D2G"
  },
  "gown_res": {
    "res_ref_id": "gown-4729",
    "name": "gown",
    "spec_id": "0629XVVS5XKGFQP0KSHV6K4V18",
    "id": "062AKE93SPWNBRYE9E47A9ZGG4",
    "previous_ids": [
      "062AKE90E02WYJX5PR026X5MXM",
      "062AKE9151GXYPRNW3GY6E5EP8"
    ]
  }
}
# staging
# ENDPOINT = 'http://65.109.11.42:8000/api'

# this function is equivalent to JSON.stringify in javascript, i.e. it does not add spaces
# Although it does not seem to matter as Zenroom removes spaces
def stringify(json_obj):
    return json.dumps(json_obj, separators=(',',':'))

import base64
DEBUG_send_signed = False

def send_signed(query, variables, username, eddsa):

    sign_script = """
    Scenario eddsa: sign a graph query
    Given I have a 'base64' named 'gql'
    Given I have a 'keyring'
    # Fix Apollo's mingling with query string
    When I remove spaces in 'gql'
    and I compact ascii strings in 'gql'
    When I create the eddsa signature of 'gql'
    And I create the hash of 'gql'
    Then print 'eddsa signature' as 'base64'
    Then print 'gql' as 'base64'
    Then print 'hash' as 'hex'
    """
    
#     body = f'{{"query": "{query}", "variables": {stringify(variables)}}}'
    

#     print("Body")
#     print(body)


#     encoded_body = base64.b64encode(body.encode('utf8')).decode('ascii')

#     zenData = f"""
#     {{
#         "gql": "{encoded_body}"
#     }}"""

    zenKeys = stringify({
        "keyring": {
            "eddsa": eddsa
        }
    })

    payload = {"query": query, "variables": variables}

    zenData = {
        "gql": base64.b64encode(bytes(json.dumps(payload), 'utf-8')).decode('utf-8')
    }

    zenData_str = stringify(zenData)
    
    try:
        result = zenroom.zencode_exec(sign_script, keys=zenKeys, data=zenData_str)
    except Exception as e:
        print(f'Exception in zenroom call: {e}')
        return None

    res_json = json.loads(result.output)

    # Reset the headears
    headers = {}
    headers['content-type'] = 'application/json'

    headers['zenflows-sign'] = res_json['eddsa_signature']   
    headers['zenflows-user'] = username
    headers['zenflows-hash'] = res_json['hash']
    
    r = requests.post(ENDPOINT, json=payload, headers=headers)

    res = r.json()

    if DEBUG_send_signed:
        print("Payload")
        print(payload)

        print("zenData")
        print(zenData)

        print("Zenroom result")
        print(result)

        print("Generated signature")
        print(json.dumps(res_json, indent=2))

        print("Headers")
        print(headers)

        print("Response")
        print(json.dumps(res, indent=2))
    
    return res

VERBOSE = False
def fill_loc(a_dpp, item):
    a_dpp['location'] = {}
    a_dpp['location']['id'] = item['id']
    a_dpp['location']['name'] = item['name']
    a_dpp['location']['alt'] = item['alt']
    a_dpp['location']['lat'] = item['lat']
    a_dpp['location']['long'] = item['long']                    
    a_dpp['location']['mappableAddress'] = item['mappableAddress']                    
    a_dpp['location']['note'] = item['note']                                    
    
    
def fill_event(a_dpp, item):
    if not 'action' in item:
        breakpoint()
    a_dpp['name'] = item['action']['id']
    if VERBOSE:
        a_dpp['label'] = item['action']['label']
        if item['atLocation'] != None:
            fill_loc(a_dpp, item['atLocation'])

def fill_res(a_dpp, item):
    a_dpp['note'] = item['note']
    a_dpp['trackingIdentifier'] = item['trackingIdentifier']
    if VERBOSE:
        a_dpp['metadata'] = item['metadata']
        if item['currentLocation'] != None:
            fill_loc(a_dpp, item['currentLocation'])

def fill_process(a_dpp, item):
    a_dpp['note'] = item['note']

MAX_DEPTH = 500000


DEBUG_er_before = True

def er_before(id, user_data, dpp, depth):

    if depth > MAX_DEPTH:
        return
    depth += 1

    variables = {
        "id": id
    }
    
    query = """query($id:ID!) {
      economicResource(id:$id) {
          previous{
            __typename
            ... on EconomicEvent {
                id
                action {
                    id
                    label
                }
                atLocation {...location}
            }
        }
      }
    }
    fragment location on SpatialThing {
        id
        alt
        lat
        long
        mappableAddress
        name
        note
    }
    """

    res = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'])
    
    if DEBUG_er_before:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(res)   

    events = res['data']['economicResource']['previous']
    if events != []:
#         for i, event in enumerate(events):
#             dpp[f'{i}'] = {}
#             a_dpp = dpp[f'{i}']
#             a_dpp['type'] = event['__typename']
#             a_dpp['id'] = event['id']
#             a_dpp['children'] = {}
#             # This must be of type EconomicEvent since the call only returns that             
#             if event['__typename'] == "EconomicEvent":
#                 fill_event(a_dpp, event)
#                 ee_before(event['id'], user_data, a_dpp['children'], depth)         
        # breakpoint()
        event = events.pop()
        # This must be of type EconomicEvent since the call only returns that             
        event['__typename'] == "EconomicEvent"
        while event['id'] in visited:
            breakpoint()
            if events == []:
                return
            event = events.pop()
        visited.append(event['id'])
        a_dpp = {}
        dpp.append(a_dpp)
        a_dpp['type'] = event['__typename']
        a_dpp['id'] = event['id']
        a_dpp['children'] = []
        
        fill_event(a_dpp, event)
        ee_before(event['id'], user_data, a_dpp['children'], depth)         

DEBUG_ee_before = True

def ee_before(id, user_data, dpp, depth):

    if depth > MAX_DEPTH:
        return
    depth += 1

    variables = {
        "id": id
    }
    
    query = """query($id:ID!) {
      economicEvent(id:$id) {
          previous{
            __typename
            ... on  EconomicResource {
                id
                name
                note
                trackingIdentifier
                metadata
                currentLocation {...location}
            }
            ... on EconomicEvent {
                id
                action {
                    id
                    label
                }
                atLocation {...location}
            }
            ... on Process {
                id
                name
                note
          }
        }
      }
    }
    fragment location on SpatialThing {
        id
        alt
        lat
        long
        mappableAddress
        name
        note
    }
    """

    res = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'])
    
    if DEBUG_ee_before:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(res)   

    pf_items = res['data']['economicEvent']['previous']
    if DEBUG_ee_before:
        print("pf_items")
        print(pf_items)
    # breakpoint()
    if type(pf_items) is dict:
        pf_items = [pf_items]
    if pf_items == None:
        return
    if pf_items != []:
        # breakpoint()
        pf_item = pf_items[-1]
        if pf_item['id'] in visited:
            breakpoint()
            return
        a_dpp = {}
        dpp.append(a_dpp)
        a_dpp['type'] = pf_item['__typename']
        a_dpp['id'] = pf_item['id']
        a_dpp['children'] = []

        if pf_item['__typename'] == "EconomicEvent":
            visited.append(pf_item['id'])
            fill_event(a_dpp, pf_item)
            ee_before(pf_item['id'], user_data, a_dpp['children'], depth)
        if pf_item['__typename'] == "EconomicResource":
            fill_res(a_dpp, pf_item)
            er_before(pf_item['id'], user_data, a_dpp['children'], depth)
        if pf_item['__typename'] == "Process":
            visited.append(pf_item['id'])
            fill_process(a_dpp, pf_item)
            pr_before(pf_item['id'], user_data, a_dpp['children'], depth)

DEBUG_pr_before = True

def pr_before(id, user_data, dpp, depth):

    if depth > MAX_DEPTH:
        return
    depth += 1

    variables = {
        "id": id
    }
    
    query = """query($id:ID!) {
      process(id:$id) {
          previous{
            __typename
            ... on EconomicEvent {
                id
                action {
                    id
                    label
                }
                atLocation {...location}
            }
        }
      }
    }
    fragment location on SpatialThing {
        id
        alt
        lat
        long
        mappableAddress
        name
        note
    }
    """

    res = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'])
    
    if DEBUG_pr_before:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(res)   

    events = res['data']['process']['previous']
    # breakpoint()
    if events != []:
        for i, event in enumerate(events):
            # This must be of type since the call only returns that
            assert event['__typename'] == "EconomicEvent"
            if event['id'] in visited:
                breakpoint()
                continue
            visited.append(event['id'])
            a_dpp = {}
            dpp.append(a_dpp)
            a_dpp['type'] = event['__typename']
            a_dpp['id'] = event['id']
            a_dpp['children'] = []
            # This must be of type since the call only returns that             
            fill_event(a_dpp, event)
            ee_before(event['id'], user_data, a_dpp['children'], depth)
#             can only be EconomicEvent
#             if event['__typename'] == "EconomicResource":
#                 fill_res(a_dpp, event)
#                 er_before(id, user_data, a_dpp['children'])
#             if event['__typename'] == "Process":
#                 fill_process(a_dpp, event)
#                 pr_before(id, user_data, a_dpp['children'])

print(f"Resource to be traced: {res_data['gown_res']['id']}")
tot_dpp = {
    "id": res_data['gown_res']['id'],
    "name" : res_data['gown_res']['name'],
    "children": []
}
visited = []
er_before(res_data['gown_res']['id'], users_data['one'], dpp=tot_dpp['children'], depth=0)
print(json.dumps(tot_dpp, indent=2))
print(visited)