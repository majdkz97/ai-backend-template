from typing import List, Optional

from sqlmodel import Session, select

from .models import Item
from .schemas import ItemCreate


def create_item(session: Session, item_in: ItemCreate) -> Item:
    db_item = Item(**item_in.model_dump())
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_items(session: Session) -> List[Item]:
    return session.exec(select(Item)).all()


def get_item(session: Session, item_id: str) -> Optional[Item]:
    return session.get(Item, item_id)

