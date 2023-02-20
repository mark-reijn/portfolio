FROM python:slim

WORKDIR /code

COPY .  /code

RUN pip install flask
RUN pip install -r requirements.txt
RUN export FLASK_APP=app.py

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]