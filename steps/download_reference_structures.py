from typing import Dict, List, Tuple
import os


from helpers.files import read_json, write_json, create_folder, write_file

from pipeline_specific_helpers import do_work


import csv
import requests


def download_and_save_pdb_file(pdb_code, file_name_part, config):
    histo_structure_url = f"https://coordinates.histo.fyi/structures/downloads/class_i/without_solvent/{pdb_code}_1_abd.pdb"
    file_name = f"{config['PATHS']['PIPELINE_PATH']}/input/reference_crystal_structures/{file_name_part}.pdb"

    if not os.path.exists(file_name):
        print (f"Downloading {histo_structure_url} to {file_name}")
        r = requests.get(histo_structure_url, allow_redirects=True)
        open(file_name, 'wb').write(r.content)
    else:
        print (f"Structure ({pdb_code}) already downloaded to {file_name}")
    


def download_reference_structures_action(**action_args) -> Tuple[bool, Dict, List]:
    verbose = action_args['verbose']
    output_path = action_args['output_path']
    item = action_args['item']
    config = action_args['config']
    reference_allele_list = action_args['reference_allele_list']



    if item['allele_slug'] in reference_allele_list:
        download_and_save_pdb_file(item['pdb_code'], item['allele_slug'], config)
    else:
        print (f"Skipping {item['pdb_code']} as {item['allele_slug']} is not in the reference allele list")


    success = False
    if success:
        return (True, {}, None)
    else:
        return (False, None, ['unable to do something'])



def download_reference_structures(**kwargs):
    verbose = kwargs['verbose']
    config = kwargs['config']
    output_path = kwargs['output_path']

    download_and_save_pdb_file('1hhk', 'canonical_class_i', config)

    loci = ['a','b','c','e','f','g']

    reference_allele_list = []
    for locus in loci:
        locus_reference_alleles = read_json(f"{config['PATHS']['PIPELINE_PATH']}/input/reference_alleles/hla_{locus}.json")['allele_groups']
        for allele in locus_reference_alleles:
            reference_allele_list.append(locus_reference_alleles[allele])

    kwargs['reference_allele_list'] = reference_allele_list

    new_work = []

    new_work = [row for row in csv.DictReader(open(f"input/reference_structures.csv"))]

    print (len(new_work))

    action_output = do_work(new_work, download_reference_structures_action, kwargs=kwargs)

    return action_output
    