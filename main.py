# source .venv/bin/activate .
from tools import parser
from tools import label 
from tools import printer
import pexpect, json, pathlib
import os
import argparse
import sys
from pathlib import Path

DEBUG_MODE = False

def eval_coverage_detail(target_labels: dict, tested_labels: dict):
    for kind in ["Rule", "Eq"]:
        print(f"================={kind}==================") 
        for label in target_labels[kind]:
            if(label[0] in tested_labels[kind]):
                print(f"{label[0]}: TESTED")
            else:
                print(f"{label[0]}: NOT TESTED")


def eval_coverage(tested_labels: dict) -> list:
    number_of_equations = 0
    number_of_rewrite = 0
    number_of_passed_eq = 0
    number_of_passed_rw = 0
    
    
    for label in tested_labels['Rule']:
        number_of_rewrite += 1
        if(tested_labels['Rule'][label]):
            number_of_passed_rw += 1
        
    for label in tested_labels['Eq']:
        number_of_equations += 1
        if(tested_labels['Eq'][label]):
            number_of_passed_eq += 1
    
    return [number_of_equations, number_of_passed_eq, number_of_rewrite, number_of_passed_rw] 


def run_test_file(maude_path: str, file: str):
    input_maude_file = file
    _ , target_labels = label.label_file(input_maude_file)
    maude = pexpect.spawn(maude_path)
    maude.sendline('set trace on .')
    maude.sendline(f'load temp/{input_maude_file}')
    maude.sendline('quit')
    result = maude.read().decode()
    
    if(DEBUG_MODE):
        print(result)    
        
    tested_labels = parser.parse_labels(result, target_labels)
    return target_labels, tested_labels
           
def main():
    parser = argparse.ArgumentParser(
        description="Run Maude coverage tests on all .maude files in a directory."
    )
    parser.add_argument(
        "test_directory",
        help="The path to the directory containing test files."
    )
    args = parser.parse_args()

    maude_path = "Maude-3.5.1/maude -no-ansi-color"
    test_dir = Path(args.test_directory)

    # 3. Validate the input directory
    if not test_dir.is_dir():
        print(f"Error: Path '{test_dir}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    test_files = list(test_dir.rglob("*.maude"))

    if not test_files:
        print(f"No .maude files found in '{test_dir}'.")
        return

    print(f"Found {len(test_files)} test file(s). Starting coverage analysis...")
    
    results = []

    for test_file_path in test_files:
        test_file_str = str(test_file_path)
        target_labels, tested_labels = run_test_file(maude_path, test_file_str)
        
        if(DEBUG_MODE):
            print(tested_labels)
        
        result = eval_coverage(tested_labels)
        
        result.append(test_file_str)
        results.append(result)

    print(results)
    printer.print_report(results) 
              
if __name__ == "__main__":
    main()