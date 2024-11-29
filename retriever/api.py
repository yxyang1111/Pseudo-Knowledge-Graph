from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple
from retriever.pkg_get_entity import encode_entity, get_entity_spacy, get_entity_embedding, get_content_embedding, get_entity_llm
from retriever.pkg_get_infor import get_infor_ent, get_infor_embedding, get_node_metapath, search_metapath, search_metapaths
from get_all_infor import get_all_infor

app = FastAPI()

class EncodeEntityParams(BaseModel):
    entity: str

@app.post("/encode_entity/")
async def encode_entity_api(params: EncodeEntityParams):
    result = encode_entity(
        entity=params.entity,
    )
    return result

class GetEntitySpacyParams(BaseModel):
    user_query: str

@app.post("/get_entity_spacy/")
async def get_entity_spacy_api(params: GetEntitySpacyParams):
    result = get_entity_spacy(
        user_query=params.user_query,
    )
    return result

class GetEntityEmbeddingParams(BaseModel):
    user_query: str
    uri: str = "bolt://localhost:7687"
    auth: Tuple[str, str] = ("neo4j", "s3cretPassword")

@app.post("/get_entity_embedding/")
async def get_entity_embedding_api(params: GetEntityEmbeddingParams):
    result = get_entity_embedding(
        user_query=params.user_query,
        uri=params.uri,
        auth=params.auth
    )
    return result

class GetContentEmbeddingParams(BaseModel):
    user_query: str
    uri: str = "bolt://localhost:7687"
    auth: Tuple[str, str] = ("neo4j", "s3cretPassword")

@app.post("/get_content_embedding/")
async def get_content_embedding_api(params: GetContentEmbeddingParams):
    result = get_content_embedding(
        user_query=params.user_query,
        uri=params.uri,
        auth=params.auth
    )
    return result

class GetInforEntParams(BaseModel):
    entity_list: List[str]
    uri: str = "bolt://localhost:7687"
    auth: Tuple[str, str] = ("neo4j", "s3cretPassword")

@app.post("/get_infor_ent/")
async def get_infor_ent_api(params: GetInforEntParams):
    result = get_infor_ent(
        entity_list=params.entity_list,
        uri=params.uri,
        auth=params.auth
    )
    return result

class GetInforEmbeddingParams(BaseModel):
    entity_list: List[str]
    uri: str = "bolt://localhost:7687"
    auth: Tuple[str, str] = ("neo4j", "s3cretPassword")

@app.post("/get_infor_embedding/")
async def get_infor_embedding_api(params: GetInforEmbeddingParams):
    result = get_infor_embedding(
        entity_list=params.entity_list,
        uri=params.uri,
        auth=params.auth
    )
    return result

class GetNodeMetapathParams(BaseModel):
    entity: str
    uri: str = "bolt://localhost:7687"
    auth: Tuple[str, str] = ("neo4j", "s3cretPassword")

@app.post("/get_node_metapath/")
async def get_node_metapath_api(params: GetNodeMetapathParams):
    result = get_node_metapath(
        entity=params.entity,
        uri=params.uri,
        auth=params.auth
    )
    return result

class SearchMetapathParams(BaseModel):
    entity: str
    meta_path: List[str]  # 期望接收字符串列表作为元路径
    uri: str = "bolt://localhost:7687"
    auth: Tuple[str, str] = ("neo4j", "s3cretPassword")

@app.post("/search_metapath/")
async def search_metapath_api(params: SearchMetapathParams):
    result = search_metapath(
        entity=params.entity,
        meta_path=params.meta_path,
        uri=params.uri,
        auth=params.auth
    )
    return result

class SearchMetapathsParams(BaseModel):
    entity: str
    meta_paths: List[List[str]]  # 期望接收字符串列表作为元路径
    uri: str = "bolt://localhost:7687"
    auth: Tuple[str, str] = ("neo4j", "s3cretPassword")

@app.post("/search_metapaths/")
async def search_metapaths_api(params: SearchMetapathsParams):
    result = search_metapaths(
        entity=params.entity,
        meta_paths=params.meta_paths,
        uri=params.uri,
        auth=params.auth
    )
    return result

class GetAllInformationParams(BaseModel):
    user_query: str
    uri: str = "bolt://localhost:7687"
    auth: Tuple[str, str] = ("neo4j", "s3cretPassword")

@app.post("/get_all_information/")
async def get_all_information(params: GetAllInformationParams):
    result = get_all_infor(
        user_query=params.user_query,
        uri=params.uri,
        auth=params.auth
    )
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, host="0.0.0.0")