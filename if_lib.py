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
import inspect
import requests
import os
import contextlib
from zenroom import zenroom
import base64
from datetime import datetime, timezone
import random
from pdb import set_trace


from if_consts import SUPPORTED_ACTIONS, IN_PR_ACTIONS, OUT_PR_ACTIONS, IN_OUT_PR_ACTIONS
from if_consts import EVENT_FRAG, AGENT_FRAG, QUANTITY_FRAG, RESOURCE_FRAG, PROPOSAL_FRAG, \
    INTENT_FRAG, PROPINT_FRAG, LOCATION_FRAG, ACTION_FRAG, PROCESS_FRAG, PROCESSGRP_FRAG, PROCESSSPEC_FRAG, \
        UNIT_FRAG, RESSPEC_FRAG

from if_utils import stringify

def zenroom_wrapper(contract, keys=None, data=None):
    with open(os.devnull, 'w') as f:
        with contextlib.redirect_stderr(f):
            # set_trace()
            return zenroom.zencode_exec(contract, keys=keys, data=data)


# Test zenroom is correctly installed and running
def generate_random_challenge():
    """
        This function calls zenroom to generate
        a random string to be used as challenge
    """
    contract = """
        rule check version 1.0.0
        Given nothing
        When I create the random object of '512' bits
        and I rename the 'random_object' to 'challenge'
        Then print 'challenge'
    """

    try:
        resz = zenroom.zencode_exec(contract)
    except Exception as e:
        print(f'Exception in zenroom call: {e}')
        return None

    resz_json = json.loads(resz.output)

    print(f"Generated challenge: {resz_json['challenge']}")

    return
# we will save endpoint specific files since the data is saved on a particular endpoint

# Get the seed from the server to later generate the keypair
DEBUG_get_HMAC = False
def get_HMAC(email, endpoint, newUser=True):

    variables = {
        "firstRegistration": newUser,
        "userData": "{\"email\": \"" + email + "\"}"
    };

    
    payload = {
      "query": """mutation ($firstRegistration: Boolean!, $userData: JSONObject!){
  
        keypairoomServer(firstRegistration: $firstRegistration, userData: $userData)
      
      }""",
      "variables": variables
    }
    

    res = requests.post(endpoint, json=payload)
    if DEBUG_get_HMAC:
        print("Payload")
        print(payload)
        print("Variables")
        print(variables)
        print("Result")
        print(res)

    try:
        res_json = res.json()
    except Exception as e:
        print("Payload")
        print(payload)
        print("Variables")
        print(variables)
        print("Result")
        print(res)
        raise Exception(f"Exception {e} in function {inspect.stack()[0][3]}")
    
    if DEBUG_get_HMAC:
        print("JSON")
        print(json.dumps(res_json, indent=2))

    has_errors = False
    if "errors" in res_json and len(res_json['errors']) > 0:
        for err in res_json['errors']:
            if err['message'] == "email exists":
                return get_HMAC(email, endpoint, newUser=False)
            else:
                has_errors = True

    if has_errors:
        print("Payload")
        print(payload)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))
        raise Exception(f"Error in function {inspect.stack()[0][3]}")


    return res_json


# if the HMAC is not in the conf files call the function to get it
def read_HMAC(file, users_data, user, endpoint):
    
    # this should not be possible since we initialize the data, but anyway
    if not f'{user}' in users_data:
        users_data[f'{user}'] = {}
        print("Warning this should not happen")

    user_data = users_data[f'{user}']

    # check we already have a credentials file with a HMAC
    if 'seedServerSideShard.HMAC' in user_data:
        print(f"Server HMAC available for {user_data['name']}")
        return
    if os.path.isfile(file):
        with open(file,'r') as f:
                tmp_users_data = json.loads(f.read())
                tmp_user_data = tmp_users_data[f'{user}'] 
                

    else:
        tmp_user_data = {}
        
    if 'seedServerSideShard.HMAC' not in tmp_user_data:
        res_json = get_HMAC(user_data['email'], endpoint)

        # save the HMAC in the user data
        user_data['seedServerSideShard.HMAC'] = res_json['data']['keypairoomServer']

        # save data with HMAC
        with open(file,'w') as f:
            # Save the entire data structure
            json.dump(users_data, f)
    else:
        user_data['seedServerSideShard.HMAC'] = tmp_user_data['seedServerSideShard.HMAC']
        # no need to save since we read it from file
    

