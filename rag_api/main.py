from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
from typing import List

app = FastAPI()

class Query(BaseModel):
    text: str
    user_id: int

