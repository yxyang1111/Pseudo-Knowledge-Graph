import jsonlines
import glob
import spacy
from tqdm import tqdm
import re
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
from fastapi import FastAPI
from pydantic import BaseModel

model_path = '/home/user/embeddings/bge_keyworkds_projectName_fields_tunning_v3'
model = SentenceTransformer(model_path)

uri = "bolt://localhost:7687"
#'http://localhost:7474'
driver = GraphDatabase.driver(uri, auth=("neo4j", "s3cretPassword"))

nlp = spacy.load("zh_core_web_trf")

def encode_entity(entity):
    return model.encode(entity, normalize_embeddings=False).tolist()

def get_entity_spacy(user_query):
    doc=nlp(user_query)
    entity_list=[]
    for ent in doc.ents:
        if ent not in entity_list:
            #print(ent)
            entity_list.append(ent.text)

    #print(entity_list)
    return entity_list

def get_entity_embedding(user_query, uri = "bolt://localhost:7687", auth = ("neo4j", "s3cretPassword")):
    entity_list=[]
    driver = GraphDatabase.driver(uri, auth = auth)
    with driver.session() as session:
        ent_vector = encode_entity(user_query)  # 编码实体以获取嵌入向量
        query = """
        MATCH (p)
        WHERE NOT (p:CONTENT) AND p.embedding IS NOT NULL 
        WITH p, gds.similarity.cosine(p.embedding, $query_vector) AS similarity_score
        WHERE similarity_score > 0.5
        RETURN p.text AS text, similarity_score AS score
        ORDER BY score DESC 
        LIMIT 10
        """
        results = session.run(query, query_vector=ent_vector)
        # 存储结果
        texts = [record['text'] for record in results]
        entity_list.extend(texts)
        #print(entity_list)
    driver.close()
    return entity_list

def get_content_embedding(user_query, uri = "bolt://localhost:7687", auth = ("neo4j", "s3cretPassword")):
    entity_list=[]
    driver = GraphDatabase.driver(uri, auth = auth)
    with driver.session() as session:
        ent_vector = encode_entity(user_query)  # 编码实体以获取嵌入向量
        query = """
        MATCH (p:CONTENT)
        WHERE p.embedding IS NOT NULL 
        WITH p, gds.similarity.cosine(p.embedding, $query_vector) AS similarity_score
        WHERE similarity_score > 0.5
        RETURN p.text AS text, similarity_score AS score
        ORDER BY score DESC 
        LIMIT 10
        """
        results = session.run(query, query_vector=ent_vector)
        # 存储结果
        texts = [record['text'] for record in results]
        entity_list.extend(texts)
        #print(entity_list)
    driver.close()
    return entity_list


def get_entity_llm(user_query):
    entity_list=[]
    return entity_list

# user_query="请帮我介绍一下罗国杰老师"
# print(get_entity_spacy(user_query))
# print(get_entity_embedding(user_query))
# print(get_content_embedding(user_query))

app = FastAPI()

class encode_entity_Params(BaseModel):
    entity: str

@app.post("/encode_entity/")
async def encode_entity_api(params: encode_entity_Params):
    result = encode_entity(
        entity=params.entity,
    )
    return result