DEBUG_generate_keypair = False
# Generate the user keypair (and the mnemonic seed)
def generate_keypair(userdata: dict) -> dict:
    """
        This function calls zenroom to generate
        a keypair using the server-provided HMAC
    """
    contract = """
        Scenario 'ecdh': Create the key
        Scenario 'ethereum': Create key
        Scenario 'reflow': Create the key
        Scenario 'schnorr': Create the key
        Scenario 'eddsa': Create the key
        Scenario 'qp': Create the key


        # Loading the user name from data
        Given my name is in a 'string' named 'username'

        # Loading the answers from 3 secret questions. The user will have to pick the 3 challenges from a list 
        # and have to remember the questions - the order is not important cause Zenroom will sort alphabetically 
        # the data in input
        #
        # NOTE: the challenges will never be communicated to the server or to anybody else!
        Given I have a 'string dictionary' named 'userChallenges'

        # Loading the individual challenges, in order to have them hashed 
        # and the hashes OPTIONALLY stored by the server, to improve regeneration of the keypair
        Given I have a 'string' named 'whereParentsMet' in 'userChallenges'
        Given I have a 'string' named 'nameFirstPet' in 'userChallenges'
        Given I have a 'string' named 'whereHomeTown' in 'userChallenges'
        Given I have a 'string' named 'nameFirstTeacher' in 'userChallenges'
        Given I have a 'string' named 'nameMotherMaid' in 'userChallenges'

        # Loading the pbkdf received from the server, containing a signed hash of known data
        Given that I have a 'base64' named 'seedServerSideShard.HMAC' 

        # Save the backup for mnemonic dump, before factoring with the salt
        # it is shortened to 16 bytes by hashing sha512 the KDF and taking the first 16 bytes
        When I create the key derivation of 'userChallenges'
        and I create the hash of 'key derivation' using 'sha512'
        and I split the leftmost '16' bytes of 'hash'
        and I delete the 'key derivation'
        and I delete the 'hash'
        and I rename the 'leftmost' to 'seed'

        # Hash again the user's challenges with salt for the seed root
        When I rename 'seedServerSideShard.HMAC' to 'salt'
        and I create the key derivation of 'seed' with password 'salt'
        and I rename the 'key derivation' to 'seed.root'

        # In the following flow the order should NOT be changed

        When I create the hash of 'seed.root'
        When I rename the 'hash' to 'seed.ecdh'

        When I create the hash of 'seed.ecdh'
        When I rename the 'hash' to 'seed.eddsa'

        When I create the hash of 'seed.eddsa'
        When I rename the 'hash' to 'seed.ethereum'

        When I create the hash of 'seed.ethereum'
        When I rename the 'hash' to 'seed.reflow'

        When I create the hash of 'seed.reflow'
        When I rename the 'hash' to 'seed.schnorr'

        # end of the sorted creation flow

        When I create the ecdh key with secret key 'seed.ecdh'
        When I create the eddsa key with secret key 'seed.eddsa'
        When I create the ethereum key with secret key 'seed.ethereum'
        When I create the reflow key with secret key 'seed.reflow'
        When I create the schnorr key with secret key 'seed.schnorr'

        When I create the ecdh public key
        When I create the eddsa public key
        When I create the ethereum address
        When I create the reflow public key
        When I create the schnorr public key

        # Creating the hashes of the single challenges, to OPTIONALLY help 
        # regeneration of the keypair

        When I create the 'base64 dictionary'
        and I rename the 'base64 dictionary' to 'hashedAnswers'

        When I create the key derivation of 'whereParentsMet'
        and I rename the 'key derivation' to 'whereParentsMet.kdf'
        When I insert 'whereParentsMet.kdf' in 'hashedAnswers'

        When I create the key derivation of 'nameFirstPet'
        and I rename the 'key derivation' to 'nameFirstPet.kdf'
        When I insert 'nameFirstPet.kdf' in 'hashedAnswers'

        When I create the key derivation of 'whereHomeTown'
        and I rename the 'key derivation' to 'whereHomeTown.kdf'
        When I insert 'whereHomeTown.kdf' in 'hashedAnswers'

        When I create the key derivation of 'nameFirstTeacher'
        and I rename the 'key derivation' to 'nameFirstTeacher.kdf'
        When I insert 'nameFirstTeacher.kdf' in 'hashedAnswers'

        When I create the key derivation of 'nameMotherMaid'
        and I rename the 'key derivation' to 'nameMotherMaid.kdf'
        When I insert 'nameMotherMaid.kdf' in 'hashedAnswers'


        # This prints the keyring
        Then print the 'keyring' 

        # this prints the hashes of the challenges
        # Then print the 'hashedAnswers'

        # This prints the seed for the private keys as mnemonic 
        Then print the 'seed' as 'mnemonic'

        Then print the 'ecdh public key'
        Then print the 'eddsa public key'
        Then print the 'ethereum address'
        Then print the 'reflow public key'
        Then print the 'schnorr public key'
    """
    
    data = json.dumps(userdata)

    try:
        resz = zenroom.zencode_exec(contract, data=data)
    except Exception as e:
        print(f'Exception in zenroom call: {e}')
        raise Exception(f"Error in function {inspect.stack()[0][3]}")
        return {}

    if DEBUG_generate_keypair:
        print(f'result: {resz}')

    resz_json = json.loads(resz.output)

    if DEBUG_generate_keypair:
        print(f"Generated keypair data: {json.dumps(resz_json, indent=2)}")

    return resz_json

