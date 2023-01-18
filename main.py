from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from typing import List
from user import Gender, Role, User, UserUpdateRequest 

app = FastAPI()

db: List[User] = [
    User(
        id=uuid4(), 
        first_name="Emmanuel", 
        last_name="Amet", 
        gender=Gender.male, 
        roles=[Role.admin]
        ),
        User(
        id=uuid4(), 
        first_name="Lucy", 
        last_name="Walls", 
        gender=Gender.female, 
        roles=[Role.user, Role.student]
        )
]

@app.get("/")
def root():
    return{
        "App" : "REST API using FastAPI"
    }

@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {
        "id" : user.id
    }

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if(user.id == user_id):
            if user.first_name is not None:
                user.first_name = user_update.first_name
            if user.last_name is not None:
                user.last_name = user_update.last_name
            if user.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code= 404,
        detail= f"user with id: {user_id} does not exits"
    )

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if(user.id == user_id):
            db.remove(user)
            return
    raise HTTPException(
        status_code= 404,
        detail= f"user with id: {user_id} does not exits"
    )