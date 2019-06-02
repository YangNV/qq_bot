FROM python:3

WORKDIR /usr/src/app

COPY ../python_core/ ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./bot.py" ]