from fastapi import APIRouter

router = APIRouter(prefix="/cart", tags=['cart'])


@router.get("/")
async def get_cart():
    return {"message": "all items in cart"}


@router.post("/")
async def add_to_cart():
    return {"message": "add items to cart"}


@router.delete("/")
async def delete_item_from_cart(id: int):
    return {"message": "delete an item from cart"}
