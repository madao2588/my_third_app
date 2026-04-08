from app.core.database import AsyncSessionLocal
from app.repositories.log_repo import LogRepository


async def record_exception_log(
    *,
    level: str,
    message: str,
    error_stack: str | None = None,
) -> None:
    async with AsyncSessionLocal() as session:
        log_repo = LogRepository(session)
        await log_repo.create(
            level=level,
            message=message,
            error_stack=error_stack,
        )
