FROM python:latest

WORKDIR /usr/src/app

COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock

RUN pip install pipenv
RUN pipenv install --system

COPY ./src ./src

CMD ["python", "./src/ranchbot/main.py"]
