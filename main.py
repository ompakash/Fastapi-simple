from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None


app = FastAPI()

my_posts = [{"title":"title of post 1", "content": "content of post 1", "id":1},
            {"title":"title of post 2", "content":"content of post 2", "id":2}]


def get_one_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post


@app.get("/")
def read_root():
    return {"message": "World is good"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}


@app.post("/createposts")
def craete_posts(new_post : Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(1,10000)
    my_posts.append(post_dict)
    return {"new_post": new_post}

@app.get("/posts/{id}")
def get_post(id:int):
    post = get_one_post(id)
    return {"post_details":post}

