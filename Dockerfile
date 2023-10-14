FROM python:3.8
ENV PYTHONUNBUFFERED=1
COPY . /django-openid
WORKDIR /django-openid
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
WORKDIR /django-openid/project
EXPOSE 8000

CMD ["/bin/bash", "-c", "python3 manage.py makemigrations;python3 manage.py migrate;python3 manage.py runserver 0.0.0.0:8000"]