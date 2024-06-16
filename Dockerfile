FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./SocialY .

EXPOSE 8000

ENV ENV_TYPE="DOCKER"
ENV POSTGRES_USER=postgres
ENV POSTGRES_HOST=localhost

CMD ["python", "./SocialY/manage.py", "runserver"]