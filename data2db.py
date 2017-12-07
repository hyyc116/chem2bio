#coding:utf-8

import sys
from util import *
import json
import urllib2
from bs4 import BeautifulSoup

def store_data(path,entity_path):
    #https://pubchem.ncbi.nlm.nih.gov/compound/11824
    entity_id = json.loads(open(entity_path).read()) 

    insert_op = dbop()
    insert_pair = dbop()
    sql="insert into generalobj(id,name,type,otherid) values(%s,%s,%s,%s)"
    pair_sql = "insert into pair(obj1_id,obj2_id,score) values(%s,%s,%s)"
    for line in open(path):
        line = line.strip()
        e1,r1,e2 = line.split('\t')

        o1 = name_type(e1)
        o2 = name_type(e2)

        if o1!=-1 and o2!=-1:

            pid,t = o1
            if t=='Compound':
                obj_id = entity_id[pid]
                name = retreive_name(pid)
                insert_op.batch_insert(sql,[obj_id,name,t,pid],5000,is_auto=False)

            elif t=='Protein':
                obj_id2 = entity_id[pid]
                name = pid
                insert_op.batch_insert(sql,[obj_id2,name,t,obj_id],5000,is_auto=False)

            insert_pair.batch_insert(pair_sql,[obj_id,obj_id2,2],5000,is_auto=False)
            insert_pair.batch_insert(pair_sql,[obj_id2,obj_id,2],5000,is_auto=False)

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

def retreive_name(pid):
    url = 'https://pubchem.ncbi.nlm.nih.gov/compound/{:}'.format(pid)
    response = urllib2.urlopen(url)
    html = response.read()
    # print html
    soup = BeautifulSoup(html,'lxml')
    name = soup.select('head title')[0].get_text().split('|')[0]
    return name



if __name__ == '__main__':
    store_data(sys.argv[1],sys.argv[2])
    # retreive_name(118244)


