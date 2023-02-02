import typing
import uuid
from typing import List

import pytest
from faker import Faker
from fastapi import FastAPI, status
from httpx import AsyncClient, Response

from apps.authorization.services import create_access_token
from apps.common.enums import JSENDStatus
from apps.common.services import ModelType
from apps.users.models import User
from tests.apps.users.factories import UserFactory


def assert_jsend_response(
    response: Response,
    http_code: status,
    status: JSENDStatus,
    message: str,
    code: int,
    data: typing.Any = ...,
) -> None:
    response_json = response.json()
    assert response.status_code == http_code
    assert response_json["status"] == status
    assert response_json["message"] == message
    assert response_json["code"] == code
    if data is not ...:
        assert response_json["data"] == data


@pytest.fixture(scope="function")
async def access_token(
    faker: Faker,
) -> str:
    user: User = UserFactory(mod_email=faker.email())
    return create_access_token(subject=user.email)


def find_created_instance(instance_id: int, data: List, attr: str) -> ModelType:
    for instance in data:
        if instance.get(attr) == instance_id:
            return instance
