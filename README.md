# Pseudo-Knowledge-Graph

This is the implementation for the paper:

Pseudo-Knowledge Graph: Meta-Path Guided Retrieval and In-Graph Text for RAG-Equipped LLM

## Overview

We introduce a framework that transitions from local to global perspectives, named the Pseudo-Knowledge Graph (PKG) approach, to enhance the processing of large volumes of information and to address challenges arising from complex relationships among data. The PKG is a special knowledge graph in which we store multiple presentations of entities and relationships and the original nature language. We developed the PKG framework that extracts
relevant entities and relationships from natural language and organizes them within a PKG. Acknowledging that LLMs often face challenges with structured data, we also preserve segments of natural language text to aid LLMs in processing the retrieved information effectively. In our retrieval process for the PKG, we employ various techniques, such as vector--
based retrieval and meta-path retrieval to improve the system’s efficiency in accessing and utilizing the underlying data.

## Requirements

```
pip install -r requirements.txt
```

## Data

The data should be in either txt or jsonl format. If your data is not in these formats, please convert it beforehand. If you intend to use jsonl format, ensure that the structure of the jsonl file is compatible with the code, as the code may need to be adapted to properly parse and process the jsonl data.

## Quick Use

To use PKG, you can use run.sh to set up the environment, construct and retrieve the PKG. First, ensure you have configured your Neo4j URI and AUTH in config/config.py. Then, place your data in ./data.  After preparing your data, run the build script：

```
./run.sh
```

## Build
To use PKG, you can use build.sh to set up the environment and construct the PKG. First, ensure you have configured your Neo4j URI and AUTH in config/config.py. Then, place your data in ./data and run the build script:

```
./build.sh
```

Alternatively, you can manually build the PKG by running:

```
python builder/pkg_create_text.py
```

You can also explore other building methods available in the ./builder directory.

## Retrieval

We provide three retrieval methods, including *Regular Expression Retrieval*, *vector--
based retrieval* and *meta-path retrieval*. You can choose the methods in ./retriever. We also provide a way to retrieve all information and combine them.

```
python retriever/get_all_information.py user_query
```

For details on API usage and parameters, please refer to the documentation provided in retriever/api.md.


## Acknowledgement

We will continuously improve the methods by incorporating the latest research findings and technological advancements. Our focus will be on optimizing efficiency, enhancing accuracy, and ensuring adaptability to changing conditions.

If you have further questions or need support, feel free to reach out to our support team.