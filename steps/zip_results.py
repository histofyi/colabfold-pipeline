from typing import Dict, List, Tuple
import os


from helpers.files import read_json, write_json, create_folder, write_file

from pipeline_specific_helpers import do_work


def zip_results_action(**action_args) -> Tuple[bool, Dict, List]:
    verbose = action_args['verbose']
    output_path = action_args['output_path']
    item = action_args['item']

    locus = item['locus']
    allele = item['allele']
    input_folder = item['input_folder'].replace(allele, '')

    print (input_folder)

    output_folder = f"{output_path}/processed_predictions/prediction_zip_archives/{locus}"

    output_file = f"{output_folder}/{allele}.zip"

    if not os.path.exists(output_file):
        os.system(f"cd {input_folder}; zip -r {output_file} {allele}/*")

    print (item)

    success = False
    errors = []

    if success:
        return (True, {}, None)
    else:
        return (False, None, errors)



def zip_results(**kwargs):
    verbose = kwargs['verbose']
    config = kwargs['config']
    output_path = kwargs['output_path']
    new_work = []


    for locus in config['CONSTANTS']['COMPLETED_LOCI']:

        locus = f"hla_{locus.lower()}"
        print (locus)

        done = 0
        errors = 0
        total = 0

        locus_folder = f"{output_path}/predictions/{locus}"

        if os.path.exists(locus_folder):

            for allele in os.listdir(locus_folder):
                allele_folder = f"{locus_folder}/{allele}"
                
                logfile = f"{allele_folder}/log.txt"

                status = None
                if os.path.exists(logfile):
                    with open(logfile) as f:
                        log = f.readlines()
                        if 'Done' in log[-1]:
                            status = 'Done'
                            new_work.append({'locus':locus, 'allele':allele, 'input_folder':allele_folder})
                            done += 1

                if not status:
                    errors += 1
                total += 1

        print (f"Found {total} folder, {done} completed colabfold predictions, {errors} errors")
        
    print (len(new_work))

    print ('Copying plots...')

    #new_work = new_work [0:10]

    action_output = do_work(new_work, zip_results_action, kwargs=kwargs)

    return action_output
    