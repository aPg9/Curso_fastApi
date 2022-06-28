#Python
from typing import Optional
from enum import Enum     #-----> Nos ayuda para crear enumeraciones de strings

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastApi
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red" 

class Location(BaseModel):
    city: str
    state: str
    country: str

# Validaciones: Modelos
class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length= 1,
        max_length=50
        )
    last_name: str = Field(
        min_length= 1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)


@app.get("/")     #-----> Path opetation decorator
def home():
    return {"First API": "Congratulations"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):     #-----> Body es una clase de FastApi que permite decir que un parametro que me llega es de tipo body; (...) parametro obligatorio en fastapi
    return person

# Validaciones Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50  characters"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"
         )
):
    return {name: age}


# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,      #-----> gt-->greater than, el id debe ser mayor a 0
        title="Person ID",
        description="This is the person ID. It's between 1 and 50 characters"
        )     
):
    return {person_id: "It exists!!"}

# Validaciones: Body Parameters

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    Location: Location = Body(...)
):  
    results = person.dict()
    results.update(Location.dict()) 
    return results