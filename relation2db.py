#coding:utf-8

import sys
from util import *
import json
import urllib2
from bs4 import BeautifulSoup
import time

def update_pair():
    insert_pair = dbop()
    pair_sql = "insert into pair(obj1_id,obj2_id,score) values(%s,%s,%s)"

    for line in open('data/all_sim.txt'):
        line = line.strip()
        if len(line.split(","))!=3:
            continue
        id1,id2,score = line.split(',')

        if float(score) > 0.5:
            insert_pair.batch_insert(pair_sql,[id1,id2,float(score)],50000,is_auto=False)
            insert_pair.batch_insert(pair_sql,[id2,id1,float(score)],50000,is_auto=False)

    insert_pair.batch_insert(pair_sql,None,5000,end=True)
    insert_pair.close_db()


if __name__ == '__main__':
    update_pair()

