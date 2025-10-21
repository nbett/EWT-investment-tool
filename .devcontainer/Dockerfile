FROM mcr.microsoft.com/devcontainers/python:3.11

# Match your repo name
WORKDIR /workspaces/EWT-investment-tool

# requirements.txt lives at repo root (context is set to "..")
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
