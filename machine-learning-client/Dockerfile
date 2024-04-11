FROM python:3.10

WORKDIR /machine-learning-client
COPY . .

RUN pip install pipenv

RUN pipenv install

#EXPOSE?

CMD ["pipenv", "run", "python", "client.py"]