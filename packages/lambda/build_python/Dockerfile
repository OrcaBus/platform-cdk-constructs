# NOTES -
# THIS IS FROM https://github.com/aws/aws-cdk/blob/main/packages/%40aws-cdk/aws-lambda-python-alpha/lib/Dockerfile
# We have made the following changes:
# 1. Added the installation of 'uv'
# 2. Addded in the UV_CACHE_DIR environment variable
# 3. Replaced 'pip' with 'uv pip' in the main code chunk
# 4. Replaced /usr/app/venv/pip with uv pip shell script wrapper
# The correct AWS SAM build image based on the runtime of the function will be
# passed as build arg. The default allows to do `docker build .` when testing.
ARG PYTHON_VERSION="3.14"
ARG IMAGE_SHA="sha256:a27b2c51c4e59815c3579417d9bec138477587c7d4cf7bdc1c056ac63a152092"
ARG IMAGE="public.ecr.aws/sam/build-python${PYTHON_VERSION}@${IMAGE_SHA}"
FROM $IMAGE

ARG TARGETPLATFORM
ARG PIP_INDEX_URL
ARG PIP_EXTRA_INDEX_URL
ARG HTTPS_PROXY
ARG POETRY_VERSION="2.4.1"
ARG POETRY_PLUGIN_EXPORT_VERSION="1.10.0"

# Add virtualenv path
ENV PATH="/usr/app/venv/bin:$PATH"

# set the pip cache location
ENV PIP_CACHE_DIR=/tmp/pip-cache

# set the poetry cache
ENV POETRY_CACHE_DIR=/tmp/poetry-cache

# ADDITION: set the uv cache
ENV UV_CACHE_DIR=/tmp/uv-cache

# ADDITION: Replace 'pip' with uv pip in the following chunk
RUN \
    # create a new virtualenv for python to use \
    # so that it isn't using root \
    uv venv /usr/app/venv "--python=${PYTHON_VERSION}" && \
    # Create a new location for the pip cache
    mkdir /tmp/pip-cache && \
    # Ensure all users can write to pip cache
    chmod -R 777 /tmp/pip-cache && \
    # Upgrade pip (required by cryptography v3.4 and above, which is a dependency of poetry)
    uv pip install --upgrade pip && \
    # Create a new location for the poetry cache
    mkdir /tmp/poetry-cache && \
    # Ensure all users can write to poetry cache
    chmod -R 777 /tmp/poetry-cache && \
    # Ensure all users can write to uv cache
    chmod -R 777 /tmp/uv-cache && \
    # Install pipenv and poetry
    uv pip install "poetry==${POETRY_VERSION}" && \
    # Install poetry export plugin
    poetry self add "poetry-plugin-export==${POETRY_PLUGIN_EXPORT_VERSION}" && \
    # Ensure no temporary files remain in the caches
    rm -rf /tmp/pip-cache/* /tmp/poetry-cache/* /tmp/uv-cache/*

# ADDITION: Replace /usr/app/venv/pip with uv pip
RUN printf '#!/usr/bin/env bash \nuv pip $@\n' > /usr/app/venv/bin/pip && \
    printf '#!/usr/bin/env bash \nuv pip $@\n' > /usr/app/venv/bin/pip3

CMD [ "python" ]