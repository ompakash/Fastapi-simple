from fastapi import FastAPI,Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


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

@app.get("/posts")
def get_posts():
    return {"data":my_posts}


@app.post("/createposts",status_code=status.HTTP_201_CREATED)
def craete_posts(new_post : Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(1,10000)
    my_posts.append(post_dict)
    return {"new_post": new_post}

@app.get("/posts/{id}")
def get_post(id:int):
    post = get_one_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")
    return {"post_details":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")
    my_posts.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data":post_dict}
