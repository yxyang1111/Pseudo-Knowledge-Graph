# Pseudo-Knowledge-Graph

This is the implementation for the paper:

Meta-Path Guided Retrieval and In-Graph Text for Enhanced LLM with Pseudo-Knowledge Graphs

### Overview

We introduce a framework that transitions from local to global perspectives, named the Pseudo-Knowledge Graph (PKG) approach, to enhance the processing of large volumes of information and to address challenges arising from complex relationships among data. The PKG is a special knowledge graph in which we store multiple presentations of entities and relationships and the original nature language. We developed the PKG framework that extracts
relevant entities and relationships from natural language and organizes them within a PKG. Acknowledging that LLMs often face challenges with structured data, we also preserve segments of natural language text to aid LLMs in processing the retrieved information effectively. In our retrieval process for the PKG, we employ various techniques, such as vector--
based retrieval and meta-path retrieval to improve the system’s efficiency in accessing and utilizing the underlying data. 

## Requirements

```
pip install -r requirements.txt
```

### 