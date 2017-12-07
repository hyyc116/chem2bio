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
    sql="insert into generalobj(id,name,type,otherid) values(%s,%s,%s,%s) on duplicate key update name=values(name),type=values(type),otherid=values(otherid)"
    pair_sql = "insert into pair(obj1_id,obj2_id,score) values(%s,%s,%s)"

    progress=0
    for line in open(path):
        line = line.strip()
        e1,r1,e2 = line.split('\t')

        o1 = name_type(e1)
        o2 = name_type(e2)
        # if progress%1000==0:
        #     logging.info('Progress {:}'.format(progress))
        # progress+=1
        if o1!=-1 and o2!=-1:

            obj1 = get_obj(o1,entity_id)
            obj2 = get_obj(o2,entity_id)

            if obj1==None or obj2==None:
                continue

            # print obj1[0],obj2[0]
            insert_op.batch_insert(sql,obj1,50000,is_auto=False)
            insert_op.batch_insert(sql,obj2,50000,is_auto=False)


            insert_pair.batch_insert(pair_sql,[obj1[0],obj2[0],2],50000,is_auto=False)
            insert_pair.batch_insert(pair_sql,[obj2[0],obj1[0],2],50000,is_auto=False)

    insert_op.batch_insert(sql,None,5000,end=True)
    insert_pair.batch_insert(pair_sql,None,5000,end=True)

    insert_pair.close_db()
    insert_op.close_db()

def get_obj(o1,entity_id):
    pid,t = o1
    if t=='Compound':
        obj_id = entity_id.get(pid,-1)
        if obj_id ==-1:
            return None
        name=pid
        ## run later
        #name = retreive_name(pid)
        return [obj_id,name,t,pid]

    elif t=='Protein':
        obj_id = entity_id.get(pid,-1)
        if obj_id==-1:
            return None
        name = pid
        return [obj_id,name,t,pid]


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


def update_name():
    query_op = dbop()
    insert_op = dbop()
    sql='select id,otherid,type from generalobj'
    insert_sql = 'insert into generalobj(id,name,otherid) values(%s,%s,%s) on duplicate key update name=values(name)'
    cursor = query_op.query_database(sql)
    progress=0
    for gid,otherid,t in cursor:
        if t=='Compound':
            logging.info('Progress {:} ..'.format(progress))
            name = retreive_name(otherid)
            insert_op.batch_insert(insert_sql,[gid,name,otherid],5000,is_auto=False)

    insert_op.batch_insert(insert_sql,None,5000,end=True)
    query_op.close_db()
    insert_op.close_db()

if __name__ == '__main__':
    # store_data(sys.argv[1],sys.argv[2])
    # retreive_name(118244)


