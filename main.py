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