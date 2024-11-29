# -*- coding: utf-8 -*-

import py2neo
from py2neo import Graph, Node, Relationship
from py2neo import NodeMatcher, RelationshipMatcher
import csv

import spacy
from spacy import displacy
import glob
from tqdm import tqdm
import re

# 连接数据库，一定要加name指定数据库
g=Graph('http://localhost:7474',user='neo4j',password='cecaceca512',name='neo4j')
g.delete_all()

nlp = spacy.load("zh_core_web_md")
path = './txt/*.txt'
# path = '/home/yuxin.yang/txt/*.txt'


patterns = r'。|？|！|（|）'

for file in glob.glob(path):
    with open(file, 'r', encoding='utf-8', errors='ignore') as file_in:
        text = file_in.read()
        #print(text)
        text=text.replace('\n','')
        lines = re.split(patterns,text)
        print(lines)
        for line in tqdm(lines):
            print(line)
            line_node=Node("TEXT",text=line)
            g.merge(line_node,"TEXT","text")
            if line!='':
                doc=nlp(line)
                # for token in doc:
                #     #print(token.text,token.pos_,token.tag_)
                #     print(token.text,token.dep_,token.head)
                # for chunk in doc.noun_chunks:
                #     print(chunk.text)
                print("===========================")
                for ent in doc.ents:
                    print (ent.text, ent.label_)
                    ent_node=Node(ent.label_,text=ent.text)
                    g.merge(ent_node,ent.label_,"text")
                    relation=Relationship(line_node,"include",ent_node)
                    g.create(relation)



