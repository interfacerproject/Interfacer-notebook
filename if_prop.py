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
from datetime import datetime, timezone
from pdb import set_trace

from if_lib import send_signed


from if_consts import SUPPORTED_ACTIONS, IN_PR_ACTIONS, OUT_PR_ACTIONS, IN_OUT_PR_ACTIONS
from if_consts import EVENT_FRAG, AGENT_FRAG, QUANTITY_FRAG, RESOURCE_FRAG, PROPOSAL_FRAG, \
    INTENT_FRAG, PROPINT_FRAG, LOCATION_FRAG, ACTION_FRAG, PROCESS_FRAG, PROCESSSPEC_FRAG, \
        UNIT_FRAG, RESSPEC_FRAG


DEBUG_create_proposal = False
def create_proposal(proposal, user_data, endpoint):
    
    # ts = datetime.now(timezone.utc).isoformat()

    variables = {
        "proposal": {
            "name": proposal['name'],
            "note": proposal['note'],
            "unitBased": proposal['unitBased'],
            "hasBeginning": proposal['hasBeginning'],
            "hasEnd": proposal['hasEnd'],
            "eligibleLocation": proposal['eligibleLocation']
        }
    }
    
    query = """mutation($proposal:ProposalCreateParams!) {
                createProposal(proposal:$proposal) {
                    proposal {
                        ...proposal
                    }
                }
            }""" + PROPOSAL_FRAG + UNIT_FRAG + RESSPEC_FRAG + INTENT_FRAG + PROPINT_FRAG + AGENT_FRAG + LOCATION_FRAG + QUANTITY_FRAG + RESOURCE_FRAG + ACTION_FRAG + PROCESS_FRAG + PROCESSSPEC_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        assert 1 == 2

    if DEBUG_create_proposal:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   


    proposal['id'] = res_json['data']['createProposal']['proposal']['id']

# Wrapper for process creation
def get_proposal(name, proposal_data, note, user_data, hasBeginning, hasEnd, eligibleLocation, unitBased, endpoint):

    if name in proposal_data:
        return

    proposal_data[f'{name}'] = {}

    cur_proposal = proposal_data[f'{name}']

    cur_proposal['name'] = name
    cur_proposal['note'] = note
    cur_proposal['hasBeginning'] = hasBeginning
    cur_proposal['hasEnd'] = hasEnd
    cur_proposal['eligibleLocation'] = eligibleLocation
    cur_proposal['unitBased'] = unitBased
    
    create_proposal(cur_proposal, user_data, endpoint)


DEBUG_show_proposal = False
def show_proposal(user_data, id, endpoint):

    variables = {
        "id": id
    }
    
    query = """query($id:ID!){
      proposal(id:$id){
        ...proposal
      }
    }""" + PROPOSAL_FRAG + PROPINT_FRAG + LOCATION_FRAG + UNIT_FRAG + RESSPEC_FRAG + INTENT_FRAG + RESOURCE_FRAG + \
        QUANTITY_FRAG + AGENT_FRAG + ACTION_FRAG + PROCESS_FRAG + PROCESSSPEC_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        assert 1 == 2

    if DEBUG_show_proposal:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   

    return res_json



