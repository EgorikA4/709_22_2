FROM python:3.10.13

WORKDIR /flask_hw

COPY /hw .
COPY /requirements/main_requirements.txt .

RUN pip install -r main_requirements.txt
