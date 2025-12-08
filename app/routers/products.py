from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.product_schema import ProductCreate, ProductRead
from app.services.product_service import get_products, create_product

router = APIRouter()

@router.get("/", response_model=List[ProductRead])
async def read_products(
    id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    products = await get_products(
        db,
        product_id=id,
        product_name=name,
        category_name=category,
    )

    return [
        ProductRead(
            id=p.id,
            name=p.name,
            description=p.description,
            price=p.price,
            available_count=p.available_count,
            seller_id=p.seller_id,
            category_id=p.category_id,
            category_name=p.category.name if p.category else None,
        )
        for p in products
    ]

@router.post(
    "/", response_model=ProductRead, status_code=status.HTTP_201_CREATED
)
async def post_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    product = await create_product(db, product_in)

    return ProductRead(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        available_count=product.available_count,
        seller_id=product.seller_id,
        category_id=product.category_id,
    )
