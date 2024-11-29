import jsonlines
import glob
import spacy
from tqdm import tqdm
import re
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

import sys
sys.path.append("..//")
from config.config import Embedding_model_path, neo4j_auth, neo4j_uri, Data_path, Spacy_name

model_path = Embedding_model_path
model = SentenceTransformer(model_path)

driver = GraphDatabase.driver(uri = neo4j_uri, auth = neo4j_auth)

nlp = spacy.load(Spacy_name)

def get_entity_spacy(user_query):
    doc = nlp(user_query)
    entity_list = []
    for ent in doc.ents:
        if ent not in entity_list:
            #print(ent)
            entity_list.append(ent.text)

    #print(entity_list)
    return entity_list


def get_entity_llm(user_query):
    entity_list = []
    return entity_list

def get_entity(user_query):
    entity_list = get_entity_spacy(user_query) + get_entity_llm(user_query)
    return entity_list