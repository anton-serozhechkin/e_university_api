from apps.common.exceptions import BackendException

from fastapi import status as http_status
from typing import Any


def check_for_empty_value(value: Any, value_name: str = '') -> None:
    if not value:
        raise BackendException(
            message=f'Input {value_name} is incorrect',
            code=http_status.HTTP_404_NOT_FOUND
        )
