FROM python:3.11-alpine as builder

WORKDIR app
RUN pip install -U pip setuptools wheel pdm
COPY ./pyproject.toml ./pdm.lock ./
RUN mkdir __pypackages__ &&\
    pdm install --prod --no-lock --no-editable

FROM python:3.11-alpine
WORKDIR /app

COPY --from=builder /app/__pypackages__/3.11 /pkgs
COPY src .
ENV PYTHONPATH "${PYTHONPATH}:/pkgs/lib"
ENV PATH "${PATH}:/pkgs/bin"
