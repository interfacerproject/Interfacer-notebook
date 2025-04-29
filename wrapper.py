import ast
import inspect
from pathlib import Path
from typing import Any, Optional, List, Dict, Union
import textwrap

TAG = "expose_as"

class InterfaceFunction:
    """
        This class encapsulate a ast.FunctionDef providing also
        the necessary parameters to generate the wrapped API call
    """
    generated_error_model = False
    preamble_generated = False
    error_model_name = 'ErrorOutput'
    mod_parameter = 'use_filesystem'
    mod_msg = """Please not that the server filesystem is never used when calling these APIs 
    (parameter use_filesystem is always set to False).
    """
    mod_code = f"{mod_parameter} = False # No server filesystem access via API"

    def __init__(self, node: ast.FunctionDef, method: str, file_to_read:str):
        self.node = node
        self.name = node.name
        self.args = node.args.args
        self.method = method
        self.file_to_read = file_to_read
    
    def get_docstring(self, arg_names):
        docstr = ast.get_docstring(self.node) or ""
        if InterfaceFunction.mod_parameter in arg_names:
            # Add warning that this parameter is always set to False
            ret = f"""{docstr}
{InterfaceFunction.mod_msg}
"""
        else:
            ret = docstr
        return repr(ret)

    @staticmethod
    def resolve_type(t):
        if t is None:
            return "Any"
        t_str = ast.unparse(t)

        # Check whether the type needs to be further specified
        if t_str == "dict":
            return "Dict[str, Any]"
        if t_str == "list":
            return "List[Any]"
        # Redundant code but explicit
        if t_str.startswith("Dict["):
            return t_str  # e.g., Dict[str, Dict[str, Any]]
        if t_str.startswith("List["):
            return t_str
        return t_str

    def _get_args(self):
        """
            Helper function to get args, their types and their defaults.
        """
        nr_arg = len(self.args)
        nr_defaults = len(self.node.args.defaults)
        args = []
        for i in range(nr_arg):
            a = self.args[i]
            idx = nr_arg-i-1
            # defaults are stored in an array starting with the last default
            default = ast.unparse(self.node.args.defaults[idx]) if (idx >= 0 and idx < nr_defaults) else None
            args.append((a.arg, self.resolve_type(a.annotation), default))
        return args
    
    def generate_IO_models(self):
        """
            Create input model for POST and output models for GET and POST
            Also create a generic output model for errors
        """
        code = []
        if not InterfaceFunction.generated_error_model:
            code.append(f"class {InterfaceFunction.error_model_name}(BaseModel):")
            code.append(f"    error: str")
            InterfaceFunction.generated_error_model = True
        
        if self.method == "post":
            args = self._get_args()
            if len(args) > 0:
                code.append(f"class {self.name.title()}Input(BaseModel):")
                
                for arg_name, arg_type, arg_default in args:
                    # breakpoint()
                    default = arg_default if arg_default else ""
                    code.append(f"    {arg_name}: {arg_type}{' = ' if default else ''}{default}")
        code.append("\n")
        code.append(f"class {self.name.title()}Output(BaseModel):")
        # breakpoint()
        if self.method == "post":
            if self.resolve_type(self.node.returns) != 'None':
                # breakpoint()
                raise Exception(f'{self.name}: only no return allowed for original functions exposed as post')
            code.append(f"    result: {self.name.title()}Input\n")
        else:
            if self.resolve_type(self.node.returns) == 'None':
                # breakpoint()
                raise Exception(f'{self.name}: must return something if exposed as get')
            returns = self.resolve_type(self.node.returns)
            code.append(f"    result: {returns}\n")

        return "\n".join(code)
        
    def generate_API(self) -> str:
        """
            This function generates the code for a single API call
        """

        # These variables are common to get and post methods
        call = (f"@app.{self.method.lower()}('/{self.name}', response_model={self.name.title()}Output|{InterfaceFunction.error_model_name})")
        arg_names = [arg.arg for arg in self.args if arg.arg != 'self']
        if self.method == 'post':
            # args_unpack = ", ".join(f"{arg}=payload.{arg}" for arg in arg_names)
            # Deep copy since we need to pass data that is going to be modified in place and returned
            args_copy = "\n    ".join(f"{arg} = copy.deepcopy(payload.{arg})" for arg in arg_names if arg != InterfaceFunction.mod_parameter)
            return_keys = ", ".join(f'\"{arg}\": {arg}' for arg in arg_names)
            fn_args = f'payload: {self.name.title()}Input' if len(arg_names)>0 else ''
            # Code to be generated
            code = f"""
{call}
def {self.name}_endpoint({fn_args}):
    ''{self.get_docstring(arg_names)}''
    
    {args_copy}
    {InterfaceFunction.mod_code if InterfaceFunction.mod_parameter in arg_names else ''}
    try:
        {self.file_to_read}.{self.name}({', '.join(arg_names)})
    except Exception as e:
        return {{"error": str(e)}}
    return {{"result": {{ {return_keys} }} }}
"""
        
        # For get methods
        else: 
            params = ", ".join([
                f"{arg}: {typ}{' = ' if default else ''}{default if default else ''}"
                for arg, typ, default in self._get_args()
                if arg != "self"
            ])
            code = f"""
{call}
def {self.name}_endpoint({params}):
    ''{self.get_docstring(arg_names)}''
    result = None
    try:
        result = {self.file_to_read}.{self.name}({', '.join(arg_names)})
    except Exception as e:
        return {{"error": str(e)}}
    return {{"result": result}}
"""
        return code


