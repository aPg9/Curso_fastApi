from fastapi import FastAPI

app = FastAPI()

@app.get("/")     #-----> Path opetation decorator
def home():
    return {"Hello": "World"}