# Read the keypair from conf files or call the function to generate it
def read_keypair(file, users_data, user):
    
    # this should not be possible since we initialize the data, but anyway
    if not f'{user}' in users_data:
        users_data[f'{user}'] = {}
        print("Warning this should not happen")
        
    user_data = users_data[f'{user}']
    
    if ('seed' in user_data and 'eddsa_public_key' in user_data and \
            'keyring' in user_data and 'eddsa' in user_data['keyring']):
        print(f"Keypair available for {user_data['name']}")
        return
        
    if os.path.isfile(file):
        with open(file,'r') as f:
                tmp_users_data = json.loads(f.read())
                tmp_user_data = tmp_users_data[f'{user}'] 
    else:
        tmp_user_data = {}

    if not ('seed' in tmp_user_data and 'eddsa_public_key' in tmp_user_data and \
            'keyring' in tmp_user_data and 'eddsa' in tmp_user_data['keyring']):

        res_json = generate_keypair(user_data)
        # Update data in user data
        user_data['seed'] = res_json['seed']
        user_data['eddsa_public_key'] = res_json['eddsa_public_key']
        user_data['keyring'] = {}
        user_data['keyring']['eddsa'] = res_json['keyring']['eddsa']

        with open(file,'w') as f:
            # save the entire data structure, not just one user
            json.dump(users_data, f)
    else:
        print(f"Keypair available from file for {user_data['name']}")
        user_data['seed'] = tmp_user_data['seed']
        user_data['eddsa_public_key'] = tmp_user_data['eddsa_public_key']
        user_data['keyring'] = {}
        user_data['keyring']['eddsa'] = tmp_user_data['keyring']['eddsa']



# Create the person using their public key
DEBUG_create_Person = False
def create_Person(name, username, email, eddsaPublicKey, endpoint, newPerson=True):

    if newPerson:
        variables = {
        "person": {
            "name": name,
            "user": username,
            "email": email,
            "eddsaPublicKey": eddsaPublicKey
            }
        }

        payload = {
          "query": """mutation ($person: PersonCreateParams!){
            createPerson(person: $person)
            {
                agent{
                    ...agent
                }
            }
           }""" + AGENT_FRAG + LOCATION_FRAG,
          "variables": json.dumps(variables)
        }
    else:
        variables = {
          "email": email,
          "eddsaPublicKey": eddsaPublicKey
        }

        payload = {
          "query": """query ($email:String!, $eddsaPublicKey: String!){
              personCheck(email:$email, eddsaPublicKey:$eddsaPublicKey){
                id
              }
        }""",
          "variables": json.dumps(variables)
        }
        
#     print(json.dumps(payload, indent=2))

    # Temporarily: we need a key to create a person, before email authentication is implemented
    if 'IF_KEY' in os.environ:
        SECRET_KEY = os.environ['IF_KEY']
    else:
        file = '.credentials.json'
        assert os.path.isfile(file)

        with open(file) as f:
            data = json.load(f)
            SECRET_KEY = data['key']
        
    headers={'zenflows-admin': SECRET_KEY}
    res = requests.post(endpoint, json=payload, headers=headers)
    
    if DEBUG_create_Person:
        print("Payload")
        print(payload)

        print("Headers")
        print(headers)

        print("Response")
        print(res)

    try:
        res_json = res.json()
    except Exception as e:
        print("Payload")
        print(payload)
        print("Headers")
        print(headers)
        print("Result")
        print(res)
        raise Exception(f"Exception {e} in function {inspect.stack()[0][3]}")


    if DEBUG_create_Person:
        print("Result")
        print(json.dumps(res_json, indent=2))

    
    if "errors" in res_json and len(res_json['errors']) > 0:
        for err in res_json['errors']:
            if err['message'] == "user: [\"has already been taken\"]":
                return create_Person(name, username, email, eddsaPublicKey, endpoint, newPerson=False)

    if newPerson:
        user_id = res_json['data']['createPerson']['agent']['id']
    else:
        user_id = res_json['data']['personCheck']['id']
    
    return user_id


