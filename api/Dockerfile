FROM rust:1.61-bullseye as every-beat
WORKDIR /src
RUN git clone https://github.com/EnigmaCurry/every_beat.git && \
    cd every_beat && \
    cargo build --release

FROM python:3.10 as build
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10
WORKDIR /code
COPY --from=every-beat /src/every_beat/target/release/every_beat /usr/bin/every_beat
COPY --from=build /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
