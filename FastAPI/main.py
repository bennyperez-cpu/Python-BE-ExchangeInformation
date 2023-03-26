from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def root():
    return "Hola FastAPI"

@app.get("/url")
async def url():
    return {"url-curso"}

#Ó se puede generar este código:
""" 
 Reemplazar desde la línea 7 por:

@app.get("/url")
async def root():
    return {"url-curso"}

"""

#Para levantar el servidor API uvicorn main:app --reload
