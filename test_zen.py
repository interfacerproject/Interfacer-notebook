import os
import sys
import contextlib
from zenroom import zenroom
import json
import base64
import subprocess

banner = '********************************************'

def zenroom_wrapper(contract, keys=None, data=None):
    with open(os.devnull, 'w') as f:
        # with contextlib.redirect_stderr(f):
        # with contextlib.redirect_stdout(os.devnull), contextlib.redirect_stderr(os.devnull):
        with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
            # sys.stderr = f
            # breakpoint()
            print("This is stdout")
            sys.stderr.write("This is stderr\n")
            # breakpoint()
            ret = zenroom.zencode_exec(contract, keys=keys, data=data)
    return ret

hello_contract = """
        Given nothing
        Then print the string 'hello'
    """

ch_contract = """
        rule check version 1.0.0
        Given nothing
        When I create the random object of '512' bits
        and I rename the 'random_object' to 'challenge'
        Then print 'challenge'
    """

# Test zenroom is correctly installed and running
def generate_random_challenge():
    """
        This function calls zenroom to generate
        a random string to be used as challenge
    """
    print(banner)
    print(f"Calling zenroom wrapped")
    try:
        resz = zenroom_wrapper(ch_contract)
        # resz = zenroom.zencode_exec(ch_contract)
    except Exception as e:
        print(f'Exception in zenroom call: {e}')
        return None

    # print(f"resz.output {resz}")
    resz_json = json.loads(resz.output)

    print(f"Generated challenge: {resz_json['challenge']}")

    return

def direct_file():
    print(banner)
    print(f"Calling zenroom directly with a contract file")
    result = subprocess.run(
        ["zenroom.command", "-z", f"{os.getcwd()}/contract.zen"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    print(result.stderr)

def direct_var():
    print(banner)
    print(f"Calling zenroom directly with an input parameter")
    input = b"\n" + base64.b64encode(ch_contract.encode())
    print(f"{input}")
    result = subprocess.run(
        ["zencode-exec"],
        capture_output=True,
        input=input,
        # text=True
    )
    print(result.stdout)
    print(result.stderr)

direct_file()
direct_var()
generate_random_challenge()