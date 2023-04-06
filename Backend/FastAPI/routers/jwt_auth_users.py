from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes = ["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "quantum1": {
    "username": "Quantum1",
    "full_name": "Benny Hammer",
    "email": "benny.perez@pucp.pe",
    "disabled": False,
    "password": "$2a$12$cxC/LFlm8EZHDH7KZJteg./zVslc/75x3ZxZ/NjsKp2oSq77JDj5O"
    },
    "quantum2": {
    "username": "Quantum2",
    "full_name": "Benny Hammer",
    "email": "benny.perez@pucp.pe",
    "disabled": True,
    "password": "$2a$12$qy4eAvY5bK2o0GoiNaGmlOblELHLSUeCkjiHOCaFmnHtcvfmgL5mS"
    }
        
}

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto")
    user = search_user_db(form.username)

    


    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}
