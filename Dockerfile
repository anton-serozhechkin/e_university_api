FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.2.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME='/usr/local'

# install `poetry` package manager:
# https://github.com/python-poetry/poetry
RUN curl -sSL 'https://install.python-poetry.org' | python -

WORKDIR /app

# install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --with parcing,documents,security,database,main


# add project files *after* dependencies
# https://docs.docker.com/build/building/cache/#order-your-layers
COPY . .

CMD ["uvicorn", "apps.main:app"]
