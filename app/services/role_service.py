from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import Set, Optional
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.schemas.role_schema import RoleCreate


async def create_or_update_role(db: AsyncSession, data: RoleCreate):
    # Validate permissions if provided
    if data.permissions:
        await validate_permission_ids(db, data.permissions)
    
    # Check if role exists
    existing_role = await get_role_by_name(db, data.role_name)
    
    if existing_role:
        return await update_existing_role(db, existing_role, data.permissions)
    
    # Create new role
    role = await create_new_role(db, data.role_name, data.permissions)
    await db.commit()
    await db.refresh(role)
    
    return {
        "message": f"Role '{data.role_name}' created.",
        "role": role
    }


async def validate_permission_ids(db: AsyncSession, permission_ids: list[int]) -> None:
    valid_perms = await db.execute(
        select(Permission.id).filter(Permission.id.in_(permission_ids))
    )
    valid_perm_ids = set(valid_perms.scalars().all())
    
    if len(valid_perm_ids) != len(set(permission_ids)):
        invalid_ids = set(permission_ids) - valid_perm_ids
        raise ValueError(f"Invalid permission IDs: {invalid_ids}")


async def get_role_by_name(db: AsyncSession, role_name: str) -> Optional[Role]:
    result = await db.execute(
        select(Role)
        .filter(Role.role_name == role_name)
        .options(selectinload(Role.permissions))
    )
    return result.scalar_one_or_none()


async def get_role_permission_ids(db: AsyncSession, role_id: int) -> Set[int]:
    result = await db.execute(
        select(RolePermission.permission_id)
        .filter(RolePermission.role_id == role_id)
    )
    return set(result.scalars().all())


async def sync_role_permissions(
    db: AsyncSession, 
    role_id: int, 
    permission_ids: Optional[list[int]]
) -> None:
    # Delete existing permissions
    await db.execute(
        delete(RolePermission).where(RolePermission.role_id == role_id)
    )
    
    # Add new permissions if provided
    if permission_ids:
        role_permissions = [
            RolePermission(role_id=role_id, permission_id=perm_id)
            for perm_id in permission_ids
        ]
        db.add_all(role_permissions)


async def create_new_role(
    db: AsyncSession, 
    role_name: str, 
    permission_ids: Optional[list[int]]
) -> Role:
    
    role = Role(role_name=role_name)
    db.add(role)
    await db.flush()  # Get the role.id without committing
    
    # Add permissions if provided
    if permission_ids:
        role_permissions = [
            RolePermission(role_id=role.id, permission_id=perm_id)
            for perm_id in permission_ids
        ]
        db.add_all(role_permissions)
    
    return role


async def update_existing_role(db: AsyncSession, role: Role, permission_ids: Optional[list[int]]) -> dict:
    current_permissions = await get_role_permission_ids(db, role.id)
    input_permissions = set(permission_ids) if permission_ids else set()
    
    if current_permissions == input_permissions:
        return {
            "message": f"Role '{role.role_name}' already exists with the same permissions.",
            "role": role
        }
    
    # Sync permissions
    await sync_role_permissions(db, role.id, permission_ids)
    await db.commit()
    await db.refresh(role)
    
    return {
        "message": f"Role '{role.role_name}' updated with new permissions.",
        "role": role
    }


async def get_roles(db: AsyncSession):
    result = await db.execute(select(Role))
    return result.scalars().all()