FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN apt update && apt install -y postgresql-client && rm -rf /var/lib/apt/lists/*

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

COPY . .

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
