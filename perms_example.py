from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException
app = FastAPI()
USERS = {"ann": "admin", "bob": "user", "eve": "user"} 
PHOTOS = {1: {"id": 1, "title": "Море", "owner": "bob"},
          2: {"id": 2, "title": "Гори", "owner": "eve"}}

def get_current_user(x_user: Annotated[str, Header()]) -> dict:
    if x_user not in USERS:  
        raise HTTPException(401, "Who are you?")
    return {"name": x_user, "role": USERS[x_user]}

Me = Annotated[dict, Depends(get_current_user)]

def require_admin(me: Me) -> dict: 
    if me["role"] != "admin":
        raise HTTPException(403, "Admins only")
    return me

@app.get("/photos/{photo_id}")
def one_photo(photo_id: int, me: Me):
    p = PHOTOS.get(photo_id)
    if p is None or p["owner"] != me["name"]:
        raise HTTPException(404, "Photo not found")  
    return p

@app.get("/admin/stats")
def stats(admin: Annotated[dict, Depends(require_admin)]):
    return {"photos": len(PHOTOS), "users": len(USERS)}