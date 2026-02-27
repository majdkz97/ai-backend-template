from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core import get_session
from app import crud
from app.schemas import ItemCreate, ItemResponse


router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    return crud.create_item(session=session, item_in=item)


@router.get("/", response_model=list[ItemResponse])
def read_items(session: Session = Depends(get_session)):
    return crud.get_items(session=session)


@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: str, session: Session = Depends(get_session)):
    item = crud.get_item(session=session, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

