from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

#Para arrancar el servidor se usa el siguiente comando: python3 -m uvicorn users:app --reload

#Url local: http://127.0.0.1:8000


#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="Benny", surname="Pérez", url="www.linkedin.com/in/bennyperez", age=36),
         User(id=2, name="Hammer", surname="Vásquez", url="https://sites.google.com/pucp.pe/bennyperez/", age=37),
         User(id=3, name="Jessika", surname="Medina", url="https://www.linkedin.com/in/jessika-milena-medina-suarez/", age=36)]

@app.get("/usersjson")
async def usersjson():
    return [{"name": "Benny", "surname": "Pérez", "url": "www.linkedin.com/in/bennyperez", "age":36},
            {"name": "Hammer", "surname": "Vásquez", "url": "https://sites.google.com/pucp.pe/bennyperez/", "age":37},
            {"name": "Jessika", "surname": "Medina", "url": "https://www.linkedin.com/in/jessika-milena-medina-suarez/", "age":36}]

@app.get("/users")
async def users():
    return users_list

@app.get("/user/{id}")
async def user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return "{Error: No se ha encontrado el usuario}"

#Url local: http://127.0.0.1:8000/url

#Ó se puede generar este código: