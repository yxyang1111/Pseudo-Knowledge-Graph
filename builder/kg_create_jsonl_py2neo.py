import jsonlines
import glob

from py2neo import Graph, Node, Relationship
from py2neo import NodeMatcher, RelationshipMatcher
import spacy
from tqdm import tqdm
import re

from sentence_transformers import SentenceTransformer
model_path='/home/user/embeddings/bge_keyworkds_projectName_fields_tunning_v3'
model = SentenceTransformer(model_path)


graph=Graph('http://localhost:7474',user='neo4j',password='s3cretPassword')
node_matcher = NodeMatcher(graph)

data_dir = '/home/user/test_retrieval/data/*.jsonl'
for file_path in glob.glob(data_dir, recursive=True):
    print(file_path)
    with jsonlines.open(file_path, 'r') as reader:
        for json_obj in tqdm(reader):
            # 处理或打印每个JSON对象
            #print(json_obj['metadata'])
            existing_node = node_matcher.match("CONTENT",text=json_obj['content']).first()
            if not existing_node:
                vec = model.encode(json_obj['content'], normalize_embeddings=False).tolist()
                content_node=Node("CONTENT", text=json_obj['content'], embedding = vec)
                graph.create(content_node)
                for key, value in json_obj['metadata'].items():
                    #print(f"Key: {key}, Value: {value}")
                    if value != "":
                        patterns = r'。|？|！|（|）|；|\r|; '
                        items = re.split(patterns,value)

                        for item in items:
                            if item!='':
                                existing_node = node_matcher.match(key,text=item).first()
                                if not existing_node:
                                    vec = model.encode(item, normalize_embeddings=False).tolist()
                                    ent_node=Node(key,text=item,embedding = vec)


                                    graph.create(ent_node)
                                    relation=Relationship(content_node,"include",ent_node)
                                    graph.create(relation)
                                else:
                                    relation=Relationship(content_node,"include",existing_node)
                                    graph.create(relation)