# Read the ID of the person from file or create a new person
def get_id_person(file, users_data, user, endpoint):
    user_data = users_data[f'{user}']
    
    if 'id' in user_data:
        print(f"Id available for {user_data['name']}")
        return
    
    if os.path.isfile(file):
        with open(file,'r') as f:
                tmp_users_data = json.loads(f.read())
                tmp_user_data = tmp_users_data[f'{user}']
    else:
        tmp_user_data = {}

    if not 'id' in tmp_user_data:
        user_data['id'] = create_Person(user_data['name'], user_data['username'], user_data['email'], user_data['eddsa_public_key'], endpoint)
#         print(json.dumps(user_data, indent=2))
        with open(file,'w') as f:
            json.dump(users_data, f)
    else:
        print(f"Id available from file for {user_data['name']}")
        user_data['id'] = tmp_user_data['id']
    
# sign and send each request now that we have a registered public key
DEBUG_send_signed = False

def send_signed(query: str, variables: dict, username: str, eddsa: str, endpoint:str) -> dict:

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
        resz = zenroom.zencode_exec(sign_script, keys=zenKeys, data=zenData_str)
    except Exception as e:
        print(f'Exception in zenroom call: {e}')
        return {}

    if DEBUG_send_signed:
        print("zenData")
        print(zenData)

        print("Zenroom result")
        print(resz)

    resz_json = json.loads(resz.output)

    if DEBUG_send_signed:
        print("Generated signature")
        print(json.dumps(resz_json, indent=2))

    # Reset the headears
    headers = {}
    headers['content-type'] = 'application/json'

    headers['zenflows-sign'] = resz_json['eddsa_signature']   
    headers['zenflows-user'] = username
    headers['zenflows-hash'] = resz_json['hash']
    
    res = requests.post(endpoint, json=payload, headers=headers)

    try:
        res_json = res.json()
    except Exception as e:
        print("Payload")
        print(payload)
        print("Headers")
        print(headers)
        print("Result")
        print(res)
        raise Exception(f"Exception {e} in function {inspect.stack()[0][3]}")


    if DEBUG_send_signed:
        print("Payload")
        print(payload)

        print("Headers")
        print(headers)

        print("Response")
        print(json.dumps(res_json, indent=2))
    
    return res_json


# Read the location id from file or generate it by calling the back-end
DEBUG_get_location_id = False
def get_location_id(file, user_data, locs_data, user, endpoint):

    # this should not be possible since we initialize the data, but anyway
    if not f'{user}' in locs_data:
        locs_data[f'{user}'] = {}
        print("Warning this should not happen")

    loc_data = locs_data[f'{user}']

    if 'id' in loc_data:
        print(f"Location id available for {loc_data['name']}")
        return

    # check we already have a location file with an id
    if os.path.isfile(file):
        with open(file,'r') as f:
                temp_locs_data = json.loads(f.read())
                temp_loc_data = temp_locs_data[f'{user}']
                
    else:
        temp_loc_data = {}


    if 'id' not in temp_loc_data:
        # Register location
        # Produce the query and variables vars to be signed
        variables = {
            "location": {
                "name": loc_data['name'],
                "alt": 0,
                "lat": loc_data['lat'],
                "long": loc_data['long'],
                "mappableAddress": loc_data['addr'],
                "note": loc_data['note']
            }
        }

        query = """mutation($location: SpatialThingCreateParams!) {
                createSpatialThing(spatialThing: $location) {
                    spatialThing {
                        id
                    }
                }
            }"""

        res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

        if 'errors' in res_json:
            print("Error message")
            print(json.dumps(res_json['errors'], indent=2))
            print("Query")
            print(query)
            print("Variables")
            print(variables)
            raise Exception(f"Error in function {inspect.stack()[0][3]}")

        if DEBUG_get_location_id:
            print("Query")
            print(query)

            print("Variables")
            print(variables)

            print("Response")
            print(json.dumps(res_json, indent=2))

        # save the id in the location data
        loc_data['id'] = res_json['data']['createSpatialThing']['spatialThing']['id']
        # reference the location in the user data
        loc_data['user_id'] = user_data['id']

        # save data with id
        with open(file,'w') as f:
            # Save the entire location data, not just the user one
            json.dump(locs_data, f)
    else:
        print(f"Location id available in file for {loc_data['name']}")
        loc_data['id'] = temp_loc_data['id']

