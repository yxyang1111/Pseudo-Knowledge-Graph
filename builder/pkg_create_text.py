import jsonlines
import glob
import spacy
from tqdm import tqdm
import re
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

from builder.get_entity import get_entity

import sys
sys.path.append("..//")
from config.config import Embedding_model_path, neo4j_auth, neo4j_uri, Data_path

model_path = Embedding_model_path
model = SentenceTransformer(model_path)

driver = GraphDatabase.driver(uri = neo4j_uri, auth = neo4j_auth)

data_dir = Data_path + "*.txt"
for file_path in glob.glob(data_dir, recursive=True):
    print(file_path)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file_in:
        text = file_in.read()
        text=text.replace('\n','')
        lines = re.split(patterns,text)
        with driver.session() as session:
            # 删除所有节点和关系
            #session.run("MATCH (n) DETACH DELETE n")
            for line in lines:


                # 创建内容节点
                existing_node = session.run(
                    "MATCH (n:CONTENT) WHERE n.text = $text RETURN n",
                    text = line
                )
                if existing_node.single() == None:
                    vec = model.encode(line, normalize_embeddings=False).tolist()
                    content_node = session.run(
                        "CREATE (n:CONTENT {text: $text, embedding: $embedding}) RETURN n",
                        text=line,
                        embedding=vec
                    )
                    # content_node = session.run(
                    #     "MATCH (c:CONTENT) WHERE c.text = $text RETURN c",
                    #     text=line
                    # )

                    # 创建元数据节点并建立关系
                    for entity_list in get_entity(line):
                        existing_nodes = session.run(
                            "MATCH (n) WHERE n.text IN $texts RETURN n.text AS text, n",
                            texts = entity_list
                        ).data()

                        nodes_dict = {record['text']: record['n'] for record in existing_nodes}


                        for entity in entity_list:
                            if nodes_dict.get(entity) is None:
                                vec = model.encode(entity, normalize_embeddings=False).tolist()
                                query = f"CREATE (n:{"Entity"} {{text: $text, embedding: $embedding}}) RETURN n"
                                session.run(
                                    query,
                                    text=entity,
                                    embedding=vec
                                )
                            query = f"""
                                MATCH (c:CONTENT), (e:{"Entity"})
                                WHERE c.text = $text AND e.text = $item
                                CREATE (c)-[:INCLUDE]->(e)
                                """
                            session.run(
                                query,
                                text=line,
                                item=entity,
                            )


driver.close()