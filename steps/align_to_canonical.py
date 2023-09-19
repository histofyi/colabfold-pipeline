from typing import Dict, List, Tuple
import os


from helpers.files import read_json, write_json, create_folder, write_file

from pipeline_specific_helpers import do_work

from pymol import cmd



def align_to_canonical_action(**action_args) -> Tuple[bool, Dict, List]:
    verbose = action_args['verbose']
    output_path = action_args['output_path']
    item = action_args['item']
    config = action_args['config']

    success = False
    if success:
        return (True, {}, None)
    else:
        return (False, None, ['unable to do something'])



def align_to_canonical(**kwargs):
    verbose = kwargs['verbose']
    config = kwargs['config']

    new_work = []

    action_output = do_work(new_work, align_to_canonical_action, kwargs=kwargs)

    return action_output


