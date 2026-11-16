from fastapi import FastAPI
from pydantic import ValidationError
import schemas as sch
from pwdlib import PasswordHash

app = FastAPI(title="Security testing")

USERS: dict[int, dict] = {}
next_id = 0

@app.post("/register", status_code=201, response_model=sch.UserRead)
def app_post():
    global next_id
    next_id += 1

    USERS[next_id] = {
        "id": next_id,
        "email": user.email,
        "password_hash": ph.hash(user.password),
    }

    return USERS[next_id]

 