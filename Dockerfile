FROM python

ARG SERVER_ADDRESS
ARG SERVER_PORT

WORKDIR /mynews

# Install chrome and django, selenium
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&\
    apt-get update && apt-get install -y ./google-chrome-stable_current_amd64.deb

ENTRYPOINT pip install -r requirements.txt &&\
    python manage.py makemigrations &&\
    python manage.py migrate &&\
    python manage.py runserver ${SERVER_ADDRESS}:${SERVER_PORT}