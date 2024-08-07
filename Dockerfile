FROM python:3.11.9-slim

RUN apt-get update && apt-get install -y curl wget

WORKDIR /phabview/
COPY requirements.lock ./
COPY pyproject.toml ./
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED="true"
RUN pip install -r requirements.lock --no-cache-dir

COPY src .

EXPOSE 8000
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--timeout", "60","--log-level", "debug", "phabview.main:asgi_app"]