DEBUG_create_intent = False
def create_intent(intent, user_data, res_spec_data, endpoint):
    
    # ts = datetime.now(timezone.utc).isoformat()

    variables = {
        "intent": {
            "action": intent['action'],
            "agreedIn": intent['agreedIn'],
            "atLocation": intent['atLocation'],
            "availableQuantity": intent['availableQuantity'],
            "due": intent['due'],
            "effortQuantity": intent['effortQuantity'],
            "finished": intent['finished'],
            "hasBeginning": intent['hasBeginning'],
            "hasEnd": intent['hasEnd'],
            "hasPointInTime": intent['hasPointInTime'],
            "inputOf": intent['inputOf'],
            "name": intent['name'],
            "note": intent['note'],
            "outputOf": intent['outputOf'],
            "provider": intent['provider'],
            "receiver": intent['receiver'],
            "resourceClassifiedAs": intent['resourceClassifiedAs'],
            "resourceConformsTo": intent['resourceConformsTo'],
            "resourceInventoriedAs": intent['resourceInventoriedAs'],
            "resourceQuantity": {
              "hasUnit": [values['defaultUnit'] for key, values in res_spec_data.items() \
                              if values['id'] == intent['resourceConformsTo']][0], 
              "hasNumericalValue": intent['amount'] 
            }
        }
    }
    
    query = """mutation($intent:IntentCreateParams!) {
                createIntent(intent:$intent) {
                    intent {
                        ...intent
                    }
                }
            }""" + UNIT_FRAG + RESSPEC_FRAG + INTENT_FRAG + PROPINT_FRAG + AGENT_FRAG + LOCATION_FRAG + \
                QUANTITY_FRAG + RESOURCE_FRAG + ACTION_FRAG + PROCESS_FRAG + PROCESSSPEC_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        assert 1 == 2

    if DEBUG_create_intent:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   


    intent['id'] = res_json['data']['createIntent']['intent']['id']


def get_intent(name, intent_data, note, user_data, res_spec_data, provider, receiver, action, \
           resourceClassifiedAs, resourceConformsTo, \
           resourceInventoriedAs, amount, agreedIn, \
           atLocation, availableQuantity, effortQuantity, \
           finished, due, hasBeginning, hasEnd, hasPointInTime, \
           inputOf, outputOf, endpoint):


    if name in intent_data:
        return

    intent_data[f'{name}'] = {}

    cur_intent = intent_data[f'{name}']

    cur_intent['name'] = name
    cur_intent['note'] = note
    cur_intent['action'] = action
    cur_intent['agreedIn'] = agreedIn
    cur_intent['amount'] = amount
    cur_intent['finished'] = finished
    cur_intent['due'] = due
    cur_intent['resourceClassifiedAs'] = resourceClassifiedAs
    cur_intent['resourceConformsTo'] = resourceConformsTo
    
    cur_intent['resourceInventoriedAs'] = resourceInventoriedAs
    cur_intent['availableQuantity'] = availableQuantity
    cur_intent['effortQuantity'] = effortQuantity
    

    if provider != None and receiver != None:
        print("At max one of provider and receiver must be specified")
        assert 1==2
    if provider == None and receiver == None:
        print("At least one of provider or receiver must be specified")
        assert 1==2
        
    cur_intent['provider'] = provider
    cur_intent['receiver'] = receiver
    if not ((hasPointInTime != None and not (hasBeginning!= None or hasEnd != None)) or \
        ((hasBeginning!= None and hasEnd != None) and not hasPointInTime != None)):
        print("Specify either hasPointInTime or  hasBeginning anf hasEnd")
        assert 1==2
    cur_intent['hasBeginning'] = hasBeginning
    cur_intent['hasEnd'] = hasEnd
    cur_intent['hasPointInTime'] = hasPointInTime
    
    cur_intent['atLocation'] = atLocation
    cur_intent['inputOf'] = inputOf
    cur_intent['outputOf'] = outputOf

    
    create_intent(cur_intent, user_data, res_spec_data, endpoint)

DEBUG_create_proposedIntent = False
def create_proposedIntent(cur_propint, user_data, endpoint):

    # ts = datetime.now(timezone.utc).isoformat()

    variables = {
        "publishedIn": cur_propint['publishedIn'],
        "publishes": cur_propint['publishes'],
        "reciprocal": cur_propint['reciprocal']
    }
    
    query = """mutation($publishedIn: ID!, $publishes: ID!, $reciprocal: Boolean){
        proposeIntent(publishedIn:$publishedIn, publishes: $publishes, reciprocal:$reciprocal){
            proposedIntent{
                id
                publishedIn {
                    ...proposal
                }
                publishes {
                    ...intent
                }
                reciprocal
            }
        }
    }""" + PROPOSAL_FRAG + UNIT_FRAG + RESSPEC_FRAG + INTENT_FRAG + PROPINT_FRAG + AGENT_FRAG + LOCATION_FRAG + QUANTITY_FRAG + \
        RESOURCE_FRAG + ACTION_FRAG + PROCESS_FRAG + PROCESSSPEC_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        assert 1 == 2

    if DEBUG_create_proposedIntent:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   


    cur_propint['id'] = res_json['data']['proposeIntent']['proposedIntent']['id']


