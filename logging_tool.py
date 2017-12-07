#coding:utf-8
'''the logging module'''
'''Yong Huang @ 19:51 02-24-2017 '''
import logging
from datetime import datetime

#logging file
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

class progress_logger:
    '''logger used to generate log'''

    def __init__(self,step,op):
        self._index=0
        self._step=step
        self._op=op
        logging.info("OPERATION:{:} starting...".format(self._op))
        self._starttime=datetime.now()
        self._steptime =self._starttime

    def reset(self,step):
        self._step=step
        self._starttime=datetime.now()
        self._steptime=self._starttime

    def step(self):
        self._index+=1
        if self._index%self._step==1:
            now = datetime.now()
            used_sec =(now-self._steptime).seconds
            self._steptime=now
            logging.debug("PROGRESS: {:}, time: {:.5f} seconds per step".format(self._index,used_sec/self._step))
            
    def end(self):
        now = datetime.now()
        used_sec = (now-self._starttime).seconds
        logging.info("OPERATION:{:} ending, time:{:.5f}...".format(self._op,used_sec))

    