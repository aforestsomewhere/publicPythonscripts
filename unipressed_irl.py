"""
Script to implement /new/ Unipressed API client (https://github.com/multimeric/Unipressed)
Bare bones for the meantime but can adapt for automated/larger scale queries in future...
Author: A. Kate Falà
Date: 02/03/23
"""

import unipressed
from unipressed import UniprotkbClient
import pandas as pd

#fetch entry
entry="P11553"
ret = UniprotkbClient.fetch_one(entry, format="json")

#fetch query 1
q1=ret['proteinDescription']['recommendedName']['fullName']['value']
#fetch query 2
q2=ret['organism']['scientificName']
#fetch query 3
df=pd.json_normalize(ret["uniProtKBCrossReferences"])
q3=df[df['database'].str.match('OpenTargets')].id.to_string(index=False)

#write results to file
outF = open("myOutFile.txt", "a")
outF.write(entry+"\n"+q1+"\n"+q2+"\n"+q3+"\n")
outF.close()

#######################
#Useful addendum for future adaptations...
#figuring out structure
#ret["primaryAccession"]
#print keys on top level
#keylist = ret.keys()
#print(keylist)
#print all keys all levels
#for key, value in ret.items():
#	print(key)
