from fastapi import FastAPI,Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from .models import Base
models.Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import Session
from fastapi import Depends

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    # rating : Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database = 'fastapi', user="postgres", password = "Admin@123", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DATABASE connection successfull")
        break
    except Exception as error:
        print("Connectiion to DATABASE failed ")
        print("Error was ", error)
        time.sleep(2)

my_posts = [{"title":"title of post 1", "content": "content of post 1", "id":1},
            {"title":"title of post 2", "content":"content of post 2", "id":2}]


def get_one_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"message": "World is good"}

@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    return {'status' : 'success'}

@app.get("/posts")
def get_posts():
    cursor.execute("Select * from posts")
    posts = cursor.fetchall()
    return {"data":posts}


@app.post("/createposts",status_code=status.HTTP_201_CREATED)
def craete_posts(post : Post):
    cursor.execute(""" INSERT INTO posts (title, content,published) VALUES (%s,%s,%s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE ID = %s """,(str(id),))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")
    return {"post_details":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE ID = %s RETURNING *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute(""" UPDATE posts SET title=%s , content=%s, published=%s WHERE ID = %s RETURNING *""",(post.title,post.content,post.published,(str(id))))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")
    return {"data":updated_post}
