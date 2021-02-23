FROM python:3.9.2 as development_build

# Setup Python and pip environment variables
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONPATH="${PYTHONPATH}:/code" \
  # pip
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    make \
  # Cleaning cache:
  && apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/* \
  # Install cookiecutter
  && pip install cookiecutter
