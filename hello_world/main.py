#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastApi
from fastapi import FastAPI
from fastapi import Body, Query

app = FastAPI()

#Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] =None


@app.get("/")     #-----> Path opetation decorator
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):     #-----> Body es una clase de FastApi que permite decir que un parametro que me llega es de tipo body; (...) parametro obligatorio en fastapi
    return person

# Validaciones Query Parameters

@app.get("/person/detail?name")
def show_person(
    name: Optional[str] = Query(default=None, min_length=1, max_length=50),
    age: int = Query(... )
):
    return {name: age}
