#dockerfile file for setting up the pipeline environment
FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"


COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

COPY ingest.py .

ENTRYPOINT ["python", "ingest.py"]   