from typing import Dict

from pipeline import Pipeline

from steps import steps

import toml

def run_pipeline(**kwargs) -> Dict:
    pipeline = Pipeline()

    pipeline.load_steps(steps)

    #pipeline.run_step('1')  # run_class_i_allele_prediction
    #pipeline.run_step('2')  # copy_best_prediction
    #pipeline.run_step('3')  # copy_plots
    #pipeline.run_step('4')  # zip_results
    #pipeline.run_step('5')  # download_reference_structures
    pipeline.run_step('6')  # align_to_canonical
    #pipeline.run_step('7')  # align_to_reference_crystal_structure
    #pipeline.run_step('8')  # align_to_reference_prediction
    #pipeline.run_step('9')  # split_best_prediction

    action_logs = pipeline.finalise()

    return action_logs

def main():

    output = run_pipeline()

if __name__ == '__main__':
    main()