# Read the location id from file or generate it by calling the back-end
DEBUG_set_user_location = False
def set_user_location(file, users_data, locs_data, user, endpoint):

    user_data = users_data[user]

    if 'location_id' in user_data:
        print(f"Location id available for {user_data['name']}")
        return

    loc_data = locs_data[f'{user}']

    variables = {
        "person": {
            "id":  user_data['id'],
            "primaryLocation": loc_data['id']
        }
    }

    query = """mutation($person: PersonUpdateParams!) {
            updatePerson(person: $person) {
                agent {
                    ...agent
                    primaryLocation {
                        id
                    }
                }
            }
        }""" + AGENT_FRAG + LOCATION_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        raise Exception(f"Error in function {inspect.stack()[0][3]}")

    if DEBUG_set_user_location:
        print("Query")
        print(query)

        print("Variables")
        print(variables)

        print("Response")
        print(json.dumps(res_json, indent=2))

    # save the id in the location data
    user_data['location_id'] = res_json['data']['updatePerson']['agent']['primaryLocation']['id']

    # save data with location id (for each user, redudant)
    with open(file,'w') as f:
        # Save the entire location data, not just the user one
        json.dump(users_data, f)


# Read the unit id from file or generate it by calling the back-end
def get_unit_id(file, user_data, units_data, name, label, symbol, endpoint):
    
    if name in units_data and 'id' in units_data[f'{name}']:
        print(f"Unit {name} available")
        return

    # check we already have a unit file with an id
    if os.path.isfile(file):
        with open(file,'r') as f:
                temp_units_data = json.loads(f.read())
    else:
        temp_units_data = {}

    if not (name in temp_units_data and 'id' in temp_units_data[f'{name}']):

        # Produce the query and variables vars to be signed
        variables = {
                    "unit": {
                            "label": label,
                            "symbol": symbol
                            }
                }


        query = """mutation($unit:UnitCreateParams!) {
                createUnit(unit: $unit) {
                    unit {
                        id
                    }
                }
              }"""

        res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

        if 'errors' in res_json:
            print("Error message")
            print(json.dumps(res_json['errors'], indent=2))
            print("Query")
            print(query)
            print("Variables")
            print(variables)
            raise Exception(f"Error in function {inspect.stack()[0][3]}")

        # save the unit info
        units_data[f'{name}'] = {}
        units_data[f'{name}']['label'] = label
        units_data[f'{name}']['symbol'] = symbol
        units_data[f'{name}']['id'] = res_json['data']['createUnit']['unit']['id']

        # save data with id
        with open(file,'w') as f:
            json.dump(units_data, f)
    else:
        print(f"Unit available in file for {temp_units_data[f'{name}']}")
        units_data[f'{name}'] = {}
        units_data[f'{name}']['label'] = temp_units_data[f'{name}']['label']
        units_data[f'{name}']['symbol'] = temp_units_data[f'{name}']['symbol']
        units_data[f'{name}']['id'] = temp_units_data[f'{name}']['id']
        


# Read the resource specification id or create a new one if not available
def get_resource_spec_id(file, user_data, res_spec_data, name, note, classification, default_unit_id, endpoint):

    if name in res_spec_data and 'id' in res_spec_data[f'{name}']:
        print(f"Specification {name} available")
        return

    # check we already have a unit file with an id
    if os.path.isfile(file):
        with open(file,'r') as f:
                temp_res_spec_data = json.loads(f.read())
    else:
        temp_res_spec_data = {}

    if not (name in temp_res_spec_data and 'id' in temp_res_spec_data[f'{name}']):

        # Produce the query and variables vars to be signed
        variables = {
            "resourceSpecification": {
                "defaultUnitOfResource": default_unit_id,
                "name": name,
                "note": note,
                "resourceClassifiedAs": classification
            }
        }


        query = """mutation ($resourceSpecification:ResourceSpecificationCreateParams!){
                    createResourceSpecification(resourceSpecification:$resourceSpecification){
                        resourceSpecification{
                            id,
                            name
                        }
                    }
                }"""

        res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

        if 'errors' in res_json:
            print("Error message")
            print(json.dumps(res_json['errors'], indent=2))
            print("Query")
            print(query)
            print("Variables")
            print(variables)
            raise Exception(f"Error in function {inspect.stack()[0][3]}")


        # save the unit info
        res_spec_data[f'{name}'] = {}
        res_spec_data[f'{name}']['note'] = note
        res_spec_data[f'{name}']['classification'] = classification
        res_spec_data[f'{name}']['defaultUnit'] = default_unit_id
        res_spec_data[f'{name}']['id'] = res_json['data']['createResourceSpecification']['resourceSpecification']['id']

        # save data with id
        with open(file,'w') as f:
            json.dump(res_spec_data, f)
    else:
        print(f"Specification available in file for {temp_res_spec_data[f'{name}']}")
        res_spec_data[f'{name}'] = {}
        res_spec_data[f'{name}']['note'] = temp_res_spec_data[f'{name}']['note']
        res_spec_data[f'{name}']['classification'] = temp_res_spec_data[f'{name}']['classification']
        res_spec_data[f'{name}']['defaultUnit'] = temp_res_spec_data[f'{name}']['defaultUnit']
        res_spec_data[f'{name}']['id'] = temp_res_spec_data[f'{name}']['id']
        