def get_proposedIntent(name, prop_int_data, user_data, publishedIn, publishes,reciprocal, endpoint):
    
    if name in prop_int_data:
        return

    prop_int_data[f'{name}'] = {}

    cur_propint = prop_int_data[f'{name}']

    cur_propint['publishedIn'] = publishedIn
    cur_propint['publishes'] = publishes
    cur_propint['reciprocal'] = reciprocal

    create_proposedIntent(cur_propint, user_data, endpoint)

DEBUG_create_satisfaction = False
def create_satisfaction(cur_sat, user_data, endpoint):

    variables = {
        "satisfaction": {
            "effortQuantity": cur_sat['effortQuantity'],
            "note": cur_sat['note'],
            "resourceQuantity": cur_sat['resourceQuantity'],
            "satisfiedByEvent": cur_sat['satisfiedByEvent'],
            "satisfies": cur_sat['satisfies']
        }
    }
    
    query = """mutation($satisfaction: SatisfactionCreateParams!){
        createSatisfaction(satisfaction:$satisfaction){
            satisfaction{
                id
                effortQuantity {
                    ...quantity
                }
                note
                resourceQuantity{
                    ...quantity
                }
                satisfiedByEvent {
                    ...event
                }
                satisfies {
                    ...intent
                }
            }
        }
    }""" + EVENT_FRAG + UNIT_FRAG + RESSPEC_FRAG + INTENT_FRAG + PROPINT_FRAG + AGENT_FRAG + LOCATION_FRAG + \
        QUANTITY_FRAG + RESOURCE_FRAG + ACTION_FRAG + PROCESS_FRAG + PROCESSSPEC_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        assert 1 == 2

    if DEBUG_create_satisfaction:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   


    cur_sat['id'] = res_json['data']['createSatisfaction']['satisfaction']['id']


def get_satisfaction(name, user_data, event_id, intent_id, note, satisfaction_data, endpoint, effortQuantity:dict={}, amount=0, cur_res:dict={}, res_spec_data:dict={}):
    
    satisfaction_data[f'{name}'] = {}
    cur_sat = satisfaction_data[f'{name}']

    cur_sat["effortQuantity"] = {
            "hasNumericalValue": effortQuantity['amount'],
            "hasUnit": effortQuantity['unit_id'],
        } if effortQuantity != {} else None

    cur_sat["note"] = note
    cur_sat["resourceQuantity"] = {
            "hasNumericalValue": amount,
            "hasUnit": [specs['defaultUnit'] for name, specs in res_spec_data.items() \
               if specs['id'] == cur_res['spec_id']][0],
        } if res_spec_data != {} else None
    
    cur_sat["satisfiedByEvent"] = event_id
    
    cur_sat["satisfies"] = intent_id

    create_satisfaction(cur_sat, user_data, endpoint)



def check_proposals(user_data, proposal_data:dict, endpoint):
    if proposal_data == {}:
        print("No proposal to check")
        return

    for key in proposal_data.keys():
        prop_id = proposal_data[key]['id']
        data = show_proposal(user_data, prop_id, endpoint)
        prop = data['data']['proposal']
        print(f"Proposal {prop['name']} has status {prop['status']}")
        print("Primary intents")
        for intent in prop['primaryIntents']:
            print(f"{intent['name']}")
        

