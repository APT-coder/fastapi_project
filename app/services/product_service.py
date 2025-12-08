from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.models.category import Category
from app.schemas.product_schema import ProductCreate
from fastapi import HTTPException, status


async def get_products(
    db: AsyncSession,
    product_id: Optional[int] = None,
    product_name: Optional[str] = None,
    category_name: Optional[str] = None,
):
    stmt = select(Product).options(joinedload(Product.category))

    if product_id:
        stmt = stmt.where(Product.id == product_id)

    if product_name:
        stmt = stmt.where(Product.name.ilike(f"%{product_name}%"))

    if category_name:
        stmt = stmt.join(Product.category).where(
            Category.name.ilike(f"%{category_name}%")
        )

    result = await db.execute(stmt)
    return result.scalars().all()


async def create_product(db: AsyncSession, product_in: ProductCreate):
    category_id = product_in.category_id

    if category_id:
        category = await db.get(Category, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with given category_id does not exist",
            )

    else:
        if not product_in.category_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either category_id or category_name must be provided",
            )

        category = Category(
            name=product_in.category_name,
            description=product_in.category_description,
        )

        db.add(category)
        await db.flush() 
        category_id = category.id

    # Create product
    product = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        available_count=product_in.available_count,
        seller_id=product_in.seller_id,
        category_id=category_id,
    )

    db.add(product)
    await db.commit()

    stmt = (
        select(Product)
        .options(selectinload(Product.category))
        .where(Product.id == product.id)
    )

    result = await db.execute(stmt)
    product = result.scalar_one()

    return product

