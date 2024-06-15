FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./SocialY .

EXPOSE 8000


CMD ["python", "./SocialY/manage.py", "runserver"]