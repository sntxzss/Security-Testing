from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
SECRET = "dev-secret-change-me-it-must-be-32-bytes-long"  # у житті — .env
ph = PasswordHash.recommended()
USERS = {"librarian": ph.hash("books123")}  # логін → хеш пароля
app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="token")  # звідки /docs бере токен
UNAUTH = HTTPException(401, "Bad credentials", {"WWW-Authenticate": "Bearer"})
