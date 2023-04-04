import sys
import unipressed
from unipressed import UniprotkbClient
import pandas as pd
import argparse

#Read input filename provided (expect.csv)
arg_parse = argparse.ArgumentParser(description='This script returns PFAM IDs associated to Uniprot accessions IDs.')
arg_parse.add_argument('input_file', type=str, nargs=1, help='Input csv file containing the Uniprot accession list (required)')
args = arg_parse.parse_args()
uniprot_id = args.input_file[0]

#data = pd.read_csv("QSHGMv2.csv", encoding='windows-1252')
data = pd.read_csv(uniprot_id, encoding='windows-1252')

#nb include this to avoid truncation by to_string function!
pd.options.display.max_colwidth = 2000


def id_2_fasta(id):
    id=str(id)
    #try to access entry
    ret=UniprotkbClient.fetch_one(id, format="json")
    #retrieve uniProtKBCrossReferences sequence
    df=pd.json_normalize(ret["uniProtKBCrossReferences"])
    q3=df[df['database'].str.match('Pfam')].id.to_string(index=False)
    q3=q3.replace("\n", ",").strip()
            
    return q3

def amend(x):
    for index, row in x.iterrows():
        row = row.copy()
        try:
            x.loc[index, 'pfams']=id_2_fasta(row['Accession'])
        except:
            x.loc[index, 'pfams']="balls..."
    new_x = x.iloc
    return new_x
amend(data)

#Write output
data.to_csv("out_file.csv", index=False)
