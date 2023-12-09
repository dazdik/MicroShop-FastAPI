import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import Post, Profile, User, db_helper, Order, Product


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


async def main_relations(session: AsyncSession):
    await create_user(session=session, username="john")
    await create_user(session=session, username="Barney")
    await create_user(session=session, username="dazdik")
    barney = await get_user_by_username(session=session, username="Barney")
    john = await get_user_by_username(session=session, username="john")
    await create_user_profile(session=session, user_id=barney.id, first_name="Barney")
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


async def create_order(
    session: AsyncSession,
    promocode: str | None = None,
) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession,
    name: str,
    description: str,
    price: int,
) -> Product:
    product = Product(name=name, description=description, price=price)
    session.add(product)
    await session.commit()
    return product


async def create_orders_and_products(session: AsyncSession):
    order = await create_order(session=session)
    order_promo = await create_order(session=session, promocode="discount20")
    peanut_butter = await create_product(
        session=session,
        name="peanut butter",
        description="tasty",
        price=400,
    )
    orange_jam = await create_product(
        session=session,
        name="jam",
        description="orange",
        price=100,
    )
    bread = await create_product(
        session=session,
        name="bread",
        description="wheat",
        price=50,
    )
    order = await session.scalar(
        select(Order).where(Order.id == order.id).options(selectinload(Order.products))
    )
    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(selectinload(Order.products))
    )
    order.products = [peanut_butter, orange_jam, bread]
    order_promo.products.append(bread)
    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(selectinload(Order.products)).order_by(Order.id)
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_m2m(session: AsyncSession):
    # await create_orders_and_products(session)
    orders = await get_orders_with_products(session)
    for order in orders:
        print(order.id, order.promocode, order.created_at, "products: ")
        for product in order.products:  # type: Product
            print("-", product.id, product.name, product.description, product.price)


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session=session)
        await demo_m2m(session=session)


if __name__ == "__main__":
    asyncio.run(main())
