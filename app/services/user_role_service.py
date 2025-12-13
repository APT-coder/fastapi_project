from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.schemas.user_role_schema import UserRoleCreate
from app.services.helper_service import get_user_with_roles

async def assign_user_role(db: AsyncSession, data: UserRoleCreate):
    # Validate if the user and roles exist
    await validate_user_and_roles(db, data)

    return await update_user_roles(db, data)

async def validate_user_and_roles(db: AsyncSession, data: UserRoleCreate) -> None:
    # Validate if the user exists
    user = await db.execute(select(User).filter(User.id == data.user_id))
    if not user.scalar_one_or_none():
        raise ValueError(f"User with ID {data.user_id} does not exist.")
    
    # Validate if the role_ids exist
    roles = await db.execute(select(Role.id).filter(Role.id.in_(data.role_ids)))
    valid_role_ids = set(roles.scalars().all())
    
    if len(valid_role_ids) != len(set(data.role_ids)):
        invalid_role_ids = set(data.role_ids) - valid_role_ids
        raise ValueError(f"Invalid role IDs: {invalid_role_ids}")

async def get_user_roles(db: AsyncSession, user_id: int) -> set:
    # Fetch the roles already assigned to the user
    result = await db.execute(
        select(UserRole.role_id)
        .filter(UserRole.user_id == user_id)
    )
    return set(result.scalars().all())


async def update_user_roles(db: AsyncSession, data: UserRoleCreate) -> dict:
    current_roles = await get_user_roles(db, data.user_id)
    input_roles = set(data.role_ids)

    if current_roles == input_roles:
        # Load user + roles to return
        user = await get_user_with_roles(db, data.user_id)
        return {
            "message": f"User '{data.user_id}' already has these roles.",
            "user": user
        }

    # Delete all current roles
    await db.execute(delete(UserRole).where(UserRole.user_id == data.user_id))

    # Insert new roles
    new_role_entries = [
        UserRole(user_id=data.user_id, role_id=r)
        for r in input_roles
    ]
    db.add_all(new_role_entries)
    await db.commit()

    # Load user with updated roles
    user = await get_user_with_roles(db, data.user_id)
    return {
        "message": f"User '{data.user_id}' updated with new roles.",
        "user": user
    }
