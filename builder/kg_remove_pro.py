import jsonlines
import glob
import spacy
from tqdm import tqdm
import re
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
#'http://localhost:7474'
driver = GraphDatabase.driver(uri, auth=("neo4j", "s3cretPassword"))
with driver.session() as session:
    query = "MATCH (n) WHERE n.text = $node_name REMOVE n.meta_path"
    session.run(query, node_name="罗国杰")