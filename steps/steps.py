from run_class_i_allele_prediction import run_class_i_allele_prediction
from copy_best_prediction import copy_best_prediction
from copy_plots import copy_plots
from zip_results import zip_results
from download_reference_structures import download_reference_structures
from align_to_canonical import align_to_canonical

def stub_function():
    return None


align_to_reference_crystal_structure = stub_function
align_to_reference_prediction = stub_function
split_best_prediction = stub_function



steps = {
    '1':{
        'function':run_class_i_allele_prediction,
        'title_template':'the colabfold allele prediction.',
        'title_verb': ['Runing','Runs'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '2':{
        'function':copy_best_prediction,
        'title_template':'the best colabfold prediction.',
        'title_verb': ['Copying','Copies'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '3':{
        'function':copy_plots,
        'title_template':'the colabfold PAE, pLDDT and coverage plots.',
        'title_verb': ['Copying','Copies'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '4':{
        'function':zip_results,
        'title_template':'the colabfold PAE, pLDDT and coverage plots.',
        'title_verb': ['Zipping','Zips'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '5':{
        'function':download_reference_structures,
        'title_template':'the reference structures.',
        'title_verb': ['Downloading','Downloads'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '6':{
        'function':align_to_canonical,
        'title_template':'the best colabfold prediction to canonical class I (1hhk).',
        'title_verb': ['Aligning','Aligns'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '7':{
        'function':align_to_reference_crystal_structure,
        'title_template':'the best colabfold prediction to reference_crystal_structure.',
        'title_verb': ['Aligning','Aligns'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '8':{
        'function':align_to_reference_prediction,
        'title_template':'the best colabfold prediction to reference prediction.',
        'title_verb': ['Aligning','Aligns'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '9':{
        'function':split_best_prediction,
        'title_template':'the best colabfold prediction into full and abd only.',
        'title_verb': ['Splitting','Splits'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    }
}