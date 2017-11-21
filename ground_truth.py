#coding:utf-8
#coding:utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scipy.spatial.distance import cosine as cos_sim
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter

def generate_id_dict(path):
    
    entity_list = set()
    relation_list = set()

    relation_id = {}
    entity_id = {}
    for line in open(path):
        line = line.strip()
        e1,r,e2 = line.strip().split('\t')

        if e1 not in entity_list:
            entity_list.add(e1)
            name = name_id(e1)
            if name !=-1:
                name = name.decode('utf8',errors='ignore')
                entity_id[name] = len(entity_list)


        if e2 not in entity_list:
            entity_list.add(e2)
            name = name_id(e2)
            if name !=-1:
                name = name.decode('utf8',errors='ignore')
                entity_id[name] = len(entity_list)

        if r not in relation_list:
            relation_list.add(r)
            # relation_id[r] = len(relation_list)


    open('data/entity_id.json','w').write(json.dumps(entity_id))
    # open('data/relation_id.json','w').write(unicode(json.dumps(relation_id), errors='ignore'))

def name_id(e):
    if 'http://chem2bio2rdf.org/pubchem/resource/pubchem_compound/' in e :
        return e.replace('http://chem2bio2rdf.org/pubchem/resource/pubchem_compound/','')

    elif 'http://chem2bio2rdf.org/uniprot/resource/gene/' in e:
        return e.replace('http://chem2bio2rdf.org/uniprot/resource/gene/','')

    else:

        return -1
## load id 
def groud_truth_cal(csv_file,emd_path,entity_id_path,outpath):
    ## entity 
    entity_id = json.loads(open(entity_id_path).read())

    emd_file = open(emd_path)
    emd_dict = {}
    print  emd_file.readline().strip()
    for line in emd_file:
        line = line.strip()
        splits = line.split()
        emd_dict[int(splits[0])] = [float(i) for i in splits[1:]]

    ### 
    results = []
    for line in open(csv_file):
        compund,protein,slapscore = line.strip().split(',')

        cid = entity_id.get(compund,-1)
        pid = entity_id.get(protein,-1)

        if cid!=-1 and pid != -1:
            sim_score = cos_sim(emd_dict[cid],emd_dict[pid])

        else:
            sime_score = None

        results.append('{:},{:},{:},{:}'.format(compund,protein,slapscore,sim_score))

    open(outpath,'w').write('\n'.join(results))


def plot_dis_result(positive,negative):
    scores = []
    for line in open(positive):
        lines = line.strip().split(',')
        num ='{:.1f}'.format(float(lines[-1]))
        scores.append(float(num))

    dis_counter = Counter(scores)
    xs= []
    ys = []
    for score in sorted(dis_counter.keys()):
        xs.append(score)
        ys.append(dis_counter[score])

    plt.figure()
    plt.bar(range(len(xs)),ys,align='center')
    plt.xticks(range(len(xs)),xs)
    plt.savefig('positive.pdf')

    scores = []
    for line in open(negative):
        lines = line.strip().split(',')
        num ='{:.1f}'.format(float(lines[-1]))
        scores.append(float(num))

    dis_counter = Counter(scores)
    xs= []
    ys = []
    for score in sorted(dis_counter.keys()):
        xs.append(score)
        ys.append(dis_counter[score])

    plt.figure()
    plt.bar(range(len(xs)),ys,align='center')
    plt.xticks(range(len(xs)),xs)
    plt.savefig('negative.pdf')

if __name__ == '__main__':
    # print 'generate entity id ...'
    # generate_id_dict(sys.argv[1])
    # print 'cal similarity ...'
    # groud_truth_cal(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    # print 'done'

    plot_dis_result(sys.argv[1],sys.argv[2])



















