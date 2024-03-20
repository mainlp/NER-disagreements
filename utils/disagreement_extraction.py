# NOTE: each annotation file has a column of tokens and a column of NER-tags, AND the num of rows of two files should be the same
from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def get_sentence(entity_ix1,entity_ix2,file_path):
    """
    entity_ix: tuple(entity_first_ix,entity_last_ix)
    given a filepath and the line ix of the entity,
    retrieve the sentence where this entity is at
    """
    with open(file_path,'r') as f:
        lines = f.readlines()
    if entity_ix1[0]:
        start_ix,end_ix = entity_ix1[0]-1,entity_ix1[1]-1  # the start_ix is gonna be used to index the list of lines
    else:
        start_ix,end_ix = entity_ix2[0]-1,entity_ix2[1]-1
        # get to the start of the sentence
    current_start_ix = start_ix
    current_end_ix = end_ix
    # find beginning of the sentence
    while True:
        if lines[current_start_ix] == "\n" or current_start_ix == 0:
            break
        else:
            current_start_ix -= 1
    # find ending of the sentence
    while True:
        if lines[current_end_ix] == "\n" or current_end_ix == len(lines)-1:
            break
        else:
            current_end_ix += 1
    # put the sentence together
    tokens = []
    for line in lines[current_start_ix:current_end_ix+1]:
        tokens.append(line.strip().split('\t')[0])

    return " ".join(tokens)

def get_tag(ix_tuple1,ix_tuple2,filepath):
    """
    retrieve the tag from a filepath given its start ix and end ix
    """
    filepath = os.sep.join(filepath[0].split(os.sep)[:-2])+os.sep+'adj'+os.sep+filepath[0].split(os.sep)[-1]
    with open(filepath,'r') as f:
        lines = f.readlines()
    tag1,tag2 = [], []
    for line in lines[ix_tuple1[0]-1:ix_tuple1[1]]:
        _, tag = line.strip().split('\t')
        tag1.append(tag)
    for line in lines[ix_tuple2[0]-1:ix_tuple2[1]]:
        _, tag = line.strip().split('\t')
        tag2.append(tag)

    return tag1,tag2


