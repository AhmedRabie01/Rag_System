from fastapi import FastAPI,APIRouter, Depends
import os 
from helpers.config import get_settings,Settings

base_route = APIRouter(
prefix="/api/v1",
tags=['api_v1'],
)

@base_route.get("/")
async def welcome(app_settings: Settings =Depends(get_settings)):

    app_name = app_settings.APP_NAME
    app_version = app_settings.App_VERSION


    return{ 
        "app_name":app_name,
        "app_version":app_version,
           
          }