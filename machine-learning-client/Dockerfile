FROM python:3.11

WORKDIR /machine-learning-client

COPY . .

RUN pip install pipenv

RUN pipenv install

EXPOSE 46377

CMD ["pipenv", "run", "python", "client.py"]