#Python
from datetime import date
from typing import Optional
from enum import Enum     #-----> Nos ayuda para crear enumeraciones de strings

#Pydantic
from pydantic import BaseModel, EmailStr, PastDate
from pydantic import Field
from pydantic.types import PaymentCardBrand, PaymentCardNumber, constr     #-----> Si funciona con tarjetas reales, desactivado

#FastApi
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models

# class Card(BaseModel):     #-----> Si funciona con tarjetas reales, desactivado
#     name: constr(strip_whitespace=True, min_length=1)
#     number: PaymentCardNumber
#     exp: date

#     @property
#     def brand(self) -> PaymentCardBrand:
#         return self.number.brand

#     @property
#     def expired(self) -> bool:
#         return self.exp < date.today()

# card = Card(
#     name='Georg Wilhelm Friedrich Hegel',
#     number='4000000000000002',
#     exp=date(2023, 9, 30),
# )

# assert card.number.brand == PaymentCardBrand.visa
# assert card.number.bin == '400000'
# assert card.number.last4 == '0002'
# assert card.number.masked == '400000******0002'

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red" 

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length= 2,
        max_length= 50,
        example = "Montreal"
        )
    state: str = Field(
        ...,
        min_length= 2,
        max_length= 50,
        example= "Quebec"
        )
    country: str = Field(
        ...,
        min_length= 2,
        max_length= 50,
        example = "Canada"
        )

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length= 1,
        max_length=50,
        example = "Rogelio"
        )
    last_name: str = Field(
        min_length= 1,
        max_length=50,
        example = "Juarez"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example = "45"
        )
    birth_day: PastDate = Field(
        ...,
        example = "2002-11-24"
        )
    email: EmailStr = Field(
        ...,
        exmaple= "prueba@pruebaemail.com"
        )
    # card: Card = Field(     #-----> Si funciona con tarjetas reales, desactivado 
    #     ...,
    #     )
    hair_color: Optional[HairColor] = Field(
        default=None,
        example= "black"
        )
    is_married: Optional[bool] = Field(
        default=None,
        example = False
        )   

# Validaciones: Modelos
class Person(PersonBase):
    password: str = Field(
        ..., 
        min_length=8
        )    

class PersonOut(PersonBase):    
    pass

@app.get("/")     #-----> Path opetation decorator
def home():
    return {"First API": "Congratulations"}

# Request and Response Body

@app.post("/person/new", response_model=PersonOut)
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
        description="This is the person name. It's between 1 and 50  characters",
        example= "Rocio"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example= 25
         )
):
    return {name: age}


# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,      #-----> gt-->greater than, el id debe ser mayor a 0
        example= 123
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
        gt=0,
        example= 123
    ),
    person: Person = Body(...),
    Location: Location = Body(...)
):  
    results = person.dict()
    results.update(Location.dict()) 
    return results