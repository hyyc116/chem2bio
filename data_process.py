#coding:utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def generate_edges(path):
    
    entity_list = set()
    relation_list = set()

    relation_id = {}
    entity_id = {}
    for line in open(path):
        line = line.strip()
        e1,r,e2 = line.split('\t')

        if e1 not in entity_list:
            entity_list.add(e1)
            entity_id[e1] = len(entity_list)


        if e2 not in entity_list:
            entity_list.add(e2)
            entity_id[e2] = len(entity_list)

        if r not in relation_list:
            relation_list.add(r)
            relation_id[r] = len(relation_list)

    open('data/entity_id.json','w').write(json.dumps(entity_id).decode('utf-8',errors='ignore'))
    open('data/relation_id.json','w').write(json.dumps(relation_id).decode('utf-8'),errors='ignore')

    lines = []
    for line in open(path):
        line = line.strip()
        e1,r,e2 = line.split('\t')
        line = '{:} {:}'.format(entity_id[e1],entity_id[e2])

        lines.append(line)

    open('data/trans_data.txt','w').write('\n'.join(lines))


if __name__ == '__main__':
    generate_edges(sys.argv[1])





