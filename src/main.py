from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv('.env')
from routes import base
from routes import data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

app = FastAPI()

@app.on_event("startup")
async def startup_db_settings():
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)  
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()
      

app.include_router(base.base_route)
app.include_router(data.data_route)


 
