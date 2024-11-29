import jsonlines
import glob
import spacy
from tqdm import tqdm
import re
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

import sys
sys.path.append("..//")
from config.config import Embedding_model_path, neo4j_auth, neo4j_uri, Data_path

model_path = Embedding_model_path
model = SentenceTransformer(model_path)

driver = GraphDatabase.driver(uri = neo4j_uri, auth = neo4j_auth)

data_dir = Data_path + "*.jsonl"
with driver.session() as session:
    query = "MATCH (n) WHERE n.text = $node_name REMOVE n.meta_path"
    session.run(query, node_name="x")