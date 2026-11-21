from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient

SECRET = "dev-secret-change-me-it-must-be-32-bytes-long"
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
app = FastAPI()
