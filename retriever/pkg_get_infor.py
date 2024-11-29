import jsonlines
import glob
import spacy
from tqdm import tqdm
import re
from collections import Counter
import json
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

import sys
sys.path.append("..//")
from config.config import Embedding_model_path, neo4j_auth, neo4j_uri, Data_path, Spacy_name

model_path = Embedding_model_path
model = SentenceTransformer(model_path)

driver = GraphDatabase.driver(uri = neo4j_uri, auth = neo4j_auth)

nlp = spacy.load(Spacy_name)

#找到entity相关的信息
def get_infor_ent(entity_list, uri = neo4j_uri, auth = neo4j_auth):
    infor=[]
    driver = GraphDatabase.driver(uri, auth = auth)
    with driver.session() as session:
        # 遍历 entity_list 中的每个实体
        for entity in entity_list:
            # 构建查询语句，找到与特定节点相连的节点
            query = (
                "MATCH (a)-[r]-(b) "
                "WHERE a.text = $entity "
                "RETURN b.text as text"
            )
            # 执行查询
            result = session.run(query, entity=entity)

            # 打印查询结果
            for record in result:
                connected_node = record['text']
                infor.append(connected_node)
                #print(f"Connected Node: {connected_node}")
    driver.close()
    return infor

def encode_entity(entity, model_path = Embedding_model_path):
    #model_path = '/home/user/embeddings/bge_keyworkds_projectName_fields_tunning_v3'
    model = SentenceTransformer(model_path)
    return model.encode(entity, normalize_embeddings=False).tolist()

def get_infor_embedding(entity_list, limited_num = 1, uri = neo4j_uri, auth = neo4j_auth):
    all_text = []
    driver = GraphDatabase.driver(uri, auth = auth)
    with driver.session() as session:
        for ent in entity_list:
            ent_vector = encode_entity(ent)  # 编码实体以获取嵌入向量
            query = """
            MATCH (p:CONTENT)
            WHERE p.embedding IS NOT NULL
            WITH p, gds.similarity.cosine(p.embedding, $query_vector) AS similarity_score
            WHERE similarity_score > 0.5
            RETURN p.text AS text, similarity_score AS score
            ORDER BY score DESC
            LIMIT limiti $limited_num
            """
            # 执行查询
            results = session.run(query, query_vector=ent_vector, limited_num = limited_num)
            # 存储结果
            texts = [record['text'] for record in results]
            all_text.extend(texts)
            #print(f"Found texts for entity '{ent}': {texts}")

    # 将所有文本结果合并为一个字符串
    driver.close()
    return all_text

def get_nodeid(node_name, uri = neo4j_uri, auth = neo4j_auth):
    node_id = -1    #如果找不到节点则返回-1
    driver = GraphDatabase.driver(uri, auth = auth)
    with driver.session() as session:
        query = "MATCH (n) WHERE n.text = $node_name RETURN n, id(n) AS node_id"
        results = session.run(query, node_name=node_name)
        for record in results:
            node = record["n"]
            node_id = record["node_id"]
            #print(f"Node: {node}, ID: {node_id}")
    driver.close()
    return node_id

def get_node(node_name, uri = neo4j_uri, auth = neo4j_auth):
    node = None
    driver = GraphDatabase.driver(uri, auth = auth)
    with driver.session() as session:
        query = "MATCH (n) WHERE n.text = $node_name RETURN n"
        results = session.run(query, node_name=node_name)
        for record in results:
            node = record["n"]
            # driver.close()
            # return node
    driver.close()
    return node


