#coding:utf-8

import sys
from util import *
import json
import urllib2

def store_data(path):
    #https://pubchem.ncbi.nlm.nih.gov/compound/11824
    entity_id = json.loads(open(path).read()) 

    for line in open(path):
        line = line.strip()
        e1,r1,e2 = line.split('\t')

        if e1.startswith('http://chem2bio2rdf.org/pubchem/resource/pubchem_compound/'):
            nid = e.replace('http://chem2bio2rdf.org/pubchem/resource/pubchem_compound/','')
            cid = entity_id[nid]
            name = 


def get_name(cid):
    url='https://pubchem.ncbi.nlm.nih.gov/compound/{:}'.format(cid)
    response = urllib2.urlopen(url)
    html = response.read()
    

