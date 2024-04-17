FROM python:3.10

WORKDIR /machine-learning-client

COPY . .

RUN pip install pipenv

RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pipenv install

EXPOSE 46377

CMD ["pipenv", "run", "python", "client.py"]