def create_node_metapath(entity, n = 3, uri = neo4j_uri, auth = neo4j_auth):
    meta_paths = []
    driver = GraphDatabase.driver(uri, auth = auth)
    with driver.session() as session:
        for i in range(1, n):
            query = """
            MATCH path = (n)-[*1..{}]-(m)
            WHERE ID(n) = $node_id
            RETURN path
            """.format(i)
            parameters = {'node_id': get_nodeid(entity)}
            results = session.run(query, **parameters)

            for record in results:
                path = record["path"]
                #print("Path nodes and their types:")
                meta_path=[]
                for node in path.nodes:
                    label = node.labels
                    #print(label)
                    clean_label = str(label).replace('frozenset({\'', '').replace('\'})','')
                    #print(clean_label)
                    meta_path.append(clean_label)
                meta_paths.append(meta_path)
        tuples = [tuple(sublist) for sublist in meta_paths]
        counter = Counter(tuples)
        str_keys_counter = {str(k): v for k, v in counter.items()}
        properties_json = json.dumps(str_keys_counter)
        #node = get_node(entity)
        #node["meta_path"] = properties_json
        #session.push(node)

        query_add_property  = "MATCH (n) WHERE n.text = $node_name SET n.meta_path = $new_value"
        session.run(query_add_property, node_name = entity, new_value = properties_json)

    driver.close()
    return json.loads(properties_json)



def get_node_metapath(entity, uri = neo4j_uri, auth = neo4j_auth):
    meta_paths = []
    driver = GraphDatabase.driver(uri, auth = auth)
    with driver.session() as session:
        query = "MATCH (n) WHERE n.text = $node_name RETURN n"
        results = session.run(query, node_name=entity)
        for record in results:
            meta_paths = record['n'].get('meta_path')
            if meta_paths is not None:
                meta_paths = json.loads(meta_paths)
            else:
                print("creating node metapaths...")
                meta_paths = create_node_metapath(entity)
    #print(meta_paths)
    driver.close()
    return meta_paths

#meta_path应该是一个节点label的list
def search_metapath(entity, meta_path, uri = neo4j_uri, auth = neo4j_auth):
    all_text = []
    all_text.append(meta_path)
    driver = GraphDatabase.driver(uri, auth = auth)
    with driver.session() as session:
        query = f"MATCH path = (n:{meta_path[0]})"
        for label in meta_path[1:]:
             query += f"-[*1]-(:{label})"
        query += f" WHERE n.text = $node_name RETURN path"
        print(query)
        results = session.run(query, node_name = entity)
        for record in results:
            path = record["path"]
            #print(path)
            text = []
            for node in path.nodes:
                #print(node["text"])
                text.append(node["text"])
            all_text.append(text)

    driver.close()
    return all_text

def search_metapaths(entity, meta_paths, uri = neo4j_uri, auth = neo4j_auth ):
    #print(type(meta_paths))
    if type(meta_paths) == str:
        meta_paths = json.loads(meta_paths)
    sorted_items = sorted(meta_paths.items(), key=lambda item: item[1], reverse=True)
    all_infor = []
    for item in sorted_items:
        key = item[0]
        value = item[1]
        # print(key, value)
        tuple_path = eval(key)
        list_path = list(tuple_path)
        #print(list_path)
        tmp_infor = search_metapath(entity, list_path, uri, auth)
        all_infor.append(tmp_infor)
    return all_infor



def get_relation(startNode, endNode, uri = neo4j_uri, auth = neo4j_auth ):
    node_infos = []
    driver = GraphDatabase.driver(uri, auth = auth)
    with driver.session() as session:
        query = """
        MATCH (a), (b)
        WHERE a.text = $startNode AND b.text = $endNode
        MATCH path = shortestPath((a)-[*]-(b))
        RETURN path
        """
        results = session.run(query, startNode = startNode, endNode = endNode)
        for record in results:
            path = record["path"]
            for node in path.nodes:
                label = node.labels
                #print(label)
                clean_label = str(label).replace('frozenset({\'', '').replace('\'})','')
                node_info = {
                    "labels": clean_label,
                    "text": node['text']
                }
                node_infos.append(node_info)
    return node_infos

# 使用示例
# entity_list = ["罗国杰"]
# entity = "罗国杰"
# # print("entity infor:" + entity + "==================================")
# # print(get_infor_ent(entity_list))
# # print("entity embedding infor" + entity + "=================================")
# # print(get_infor_embedding(entity_list))

# meta_paths = get_node_metapath(entity)
# print("meta_paths:" + entity + "==================================================")
# print(meta_paths)
# print(search_metapaths(entity,meta_paths))
# print(get_relation("罗国杰", "王韬"))

# # 关闭数据库连接
# driver.close()