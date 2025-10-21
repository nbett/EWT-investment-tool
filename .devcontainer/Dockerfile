FROM mcr.microsoft.com/devcontainers/python:3.11

# Must match your repo folder name
WORKDIR /workspaces/EWT-investment-tool

# Context is the repo root (..), so this path is valid
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
