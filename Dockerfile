FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . .

EXPOSE 8888

RUN uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=project

CMD ["uv", "run", "--with", "jupyter", "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

