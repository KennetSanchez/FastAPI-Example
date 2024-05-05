from datetime import datetime
from http.client import HTTPException
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class Articulo(BaseModel):
    id: int | None = None
    titulo: str
    autor: str
    contenido: str
    categoria: str
    creado: datetime


articulos : List[Articulo] = []

@app.get("/articulos/")
async def leer_articulos():
    return articulos

@app.post("/articulos/")
async def crear_articulo(articulo: Articulo):
    articulo.id = articulos.__len__() + 1
    articulos.append(articulo)
    return articulo

@app.get("/articulos/{id_articulo}")
async def leer_articulo(id_articulo : int):
    
    for articulo in articulos:
        if articulo.id == id_articulo:
            return articulo

    raise HTTPException(status_code=404, detail="Articulo no encontrado con id: %s" % id_articulo)


@app.put("/articulos/{id_articulo}")
async def modificar_articulo(id_articulo: int, articulo_actualizado : Articulo):
    
    for index, articulo in enumerate(articulos):
        if articulo.id == id_articulo:
            articulo_actualizado.id = articulo.id
            articulos.__setitem__(index, articulo_actualizado)

    # Intenté usar el JSONResponse, pero parece que automáticamente responde con un JSON, 
    # y al tratar de hacerlo explícito la respuesta quedaba con mala legibilidad 
    return articulo_actualizado    

@app.delete("/articulos/{id_articulo}")
async def eliminar_articulo(id_articulo : int):

    for articulo in articulos:
        if articulo.id == id_articulo:
            articulos.remove(articulo)
            return JSONResponse(content={"Mensaje": "Articulo eliminado con id: %s" %articulo.id})
        
    raise HTTPException(status_code=404, detail="No se encontró ningún artículo con id: %s" %id_articulo)