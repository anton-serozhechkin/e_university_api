from faker import Faker
from fastapi import FastAPI, status
from httpx import AsyncClient
from typing import List

from apps.authorization.services import create_access_token, create_refresh_token
from apps.authorization.services import create_access_token
from apps.common.schemas import JSENDStatus
from apps.users.models import User
from apps.authorization.models import Role
from tests.apps.conftest import assert_jsend_response
from tests.apps.authorization.factories import RoleFactory
from tests.apps.users.factories import UserFactory


class TestLoginRouter:
    async def test_login_200(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
    ):
        password = faker.pystr(max_chars=255, min_chars=8)
        mod_email = faker.email()
        mod_login = faker.pystr(min_chars=6, max_chars=40)
        user: User = UserFactory(
            mod_email=mod_email, mod_login=mod_login, simple_password=password
        )
        response = await async_client.request(
            method="POST",
            url=app_fixture.url_path_for(name="login"),
            data={
                "grant_type": None,
                "username": user.login,
                "password": password,
                "scope": "",
                "client_id": None,
                "client_secret": None,
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
                "Access-Control-Allow-Origin": "*",
            }
        )
        data = response.json()
        assert data.get("access_token") == create_access_token(user.email)
        assert data.get("refresh_token") == create_refresh_token(user.email)
        assert data.get("user_id") == user.user_id

    async def test_read_available_roles(
            self,
            async_client: AsyncClient,
            app_fixture: FastAPI,
            faker: Faker,
    ):
        user: User = UserFactory(email="c@a.com")
        roles: List[Role] = RoleFactory.create_batch(size=3)
        token: str = create_access_token(subject="c@a.com")
        response = await async_client.get(
            url=app_fixture.url_path_for("read_available_roles"),
            headers={"Authorization": f"Bearer {token}"},
        )
        assert_jsend_response(
            response=response,
            http_code=status.HTTP_200_OK,
            status=JSENDStatus.SUCCESS,
            message="Got roles",
            code=status.HTTP_200_OK,
        )
        data = response.json()["data"]
        amend = len(data) - 3
        for i in range(3):
            assert data[i+amend].get("role_id") == roles[i].role_id
            assert data[i+amend].get("role_name") == roles[i].role_name
