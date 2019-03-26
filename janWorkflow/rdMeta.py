#!/usr/bin/env python
from ruamel.yaml import YAML
from pprint import pprint
import sys

def read_yaml(yaml_fn,verb=1):
        data={}

        if verb:  print('  read  yaml:',yaml_fn)
        with open(yaml_fn) as yamlfile:
            for key, val in YAML().load(yamlfile).items():
                print('hpar:',key, val)
                data[key]=val
        assert len(data['namePar']) == len(data['unitPar'])
        assert len(data['physPar']) == len(data['unitPar'])

        return data



# = = = = = = = = = = = = =
# = = = = = = = = = = = = =
if __name__ == '__main__':

    print('inp num args:',len(sys.argv))
    #ymlF='../janWorkflow/out/cosmoMeta.yaml'
    ymlF='./cosmoMeta.yaml'
    if len(sys.argv)>1:
        ymlF=sys.argv[1]
    print ("read YAML from ",ymlF,' and pprint it:')

    blob=read_yaml(ymlF)
    pprint(blob)

    assert len(blob['namePar']) == len(blob['unitPar']) 
    assert len(blob['physPar']) == len(blob['unitPar']) 


