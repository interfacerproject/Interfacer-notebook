import papermill as pm
from pathlib import Path
import json

TRACE_DIR = './traces'
REF_DIR = './test_ref'

NOT_COMPARABLE = ['id', 'trackingIdentifier', 'hasPointInTime', 'hasBeginning', 'hasEnd']

def cmp_nodes(ref_dpp, new_dpp, prt=False):
    
    if type(ref_dpp) is not dict:
        if not ref_dpp == new_dpp:
            # print(f'Values {ref_dpp} and {new_dpp} differ')
            return False
        else:
            return True

    for key in ref_dpp.keys():
        if key in NOT_COMPARABLE:
            continue
        elif type(ref_dpp[key]) is dict:
            if not cmp_nodes(ref_dpp[key], new_dpp[key]):
                # breakpoint()
                # print(f'Dict {key} is diffent')
                return False
        elif type(ref_dpp[key]) is list:
            for ref_item in ref_dpp[key]:
                found = False
                for new_item in new_dpp[key]:
                    if cmp_nodes(ref_item, new_item):
                        found = True
                        break
                if not found:
                    # breakpoint()
                    # print(f'Item {ref_item} is not in new trace')
                    return False
        elif ref_dpp[key] != new_dpp[key]:
            # breakpoint()
            # print(f'Key {key} is diffent: {ref_dpp[key]} != {new_dpp[key]}')
            return False
    return True

def cmp_traces_rec(ref_dpp, new_dpp):
    for ref_child in ref_dpp['children']:
        found = False
        for new_child in new_dpp['children']:
            if cmp_nodes(ref_child, new_child):
                found = True
                if not cmp_traces_rec(ref_child, new_child):
                    return False
                break
        if not found:
            print(
                f"{ref_dpp['name']} and {new_dpp['name']} have diffent children")
            return False

    return True

def cmp_traces(ref_dpp, new_dpp):

    if not cmp_nodes(ref_dpp, new_dpp):
        print(f"{ref_dpp['name']} and {new_dpp['name']} are different")
        return False

    return cmp_traces_rec(ref_dpp, new_dpp)


def main(nb_file, endpoint, present):
    parameters = pm.inspect_notebook(nb_file)
    exp_name = parameters['USE_CASE']['default'].replace("'", "")

    if not present:
        pm.execute_notebook(nb_file, '/dev/null', parameters=dict(ENDPOINT=endpoint))


    trace_file = f'{exp_name}_fe_trace.json'

    file_to_read = Path(REF_DIR, trace_file)
    with open(file_to_read, 'r') as f:
        ref_dpp = json.loads(f.read())
        ref_dpp = ref_dpp[0]

    file_to_read = Path(TRACE_DIR, trace_file)
    with open(file_to_read, 'r') as f:
        new_dpp = json.loads(f.read())
        new_dpp = new_dpp[0]

    if cmp_traces(ref_dpp, new_dpp):
        print("verification passed")
    else:
        print("verification NOT passed")


if __name__ == "__main__":
    import argparse
    from six import text_type

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '-e', '--endpoint',
        dest='endpoint',
        type=text_type,
        nargs=1,
        default=['http://zenflows-debug.interfacer.dyne.org/api'],
        help='specifies the endpoint to talk to',
    )

    parser.add_argument(
        '-f', '--filename',
        dest='filename',
        type=text_type,
        nargs=1,
        default=['IFServices.ipynb'],
        help='specifies the full path to the notebook',
    )

    parser.add_argument(
        '-p', '--present',
        dest='present',
        action='store_true',
        default=False,
        help='specifies whether the trace has already been calculated',
    )
    args, unknown = parser.parse_known_args()

    main(args.filename[0], args.endpoint[0], args.present)
