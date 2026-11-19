from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import schemas as sch
from deps import CurrentUser
from security import create_access_token, hash_password, verify_password
from store import USERS, new_user_id

app = FastAPI(title="Security testing")


@app.post("/register", status_code=201, response_model=sch.UserRead)
def register(user: sch.UserCreate):
    role = "admin" if len(USERS) == 0 else "user"
    user_id = new_user_id()
    USERS[user_id] = {
        "id": user_id,
        "email": user.email,
        "password_hash": hash_password(user.password),
    }
    return USERS[user_id]

@app.post("/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    found_user = None
    for user in USERS.values():
        if user["email"] == form.username:
            found_user = user
            break

    if found_user is None or not verify_password(form.password, found_user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=found_user["email"])
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", response_model=sch.UserRead)
def me(current_user: CurrentUser):
    return current_user