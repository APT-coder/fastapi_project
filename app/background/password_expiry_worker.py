import asyncio
import logging
from app.db.database import AsyncSessionLocal
from app.services.user_service import deactivate_expired_password_users

logger = logging.getLogger(__name__)

CHECK_INTERVAL_SECONDS = 300  # 5 minutes


async def password_expiry_worker():
    while True:
        try:
            async with AsyncSessionLocal() as db:
                count = await deactivate_expired_password_users(db)

                if count > 0:
                    logger.info(f"Password expiry job: {count} users deactivated")

        except Exception as e:
            logger.exception("Password expiry job failed")

        await asyncio.sleep(CHECK_INTERVAL_SECONDS)
