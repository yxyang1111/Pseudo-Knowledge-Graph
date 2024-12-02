# Pseudo-Knowledge-Graph

This is the implementation for the paper:

Pseudo-Knowledge Graph: Meta-Path Guided Retrieval and In-Graph Text for Enhanced LLM

## Overview

We introduce a framework that transitions from local to global perspectives, named the Pseudo-Knowledge Graph (PKG) approach, to enhance the processing of large volumes of information and to address challenges arising from complex relationships among data. The PKG is a special knowledge graph in which we store multiple presentations of entities and relationships and the original nature language. We developed the PKG framework that extracts
relevant entities and relationships from natural language and organizes them within a PKG. Acknowledging that LLMs often face challenges with structured data, we also preserve segments of natural language text to aid LLMs in processing the retrieved information effectively. In our retrieval process for the PKG, we employ various techniques, such as vector--
based retrieval and meta-path retrieval to improve the system’s efficiency in accessing and utilizing the underlying data. 

## Requirements

```
pip install -r requirements.txt
```

## Build

To use PKG, we provide a method to build PKG using neo4j. You can change your neo4j URI and AUTH in config/config.py. Then you can put your data in ./data and run building script.

```
python builder/pkg_create_text.py
```

You can also use other building methods in ./builder

## Retrieval

We provide three retrieval methods, including *Regular Expression Retrieval*, *vector--
based retrieval* and *meta-path retrieval*. You can choose the methods in ./retriever. We also provide a way to retrieve all information and combine them.

```
python retriever/get_all_information.py
```

For details on API usage and parameters, please refer to the documentation provided in retriever/api.md. 

## Acknowledgement

We will continuously improve the methods by incorporating the latest research findings and technological advancements. Our focus will be on optimizing efficiency, enhancing accuracy, and ensuring adaptability to changing conditions.

If you have further questions or need support, feel free to reach out to our support team.