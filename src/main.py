from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv('.env')
from routes import base
from routes import data

app = FastAPI()

app.include_router(base.base_route)
app.include_router(data.data_route)

