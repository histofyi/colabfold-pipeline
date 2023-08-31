from typing import Dict, List, Tuple
import os


from helpers.files import read_json, write_json, create_folder, write_file

from pipeline_specific_helpers import do_work


def do_something(item:str) -> Tuple[Dict, bool, List]:
    return None, None, None


def run_class_i_allele_prediction_action(**action_args) -> Tuple[bool, Dict, List]:

    output_path = action_args['output_path']
    verbose = action_args['verbose']
    item = action_args['item']
    config = action_args['config']

    print (output_path)


    alpha_chain = item['canonical_sequence']
    beta2m = 'IQRTPKIQVYSRHPAENGKSNFLNCYVSGFHPSDIEVDLLKNGERIEKVEHSDLSFSKDWSFYLLYYTEFTPTEKDEYACRVNHVTLSQPKIVKWDRDM'
    
    allele_slug = item['allele_slug']

    sequence = f"{alpha_chain}:{beta2m}"

    fasta_file = f">{item['allele_slug']}\n{sequence}\n"
    tmp_fasta_file = f"{action_args['config']['PATHS']['TMP_PATH']}/{action_args['config']['PATHS']['PIPELINE_WAREHOUSE_FOLDER']}/{item['locus_slug']}/{item['allele_slug']}.fasta"

    write_file(tmp_fasta_file, fasta_file, verbose)

    output_folder = f"{output_path}/{config['PATHS']['PIPELINE_WAREHOUSE_FOLDER']}/{item['locus_slug']}/{item['allele_slug']}"

    create_folder(output_folder, verbose)

    if not os.path.exists(f"{output_folder}/{allele_slug}.done.txt"):

        localcolabfold_command = f"colabfold_batch {tmp_fasta_file} {output_folder}/ --num-recycle 3 --random-seed 42 --amber --use-gpu-relax"

        os.system(localcolabfold_command)

        print (localcolabfold_command)
    else:
        print (f"Skipping {allele_slug}, it already exists")

    data, success, errors = do_something(item)

    if success:
        # do something here

        return (True, {}, None)
    else:
        return (False, None, ['unable to do something'])



def run_class_i_allele_prediction(**kwargs):
    verbose = kwargs['verbose']
    config = kwargs['config']
    new_work = []

    locus = 'hla_f'

    create_folder(f"{config['PATHS']['TMP_PATH']}/{config['PATHS']['PIPELINE_WAREHOUSE_FOLDER']}//{locus}", verbose)
    create_folder(f"{config['PATHS']['OUTPUT_PATH']}/{config['PATHS']['PIPELINE_WAREHOUSE_FOLDER']}/{locus}", verbose)

    locus_file_name = f"{config['PATHS']['WAREHOUSE_PATH']}/alleles/processed_data/protein_alleles/{locus}.json"

    locus_data = read_json(locus_file_name)

    for allele in locus_data:
        allele_record = locus_data[allele]
        allele_record['allele_slug'] = allele
        allele_record['locus_slug'] = locus

        new_work.append(allele_record)

    action_output = do_work(new_work, run_class_i_allele_prediction_action, kwargs=kwargs)

    return action_output