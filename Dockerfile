# syntax=docker/dockerfile:1.7
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HF_HOME=/opt/hf \
    TRANSFORMERS_CACHE=/opt/hf \
    HUGGINGFACE_HUB_CACHE=/opt/hf

# 1) System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 python3.10-venv python3-pip \
    git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2) Virtualenv
RUN python3.10 -m venv /opt/venv && . /opt/venv/bin/activate \
    && python -m pip install --upgrade pip wheel
ENV PATH="/opt/venv/bin:${PATH}"

# 3) Caches
RUN mkdir -p /opt/hf && chmod -R 777 /opt/hf

WORKDIR /app

# 4) Pre-copy requirements for better caching if present
COPY requirements.txt /app/requirements.txt

# Then install project requirements if the file exists
RUN if [ -f /app/requirements.txt ]; then pip install --no-cache-dir -r /app/requirements.txt; fi

# 5) Copy the project and install in editable mode
COPY . /app
RUN pip install -e .


# 6) Use bash as default entrypoint for manual operation
ENTRYPOINT ["bash"]