from fastapi import FastAPI

app = FastAPI()

@app.get('/test')
def home():
    return {"message":"Connection Test Successfull"}