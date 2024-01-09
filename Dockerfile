# 
FROM python:3.11-slim

# 
COPY . /app
COPY pyproject.toml /app 
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root


RUN apt-get update && apt-get install nano

COPY . .

# 
RUN chmod +x ./start.sh
CMD ./start.sh
