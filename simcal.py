#coding:utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scipy.spatial.distance import cosine as cos_sim


def emd_sim(emd_path):
    emd_file = open(emd_path)
    emd_dict = {}
    print  emd_file.readline().strip()
    for line in emd_file:
        line = line.strip()
        splits = line.split()
        emd_dict[int(splits[0])] = [float(i) for i in splits[1:]]


    ids = emd_dict.keys()
    for i,emd_id in enumerate(ids):
        j=i+1
        while j<len(ids):
            emd_id2 = ids[j]

            print "{:},{:},{:}".format(emd_id,emd_id2,cos_sim(emd_dict[emd_id],emd_dict[emd_id2]))

if __name__ == '__main__':
    emd_sim(sys.argv[1])