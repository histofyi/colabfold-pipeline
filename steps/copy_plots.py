from typing import Dict, List, Tuple
import os


from helpers.files import read_json, write_json, create_folder, write_file

from pipeline_specific_helpers import do_work


def copy_plots_action(**action_args) -> Tuple[bool, Dict, List]:
    verbose = action_args['verbose']
    output_path = action_args['output_path']
    item = action_args['item']

    success = False
    errors = []
    locus = item['locus']
    allele = item['allele']
    input_folder = item['input_folder']

    file_types = ['coverage', 'plddt', 'pae']

    output_folder = f"{output_path}/processed_predictions/prediction_plots/{locus}"

    for file_type in file_types:
        output_file = f"{output_folder}/{allele}_{file_type}.png"
        input_file = f"{input_folder}/{allele}_{file_type}.png"

        if not os.path.exists(output_file):
            if not os.path.exists(input_file):
                errors.append({'allele':allele, 'file_type':file_type, 'error':'file not found'})
            else:
                print (f"Copying {input_file} to {output_file}")
                os.system(f"cp {input_file} {output_file}")

                if os.path.exists(output_file):
                    success = True
                else:
                    success = False

        

    success = False

    for error in errors:
        print (error)

    if success:
        return (True, {}, None)
    else:
        return (False, None, errors)



def copy_plots(**kwargs):
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

    action_output = do_work(new_work, copy_plots_action, kwargs=kwargs)

    return action_output
    