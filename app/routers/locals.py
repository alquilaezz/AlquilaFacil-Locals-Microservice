from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db, get_current_user, CurrentUser

router = APIRouter(prefix="/api/v1/locals", tags=["Locals"])

# ---- Helpers ----

def _local_to_out(local: models.Local) -> schemas.LocalOut:
    return schemas.LocalOut(
        id=local.id,
        userId=local.user_id,
        localName=local.local_name,
        descriptionMessage=local.description,
        country=local.country,
        city=local.city,
        district=local.district,
        street=local.street,
        price=local.price_per_hour,
        capacity=local.capacity,
        features=local.features,
        localCategoryId=local.local_category_id,
        created_at=local.created_at,
        updated_at=local.updated_at,
        photoUrls=[p.url for p in local.photos],
    )

def _check_owner(local: models.Local, current_user: CurrentUser):
    if local.user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")

# ---- POST /api/v1/locals ----

@router.post("", response_model=schemas.LocalOut, status_code=status.HTTP_201_CREATED)
def create_local(
    payload: schemas.LocalCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    # (opcional) validar que exista la categoría
    category = (
        db.query(models.LocalCategory)
        .filter(models.LocalCategory.id == payload.localCategoryId)
        .first()
    )
    if not category:
        raise HTTPException(status_code=404, detail="Local category not found")

    local = models.Local(
        local_name=payload.localName,
        description=payload.descriptionMessage,
        country=payload.country,
        city=payload.city,
        district=payload.district,
        street=payload.street,
        price_per_hour=payload.price,
        capacity=payload.capacity,
        features=payload.features,
        local_category_id=payload.localCategoryId,
        user_id=current_user.id,
    )

    db.add(local)
    db.flush()  # para tener el id antes del commit

    # fotos
    if payload.photoUrls:
        for url in payload.photoUrls:
            db.add(models.LocalPhoto(url=url, local_id=local.id))

    db.commit()
    db.refresh(local)
    return _local_to_out(local)

# ---- GET /api/v1/locals ----

@router.get("", response_model=List[schemas.LocalOut])
def list_locals(db: Session = Depends(get_db)):
    locals_ = db.query(models.Local).all()
    return [_local_to_out(l) for l in locals_]

# ---- GET /api/v1/locals/{localId} ----

@router.get("/{local_id}", response_model=schemas.LocalOut)
def get_local(local_id: int, db: Session = Depends(get_db)):
    local = db.query(models.Local).filter(models.Local.id == local_id).first()
    if not local:
        raise HTTPException(status_code=404, detail="Local not found")
    return _local_to_out(local)

# ---- PUT /api/v1/locals/{localId} ----

@router.put("/{local_id}", response_model=schemas.LocalOut)
def update_local(
    local_id: int,
    payload: schemas.LocalUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    local = db.query(models.Local).filter(models.Local.id == local_id).first()
    if not local:
        raise HTTPException(status_code=404, detail="Local not found")

    _check_owner(local, current_user)

    data = payload.dict(exclude_unset=True)
    photo_urls = data.pop("photo_urls", None)

    for field, value in data.items():
        setattr(local, field, value)

    # actualizar fotos (simple: borramos y volvemos a crear si se envían)
    if photo_urls is not None:
        for p in list(local.photos):
            db.delete(p)
        for url in photo_urls:
            db.add(models.LocalPhoto(url=url, local_id=local.id))

    db.add(local)
    db.commit()
    db.refresh(local)
    return _local_to_out(local)

# ---- GET /search-by-category-id-capacity-range/{categoryId}/{minCapacity}/{maxCapacity} ----

@router.get(
    "/search-by-category-id-capacity-range/{category_id}/{min_capacity}/{max_capacity}",
    response_model=List[schemas.LocalOut],
)
def search_by_category_and_capacity(
    category_id: int,
    min_capacity: int,
    max_capacity: int,
    db: Session = Depends(get_db),
):
    locals_ = (
        db.query(models.Local)
        .filter(
            models.Local.local_category_id == category_id,
            models.Local.capacity >= min_capacity,
            models.Local.capacity <= max_capacity,
        )
        .all()
    )
    return [_local_to_out(l) for l in locals_]

# ---- GET /get-all-districts ----

@router.get("/get-all-districts", response_model=List[str])
def get_all_districts(db: Session = Depends(get_db)):
    # DISTINCT district
    districts = (
        db.query(models.Local.district)
        .distinct()
        .order_by(models.Local.district.asc())
        .all()
    )
    return [d[0] for d in districts]

# ---- GET /get-user-locals/{userId} ----

@router.get("/get-user-locals/{user_id}", response_model=List[schemas.LocalOut])
def get_user_locals(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    locals_ = (
        db.query(models.Local)
        .filter(models.Local.user_id == user_id)
        .order_by(models.Local.created_at.desc())
        .all()
    )
    return [_local_to_out(l) for l in locals_]