# Create the resource by calling the back-end
DEBUG_create_resource = False
def create_resource(user_data, res_data, res_spec_data, amount, endpoint):
    
    provider = user_data['id']
    receiver = user_data['id']
    # Get the unit from the spec, no need to pass it     
    unit_id = [specs['defaultUnit'] for name, specs in res_spec_data.items() \
               if specs['id'] == res_data['spec_id']][0]
    
    # Produce the query and variables vars to be signed
    # Getting the current date and time
    ts = datetime.now(timezone.utc).isoformat()

    variables = {
        "event": {
            "note": "create resource",
            "action": "raise",
            "provider": provider, 
            "receiver": receiver,
            "hasPointInTime" : ts,
            "resourceQuantity": {
              "hasUnit": unit_id,
              "hasNumericalValue": amount 
            },
            "resourceConformsTo": res_data['spec_id'],
            "toLocation" : user_data['location_id']
        },
        "newInventoriedResource": { 
            "name": res_data['name'],
            "trackingIdentifier": res_data['res_ref_id']
        }
    }

    query = """mutation($event:EconomicEventCreateParams!, $newInventoriedResource:EconomicResourceCreateParams) {
                createEconomicEvent(event:$event, newInventoriedResource:$newInventoriedResource) {
                    economicEvent {
                        id
                        provider {
                            ...agent
                        }
                        resourceQuantity {
                            ...quantity
                        }
                        resourceInventoriedAs {
                            ...resource
                      }
                    }
                }
            }""" + AGENT_FRAG + LOCATION_FRAG + QUANTITY_FRAG + RESOURCE_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        raise Exception(f"Error in function {inspect.stack()[0][3]}")

    if DEBUG_create_resource:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))

    # save the unit info
    res_data['id'] = res_json['data']['createEconomicEvent']['economicEvent']['resourceInventoriedAs']['id']
    
    return res_json['data']['createEconomicEvent']['economicEvent']['id'], ts



# Create the resource by calling the back-end
DEBUG_reduce_resource = False
def reduce_resource(user_data, res_data, res_spec_data, amount, endpoint):
    
    provider = user_data['id']
    receiver = user_data['id']
    # Get the unit from the spec, no need to pass it     
    unit_id = [specs['defaultUnit'] for name, specs in res_spec_data.items() \
               if specs['id'] == res_data['spec_id']][0]
    
    # Produce the query and variables vars to be signed
    # Getting the current date and time
    ts = datetime.now(timezone.utc).isoformat()

    variables = {
        "event": {
            "note": "update event",
            "action": "lower",
            "provider": provider, 
            "receiver": receiver,
            "hasPointInTime" : ts,
            "resourceInventoriedAs" : res_data['id'],
            "resourceQuantity": {
              "hasUnit": unit_id,
              "hasNumericalValue": amount 
            },
            "resourceConformsTo": res_data['spec_id']
        }
    }

    query = """mutation($event:EconomicEventCreateParams!, $newInventoriedResource:EconomicResourceCreateParams) {
                createEconomicEvent(event:$event, newInventoriedResource:$newInventoriedResource) {
                    economicEvent {
                        id
                        provider {
                            ...agent
                        }
                        resourceQuantity {
                            ...quantity
                        }
                        resourceInventoriedAs {
                            ...resource
                      }
                    }
                }
            }""" + AGENT_FRAG + LOCATION_FRAG + QUANTITY_FRAG + RESOURCE_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        raise Exception(f"Error in function {inspect.stack()[0][3]}")

    if DEBUG_reduce_resource:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))

   
    return res_json['data']['createEconomicEvent']['economicEvent']['id'], ts


# Wrapper for the resource creation
def get_resource(res_data, res_spec_data, res_name, user_data, event_seq, amount, endpoint):
    
#     breakpoint()
    res_data[f'{res_name}_res'] = {}
    cur_res = res_data[f'{res_name}_res']

    rnd = random.randint(0, 10000)
    cur_res['res_ref_id'] = f'{res_name}-{rnd}'
    cur_res['name'] = res_name
    cur_res['spec_id'] = res_spec_data[f'{res_name}']['id']


    event_id, ts = create_resource(user_data, cur_res, res_spec_data, amount, endpoint)

    event_seq.append({'ts': ts, 'event_id':event_id, 'action' : 'raise', 'res_name': cur_res['name'], 'res': cur_res['id']})



