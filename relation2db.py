#coding:utf-8

import sys
from util import *
import json
import urllib2
from bs4 import BeautifulSoup
import time

def update_pair():

    query_op = dbop()
    sql="select id from generalobj"
    all_ids=set()
    for row in query_op.query_database(sql):
        all_ids.add(row[0])
    query_op.close_db()

    insert_pair = dbop()
    pair_sql = "insert into pair(obj1_id,obj2_id,score) values(%s,%s,%s)"

    for line in open('data/all_sim.txt'):
        line = line.strip()
        if len(line.split(","))!=3:
            continue
        id1,id2,score = line.split(',')

        if id1 is not in all_ids or id2 is not in all_ids:
            continue 


        if float(score) > 0.5:
            try:
                insert_pair.batch_insert(pair_sql,[id1,id2,float(score)],50000,is_auto=False)
                insert_pair.batch_insert(pair_sql,[id2,id1,float(score)],50000,is_auto=False)
            except:
                continue

    insert_pair.batch_insert(pair_sql,None,50000,end=True)
    insert_pair.close_db()


if __name__ == '__main__':
    update_pair()

