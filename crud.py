import asyncio

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import Post, Profile, User, db_helper


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def get_user_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:  # type: User
        print(user)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *post_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in post_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_post_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts:  # type: Post
        print("post:", post)
        print("author:", post.user)


async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users:  # type: User
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)


async def get_profile_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)
    for profile in profiles:  # type: Profile
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def main():
    async with db_helper.session_factory() as session:
        await create_user(session=session, username="john")
        await create_user(session=session, username="Barney")
        await create_user(session=session, username="dazdik")
        barney = await get_user_by_username(session=session, username="Barney")
        john = await get_user_by_username(session=session, username="john")
        await create_user_profile(
            session=session, user_id=barney.id, first_name="Barney"
        )
        await create_user_profile(session=session, user_id=john.id, first_name="John")
        await get_user_with_profiles(session=session)
        await create_posts(
            session,
            barney.id,
            "I'm irish terrier",
        )
        await create_posts(session, john.id, "I'm kidult", "FastAPI")
        await get_users_with_posts_and_profiles(session=session)
        await get_post_with_authors(session=session)
        await get_profile_with_users_and_users_with_posts(session=session)


if __name__ == "__main__":
    asyncio.run(main())
