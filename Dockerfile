FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-venv \
    build-essential \
    libatlas-base-dev \
    liblapack-dev \
    libblas-dev \
    libgomp1 \
    curl \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN ln -s /usr/bin/python3.10 /usr/local/bin/python && \
    ln -s /usr/bin/pip3 /usr/local/bin/pip

WORKDIR /app

COPY . .

EXPOSE 8888

RUN uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=project

CMD ["uv", "run", "--with", "jupyter", "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]