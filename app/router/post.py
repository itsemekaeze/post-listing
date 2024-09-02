from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..database import get_db
from .. import models, schemas
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/post",
    tags=['Posts']
)


@router.get("/")
def get_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts""")
    # post = cursor.fetchall()
    # print(post)
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    # (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(new_post)
    new_post = models.Post(**dict(post))
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}")
def get_one_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id  = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return post


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    # (post.title, post.content, post.published, str(id)))
    # update = cursor.fetchone()
    # conn.commit()
    # print(update)
    update = db.query(models.Post).filter(models.Post.id == id)
    updated = update.first()
    if updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    update.update(dict(post), synchronize_session=False)
    db.commit()

    return update.first()


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
