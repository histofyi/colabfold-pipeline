from typing import Dict, List, Tuple
import os


from helpers.files import read_json, write_json, create_folder, write_file

from pipeline_specific_helpers import do_work




def run_copy_best_prediction_action(**action_args) -> Tuple[bool, Dict, List]:
    verbose = action_args['verbose']
    output_path = action_args['output_path']
    item = action_args['item']

    success = False

    locus = item['locus']
    allele = item['allele']
    input_folder = item['input_folder']

    output_folder = f"{output_path}/processed_predictions/best_coordinates/{locus}"

    output_file = f"{output_folder}/{allele}_best_relaxed_unaligned.pdb"

    if not os.path.exists(output_file):
        print (f"Finding best relaxed prediction for {allele}...")

        best_relaxed = f"{allele}_relaxed_rank_001"
        best_relaxed_file = None

        for file in os.listdir(input_folder):
            if best_relaxed in file:
                best_relaxed_file = f"{input_folder}/{file}"

                print (f"Found {file}")
                print (f"Copying {best_relaxed_file} to {output_file}")

                os.system(f"cp {best_relaxed_file} {output_file}")

        if best_relaxed_file:
            with open(best_relaxed_file, 'r') as f:
                best_relaxed_structure = f.read()

            with open(output_file, 'r') as f:
                output_structure = f.read()

            if best_relaxed_structure != output_structure:
                print ('Best relaxed prediction is different to the output prediction')
                success = False
            else:
                success = True
    
    else:
        print (f"Skipping {allele}, it has already been processed")

    if success:
        return (True, {}, None)
    else:
        return (False, None, ['unable to do something'])



def copy_best_prediction(**kwargs):
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

    print ('Copying best relaxed predictions...')

    new_work = new_work
    action_output = do_work(new_work, run_copy_best_prediction_action, kwargs=kwargs)

    return action_output
    