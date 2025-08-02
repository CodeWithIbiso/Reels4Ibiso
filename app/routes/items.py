from fastapi import APIRouter, HTTPException
from app.schemas.user import ItemModel
from app.connections.database import db
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=ItemModel)
async def create_item(item: ItemModel):
    item_dict = item.dict(by_alias=True)
    result = await db.items.insert_one(item_dict)
    item_dict["_id"] = result.inserted_id
    return item_dict

@router.get("/{item_id}", response_model=ItemModel)
async def get_item(item_id: str):
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
