"""
Script to implement /new/ Unipressed API client (https://github.com/multimeric/Unipressed)
Input: UniProt ID
Returns: Amino acid sequence (string to stdout)
Author: A. Kate Falà
Date: 02/03/23
"""

import sys
from unipressed import UniprotkbClient
import pandas as pd
import argparse

#capture the query ID
arg_parse = argparse.ArgumentParser(description='This script extracts or remove\
s fasta sequences by sequence IDs.')
arg_parse.add_argument('ID', type=str, nargs=1, help='Input UNIPROT ID (require\
d)')
args = arg_parse.parse_args()
uniprot_id = args.ID[0]

#fetch entry
ret = UniprotkbClient.fetch_one(uniprot_id, format="json")
#retrieve fasta sequence
df=pd.json_normalize(ret["sequence"])
fasta=df['value'].to_string(index=False)

#return fasta
print(fasta)

