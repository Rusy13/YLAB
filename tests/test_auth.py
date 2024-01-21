# import pytest
# from sqlalchemy import insert, select

# from src.auth.models import department
# from conftest import client, async_session_maker

# def test_register():
#     assert 1==1
# def test_a():
#     assert 1==1
# # def test_b():
#     # assert 1==2
 






import pytest
from sqlalchemy import insert, select

from src.auth.models import department
from conftest import client, async_session_maker


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(department).values(id=1, name="IU5-55")
        await session.execute(stmt)
        await session.commit()

        query = select(department)
        result = await session.execute(query)
        assert result.all() == [(1, 'IU5-55')], "Группа не добавилась"

def test_register():
    response = client.post("/auth/register", json={
        "email": "string",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "department_id": 1
    })

    assert response.status_code == 201