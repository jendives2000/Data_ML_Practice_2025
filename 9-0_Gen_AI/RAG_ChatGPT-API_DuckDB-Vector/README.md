# **Hands-On Practice Gen AI 🤖: IMDb Chatbot based on RAG + OpenAi API + 🦆DuckDB**

---

By Jean-Yves Tran | jy.tran@[datascience-jy.com](https://datascience-jy.com) | [LinkedIn](https://www.linkedin.com/in/jytran-datascience/)  
IBM Certified Data Analyst 

---

---

Source: 
- [Kaggle IMDb Dataset](https://www.kaggle.com/datasets/ishikajohari/imdb-data-with-descriptions?resource=download) - IMDb Movies/Shows with Descriptions |  Ishika Johari
- [OpenAI API](https://openai.com/api) - OpenAI API Documentation
- [DuckDB for Python](https://duckdb.org/docs/installation/?version=stable&environment=python) - DuckDB DBMS
- [Retrieval Augmented Generation with the OpenAI API & DuckDB](https://www.packtpub.com/product/retrieval-augmented-generation-with-the-openai-api-duckdb/9781806025039?_gl=1*bsv5pl*_gcl_au*MTY1NjQ5NzM3NS4xNzM5NjI4ODI4LjE1MjY5MTc2MDUuMTc0NzE1MjI2MS4xNzQ3MTUyMjYx*FPAU*MTY1NjQ5NzM3NS4xNzM5NjI4ODI4) - Packt Platform | Vincent Vankrunkelsven
---

This is a practice project aiming at the creation of a chatbot that can answer questions on movies using the following tech:  
- LLM: openAI 4o-mini
- vector embedding: 
  - cost: openAI "text-embedding-3-large" (openAI tiktoken module)
  - embedding: DuckDB (~50MB vector DB size)
- RAG: langchain + Kaggle IMDb dataset

Here are the main steps of the project:  
- The dataset was first cleaned and then left with a 4 selected columns
- Langchain documents were prepped for vectorizing (langchain document)
- the cost of the embedding was calculated (tokenizer): only 4.9 cents (0.049$)
- the vector database filling: total of 4963 documents (4 columns describing a movie)
- testing the RAG with a question (similarity_search): 
  - What's a good movie about climate change?
  - and checking the answer given

**NOTES**: 
The RAG is processing a similarity search, meaning it answers the questions based on similarities found in its vector DB. A question about the quality of a movie, like "What is the best Action movie" will not apply that quality concept to its answer.
However, the LLM is taking over for that part and answers the question a more relevant way. 