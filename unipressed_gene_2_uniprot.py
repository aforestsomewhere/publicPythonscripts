"""
Script to implement /new/ Unipressed API client (https://github.com/multimeric/Unipressed)
Input: CSV file containing column titled 'Enzyme' containing gene/protein names
Returns: Modified CSV file, with added column titled 'uniprot_acc'
To do: Speed up. Better case/error handling.
Author: A. Kate Falà
Date: 05/03/23
"""

import sys
from unipressed import UniprotkbClient
import pandas as pd
import argparse

#Read input filename provided (expect.csv)
arg_parse = argparse.ArgumentParser(description='This script tries to retrieve UniprotKB entry numbers for supplied gene/protein names.')
arg_parse.add_argument('input_file', type=str, nargs=1, help='Input csv file containing the gene/protein names in a column Enzyme (required)')
args = arg_parse.parse_args()
uniprot_id = args.input_file[0]

data = pd.read_csv(uniprot_id, encoding='windows-1252')

#for each Uniprot entry, search for matching gene/protein names and return the primaryAccession ID
def name_2_acc(acc):
    acc=str(acc)
    for record in UniprotkbClient.search(
        query={
            "or_": [
                {"gene": acc},
                {"protein_name": acc},
                ]
            },
        format="json",
        fields=["accession"]
        ).each_record():
        return record['primaryAccession']

def amend(x):
    for index, row in x.iterrows():
        row = row.copy()
        try:
            x.loc[index, 'uniprot_acc']=name_2_acc(row['Enzyme'])
        except:
            x.loc[index, 'uniprot_acc']="balls..."
    new_x = x.iloc
    return new_x
amend(data)

#Write output
data.to_csv("out_file.csv", index=False)
