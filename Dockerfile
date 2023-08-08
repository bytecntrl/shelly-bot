FROM python:alpine

RUN apk add --no-cache gcc musl-dev libffi-dev

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["python", "main.py"]
