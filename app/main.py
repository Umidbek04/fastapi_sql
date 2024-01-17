from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
import time
from psycopg2.extras import RealDictCursor
import mysql.connector
import pymysql


app = FastAPI()



while True:
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='umidbek04#',
            database='fastapi_sql'
        )

        cursor = connection.cursor()

        print("Database successfully connected")
        break


    except Exception as error:
        print('connecting  to database failed')
        print('error ', error)
        time.sleep(3)



class Post(BaseModel):
    city_name: str
    size: str
    overpopulated: bool = True  

@app.get("/vivo")
def gettur():
    return {"message":"success"}



@app.get('/cities')
def get_data():
    cursor.execute("""SELECT * FROM cities""")
    cities = cursor.fetchall()

    return {"data": cities}

@app.get('/getcity')
def get_city():
    cursor.execute("""SELECT * FROM cities
                    order by id
                    limit 3 offset 2;""")
    cities = cursor.fetchall()
    return cities



@app.post('/cities', status_code=status.HTTP_201_CREATED)
def make_post(post: Post):
    cursor.execute("""insert into cities (city_name, size, overpopulated) 
                   values (%s, %s, %s)""", (post.city_name, post.size, post.overpopulated))
    
    connection.commit()
    new_city_id = cursor.lastrowid
    cursor.execute("SELECT * FROM cities WHERE id = %s", (new_city_id,))
    new_city = cursor.fetchone()
    return {"new post": new_city}




@app.get('/cities/{id}', status_code=status.HTTP_200_OK)
def get_one(id: int):
    cursor.execute("""select * from cities where id = %s""", (id,))
    interested_post = cursor.fetchone()

    if not interested_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"city with id: {id} does not exist")
    
    return {"interested post": interested_post}




@app.delete("/cities/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM cities WHERE id = %s""", (id,))
    connection.commit()

    if cursor.rowcount > 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"City with id {id} not found")





@app.put("/cities/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE cities SET city_name = %s, size = %s, overpopulated = %s WHERE id = %s""",
                   (post.city_name, post.size, post.overpopulated, id))
    connection.commit()

    cursor.execute("""SELECT * FROM cities WHERE id = %s""", (id,))
    updated_post = cursor.fetchone()

    if updated_post:
        return {"updated_post": updated_post}
    else:
        raise HTTPException(status_code=404, detail=f"City with id {id} not found")

