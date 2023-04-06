from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()
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
    "username": "quantum1",
    "full_name": "Benny Hammer",
    "email": "benny.perez@pucp.pe",
    "disabled": False,
    "password": "$2a$12$cxC/LFlm8EZHDH7KZJteg./zVslc/75x3ZxZ/NjsKp2oSq77JDj5O"
    },
    "quantum2": {
    "username": "quantum2",
    "full_name": "Benny Hammer",
    "email": "benny.perez@pucp.pe",
    "disabled": True,
    "password": "$2a$12$qy4eAvY5bK2o0GoiNaGmlOblELHLSUeCkjiHOCaFmnHtcvfmgL5mS"
    }
        
}

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "4329c7cc794dbaa73692718e7e4af7a4c3e4d41df304ca120de947e2e3104a79"


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) 
    
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas",
            headers ={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        

    except JWTError: 
        raise exception
    
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST , 
            detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto")
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta")
    access_token_expiration = timedelta(minutes =ACCESS_TOKEN_DURATION)
    expire = datetime.utcnow() + access_token_expiration

    access_token = {"sub": user.username,
                    "exp": expire}


    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user