# Rag_System


### Installation

1) install Miniconda 
2) Create new environment by following command
```bash
conda create -n 'env-name' python=3.10
```
3) install pakages
```bash
pip install -r requirements.txt
```
4) setup environment variables
```bash
cp .env.example .env
```
set your environment variables in the '.env' file

5) Run the FastAPI server
```bash
uvicorn main:app --reload 
```

- you can download postman files from assets
from 
'Rag_System\assets\Rag-App.postman_collection.json'
