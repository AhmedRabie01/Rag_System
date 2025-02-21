# Rag_System
This End-to-End application is designed to process unstructured data files and enable intelligent querying through advanced Natural Language Processing (NLP) techniques. The app
automates the workflow, starting with data ingestion, text preprocessing, and embedding generation using Open AI and Cohere models. These embeddings are then stored in a
vector database for efficient retrieval and querying. The solution is built strongly on software engineering best practices, ensuring modularity, scalability, and maintainability.
The project demonstrates expertise in NLP, vector search technologies, and seamless integration of AI models into production-ready pipelines, making it a standout example of cutting-edge machine learning applications

### Installation

1) install Miniconda 

2) Create a new environment by following the command
```bash
conda create -n 'env-name' python=3.10
```
3) install packages
```bash
pip install -r requirements.txt
```
4) setup environment variables
```bash
cp .env.example .env
```
set your environment variables in the '.env' file

5) Run Docker Compose Services

```bash
cd docker
cp .env.example .env
```
6) update .env with your credentials

```bash
cd docker
sudo docker-compose up -d
```

7) Run the FastAPI server
```bash
uvicorn main:app --reload 
```

- you can download postman files from assets
from 
'Rag_System\assets\Rag-App.postman_collection.json'
