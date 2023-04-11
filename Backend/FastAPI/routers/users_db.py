from fastapi import FastAPI, HTTPException, APIRouter, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId
from pydantic import BaseModel
# from typing import Any, List, Union

router = APIRouter(prefix="/userdb",
                    responses={status.HTTP_404_NOT_FOUND: {"messaje": "No encontrado"}},
                    tags=["userdb"])

#Para arrancar el servidor se usa el siguiente comando: python3 -m uvicorn users:app --reload

#Url local: http://127.0.0.1:8000


#Entidad user


users_list = []

@router.get("/usersjson")
async def usersjson():
    return [{"name": "Benny", "surname": "Pérez", "url": "www.linkedin.com/in/bennyperez", "age":36},
            {"name": "Hammer", "surname": "Vásquez", "url": "https://sites.google.com/pucp.pe/bennyperez/", "age":37},
            {"name": "Jessika", "surname": "Medina", "url": "https://www.linkedin.com/in/jessika-milena-medina-suarez/", "age":36}]

def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        print(user)
        return User(**user_schema(user))
    except:
        return "{Error: No se ha encontrado el usuario}"

def search_user_by_email(email: str):
    # users = filter(lambda user: user.id == id, users_list)
    try:
        user = db_client.users.find_one({"email":email})
        print(user)
        return User(**user_schema(user))
    except:
        return "{Error: No se ha encontrado el usuario}"

@router.get("/", response_model = list[User])
async def users():
    return users_schema(db_client.users.find())

@router.get("/{id}") #Path
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.get("/") #Query
async def user(id: int):
    return search_user("_id", ObjectId(id))
    
@router.post("/", response_model= User, status_code=201)
async def user(user: User): 
    if type (search_user("email", user.email)) == User:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Error: El usuario ya existe")
    #    #raise HTTPException(status_code=204, detail="Error: El usuario ya existe")
    # else:
    #     users_list.append(user)

    user_dict = dict(user)
    
    del user_dict["id"]
    id = db_client.users.insert_one(user_dict).inserted_id
    print(id)
    new_user = user_schema(db_client.users.find_one({"_id":id}))
    return User(**new_user)


@router.put("/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"Error": "No se ha actualizado el usuario"}
    else:
        return user

@router.delete("/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"Error": "No se ha eliminado el usuario"}
    else:
        return {"El usuario se ha eliminado satisfactoriamente"}   

#Url local: http://127.0.0.1:8000/url

#Ó se puede generar este código: