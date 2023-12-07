import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def main():
    async with db_helper.session_factory() as session:
        await create_user(session=session, username="john")
        await create_user(session=session, username="Barney")


if __name__ == "__main__":
    asyncio.run(main())
