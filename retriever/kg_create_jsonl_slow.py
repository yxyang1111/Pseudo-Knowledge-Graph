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

data_dir = '/home/user/test_retrieval/data/*.jsonl'

for file_path in glob.glob(data_dir, recursive=True):
    print(file_path)
    with jsonlines.open(file_path, 'r') as reader:
        for json_obj in tqdm(reader):
            with driver.session() as session:
                # 删除所有节点和关系s
                #session.run("MATCH (n) DETACH DELETE n")

                # 创建内容节点
                existing_node = session.run(
                    "MATCH (n:CONTENT) WHERE n.text = $text RETURN n",
                    text=json_obj['content']
                )
                if existing_node.single() == None:
                    vec = model.encode(json_obj['content'], normalize_embeddings=False).tolist()
                    content_node = session.run(
                        "CREATE (n:CONTENT {text: $text, embedding: $embedding}) RETURN n",
                        text=json_obj['content'],
                        embedding=vec
                    )
                    # content_node = session.run(
                    #     "MATCH (c:CONTENT) WHERE c.text = $text RETURN c",
                    #     text=json_obj['content']
                    # )
                
                    # 创建元数据节点并建立关系
                    for key, value in json_obj['metadata'].items():
                        patterns = r'。|？|！|；|\r|;| '
                        # items = re.split(patterns, value)
                        items = [item.replace(' ', '') for item in re.split(patterns, value)]
                        for item in items:
                            if item.strip() != '':
                                label = key.replace("/", "")  # 将标签存储在变量中
                                query = f"MATCH (n:{label}) WHERE n.text = $text RETURN n"
                                existing_node = session.run(
                                    query,
                                    text=item
                                )
                                if existing_node.single() == None:
                                    vec = model.encode(item, normalize_embeddings=False).tolist()
                                    query = f"CREATE (n:{label} {{text: $text, embedding: $embedding}}) RETURN n"
                                    session.run(
                                        query,
                                        text=item,
                                        embedding=vec
                                    )
                                if content_node.single() != None:
                                    query = f"""
                                        MATCH (c:CONTENT), (e:{label})
                                        WHERE c.text = $text AND e.text = $item
                                        CREATE (c)-[:INCLUDE]->(e)
                                        """
                                    session.run(
                                        query,
                                        text=json_obj['content'],
                                        item=item,
                                    )
                                

driver.close()