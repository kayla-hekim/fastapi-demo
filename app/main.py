#!/usr/bin/env python3

from fastapi import Request, FastAPI
from typing import Optional
from pydantic import BaseModel
import pandas as pd
import json
import os
import mysql.connector
from mysql.connector import Error

DBHOST = os.getenv('DB_HOST', 'ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com')
DBUSER = os.getenv('DB_USER', 'admin')
DBPASS = os.getenv('DB_PASS')  # Set this in your environment
DB = os.getenv('DB', 'rkf9wd')

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

api = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}

@api.get('/songs')
def get_songs():
    query = """
    SELECT 
        songs.title AS title,
        songs.album AS album,
        songs.artist AS artist,
        songs.year AS year,
        CONCAT('https://rkf9wd-dp1-spotify.s3.amazonaws.com/', songs.file) AS file,
        CONCAT('https://rkf9wd-dp1-spotify.s3.amazonaws.com/', songs.image) AS image,
        genres.genre AS genre
    FROM 
        songs
    JOIN 
        genres ON songs.genre = genres.genreid
    ORDER BY 
        songs.title;
    """
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        return json_data
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}



@api.get("/")  # zone apex
def zone_apex():
    return {"Hello": " Kayla Kim"}

@api.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@api.get("/multiply/{c}/{d}")
def multiply(c: int, d: int):
    return {"product": c * d}

@api.get("/square/{a}")
def square(a: int):
    return {"square": a * a}

@api.get("/boogieoogie")
def boogieoogie():
    return {"message": "Boogieoogie"}

@api.get("/yesorno/{a}")
def yesorno(a: str):
    if a == "yes":
        return {"message": "yes"}
    else:
        return {"message": "no"}

@api.get("/customer/{idx}")
def customer(idx: int):
    # read the data into a df
    df = pd.read_csv("../customers.csv")
    # filter the data based on the index
    customer = df.iloc[idx] # index locator
    return customer.to_dict()

@api.post("/get_body")
async def get_body(request: Request):
    response =  await request.json()
    first_name = request["fname"]
    last_name = request["lname"]
    favorite_number = request["favnu"]
    return {"first_name": first_name, "last_name": last_name, "favorite_number": favorite_number}

    # return await request.json()
