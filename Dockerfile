FROM python:latest

WORKDIR /usr/src/app

COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml
COPY ./Makefile ./Makefile

RUN make environment

COPY ./src/ranchbot ./src/ranchbot
COPY ./src/main.py ./src/main.py

CMD ["python3", "-m", "poetry", "run", "python", "./src/main.py"]
