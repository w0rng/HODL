FROM python:3.10-slim as builder

WORKDIR app
RUN pip install -U pip setuptools wheel pdm
COPY ./pyproject.toml ./pdm.lock ./
RUN mkdir __pypackages__ &&\
    pdm install --prod --no-lock --no-editable

FROM python:3.10-alpine
RUN apk add --no-cache libgcc
WORKDIR /app

COPY --from=builder /app/__pypackages__/3.10 /pkgs
COPY src .
ENV PYTHONPATH "${PYTHONPATH}:/pkgs/lib"
ENV PATH "${PATH}:/pkgs/bin"
