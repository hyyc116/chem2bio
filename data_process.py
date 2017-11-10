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


    # open('data/entity_id.json','w').write(unicode(json.dumps(entity_id), errors='ignore'))
    # open('data/relation_id.json','w').write(unicode(json.dumps(relation_id), errors='ignore'))

    lines = []
    for line in open(path):
        line = line.strip()
        e1,r,e2 = line.split('\t')
        line = '{:} {:}'.format(entity_id[e1],entity_id[e2])

        lines.append(line)

    open('data/trans_data.txt','w').write('\n'.join(lines))

def get_node_id(compound_path,protein_path,path):
    entity_list = set()
    relation_list = set()

    relation_id = {}
    entity_id = {}
    for line in open(path):
        line = line.strip()
        e1,r,e2 = line.split('\t')
        e1 = e1.strip()
        r = r.strip()
        e2 = e2.strip()

        if e1 not in entity_list:
            entity_list.add(e1)
            entity_id[e1] = len(entity_list)


        if e2 not in entity_list:
            entity_list.add(e2)
            entity_id[e2] = len(entity_list)

        if r not in relation_list:
            relation_list.add(r)
            relation_id[r] = len(relation_list)

    compounds = [[line.strip().split(',')[1],line.strip().split(',')[2]] for line in open(compound_path)]
    proteins = [line.strip().split(',')[2] for line in open(protein_path)]

    compound_id_dict  = {}
    for compound,chemid in compounds:
        compound_url = 'http://chem2bio2rdf.org/pubchem/resource/pubchem_compound/'+chemid
        cid = entity_id.get(compound_url,-1)
        if cid !="-1":
            compound_id_dict[compound] = cid
        else:
            print 'Not found compound',compound

    protein_dict = {}
    for protein in proteins:
        protein_url = 'http://chem2bio2rdf.org/uniprot/resource/gene/'+protein
        pid = entity_id.get(protein_url,'-1')
        if pid!='-1':
            protein_dict[protein] = pid
        else:
            print 'Not found protein',protein

    open('data/compound_dict.json','w').write(json.dumps(compound_id_dict))
    open('data/protein_dict.json','w').write(json.dumps(protein_dict))

    # open('data/entity_id.json','w').write(json.dumps(entity_id))

def cal_sim_compund_protein(emd_path,compound_dict,protein_dict):
    emd_file = open(emd_path)
    emd_dict = {}
    print  emd_file.readline().strip()
    for line in emd_file:
        line = line.strip()
        splits = line.split()
        emd_dict[splits[0]] = splits[1:]

    ## get compound emd 
    compound_emd = {}
    emd_list = []
    labels = []
    for compound in compound_dict.keys():
        emd = emd_dict[compound_dict[compound]]
        compound_emd[compound] = emd
        emd_list.append(emd)
        labels.append(compound)

    protein_emd = {}
    for protein in protein_dict.keys():
        emd = emd_dict[protein_dict[protein]]
        protein_emd[protein] = emd
        emd_list.append(emd)
        labels.append(protein)

    emd_list = [' '.join([str(i) for i in emd]) for emd in emd_list]
    open('data/emd_list.txt','w').write('\n'.join(emd_list))
    open('data/labels.txt','w').write('\n'.join(labels))


if __name__ == '__main__':
    # generate_edges(sys.argv[1])
    # get_node_id(sys.argv[1],sys.argv[2],sys.argv[3])
    cal_sim_compund_protein(sys.argv[1],sys.argv[2],sys.argv[3])