def extract_interface_functions(file_to_read):
    """
        Parses the file and extracts function tagged for the interface
    """
    source_code = file_to_read.read_text()
    tree = ast.parse(source_code)
    lines = source_code.splitlines()
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            comment_line = lines[node.lineno - 2].strip()
            if comment_line.startswith(f"# {TAG}"):
                parts = comment_line.split()
                method = parts[2] if len(parts) > 2 else "post"
                functions.append(InterfaceFunction(node, method, file_to_read.stem))
    return functions


def build_fastapi_code(functions_in_file):
    if len(functions_in_file) == 0:
        return ""
    if not InterfaceFunction.preamble_generated:
        code = [
            "from fastapi import FastAPI",
            "from pydantic import BaseModel, Field",
            "from typing import Any, Optional, List, Dict, Union, Tuple",
            "import copy"
        ]
    else:
        code = []

    code.append(f"import {functions_in_file[0].file_to_read}")

    if not InterfaceFunction.preamble_generated:
        code.append("app = FastAPI()")
        code.append("")
        InterfaceFunction.preamble_generated = True

    for func in functions_in_file:
        code.append(func.generate_IO_models())
        wrapper = func.generate_API()
        code.append(textwrap.dedent(wrapper))
    # breakpoint()
    return "\n".join(code)
    

def main(inputs:list[str], output:str):
    # breakpoint()
    if 'wrapped' not in output:
        # require wrapped in the file name to write to avoid accidentally 
        # overwriting other files
        raise Exception(f"Refuse to possibly overwrite file {output}")
    wrapped_file = Path(output)
    fastapi_code = []
    
    for input in inputs: 
        file_to_read = Path(input)
        if not file_to_read.exists():
            raise Exception(f"Cannot read file {input}")
        
        functions = extract_interface_functions(file_to_read)
        if len(functions) == 0:
            print(f"Warning: file {file_to_read} does not contain any function to extract")
        else:
            fastapi_code.append(build_fastapi_code(functions))
    
    if len(fastapi_code) > 0:
        wrapped_file.write_text("\n".join(fastapi_code))
    
    print(f"✅ FastAPI wrapper generated in {output}")


if __name__ == "__main__":
    import argparse    
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '-i', '--input',
        dest='inputs',
        action='store',
        required=True,
        nargs="+",
        help='specifies the name of the files containing the functions',
    )
    parser.add_argument(
        '-o', '--output',
        dest='output',
        action='store',
        required=True,
        help='specifies the name of the file to write',
    )
    args, unknown = parser.parse_known_args()

    if len(unknown) > 0:
        print(f'Unknown options {unknown}')
        parser.print_help()
        exit(-1)

    main(args.inputs, args.output)


# if_lib
# generate_random_challenge, read_HMAC, read_keypair, get_id_person, get_location_id, \
# get_unit_id, get_resource_spec_id, get_resource, get_process, create_event, make_transfer, reduce_resource, set_user_location

# if_dpp
# trace_query, check_traces, er_before, get_dpp