from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient

SECRET = "dev-secret-change-me-it-must-be-32-bytes-long"
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
app = FastAPI()

def make_token(user_id: int) -> str:  # JWT: sub — рядок, exp — час
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    return jwt.encode({"sub": str(user_id), "exp": exp}, SECRET)

def get_current_user(token: Annotated[str, Depends(oauth2)]) -> int:
    try:
        return int(jwt.decode(token, SECRET, algorithms=["HS256"])["sub"])
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Bad token", {"WWW-Authenticate": "Bearer"})

@app.get("/me")
def me(user_id: Annotated[int, Depends(get_current_user)]):
    return {"user_id": user_id}

def test_real_token(): 
    auth = {"Authorization": f"Bearer {make_token(7)}"}
    assert TestClient(app).get("/me", headers=auth).json() == {"user_id": 7}

def test_override():  
    app.dependency_overrides[get_current_user] = lambda: 99
    assert TestClient(app).get("/me").json() == {"user_id": 99}
    app.dependency_overrides.clear()  # обов'язково прибрати

