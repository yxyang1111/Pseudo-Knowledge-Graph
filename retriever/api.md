# KG-API 文档

目前API被放置在8000端口上

以下是可用的 API 接口列表及其说明：

#### 1. 编码实体

**POST** `/encode_entity/`

- **描述**：对给定实体进行编码。
- **请求参数**：
  - `entity` (string): 需要编码的实体。
- **输出**：一个向量，为通过encode模型对实体进行编码的向量

#### 2. 使用 spaCy 获取实体
**POST** `/get_entity_spacy/`
- **描述**：使用 spaCy 从用户查询中提取实体。
- **请求参数**：
  - `user_query` (string): 用户的查询语句。
- **输出**：一个list，通过spaCy提取出来的实体列表

#### 3. 获取实体
**POST** `/get_entity_embedding/`
- **描述**：通过嵌入表示获取实体。
- **请求参数**：
  - `user_query` (string): 需要获取嵌入的实体。
  - `uri` (string, 可选): 默认为 "bolt://localhost:7687". 连接 URI。
  - `auth` (tuple, 可选): 默认为 ("neo4j", "s3cretPassword"). 认证信息。
- **输出**：一个list，通过embedding在现有图谱中查询到的相似实体列表

#### 4. 获取内容
**POST** `/get_content_embedding/`

- **描述**：通过嵌入表示获取内容。
- **请求参数**：
  - `entity_list` (list of strings): 需要获取嵌入的内容列表。
  - `uri` (string, 可选): 默认为 "bolt://localhost:7687". 连接 URI。
  - `auth` (tuple, 可选): 默认为 ("neo4j", "s3cretPassword"). 认证信息。
- **输出**：与实体embedding相关的信息list

#### 5. 获取实体信息

**POST** `/get_infor_ent/`

- **描述**：获取一组实体的相关信息。
- **请求参数**：
  - `entity_list` (list of strings): 需要获取信息的实体列表。
  - `uri` (string, 可选): 默认为 "bolt://localhost:7687". 连接 URI。
  - `auth` (tuple, 可选): 默认为 ("neo4j", "s3cretPassword"). 认证信息。
- **输出**：与给定实体直接相关的信息list

**POST** `/get_infor_embedding/`

- **描述**：根据嵌入表示获取一组实体的相关信息。
- **请求参数**：
  - `entity_list` (list of strings): 需要获取信息的实体列表。
  - `uri` (string, 可选): 默认为 "bolt://localhost:7687". 连接 URI。
  - `auth` (tuple, 可选): 默认为 ("neo4j", "s3cretPassword"). 认证信息。
- **输出**：与给定实体embedding相关的信息list，同**POST** `/get_content_embedding/`

#### 6. 获取节点的元路径
**POST** `/get_node_metapath/`

- **描述**：获取节点的元路径信息。
- **请求参数**：
  - `entity` (string): 需要获取元路径的节点。
  - `uri` (string, 可选): 默认为 "bolt://localhost:7687". 连接 URI。
  - `auth` (tuple, 可选): 默认为 ("neo4j", "s3cretPassword"). 认证信息。
- **输出**：从节点出发长度小于等于n(现在取3)的元路径计数

#### 7. 根据元路径进行搜索

**POST** `/search_metapath/`

- **描述**：根据所给的一条元路径进行搜索。
- **请求参数**：
  - `entity` (string): 需要搜索元路径的实体。
  - `meta_path` (string): 要搜索的元路径。
  - `uri` (string, 可选): 默认为 "bolt://localhost:7687". 连接 URI。
  - `auth` (tuple, 可选): 默认为 ("neo4j", "s3cretPassword"). 认证信息。
- **输出**：一个list，第一项是元路径类型，即给定的meta_path，后面是该类型的元路径涉及的路径list（包括路径上各个节点的内容）

**POST** `/search_metapaths/`

- **描述**：根据元路径进行搜索。
- **请求参数**：
  - `entity` (string): 需要搜索元路径的实体。
  - `meta_paths` (List[List[str]]): 要搜索的元路径列表。
  - `uri` (string, 可选): 默认为 "bolt://localhost:7687". 连接 URI。
  - `auth` (tuple, 可选): 默认为 ("neo4j", "s3cretPassword"). 认证信息。
- **输出**：一个list，每一项都是如同**POST** `/search_metapath/`结果一样



POST `/get_all_information/`

- **描述**：综合所有方法，进行信息检索
- **请求参数**：
  - `user_query` (string): 用户的查询语句。
- **输出**：一个list，包含两个部分，每个部分都是一个list，第一部分是通过实体或向量搜索得到的结果，list中都为节点字符串；第二部分是通过元路径搜索得到的结果，list中每一项都是如同**POST** `/search_metapath/`结果一样
