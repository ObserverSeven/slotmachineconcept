FROM python:3.12-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder --chown=nobody:nogroup /root/.local /home/nobody/.local

COPY --chown=nobody:nogroup . .

ENV PATH=/home/nobody/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN groupadd -r nobody || true && useradd -r -g nobody nobody 2>/dev/null || true

USER nobody

CMD ["python", "run.py"]
