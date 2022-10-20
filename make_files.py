import urllib.parse
import glob
import argparse
from six import text_type
import shutil
import os
    


endpoint = None
def get_filename(filename):
    new_filename = filename.replace('_example.json',f'.{urllib.parse.quote_plus(endpoint)}.json')
    return new_filename

def copy_files():
    files = glob.glob('*_example.json')
    for afile in files:
        new_file = get_filename(afile)
        if os.path.isfile(new_file):
            print(f"{new_file} exists. Skipping")
        else:
            print(f'cp {afile} {new_file}')
            shutil.copyfile(afile, new_file)
            
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '-e', '--endpoint',
        dest='endpoint',
        type=text_type,
        nargs=1,
        default = '',
        required=True,
        help='specifies the endpoint of the GraphQL back-end',
    )
    args, unknown = parser.parse_known_args()

    endpoint = args.endpoint[0]

    copy_files()