def extract_disagreement(file1,file2):
    """
    len(file1) must be the same as len(file2)
    """
    out_dict = {dis_type:[] for dis_type in ['full_disagreement','partial_disagreement','o_disagreement','including_disagreement']}
    with open(file1,'r') as f1:
        f1_lines = f1.readlines()
    with open(file2,'r') as f2:
        f2_lines = f2.readlines()

    # flags
    def choose_type(memory_list):
        entity1, entity2,ner_type1, ner_type2 = memory_list[0],memory_list[1],memory_list[2],memory_list[3]
        span_start1,span_end1 = entity1
        span_start2,span_end2 = entity2
        if span_start1==span_start2 and span_end1 == span_end2 and ner_type1 != ner_type2:
            return 'full_disagreement'
        elif span_start1==span_start2 and span_end1 == span_end2 and ner_type1 == ner_type2:
            # agreement
            return None
        elif span_start1==span_end1==0 or span_start2==span_end2==0:
            return "o_disagreement"
        elif span_start1<=span_start2<=span_end2<=span_end1 or span_start2<=span_start1<=span_end1<=span_end2:
            return 'including_disagreement'
        elif span_start1<=span_start2<=span_end1<=span_end2 or span_start2<=span_start1<=span_end2<=span_end1:
            return 'partial_disagreement'
        else:
            print('situations not cosindered: ')
            print(memory_list)
            return False

    def check4saving(memory_list):
        tosave = []
        for memory_unit in memory_list:
            if isinstance(memory_unit[0],tuple) and isinstance(memory_unit[1],tuple):
                tosave.append(memory_unit)
                memory_list.remove(memory_unit)
        if tosave:
            for dis in tosave:
                # remove empty strings
                dis[-2] = [t for t in dis[-2] if t]
                dis[-1] = [t for t in dis[-1] if t]
                dis_type = choose_type(dis)
                # save memory
                if dis_type is not None:
                    out_dict[dis_type].extend([dis])

    def register(memory_list,span_ix1=0,span_ix2=0,nertypes1_2 = [],tokens1_2=[],finish=(False,False)):
        def new_memory4entity(memory_list):
            if not len(memory_list):
                return True
            elif (isinstance(memory_list[-1][0],tuple) and span_ix1) or (isinstance(memory_list[-1][1],tuple) and span_ix2):
                return True
            else:
                return False
        # freeze the finished entities
        finish_left,finish_right=finish
        if finish_left and finish_right:
            for unit in memory_list:
                unit[0],unit[1] = tuple(unit[0]), tuple(unit[1])
        elif finish_left:
            for unit in memory_list:
                if unit[0] != [0,0]:
                    unit[0]=tuple(unit[0])
        elif finish_right:
            for unit in memory_list:
                if unit[1] != [0,0]:
                    unit[1]=tuple(unit[1])

        # add new memory for entity if needed
        if new_memory4entity(memory_list) and (span_ix1 or span_ix2):  # at least one span ix for one entity is given, otherwise it is O O
            new_entity = [[span_ix1,span_ix1],[span_ix2,span_ix2],nertypes1_2[0],nertypes1_2[1],[],[]]
            # inherit from previous not finished entity's start index and their tokens
            if len(memory_list) > 0 and not isinstance(memory_list[-1][0],tuple):  # the memory must already have some entity units for new entity to inherit from
                if memory_list[-1][0][0]:  # if not 0
                    new_entity[0][0],new_entity[4] = memory_list[-1][0][0], memory_list[-1][4].copy()
                else:  # if 0
                    new_entity[4]=memory_list[-1][4].copy()
            if len(memory_list) > 0 and not isinstance(memory_list[-1][1],tuple):
                if memory_list[-1][1][0]:
                    new_entity[1][0],new_entity[5] = memory_list[-1][1][0], memory_list[-1][5].copy()
                else:
                    new_entity[5]=memory_list[-1][5].copy()
            memory_list.append(new_entity)

        # update the end_ix and token list of all the unfinished entities in the memory
        for entity_unit in memory_list:
            if not isinstance(entity_unit[0],tuple):
                if not entity_unit[0][0]:
                    entity_unit[0][0] = span_ix1
                    entity_unit[2]=nertypes1_2[0]
                entity_unit[0][1] = span_ix1
                entity_unit[4].append(tokens1_2[0])
            if not isinstance(entity_unit[1],tuple):
                if not entity_unit[1][0]:
                    entity_unit[1][0] = span_ix2
                    entity_unit[3]=nertypes1_2[1]
                entity_unit[1][1] = span_ix2
                entity_unit[5].append(tokens1_2[1])

    # memory
    memory = []
    # dis_sample = [['',''],['',''],"","",[],[]]  # [[ix_start,ix_end],[ix1_start_prime,ix2_end_prime],ner_type1, ner_type2,[ner1],[ner2]]


    for line_ix,(line1, line2) in enumerate(zip(f1_lines,f2_lines)):
        line_ix += 1
        if line1 != "\n" and line2 != "\n":
            comps1 = line1.strip().split("\t")
            comps2 = line2.strip().split("\t")
            token1, tag1 = comps1[0],comps1[1]
            token2, tag2 = comps2[0],comps2[1]

            # check types
            # O + O
            if tag1==tag2=="O":
                register(memory, finish=(True,True))
                check4saving(memory)
            # possibilities: full dis. / agreement / include
            # B+B / B+I / I+B / I+I
            elif tag1 != "O" and tag2 !="O":
                # B + B
                if tag1[0] == "B" and tag2[0] == "B":
                    register(memory,span_ix1=line_ix,span_ix2=line_ix,nertypes1_2=[tag1.split('-')[-1],tag2.split('-')[-1]],tokens1_2=[token1,token2], finish=(True,True))
                    check4saving(memory)
                # I + I
                elif tag2[0]==tag1[0]=="I":
                    register(memory,span_ix1=line_ix,span_ix2=line_ix,nertypes1_2=[tag1.split('-')[-1],tag2.split('-')[-1]],tokens1_2=[token1,token2])
                    check4saving(memory)
                # B+I
                elif tag1[0]=="B" and tag2[0]=="I":
                    register(memory,span_ix1=line_ix,span_ix2=line_ix,nertypes1_2=[tag1.split('-')[-1],tag2.split('-')[-1]],tokens1_2=[token1,token2],finish=(True,False))
                    check4saving(memory)
                # I + B
                else:
                    register(memory,span_ix1=line_ix,span_ix2=line_ix,nertypes1_2=[tag1.split('-')[-1],tag2.split('-')[-1]],tokens1_2=[token1,token2],finish=(False,True))
                    check4saving(memory)

            # possibilities: partial / o_dis
            # B+O / O+B / I+O / O+I
            elif tag1 != "O" or tag2 != "O":
                if tag1[0]=="B":  # B O
                    register(memory,span_ix1=line_ix,span_ix2=0,nertypes1_2=[tag1.split('-')[-1],""],tokens1_2=[token1,""],finish=(True,True))
                    check4saving(memory)
                elif tag2[0]=="B":
                    register(memory,span_ix1=0,span_ix2=line_ix,nertypes1_2=["",tag2.split('-')[-1]],tokens1_2=["",token2],finish=(True,True))
                    check4saving(memory)
                elif tag1[0] == "I":
                    register(memory,span_ix1=line_ix,span_ix2=0,nertypes1_2=[tag1.split('-')[-1],""],tokens1_2=[token1,""],finish=(False,True))
                    check4saving(memory)
                elif tag2[0] == "I":
                    register(memory,span_ix1=0,span_ix2=line_ix,nertypes1_2=["",tag2.split('-')[-1]],tokens1_2=["",token2],finish=(True,False))
                    check4saving(memory)

    return out_dict


