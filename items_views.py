from typing import Annotated

from fastapi import APIRouter, Path

router = APIRouter(prefix="/items")


@router.get("/")
def get_items():
    return ["ящер Первый", "ящер Второй"]


@router.get("/latest")
def get_last_item():
    return {"item": {"id": "0", "name": "latest"}}


@router.get("/{item_id}")
def get_item_id(item_id: Annotated[int, Path(..., ge=1, lt=1_000_000)]):
    return {
        "item": {"id": item_id},
    }
