FROM python:3.7.10

COPY . /usr/src/loungebot

WORKDIR /usr/src/loungebot

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]
