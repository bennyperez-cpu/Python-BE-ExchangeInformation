from fastapi import FastAPI
from routers import products,users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Url local: http://127.0.0.1:8000

@app.get("/")
async def root():
    return "Hola FastAPI"

@app.get("/url")
async def url():
    return {"url-curso"}

#Url local: http://127.0.0.1:8000/url

#Ó se puede generar este código:
""" 
 Reemplazar desde la línea 7 por:

@app.get("/url")
async def root():
    return {"url-curso"}

"""

#Router
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")




#Para levantar el servidor API uvicorn main:app --reload
