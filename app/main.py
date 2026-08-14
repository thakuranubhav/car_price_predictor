from fastapi import FastAPI
import dotenv

app= FastAPI()

@app.get('/home')
def get_home():
    return {'message':"Welcome to the food Munch"}


@app.get('/users')
def get_users():
    return {'User':'Rohit'}