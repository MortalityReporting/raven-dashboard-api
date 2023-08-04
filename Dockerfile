# FASTAPI Builder Stage
FROM python:3.11-slim AS fastapi-builder

WORKDIR /app

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt --no-cache-dir --use-pep517

# Operational stage
FROM python:3.11-slim

WORKDIR /app

# Get the virtual environment from builder stage
COPY --from=fastapi-builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

COPY ./api ./api


CMD ["hypercorn", "api.main:app", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--access-logformat", "%(h)s %(l)s \"%(r)s\" %(s)s Origin:\"%({origin}i)s\" X-Forwarded-For:\"%({x-forwarded-for}i)s\""]