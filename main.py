# source .venv/bin/activate .
from tools import parser
from tools import label 
import pexpect, json, pathlib
import os

def eval_coverage(target_labels: dict, tested_labels: dict):
    for kind in ["Rule", "Eq"]:
        print(f"================={kind}==================") 
        # print(tested_labels)
        for label in target_labels[kind]:
            if(label[0] in tested_labels[kind]):
                print(f"{label[0]}: TESTED")
            else:
                print(f"{label[0]}: NOT TESTED")
                
                
if __name__ == "__main__":
    input_maude_file = "samples/test.maude"
    
    _ , target_labels = label.label_file(input_maude_file) 
    print(target_labels)
    maude = pexpect.spawn('Maude-3.5.1/maude -no-ansi-color')
    maude.sendline('set trace on .')
    maude.sendline(f'load temp/{input_maude_file}')
    maude.sendline('quit')

    result = maude.read().decode()
    # print(result)
    tested_labels = parser.parse_labels(result)
    # print(tested_labels)
    
    eval_coverage(target_labels, tested_labels)