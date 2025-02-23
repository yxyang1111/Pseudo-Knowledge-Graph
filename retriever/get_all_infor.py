import jsonlines
import glob
import spacy
from tqdm import tqdm
import re
from collections import Counter
import json
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
import numpy as np
import argparse
import sys


from retriever.pkg_get_entity import encode_entity, get_entity_spacy, get_entity_embedding, get_content_embedding, get_entity_llm
from retriever.pkg_get_infor import get_infor_ent, get_infor_embedding, get_node_metapath, search_metapath, search_metapaths

import sys
sys.path.append("..//")
from config.config import Embedding_model_path, neo4j_auth, neo4j_uri, Data_path


# 获得的信息有三类，节点，content，关系

def get_all_infor(user_query, uri = neo4j_uri, auth = neo4j_auth):
    all_infor = []
    entities = []
    entity_spacy = get_entity_spacy(user_query)
    entity_embedding = get_entity_embedding(user_query)
    entities = list(set(entity_spacy) | set(entity_embedding))
    # all_infor += entities

    content_embeddding = get_content_embedding(user_query)
    content_entity = get_infor_ent(entities)


    all_infor.append(list(set(content_embeddding) | set(content_entity)))

    content_metapath = []

    for entity in entities:
        meta_paths = get_node_metapath(entity)
        content_metapath += search_metapaths(entity, meta_paths)

    all_infor.append(content_metapath)
    # print(all_infor)
    return all_infor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve information based on user query.")
    parser.add_argument("user_query", type=str, help="The user query to process.")
    args = parser.parse_args()

    result = get_all_infor(args.user_query)
    print(result)