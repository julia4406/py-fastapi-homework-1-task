from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import MovieModel


async def get_movie(
        movie_id: int,
        db: AsyncSession
):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    return movie


async def get_all_movies_paginated(
        db: AsyncSession,
        page: int,
        per_page: int
):
    # з якого елемента починати вибірку (напр page = 2 і per_page = 10 -> з 10
    offset = (page - 1) * per_page

    # Звертаємось до бази даних, повертає об'єкт, з потрібним зрізом (offset),
    # limit - відобразить кількість на сторінці
    result = await db.execute(select(MovieModel))
    # через scalars отримуємо результати (як objects)
    all_movies = result.scalars().all()

    movies = all_movies[offset:offset + per_page]
    total_items = len(movies)
    total_pages = total_items // per_page + (
        1 if total_items % per_page != 0 else 0
    )
    # previous page
    if page <= 1:
        prev_page = None
    else:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"

    # next page
    if page >= total_pages:
        next_page = None
    else:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_items": total_items,
        "total_pages": total_pages
    }
