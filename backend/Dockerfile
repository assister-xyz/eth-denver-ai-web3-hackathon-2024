FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

WORKDIR /app/

COPY ./requirements.txt /app/

RUN pip install --upgrade pip
RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 5000

COPY . /app/

CMD ["python","main.py"]