def create_disagreement_df(src_folder,domain_list,annotator_list,datasplit=['train','dev','test']):
    annotator_files = []
    for domain in domain_list:
        files = defaultdict(list)
        for annotator in annotator_list:
            for split in datasplit:
                files[annotator].append(src_folder+os.sep+domain+os.sep+annotator+os.sep+split+".tsv")
        annotator_files.extend(list(zip(*files.values())))

    df = pd.DataFrame(columns=['disagreement type',
                               'entity indices annotation1',
                               'entity indices annotation2',
                               'entity type1',
                               'entity type2',
                               'entity tokens1',
                               'entity tokens2',
                               'context sentence',
                               'domain',
                               'filepath'])

    for files_tuple in annotator_files:
        disagreement_dict = extract_disagreement(*files_tuple)
        for dis_type in disagreement_dict:
            if disagreement_dict[dis_type]:
                for row in disagreement_dict[dis_type]:
                    # get domain
                    domain = files_tuple[0].split(os.sep)[-3]
                    new_row = pd.DataFrame(
                        {
                            'disagreement type':[dis_type],
                            'entity indices annotation1':[row[0]],
                            'entity indices annotation2':[row[1]],
                            'entity type1':[row[2]],
                            'entity type2':[row[3]],
                            'entity tokens1':[row[4]],
                            'entity tokens2':[row[5]],
                            'context sentence':[None],
                            'domain':[domain],
                            'filepath':[files_tuple]
                        }
                    )
                    df = pd.concat([df,new_row],ignore_index=True)
    df['context sentence']=df.apply(lambda row:get_sentence(row['entity indices annotation1'],row['entity indices annotation2'],row['filepath'][0]),axis=1)
    return df

def get_disagreeement_df2files(file1,file2):
    """
    create disagreement df given two files
    """
    df = pd.DataFrame(columns=['disagreement type',
                               'entity indices annotation1',
                               'entity indices annotation2',
                               'entity type1',
                               'entity type2',
                               'entity tokens1',
                               'entity tokens2',
                               'context sentence',
                               'filepath'])
    disagreement_dict = extract_disagreement(file1,file2)
    for dis_type in disagreement_dict:
        if disagreement_dict[dis_type]:
            for row in disagreement_dict[dis_type]:
                # get domain
                new_row = pd.DataFrame(
                    {
                        'disagreement type':[dis_type],
                        'entity indices annotation1':[row[0]],
                        'entity indices annotation2':[row[1]],
                        'entity type1':[row[2]],
                        'entity type2':[row[3]],
                        'entity tokens1':[row[4]],
                        'entity tokens2':[row[5]],
                        'context sentence':[None],
                        'filepath':[tuple([file1,file2])]
                    }
                )
                df = pd.concat([df,new_row],ignore_index=True)
    df['context sentence']=df.apply(lambda row:get_sentence(row['entity indices annotation1'],row['entity indices annotation2'],row['filepath'][0]),axis=1)
    return df


def plot_disagreement_propotion(df,dimensions_list=['disagreement type'],ylabel='Disagreement Types',title='Proportion of Each Disagreement Type',threshold=0,savepath=None):
    data = defaultdict(int)

    for _,row in df.iterrows():
        keys = sorted([row[dim] for dim in dimensions_list])
        data["+".join(keys)] += 1
    if dimensions_list==["disagreement type"]:
        for dis_type in ['full_disagreement','o_disagreement','including_disagreement','partial_disagreement']:
            if dis_type not in data:
                data[dis_type]=0
    data = {k:v for k, v in sorted(data.items(), key=lambda item:item[1])}


    plot_data = {k:v for k,v in data.items() if v >=threshold}

    fig, ax = plt.subplots(figsize=(12,8))
    bars = ax.barh(list(plot_data.keys()),list(plot_data.values()),height=0.4)
    ax.margins(x=0.2)

    # add value numbers on the top of the bars
    for i, bar in enumerate(bars):
        value = (bar.get_width() / sum(data.values())) * 100  # proportion to all data
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, '{:.1f}% | {}'.format(value,bar.get_width()),
                va='center', ha='left', color='black')
    plt.ylabel(ylabel)
    plt.xlabel('Counts')
    plt.title(title)
    if savepath:
        plt.savefig(savepath+title+'.png',bbox_inches='tight')
    plt.show()


def sampling(num_samples,df,savepath=None):
    """
    num_samples: total number of samples wished; sampling after disagreement type proportion
    df: dataframe obtained from create_disagreement_df function
    savepath: path for saving the randomly selected samples

    return: saving an Excel file with two extra column: ['disagreement major type','disagreement subtypes']

    function usage: the user can annotate/eye-balling examples in the saved Excel. And Later analysis the Excel as Dataframe
    """
    # get the number of samples for each disagreement type
    num_dict = {}
    for dis_type in df['disagreement type'].unique():
        num_dict[dis_type] = round(num_samples * (len(df[df['disagreement type']==dis_type]) / len(df)))
    # out df
    new_df = pd.DataFrame(columns=list(df.columns)+['disagreement major type','disagreement subtypes'])
    # add samples to out df
    for dis_type in num_dict:
        new_df=pd.concat([new_df,df[df['disagreement type']==dis_type].sample(num_dict[dis_type])],ignore_index=True)
    if savepath:
        new_df.to_excel(savepath,index=False)
    return new_df



