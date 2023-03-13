FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir app
WORKDIR /app
ADD . /app
COPY . /app

RUN pip install -r requirements.txt
CMD python main.py