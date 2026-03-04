from fastapi import FastAPI
from fastapi import Body,Response,status,HTTPException,Depends
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app=FastAPI()




class Post(BaseModel):
    title:str
    content:str
    published:bool=True

while True:

    try:
        conn = psycopg2.connect(
    host="::1",
    port=5432,
    database="fastapi",
    user="postgres",
    password="krisp123",
    cursor_factory=RealDictCursor,
)

        cursor=conn.cursor()
        print("database connection was successful")
        break
    except Exception as error:
        print("connection to database failed")
        print("error:",error)
        time.sleep(60)

my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favourite foods","content":"i like cake","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
#get for retreiving the data
@app.get("/")
def root():
    return{"message":"krishna!!!!"}

@app.get("/sqlalchemy")
def test_post(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return{"data":posts}

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts=cursor.fetchall()
    print(posts)
    return{"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post,db:Session=Depends(get_db)):
    new_post= models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    


@app.get("/posts/{id}")#path parameter
def get_post(id:str):
    cursor.execute("SELECT * FROM posts WHERE id=%s",(str(id),))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return{"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("DELETE FROM posts WHERE id=%s returning*",(str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()
    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")

   
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def Update_post(id:int,post:Post):
    cursor.execute("UPDATE posts SET title=%s,content=%s,published=%s  WHERE id=%s RETURNING *",(post.title,post.content,post.published,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    
    return{"data":updated_post}

