import jsonlines
import glob
import spacy
from tqdm import tqdm
import re
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

import sys
sys.path.append("..//")
from config.config import Embedding_model_path, neo4j_auth, neo4j_uri

model_path = Embedding_model_path
model = SentenceTransformer(model_path)


driver = GraphDatabase.driver(uri = neo4j_uri, auth = neo4j_auth)
with driver.session() as session:
    # 删除所有节点和关系
    session.run("MATCH (n) DETACH DELETE n")