# Create a process by calling the back-end
def create_process(cur_process, user_data, endpoint):

    # Produce the query and variables vars to be signed
    # Getting the current date and time
    ts = datetime.now(timezone.utc).isoformat()

    variables = {
      "process": {
        "name": cur_process['name'],
        "note": cur_process['note'],
        "hasBeginning": ts,
        "hasEnd": ts
      }
    }

    query = """mutation($process:ProcessCreateParams!) {
        createProcess(process: $process) {
            process {
                id
            }
        }
    }"""

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        raise Exception(f"Error in function {inspect.stack()[0][3]}")


    # save the unit info
    cur_process['id'] = res_json['data']['createProcess']['process']['id']


# Wrapper for process creation
def get_process(process_name, process_data, note, user_data, endpoint):

#     name = process_name.replace(' ', '_')

    if process_name in process_data:
        return
    process_data[f'{process_name}'] = {}

    cur_process = process_data[f'{process_name}']

    cur_process['name'] = process_name
    cur_process['note'] = note
    
    create_process(cur_process, user_data, endpoint)    

DEBUG_create_event = False
# This function implements all actions != transfer actions
def create_event(provider, action, note, amount, process, res_spec_data, endpoint, \
                 existing_res:dict={}, new_res:dict={}, effort_spec:dict={}, receiver:dict={}, process2:dict={}):

    if not action in SUPPORTED_ACTIONS:
        print(f"We do not support {action} yet")
        raise Exception(f"Error in function {inspect.stack()[0][3]}")

    if not action in ['work']:
        # Sanity checks, the code does not support
        # these cases (there might be valid VF actions that fall into these,
        # but we have not addressed them yet)
        if existing_res == {} and new_res == {}:
            print(f"No resource given for event")
            raise Exception(f"Error in function {inspect.stack()[0][3]}")

        if existing_res != {} and new_res != {}:
            print(f"Both existing and new resource given for event")
            raise Exception(f"Error in function {inspect.stack()[0][3]}")
    
    ts = datetime.now(timezone.utc).isoformat()
    variables = {
        "event": {
            "action": action,
            "note": note,
            "provider": provider['id'],
            "receiver": receiver['id'] if receiver != {} else provider['id'],
            "hasPointInTime" : ts
        }
    }

    # set_trace()
    if action in ['work']:
        # Need to provide the specification of the type of work
        variables['event']['resourceConformsTo'] = effort_spec['spec_id']
        # If action is work then the quantity is about the action
        variables['event']['effortQuantity'] = {}
        var_obj = variables['event']['effortQuantity']
        var_obj['hasUnit'] = effort_spec['unit_id']
        var_obj['hasNumericalValue'] = effort_spec['amount']
    else:
        if action in ['use']:
            # If action is use it might include a duration of usage
            if effort_spec['unit_id'] != {}:
                variables['event']['effortQuantity'] = {}
                var_obj = variables['event']['effortQuantity']
                var_obj['hasUnit'] = effort_spec['unit_id']
                var_obj['hasNumericalValue'] = effort_spec['amount']

        # If action is not work then the quantity is about the resource
        variables['event']['resourceQuantity'] = {}
        var_obj = variables['event']['resourceQuantity']

        _res = {}
        if existing_res != {}:
            _res = existing_res
        elif new_res != {}:
            _res = new_res
        
        # if action in ['produce']:
        #     _res = new_res
        # else:
        #     _res = existing_res
        # find the unit from the resource's specification
        var_obj['hasUnit'] = [specs['defaultUnit'] for name, specs in res_spec_data.items() \
                              if specs['id'] == _res['spec_id']][0]
        var_obj['hasNumericalValue'] = amount


    if action in IN_PR_ACTIONS:
        # These actions are input to a process
        variables['event']['inputOf'] = process['id']
    elif action in OUT_PR_ACTIONS:
        # These actions are output of a process
        variables['event']['outputOf'] = process['id']
    elif action in IN_OUT_PR_ACTIONS:
        # These actions can be either input or output of a process
        if process2 == {}:
            if existing_res != {}:
                variables['event']['inputOf'] = process['id']
            elif new_res != {}:
                variables['event']['outputOf'] = process['id']
        else:
            variables['event']['inputOf'] = process['id']
            variables['event']['outputOf'] = process2['id']
        
    if action in ['accept', 'cite', 'consume', 'modify', 'use']:
        # These actions require a resource id to act upon
        variables['event']['resourceInventoriedAs'] = existing_res['id']
        
    if action in ['produce']:
        variables['newInventoriedResource'] = {};
        variables['newInventoriedResource']['name'] = new_res['name']
        variables['newInventoriedResource']['trackingIdentifier'] = new_res['res_ref_id']

        variables['event']['resourceConformsTo'] = new_res['spec_id']
        variables['event']['toLocation'] = provider['location_id']
    
    if action in ['deliverService']:
        if existing_res != {}:
            variables['event']['resourceConformsTo'] = existing_res['spec_id']
        elif new_res != {}:
            variables['event']['resourceConformsTo'] = new_res['spec_id']
        
    
    # Define the fields for the GraphQL response

    response = """economicEvent {
                        id
                        provider {
                            ...agent
                        }
                        resourceQuantity {
                            ...quantity
                        }
                        toResourceInventoriedAs {
                            ...resource
                        }
                        resourceInventoriedAs {
                            ...resource
                        }
                    }"""
                    
    if action in ['produce']:
        query = f"""
        mutation($event:EconomicEventCreateParams!, $newInventoriedResource: EconomicResourceCreateParams) {{
                createEconomicEvent(event:$event, newInventoriedResource:$newInventoriedResource) {{
                    {response}
                }}
            }}"""
    else:
        query = f"""
        mutation($event:EconomicEventCreateParams!) {{
                createEconomicEvent(event:$event) {{
                    {response}
                }}
            }}"""

    query = query + AGENT_FRAG + LOCATION_FRAG + QUANTITY_FRAG + RESOURCE_FRAG
    # assert False
    res_json = send_signed(query, variables, provider['username'], provider['keyring']['eddsa'], endpoint)
    
    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        raise Exception(f"Error in function {inspect.stack()[0][3]}")

    if DEBUG_create_event:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))

    if action in ['produce']:
        # save the id of the new resource
        new_res['id'] = res_json['data']['createEconomicEvent']['economicEvent']['resourceInventoriedAs']['id']

    return res_json['data']['createEconomicEvent']['economicEvent']['id'], ts


