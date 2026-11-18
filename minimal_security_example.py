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

@app.post("/token")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    h = USERS.get(form.username)
    if h is None or not ph.verify(form.password, h):
        raise UNAUTH  # однакова відповідь для обох випадків
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    token = jwt.encode({"sub": form.username, "exp": exp}, SECRET)
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: Annotated[str, Depends(oauth2)]) -> str:
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])["sub"]
    except jwt.InvalidTokenError:
        raise UNAUTH
@app.get("/secret-room")
def secret_room(user: Annotated[str, Depends(get_current_user)]):
    return {"msg": f"Вітаю, {user}! Тут тихо."}
