from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv('.env')
from routes import base
from routes import data

import logging

logging.basicConfig(
    level=logging.INFO,  # Adjust the level to DEBUG for more details
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # This will print logs to console
        logging.FileHandler("app.log")  # This will write logs to a file
    ]
)

logger = logging.getLogger("uviconrn.error")




app = FastAPI()

app.include_router(base.base_route)
app.include_router(data.data_route)

