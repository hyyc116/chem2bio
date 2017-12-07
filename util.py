#coding:utf8
'''Some common tools'''
'''Yong Huang @ 10:35 02-24-2017 '''
import MySQLdb
from MySQLdb import cursors
from logging_tool import *
import sys
from collections import defaultdict
import re
import codecs
import random as rn

class dbop:

    def __init__(self,insert_index=0,isSS=False):
        
        if isSS:
            logging.debug("connect database with normal SScursor.")
            self._db = MySQLdb.connect("localhost","root","irlab2013","chem2biosys",cursorclass = cursors.SSCursor)
        else:
            logging.debug("connect database with normal cursor.")
            self._db = MySQLdb.connect("localhost","root","irlab2013","chem2biosys")    
        self._cursor = self._db.cursor()
        
        self._insert_index=insert_index
        self._insert_values=[]


    def query_database(self,sql):
        self._cursor.close()
        self._cursor = self._db.cursor()
        self._cursor.execute(sql)
        logging.debug("query database with sql {:}".format(sql))
        return self._cursor

    def insert_database(self,sql,values):
        self._cursor.close()
        self._cursor = self._db.cursor()
        self._cursor.executemany(sql,values)
        logging.debug("insert data to database with sql {:}".format(sql))
        self._db.commit()
        

    def batch_insert(self,sql,row,step,is_auto=True,end=False):
        if end:
            if len(self._insert_values)!=0:
                logging.info("insert {:}th data into database,final insert, of {:}".format(self._insert_index,sql))
                self.insert_database(sql,self._insert_values)
        else:
            self._insert_index+=1
            if is_auto:
                row[0] = self._insert_index
            self._insert_values.append(tuple(row))
            if self._insert_index%step==0:
                logging.info("insert {:}th data into database, sql = {:}".format(self._insert_index,sql))
                self.insert_database(sql,self._insert_values)
                self._insert_values=[]

    def get_insert_count(self):
        return self._insert_index

    def execute_del_update(self,sql):
        self._cursor.execute(sql)
        self._db.commit()
        logging.debug("execute delete or update sql {:}.".format(sql))

    def execute_sql(self,sql):
        self._cursor.execute(sql)
        self._db.commit()
        logging.debug("execute sql {:}.".format(sql))

    def close_db(self):
        self._db.close()


def export_table(table,splitor='\t'):
    column_sql = "select COLUMN_NAME from information_schema.COLUMNS  where table_name = '{:}'  and table_schema = 'hdata'".format(table)
    sql = 'select * from {:}'.format(table)
    query_op = dbop()
    cursor = query_op.query_database(column_sql)
    columns=[]
    for name in cursor:
        columns.append(name[0])

    lines=[]
    header = splitor.join(columns)
    print header,len(columns)
    lines.append(header)
    cursor = query_op.query_database(sql)
    for row in cursor:
        # print row
        if len(row)!=len(columns):
            print row
        line = splitor.join([re.sub(r"\s+",'',str(i)).decode('utf-8').replace(',','#') for i in row])
        line = line.encode('utf-8')
        lines.append(line)

    open('/Users/huangyong/Downloads/{:}.txt'.format(table),'w').write('\n'.join(lines)) 
    return len(columns) 

def check_columns_length(path,length,splitor='\t'):
    count = 0
    for line in open(path):
        line = line.strip()
        if len(line.split(splitor))!=length:
            print line,len(line.split(splitor))
            count+=1

    print 'Number of error lines:',count

def export_and_check(table,splitor=','):
    print 'check table:',table
    path = '/Users/huangyong/Downloads/{:}.txt'.format(table)
    length= export_table(table,splitor)
    check_columns_length(path,length,splitor)

if __name__=="__main__":
    export_and_check('m_car_info')
    export_and_check('m_car_details')
    export_and_check('order_trace')

    



    












