FROM python:3.8

ENV PYTHONPATH=/backend
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /backend
WORKDIR /backend

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8889

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8889"]
