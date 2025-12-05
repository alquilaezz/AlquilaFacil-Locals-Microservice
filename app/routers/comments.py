from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db, get_current_user, CurrentUser

router = APIRouter(prefix="/api/v1/comment", tags=["Comment"])

# ---- POST /api/v1/comment ----

@router.post("", response_model=schemas.CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(
    payload: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    local = db.query(models.Local).filter(models.Local.id == payload.local_id).first()
    if not local:
        raise HTTPException(status_code=404, detail="Local not found")

    comment = models.Comment(
        user_id=current_user.id,
        local_id=payload.local_id,
        text=payload.text,
        rating=payload.rating,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

# ---- GET /api/v1/comment/local/{localId} ----

@router.get("/local/{local_id}", response_model=List[schemas.CommentOut])
def get_comments_by_local(
    local_id: int,
    db: Session = Depends(get_db),
):
    local = db.query(models.Local).filter(models.Local.id == local_id).first()
    if not local:
        raise HTTPException(status_code=404, detail="Local not found")

    comments = (
        db.query(models.Comment)
        .filter(models.Comment.local_id == local_id)
        .order_by(models.Comment.id.desc())
        .all()
    )
    return comments