# Update the id of the resource in case of transfer
def update_id(resource, new_id):
    if not 'previous_ids' in resource:
        resource['previous_ids'] = []
    resource['previous_ids'].append(resource['id'])
    resource['id'] = new_id

# This function implements all transfer actions
DEBUG_make_transfer = False
def make_transfer(provider_data, action, note, receiver_data, amount, existing_res, locs_data, res_spec_data, endpoint):

    ts = datetime.now(timezone.utc).isoformat()

    variables = {
        "event": {
            "note": note,
            "action": action,
            "provider": provider_data['id'], 
            "receiver": receiver_data['id'], 
            "resourceInventoriedAs": existing_res['id'],
            "hasPointInTime": ts,
            "toLocation": [values['id'] for key, values in locs_data.items() \
                              if values['user_id'] == receiver_data['id']][0],
            "resourceQuantity": {
              "hasUnit": [values['defaultUnit'] for key, values in res_spec_data.items() \
                              if values['id'] == existing_res['spec_id']][0], 
              "hasNumericalValue": amount 
            }
        },
        "newInventoriedResource": {
            "name" : existing_res['name']
        }
    }
    
    query = """mutation($event:EconomicEventCreateParams!, $newInventoriedResource: EconomicResourceCreateParams) {
                createEconomicEvent(event:$event, newInventoriedResource:$newInventoriedResource) {
                    economicEvent {
                        id
                        provider {
                            ...agent
                        }
                        resourceQuantity {
                            ...quantity
                        }
                        toResourceInventoriedAs { 
                            ...resource
                        }
                        resourceInventoriedAs {
                            ...resource
                        }
                    }
                }
            }""" + AGENT_FRAG + LOCATION_FRAG + QUANTITY_FRAG + RESOURCE_FRAG

    res_json = send_signed(query, variables, provider_data['username'], provider_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        raise Exception(f"Error in function {inspect.stack()[0][3]}")

    if DEBUG_make_transfer:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   

    transferred_id = res_json['data']['createEconomicEvent']['economicEvent']['toResourceInventoriedAs']['id']

    update_id(existing_res, transferred_id)

    return res_json['data']['createEconomicEvent']['economicEvent']['id'], ts


DEBUG_show_resource = False
def show_resource(user_data, id, endpoint):

    variables = {
        "id": id
    }
    
    query = """query($id:ID!){
          economicResource(id:$id){
            ...resource    
          }
        }
    """ + RESOURCE_FRAG

    res_json = send_signed(query, variables, user_data['username'], user_data['keyring']['eddsa'], endpoint)

    if 'errors' in res_json:
        print("Error message")
        print(json.dumps(res_json['errors'], indent=2))
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        raise Exception(f"Error in function {inspect.stack()[0][3]}")

    if DEBUG_show_resource:
        print("Query")
        print(query)
        print("Variables")
        print(variables)
        print("Result")
        print(json.dumps(res_json, indent=2))   

    return res_json

