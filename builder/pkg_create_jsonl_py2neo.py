import jsonlines
import glob

from py2neo import Graph, Node, Relationship
from py2neo import NodeMatcher, RelationshipMatcher
import spacy
from tqdm import tqdm
import re

from sentence_transformers import SentenceTransformer

import sys
sys.path.append("..//")
from config.config import Embedding_model_path, neo4j_auth, neo4j_uri, Data_path


model_path=Embedding_model_path
model = SentenceTransformer(model_path)


graph=Graph(neo4j_uri ,user=neo4j_auth[0],password=neo4j_auth[1])
node_matcher = NodeMatcher(graph)

data_dir = Data_path + "*.jsonl"
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

