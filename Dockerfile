FROM python:3.10.3

COPY . /app

WORKDIR /app

RUN pip install poetry

RUN poetry install

CMD ["poetry", "run", "python", "./cov_pred_py/main.py"]