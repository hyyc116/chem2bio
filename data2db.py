#coding:utf-8

import sys
from util import *
import json
import urllib2

def store_data(path):
    #https://pubchem.ncbi.nlm.nih.gov/compound/11824
    entity_id = json.loads(open(path).read()) 

    insert_op = dbop()
    insert_pair = dbop()
    sql="insert into generalobj(id,name,type) values(%s,%s,%s)"
    pair_sql = "insert into pair(obj1_id,obj2_id,score) values(%s,%s,%s)"
    for line in open(path):
        line = line.strip()
        e1,r1,e2 = line.split('\t')

        o1 = name_type(e1)
        o2 = name_type(e2)

        if o1!=-1 and o2!=-1:
            # print 
            insert_op.batch_insert(sql,[e1,o1[0],o1[1]],5000,is_auto=False)
            insert_op.batch_insert(sql,[e2,o2[0],o2[1]],5000,is_auto=False)

            insert_pair.batch_insert(pair_sql,[e1,e2,2],5000,is_auto=False)
            insert_pair.batch_insert(pair_sql,[e2,e1,2],5000,is_auto=False)

    insert_op.batch_insert(sql,None,5000,end=True)
    insert_pair.batch_insert(pair_sql,None,5000,end=True)
    
    insert_pair.close_db()
    insert_op.close_db()



def name_type(e):
    if 'http://chem2bio2rdf.org/pubchem/resource/pubchem_compound/' in e :
        return e.replace('http://chem2bio2rdf.org/pubchem/resource/pubchem_compound/',''),'Compound'

    elif 'http://chem2bio2rdf.org/uniprot/resource/gene/' in e:
        return e.replace('http://chem2bio2rdf.org/uniprot/resource/gene/',''),"Protein"

    else:

        return -1




def get_name(cid):
    url='https://pubchem.ncbi.nlm.nih.gov/compound/{:}'.format(cid)
    response = urllib2.urlopen(url)
    html = response.read()
    ls

