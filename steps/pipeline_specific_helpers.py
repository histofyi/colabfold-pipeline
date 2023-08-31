from typing import Callable, Dict, List, Tuple

import os 

from helpers.files import read_json, write_json, write_step_tmp_output

from pipeline import create_folder

from rich.progress import Progress


def do_work(new_work:List, action:Callable, kwargs=None) -> Dict:
    """
    This function is used to run a function on a list of data, and return a tuple of lists of successful, unchanged and errored items.

    Args:
        new_work (List): A list of data to be processed
        action (Callable): The function to be run on each item in the list
        output_facet (str): The name of the output facet where the data will be stored

    Returns:
        Tuple[List, List, List]: A tuple containing lists of successful, unchanged and errored items

    Keyword Args:
        verbose (bool): Whether to print verbose output
        config (Dict): The configuration object
        console (Console): The Rich console object
        datehash (str): The datehash of the current pipeline run
        function_name (str): The name of the current pipeline step
        output_path (str): The path to the output folder
        force (bool): Whether to force the pipeline step to run
    """

    verbose = kwargs['verbose']
    config = kwargs['config']
    console = kwargs['console']
    datehash = kwargs['datehash']
    function_name = kwargs['function_name']
    output_path = kwargs['output_path']
    force = kwargs['force']
    has_progress = kwargs['has_progress']

    unchanged = []
    successful = []
    errors = []
        
    with Progress() as progress:
        task = progress.add_task("[white]Processing...", total=len(new_work))
        for item in new_work:

            kwargs['item'] = item   
            success, data, errors = action(**kwargs)
            progress.update(task, advance=1)

    raw_output = {
        'successful':successful,
        'errors':errors,
        'unchanged':unchanged
    }


    action_output = {}
    for key in raw_output:
        action_output[key] = len(raw_output[key])

    return action_output
