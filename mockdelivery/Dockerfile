FROM python:3.11
RUN pip install poetry
WORKDIR /app
COPY . /app
RUN poetry config virtualenvs.create false
RUN poetry install --only main
CMD ["poetry", "run", "python", "mockdelivery/main.py"]