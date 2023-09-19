from typing import Dict, List, Tuple
import os


from helpers.files import read_json, write_json, create_folder, write_file

from pipeline_specific_helpers import do_work

from pymol import cmd


alignment_residues = [(3,13),(20,37),(43,48),(92,103),(110,127),(133,135)]

def build_alignment_residue_list(alignment_residues:List) -> List:
    alignment_residue_list = []
    for low_high in alignment_residues:
        low = low_high[0]
        high = low_high[1]

        i = low
        while i <= high:
            i += 1
            alignment_residue_list.append(i)
    return alignment_residue_list


def build_pymol_selection_command(alignment_residues_list:List) -> str:
    pymol_selection_cmd = f"target and resi "
    for residue_id in alignment_residues_list:
        pymol_selection_cmd += f'{residue_id}+'
    pymol_selection_cmd = pymol_selection_cmd[0:-1]   
    return pymol_selection_cmd


def pymol_alignment(fixed_structure:str, mobile_structure:str, output_filename:str, metadata_filename:str, alignment_residues_list, alignment_type, allele_slug, locus) -> Dict:

    cmd.load(fixed_structure, 'target', quiet=1)

    cmd.select('alignment_region', build_pymol_selection_command(alignment_residues_list))
    
    cmd.load(mobile_structure, 'mobile', quiet=1)
    align = cmd.align('mobile', 'alignment_region')
    cmd.delete('target')
    cmd.remove('hydro')
    cmd.save(output_filename)
    cmd.delete('mobile')


    alignment_data = {
        'input_type':'colabfold_prediction',
        'locus': locus,
        'allele_slug':allele_slug,
        'alignment_information':dict(zip(['rmsd','atom_count','cycle_count','starting_rmsd','starting_atom_count','match_align_score','aligned_residue_count'], list(align))),
        'alignment_type':alignment_type,
        'alignment_residues':alignment_residues_list
    }

    write_json(metadata_filename, alignment_data)

    return alignment_data



def align_to_canonical_action(**action_args) -> Tuple[bool, Dict, List]:
    verbose = action_args['verbose']
    output_path = action_args['output_path']
    item = action_args['item']
    config = action_args['config']
    reference_alleles = action_args['reference_alleles']
    reference_crystal_structures = action_args['reference_crystal_structures']

    alignment_residue_list = action_args['alignment_residue_list']

    locus = item['locus']
    allele = item['allele']
    allele_group = '_'.join(allele.split('_')[0:3])

    print (allele)

    #reference_allele = reference_alleles[locus][allele_group]

    # ALL PREDICTIONS
    alignment_info = pymol_alignment(
            f"{config['PATHS']['PIPELINE_PATH']}/input/reference_crystal_structures/canonical_class_i.pdb",
            f"{output_path}/processed_predictions/best_coordinates/{locus}/{allele}_best_relaxed_unaligned.pdb",
            f"{output_path}/processed_predictions/aligned_predictions/{locus}/{allele}_canonical.pdb", 
            f"{output_path}/processed_predictions/aligned_predictions/{locus}/{allele}_canonical.json", 
            alignment_residue_list,
            'canonical_class_i',
            allele,
            locus
        )
    
    print (alignment_info)

    #if reference_allele in reference_crystal_structures:
        # align to reference crystal structure (if it exists)
    #    print ('do alignment to reference crystal structure')
    
    # THIS ONE NEEDS MORE THOUGHT
    #if allele != reference_allele:
        # align to reference allele structure





    success = False
    if success:
        return (True, {}, None)
    else:
        return (False, None, ['unable to do something'])



def align_to_canonical(**kwargs):
    verbose = kwargs['verbose']
    config = kwargs['config']
    output_path = kwargs['output_path']

    new_work = []

    alignment_residue_list = build_alignment_residue_list(alignment_residues)

    reference_crystal_structures = [filename.split('.')[0] for filename in os.listdir(f"{config['PATHS']['PIPELINE_PATH']}/input/reference_crystal_structures") if filename != 'canonical_class_i.pdb']


    kwargs['alignment_residue_list'] = alignment_residue_list
    kwargs['reference_alleles'] = {}
    kwargs['reference_crystal_structures'] = reference_crystal_structures


    for locus in config['CONSTANTS']['COMPLETED_LOCI']:
        locus = f"hla_{locus.lower()}"
        kwargs['reference_alleles'][locus] = read_json(f"{config['PATHS']['PIPELINE_PATH']}/input/reference_alleles/{locus}.json")['allele_groups']    


    for locus in config['CONSTANTS']['COMPLETED_LOCI']:
        locus = f"hla_{locus.lower()}"
        best_predictions = f"{output_path}/processed_predictions/best_coordinates/{locus}"
        for filename in os.listdir(best_predictions):
            allele = filename.replace('_best_relaxed_unaligned.pdb','')
            locus = '_'.join(allele.split('_')[0:2])
            item = {'allele':allele, 'locus':locus}
            new_work.append(item)

    #new_work = new_work[0:10]

    action_output = do_work(new_work, align_to_canonical_action, kwargs=kwargs)

    return action_output


