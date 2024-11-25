import jsonlines
import glob
import spacy
from tqdm import tqdm
import re
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

model_path = '/home/user/embeddings/bge_keyworkds_projectName_fields_tunning_v3'
model = SentenceTransformer(model_path)

uri = "bolt://localhost:7687"
#'http://localhost:7474'
driver = GraphDatabase.driver(uri, auth=("neo4j", "s3cretPassword"))
with driver.session() as session:
    # 删除所有节点和关系
    session.run("MATCH (n) DETACH DELETE n")